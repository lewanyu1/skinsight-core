zai#!/usr/bin/env python3
"""
SteamDT 开放平台 API 文档爬虫
从 Apifox 托管页面提取完整 API 端点定义，输出 JSON + Markdown。
"""

import json
import re
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://doc.steamdt.com"

PAGES = {
    "278832832e0": "获取steam饰品基础信息",
    "278832830e0": "通过marketHashName查询饰品价格",
    "278832831e0": "通过marketHashName批量查询饰品价格",
    "428124801e0": "查询steam饰品k线数据",
    "319748133e0": "通过MarketHashName查询所有平台近7天均价",
    "273806087e0": "通过检视链接查询磨损度相关数据",
    "273806088e0": "通过ASMD参数查询磨损度相关数据",
    "273806089e0": "通过检视链接生成检视图",
    "273806090e0": "通过ASMD参数生成检视图",
    "450452402e0": "查询大盘k线数据",
    "450452403e0": "查询大盘最新指数数据",
}

# 端点 slug → API URL 映射（从侧边栏链接提取）
ENDPOINT_URLS = {
    "278832832e0": "/open/cs2/v1/base",
    "278832830e0": "/open/cs2/v1/price/single",
    "278832831e0": "/open/cs2/v1/price/batch",
    "428124801e0": "/open/cs2/item/v1/kline",
    "319748133e0": "/open/cs2/v1/price/avg",
    "273806087e0": "/open/cs2/v1/wear",
    "273806088e0": "/open/cs2/v2/wear",
    "273806089e0": "/open/cs2/v1/inspect",
    "273806090e0": "/open/cs2/v2/inspect",
    "450452402e0": "/open/cs2/broad/v1/kline",
    "450452403e0": "/open/cs2/broad/v1/index",
}


def fetch_page(slug: str) -> str:
    """下载单个 Apifox 页面 HTML"""
    url = f"{BASE_URL}/{slug}"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return resp.text


def extract_method(soup: BeautifulSoup, slug: str) -> str:
    """从页面提取 HTTP 方法"""
    # 方式1: 查找 GET/POST badge 文本紧邻 API URL
    text = soup.get_text()
    url = ENDPOINT_URLS[slug]
    # 找 URL 前面最近的 GET 或 POST
    pattern = rf"(GET|POST)\s*{re.escape(url)}"
    m = re.search(pattern, text)
    if m:
        return m.group(1)

    # 方式2: curl 示例中有 --data → POST
    curl_text = _get_curl_text(soup)
    if "--data" in curl_text:
        return "POST"

    # 方式3: URL 有 ?param → GET
    if re.search(rf"{re.escape(url)}\?", curl_text):
        return "GET"

    # 默认: 按已知规则
    if slug in ("278832830e0", "319748133e0", "450452403e0", "278832832e0"):
        return "GET"
    return "POST"


def _get_curl_text(soup: BeautifulSoup) -> str:
    """获取 curl 示例的纯文本"""
    # 找 code/pre 块中的 curl 命令
    for code in soup.find_all(["code", "pre"]):
        text = code.get_text()
        if "curl" in text or "open.steamdt.com" in text:
            return text
    return ""


def extract_request_params(soup: BeautifulSoup, method: str) -> list[dict]:
    """提取请求参数"""
    params = []
    curl_text = _get_curl_text(soup)

    if method == "POST" and "--data" in curl_text:
        # 从 curl --data JSON 中提取
        m = re.search(r"--data\s+'(\{.*?\})'", curl_text, re.DOTALL)
        if m:
            body_str = m.group(1)
            # 去掉 HTML 标签后提取 key
            clean = re.sub(r'<[^>]+>', '', body_str)
            keys = re.findall(r'"(\w+)"\s*:', clean)
            for key in keys:
                ptype = _infer_param_type(clean, key)
                params.append({"name": key, "type": ptype, "required": True})
    else:
        # GET: 从 curl URL 或页面文本中提取 ?param=
        # 方式1: 从 curl 示例
        url_match = re.search(r"'(https://open\.steamdt\.com[^']+)'", curl_text)
        if url_match:
            url = url_match.group(1)
        else:
            # 方式2: 从页面文本
            text = soup.get_text()
            url_match = re.search(r"(/open/cs2/[^\s']+)\?(\w+)", text)
            url = url_match.group(0) if url_match else ""

        for m in re.finditer(r"[?&](\w+)=", url):
            params.append({"name": m.group(1), "type": "string", "required": True})

    return params


def _infer_param_type(body_text: str, key: str) -> str:
    """从 curl --data 中推断参数类型"""
    # 找 "key": <value> 的 value 类型
    pattern = rf'"{key}"\s*:\s*(?:"[^"]*"|(\d+(?:\.\d+)?)|(\[)|(\{{)|(true|false))'
    m = re.search(pattern, body_text)
    if m:
        if m.group(1):  # number
            return "number"
        if m.group(2):  # array
            return "array"
        if m.group(3):  # object
            return "object"
        if m.group(4):  # boolean
            return "boolean"
    return "string"


def extract_response_fields(soup: BeautifulSoup, request_param_names: set) -> list[dict]:
    """从 <code class="hljs"> 块中提取响应字段，排除请求参数"""
    html = str(soup)

    # 找包含 hljs-attr 的 <code> 块（响应 JSON 示例）
    code_blocks = re.findall(
        r'<code[^>]*class="[^"]*hljs[^"]*"[^>]*>(.*?)</code>', html, re.DOTALL
    )

    skip = {"success", "errorCode", "errorMsg", "errorData", "errorCodeStr"}
    all_fields = []

    for block in code_blocks:
        attrs = re.findall(r'class="hljs-attr">"(\w+)"<', block)
        # 只处理包含 success/data 的响应块（跳过请求体块）
        if "success" not in attrs and "data" not in attrs:
            continue
        fields = []
        _parse_hljs_block(block, 0, fields, skip | request_param_names)
        all_fields = fields
        break  # 只取第一个响应块

    return all_fields


def _parse_hljs_block(block: str, pos: int, fields: list, exclude: set, parent: str = "") -> int:
    """递归解析 hljs 代码块中的 JSON 字段。返回消耗的字符数。"""
    attr_pattern = r'class="hljs-attr">"(\w+)"<'
    punct_pattern = r'class="hljs-punctuation">([{}\[\]])<'
    wrapper_fields = {"success", "errorCode", "errorMsg", "errorData", "errorCodeStr"}

    seen = set()
    start_pos = pos
    depth = 0

    while pos < len(block):
        next_attr = re.search(attr_pattern, block[pos:])
        next_punct = re.search(punct_pattern, block[pos:])

        events = []
        if next_attr:
            events.append(('attr', next_attr.start(), next_attr))
        if next_punct:
            events.append(('punct', next_punct.start(), next_punct))

        if not events:
            break

        events.sort(key=lambda x: x[1])
        event_type, rel_pos, match = events[0]
        abs_pos = pos + match.end()

        if event_type == 'punct':
            char = match.group(1)
            if char in ('{', '['):
                depth += 1
                pos = abs_pos
                continue
            elif char in ('}', ']'):
                depth -= 1
                return abs_pos - start_pos

        # event_type == 'attr'
        field_name = match.group(1)
        pos = abs_pos

        if field_name in exclude or field_name in wrapper_fields:
            continue

        full_name = f"{parent}.{field_name}" if parent else field_name
        if full_name in seen:
            continue
        seen.add(full_name)

        after = block[pos:pos + 200]
        field_type = "string"
        sub_fields = []

        open_arr = re.search(r'class="hljs-punctuation">\[<', after[:100])
        open_obj = re.search(r'class="hljs-punctuation">\{<', after[:100])

        if open_arr:
            field_type = "array"
            inner_start = pos + open_arr.end()
            consumed = _parse_hljs_block(block, inner_start, sub_fields, set(), full_name)
            pos = inner_start + consumed
        elif open_obj:
            field_type = "object"
            inner_start = pos + open_obj.end()
            consumed = _parse_hljs_block(block, inner_start, sub_fields, set(), full_name)
            pos = inner_start + consumed
        elif re.search(r'class="hljs-number"', after[:100]):
            field_type = "number"
        elif re.search(r'class="hljs-literal"', after[:100]):
            field_type = "boolean"

        entry = {"name": full_name, "type": field_type}
        if sub_fields:
            entry["fields"] = sub_fields
        fields.append(entry)

    return pos - start_pos


def _extract_hljs_fields_recursive(html: str, start: int, fields: list, depth: int, parent: str = ""):
    """从 HTML 中递归提取 hljs-attr 标注的字段"""
    if depth > 10:
        return

    # 找所有 hljs-attr
    pattern = r'class="hljs-attr">"(\w+)"<'
    pos = start

    while True:
        m = re.search(pattern, html[pos:])
        if not m:
            break

        field_name = m.group(1)
        abs_pos = pos + m.end()

        # 跳过通用字段
        if field_name in ("success", "errorCode", "errorMsg", "errorData", "errorCodeStr"):
            pos = abs_pos
            continue

        # 判断字段类型：看后面的 hljs 标签
        after = html[abs_pos:abs_pos + 300]

        field_type = "string"  # 默认
        sub_fields = []

        if 'hljs-punctuation">[' in after[:100]:
            field_type = "array"
            # 检查数组元素是否有子字段
            next_obj = re.search(r'class="hljs-attr"', after[:500])
            if next_obj:
                sub_start = abs_pos + next_obj.start()
                _extract_hljs_fields_recursive(html, sub_start, sub_fields, depth + 1, field_name)
        elif 'hljs-punctuation">{' in after[:100]:
            field_type = "object"
            # 递归提取子字段
            next_attr = re.search(r'class="hljs-attr"', after[:500])
            if next_attr:
                sub_start = abs_pos + next_attr.start()
                _extract_hljs_fields_recursive(html, sub_start, sub_fields, depth + 1, field_name)
        elif "hljs-number" in after[:100]:
            field_type = "number"
        elif "hljs-literal" in after[:100]:
            field_type = "boolean"

        full_name = f"{parent}.{field_name}" if parent else field_name
        entry = {"name": full_name, "type": field_type}
        if sub_fields:
            entry["fields"] = sub_fields
        fields.append(entry)

        pos = abs_pos


def extract_model_name(soup: BeautifulSoup) -> str:
    """提取响应模型名（WebApiRes*），只从响应示例附近提取"""
    html = str(soup)
    # 找 "成功示例" 附近的 WebApiRes 引用
    idx = html.find("成功示例")
    if idx < 0:
        idx = html.find("返回响应")
    if idx < 0:
        return ""
    # 在前后 500 字符内找 WebApiRes
    region = html[max(0, idx - 500):idx + 500]
    m = re.search(r"(WebApiRes\w+)", region)
    return m.group(1) if m else ""


def parse_endpoint(slug: str, html: str) -> dict:
    """解析单个端点的完整信息"""
    soup = BeautifulSoup(html, "html.parser")

    method = extract_method(soup, slug)
    params = extract_request_params(soup, method)
    param_names = {p['name'] for p in params}
    response_fields = extract_response_fields(soup, param_names)
    model_name = extract_model_name(soup)

    return {
        "slug": slug,
        "name": PAGES[slug],
        "url": ENDPOINT_URLS[slug],
        "method": method,
        "doc_url": f"{BASE_URL}/{slug}",
        "request_params": params,
        "response_model": model_name,
        "response_fields": response_fields,
    }


def generate_markdown(endpoints: list[dict]) -> str:
    """从结构化数据生成 Markdown 文档"""
    lines = []
    lines.append("# SteamDT 开放平台 API 文档")
    lines.append("")
    lines.append("> 来源: https://doc.steamdt.com")
    lines.append("> 基础域名: `https://open.steamdt.com`")
    lines.append("> 数据格式: JSON")
    lines.append("> 鉴权方式: 待确认")
    lines.append(f"> 生成方式: scraper.py 自动爬取")
    lines.append("")
    lines.append("---")
    lines.append("")

    # 目录
    lines.append("## 目录")
    lines.append("")
    for i, ep in enumerate(endpoints, 1):
        anchor = f"{i}-{ep['name'].replace(' ', '-')}"
        lines.append(f"{i}. [{ep['name']}](#{anchor})")
    lines.append(f"{len(endpoints)+1}. [通用响应结构](#通用响应结构)")
    lines.append("")
    lines.append("---")
    lines.append("")

    # 各端点
    for i, ep in enumerate(endpoints, 1):
        lines.append(f"## {i}. {ep['name']}")
        lines.append("")
        lines.append("| 项目 | 说明 |")
        lines.append("|------|------|")
        lines.append(f"| **URL** | `{ep['method']} {ep['url']}` |")
        lines.append(f"| **文档页** | {ep['doc_url']} |")
        if ep['response_model']:
            lines.append(f"| **响应模型** | `{ep['response_model']}` |")
        lines.append("")

        # 请求参数
        if ep['request_params']:
            lines.append("### 请求参数")
            lines.append("")
            lines.append("| 参数 | 类型 | 必填 | 说明 |")
            lines.append("|------|------|------|------|")
            for p in ep['request_params']:
                lines.append(f"| `{p['name']}` | {p['type']} | ✅ | |")
            lines.append("")
        else:
            lines.append("### 请求参数")
            lines.append("")
            lines.append("无。")
            lines.append("")

        # 响应字段
        if ep['response_fields']:
            lines.append("### 响应字段")
            lines.append("")
            _fields_to_table(ep['response_fields'], lines, depth=0)
            lines.append("")
        else:
            lines.append("### 响应字段")
            lines.append("")
            lines.append("> ⚠️ 原始文档中响应示例为空，具体字段需实际调用确认。")
            lines.append("")

        lines.append("---")
        lines.append("")

    # 通用响应
    lines.append("## 通用响应结构")
    lines.append("")
    lines.append("```json")
    lines.append('{')
    lines.append('  "success": true,')
    lines.append('  "data": {},')
    lines.append('  "errorCode": 0,')
    lines.append('  "errorMsg": "",')
    lines.append('  "errorData": {},')
    lines.append('  "errorCodeStr": ""')
    lines.append('}')
    lines.append("```")

    return "\n".join(lines)


def _fields_to_table(fields: list, lines: list, depth: int = 0):
    """递归将字段列表转为 Markdown 表格行"""
    for f in fields:
        name = f['name']
        ftype = f['type']
        indent = "  " * depth
        lines.append(f"| `{indent}{name}` | {ftype} | |")
        if f.get('fields'):
            _fields_to_table(f['fields'], lines, depth + 1)


def _count_fields(fields: list) -> int:
    """递归计算字段总数"""
    count = 0
    for f in fields:
        count += 1
        if f.get('fields'):
            count += _count_fields(f['fields'])
    return count


def main():
    output_dir = Path(__file__).parent
    endpoints = []

    print("开始爬取 SteamDT API 文档...")
    print(f"共 {len(PAGES)} 个端点")
    print()

    for slug, name in PAGES.items():
        print(f"  [{slug}] {name} ... ", end="", flush=True)
        try:
            html = fetch_page(slug)
            ep = parse_endpoint(slug, html)
            endpoints.append(ep)

            param_count = len(ep['request_params'])
            field_count = _count_fields(ep['response_fields'])
            print(f"✅ params={param_count} fields={field_count}")
        except Exception as e:
            print(f"❌ {e}")
            endpoints.append({
                "slug": slug, "name": name,
                "url": ENDPOINT_URLS[slug], "method": "GET",
                "doc_url": f"{BASE_URL}/{slug}",
                "request_params": [], "response_model": "",
                "response_fields": [], "error": str(e),
            })

    # 输出 JSON
    json_path = output_dir / "api_endpoints.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(endpoints, f, ensure_ascii=False, indent=2)
    print(f"\n✅ JSON → {json_path}")

    # 输出 Markdown
    md_path = output_dir / "steamdt-api.md"
    md_content = generate_markdown(endpoints)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"✅ Markdown → {md_path}")

    # 汇总
    print(f"\n{'='*50}")
    print(f"爬取完成: {len(endpoints)} 个端点")
    total_params = sum(len(e['request_params']) for e in endpoints)
    total_fields = sum(_count_fields(e['response_fields']) for e in endpoints)
    print(f"请求参数: {total_params} 个")
    print(f"响应字段: {total_fields} 个")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
