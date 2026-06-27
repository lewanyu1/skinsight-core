#!/usr/bin/env python3
"""
SteamDT 开放平台全量爬虫
从 llms.txt 获取完整页面列表，爬取所有 44 个页面的完整内容。
输出: raw HTML, clean Markdown, structured JSON

用法:
    python crawl_all.py              # 爬取所有页面
    python crawl_all.py --verify     # 仅验证已有数据完整性
    python crawl_all.py --slug XXX   # 只爬取指定 slug
"""

import argparse
import json
import re
import sys
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

import requests
from bs4 import BeautifulSoup

# ============================================================
# Constants
# ============================================================

BASE_URL = "https://doc.steamdt.com"
LLMS_TXT_URL = f"{BASE_URL}/llms.txt"
OUTPUT_DIR = Path(__file__).parent
RAW_DIR = OUTPUT_DIR / "raw"
MD_DIR = OUTPUT_DIR / "markdown"
STRUCTURED_DIR = OUTPUT_DIR / "structured"

# Request config
TIMEOUT = 30
DELAY_BETWEEN_REQUESTS = 0.5  # seconds, be polite
MAX_RETRIES = 3
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}


# ============================================================
# Data Models
# ============================================================

@dataclass
class PageInfo:
    """单个页面的元信息"""
    slug: str
    title: str
    url: str
    page_type: str  # "doc", "api", "schema"
    category: str = ""  # API 分类，如 "饰品价格相关接口"
    description: str = ""
    doc_url: str = ""

    def __post_init__(self):
        if not self.doc_url:
            self.doc_url = f"{BASE_URL}/{self.slug}"


@dataclass
class APIEndpoint:
    """API 端点结构化数据"""
    slug: str
    name: str
    url: str
    method: str
    doc_url: str
    category: str
    description: str
    request_params: list = field(default_factory=list)
    request_body: dict = field(default_factory=dict)
    response_model: str = ""
    response_fields: list = field(default_factory=list)
    response_example: str = ""
    curl_example: str = ""
    notes: list = field(default_factory=list)


@dataclass
class SchemaInfo:
    """Schema/DTO 结构化数据"""
    slug: str
    name: str
    doc_url: str
    fields: list = field(default_factory=list)
    description: str = ""


# ============================================================
# Step 1: Fetch llms.txt and parse all pages
# ============================================================

def fetch_llms_txt() -> str:
    """获取 llms.txt 内容"""
    print("📋 获取 llms.txt ...")
    resp = requests.get(LLMS_TXT_URL, headers=HEADERS, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.text


def parse_llms_txt(content: str) -> list[PageInfo]:
    """解析 llms.txt，提取所有页面信息"""
    pages = []
    current_section = ""

    for line in content.split("\n"):
        line = line.strip()

        # 检测 section
        if line.startswith("## "):
            current_section = line[3:].strip()
            continue

        # 解析链接 - 支持多种格式:
        # - [title](url)
        # - category > [title](url)
        # - category > subcategory [title](url)
        match = re.match(r'-\s+.*?\[([^\]]+)\]\(([^)]+)\)(?::\s*(.*))?', line)
        if not match:
            continue

        title = match.group(1)
        url = match.group(2)
        desc = match.group(3).strip() if match.group(3) else ""

        # 提取 slug
        slug_match = re.search(r'/([a-f0-9]+[med]0)(?:\.md)?$', url)
        if not slug_match:
            continue

        slug = slug_match.group(1)

        # 判断页面类型
        if slug.endswith("m0"):
            page_type = "doc"
        elif slug.endswith("e0"):
            page_type = "api"
        elif slug.endswith("d0"):
            page_type = "schema"
        else:
            page_type = "unknown"

        # 提取分类 (从原始行中提取)
        category = ""
        category_match = re.match(r'-\s+(.*?)\s*\[', line)
        if category_match:
            raw_category = category_match.group(1).strip()
            if raw_category and ">" in raw_category:
                parts = raw_category.split(">")
                category = parts[0].strip()

        pages.append(PageInfo(
            slug=slug,
            title=title,
            url=url,
            page_type=page_type,
            category=category,
            description=desc,
        ))

    return pages


# ============================================================
# Step 2: Fetch raw HTML for each page
# ============================================================

def fetch_page(slug: str) -> Optional[str]:
    """获取单个页面的原始 HTML"""
    url = f"{BASE_URL}/{slug}"
    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
            resp.raise_for_status()
            return resp.text
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(1)
            else:
                print(f"  ❌ 获取失败: {e}")
                return None


def save_raw_html(slug: str, html: str):
    """保存原始 HTML"""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    path = RAW_DIR / f"{slug}.html"
    path.write_text(html, encoding="utf-8")


# ============================================================
# Step 3: Convert HTML to clean Markdown
# ============================================================

def html_to_markdown(html: str, title: str) -> str:
    """将 HTML 转换为干净的 Markdown"""
    soup = BeautifulSoup(html, "html.parser")

    # 移除脚本和样式
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    # 提取主要内容区域
    main = soup.find("main") or soup.find("article") or soup.find("div", class_=re.compile(r"content|main|doc"))
    if not main:
        main = soup.body or soup

    # 转换为 markdown
    lines = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"> 来源: {BASE_URL}")
    lines.append("")

    _extract_markdown(main, lines)

    return "\n".join(lines)


def _extract_markdown(element, lines: list, depth: int = 0):
    """递归提取 HTML 元素为 Markdown"""
    if depth > 20:
        return

    for child in element.children:
        if hasattr(child, 'name'):
            tag = child.name
            if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
                level = int(tag[1])
                text = child.get_text(strip=True)
                if text:
                    lines.append("")
                    lines.append(f"{'#' * (level + 1)} {text}")
                    lines.append("")
            elif tag == 'p':
                text = child.get_text(strip=True)
                if text:
                    lines.append(text)
                    lines.append("")
            elif tag in ('pre', 'code'):
                text = child.get_text()
                if tag == 'pre':
                    lines.append("```")
                    lines.append(text.strip())
                    lines.append("```")
                else:
                    lines.append(f"`{text}`")
            elif tag == 'table':
                _extract_table(child, lines)
            elif tag in ('ul', 'ol'):
                for i, li in enumerate(child.find_all('li', recursive=False)):
                    prefix = f"{i+1}." if tag == 'ol' else "-"
                    text = li.get_text(strip=True)
                    lines.append(f"{prefix} {text}")
                lines.append("")
            elif tag == 'div':
                _extract_markdown(child, lines, depth + 1)
            elif tag in ('span', 'strong', 'em', 'b', 'i'):
                # 内联元素，跳过
                pass
        else:
            # 文本节点
            text = str(child).strip()
            if text and text not in ('\n', '\r'):
                lines.append(text)


def _extract_table(table, lines: list):
    """提取 HTML 表格为 Markdown 表格"""
    rows = []
    for tr in table.find_all('tr'):
        cells = []
        for td in tr.find_all(['td', 'th']):
            cells.append(td.get_text(strip=True))
        if cells:
            rows.append(cells)

    if not rows:
        return

    # 计算列数
    max_cols = max(len(r) for r in rows)

    # 补齐列数
    for r in rows:
        while len(r) < max_cols:
            r.append("")

    # 输出 markdown 表格
    lines.append("")
    lines.append("| " + " | ".join(rows[0]) + " |")
    lines.append("| " + " | ".join(["---"] * max_cols) + " |")
    for row in rows[1:]:
        lines.append("| " + " | ".join(row) + " |")
    lines.append("")


def save_markdown(slug: str, content: str):
    """保存 Markdown 文件"""
    MD_DIR.mkdir(parents=True, exist_ok=True)
    path = MD_DIR / f"{slug}.md"
    path.write_text(content, encoding="utf-8")


# ============================================================
# Step 4: Extract structured data from API pages
# ============================================================

def extract_api_endpoint(html: str, page: PageInfo) -> APIEndpoint:
    """从 API 页面提取结构化数据"""
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text()

    # 首先尝试从嵌入的 JSON 数据中提取
    method, api_url = _extract_from_embedded_json(html, page.slug)

    # 如果没有找到，从页面文本中提取
    if not api_url:
        url_match = re.search(r'(GET|POST|PUT|DELETE)\s+(/open/[^\s<>]+)', text)
        if url_match:
            method = url_match.group(1)
            api_url = url_match.group(2)
        else:
            curl_match = re.search(r'curl[^"]*"(https://open\.steamdt\.com[^"]*)"', text)
            if curl_match:
                full_url = curl_match.group(1)
                api_url = re.sub(r'https://open\.steamdt\.com', '', full_url)
                if '--data' in text:
                    method = "POST"

    # 提取请求参数
    request_params = _extract_request_params_from_json(html, page.slug)
    if not request_params:
        request_params = _extract_request_params(soup, method, text)

    # 提取响应字段
    response_fields = _extract_response_fields(soup)

    # 提取 curl 示例
    curl_example = _extract_curl_example(soup)

    # 提取响应示例
    response_example = _extract_response_example(soup)

    # 提取备注
    notes = _extract_notes(soup)

    return APIEndpoint(
        slug=page.slug,
        name=page.title,
        url=api_url,
        method=method,
        doc_url=page.doc_url,
        category=page.category,
        description=page.description,
        request_params=request_params,
        response_fields=response_fields,
        response_example=response_example,
        curl_example=curl_example,
        notes=notes,
    )


def _extract_from_embedded_json(html: str, slug: str) -> tuple:
    """从嵌入的 JSON 数据中提取 HTTP 方法和 API URL"""
    # 提取 slug 中的数字 ID
    slug_id = slug.replace('e0', '')

    # 格式1: apiDetail.{slug_id}\",\"get|post\",\"/open/...\"
    # 注意: 引号可能是转义的 (\") 或未转义的 (")
    pattern1 = rf'apiDetail\.{slug_id}[\\"\s,]+(get|post)[\\"\s,]+(/open/[^"\\]+)'
    match1 = re.search(pattern1, html, re.IGNORECASE)
    if match1:
        method = match1.group(1).upper()
        api_url = match1.group(2).replace('\\/', '/')
        return method, api_url

    # 格式2: apiDetail.{slug_id}\",\"method\",\"get|post\",\"path\",\"/open/...\"
    pattern2 = rf'apiDetail\.{slug_id}.*?method[\\"\s,]+(get|post).*?path[\\"\s,]+(/open/[^"\\]+)'
    match2 = re.search(pattern2, html, re.DOTALL | re.IGNORECASE)
    if match2:
        method = match2.group(1).upper()
        api_url = match2.group(2).replace('\\/', '/')
        return method, api_url

    # 格式3: apiDetail.{slug_id}\",\"/open/...\" (method 在前面)
    # 先找到包含 slug_id 的行
    pattern3 = rf'apiDetail\.{slug_id}[\\"\s,]+(/open/[^"\\]+)'
    match3 = re.search(pattern3, html)
    if match3:
        api_url = match3.group(1).replace('\\/', '/')
        # 在前面查找 method
        start = max(0, match3.start() - 200)
        context = html[start:match3.start()]
        # 查找最后一个 get 或 post
        method_matches = list(re.finditer(r'(get|post)', context, re.IGNORECASE))
        if method_matches:
            method = method_matches[-1].group(1).upper()
        else:
            # 默认方法
            method = "GET"
        return method, api_url

    # 格式4: 在 sidebarTree 中查找
    # 先找到 apiDetail.{slug_id} 的位置
    sidebar_pattern = rf'apiDetail\.{slug_id}'
    sidebar_match = re.search(sidebar_pattern, html)
    if sidebar_match:
        # 在附近 1000 字符内查找 method 和 path
        start = max(0, sidebar_match.start() - 100)
        end = min(len(html), sidebar_match.end() + 1000)
        context = html[start:end]

        # 查找 method
        method_match = re.search(r'(get|post)', context, re.IGNORECASE)
        if method_match:
            method = method_match.group(1).upper()
            # 在 method 后面查找 path
            path_match = re.search(r'/open/[^\s"\\]+', context[method_match.end():])
            if path_match:
                api_url = path_match.group(0).replace('\\/', '/')
                return method, api_url

    return "GET", ""


def _extract_request_params_from_json(html: str, slug: str) -> list:
    """从嵌入的 JSON 数据中提取请求参数"""
    params = []

    # 提取 slug 中的数字 ID
    slug_id = slug.replace('e0', '')

    # 查找 parameters 部分
    # 格式: "parameters",{"query":[{"name":"marketHashName",...}]}
    param_pattern = rf'"{slug_id}".*?"parameters",\{{(.*?)\}}'
    match = re.search(param_pattern, html, re.DOTALL)
    if not match:
        return params

    param_text = match.group(1)

    # 提取 query 参数
    query_match = re.search(r'"query",\[(.*?)\]', param_text, re.DOTALL)
    if query_match:
        query_text = query_match.group(1)
        # 提取每个参数对象
        param_objects = re.findall(r'\{(.*?)\}', query_text)
        for obj in param_objects:
            name_match = re.search(r'"name","([^"]+)"', obj)
            type_match = re.search(r'"type","([^"]+)"', obj)
            required_match = re.search(r'"required",(true|false)', obj)
            desc_match = re.search(r'"description","([^"]*)"', obj)

            if name_match:
                param = {
                    "name": name_match.group(1),
                    "type": type_match.group(1) if type_match else "string",
                    "required": required_match.group(1) == "true" if required_match else True,
                    "description": desc_match.group(1) if desc_match else "",
                }
                params.append(param)

    # 提取 body 参数
    body_match = re.search(r'"body",\[(.*?)\]', param_text, re.DOTALL)
    if body_match:
        body_text = body_match.group(1)
        param_objects = re.findall(r'\{(.*?)\}', body_text)
        for obj in param_objects:
            name_match = re.search(r'"name","([^"]+)"', obj)
            type_match = re.search(r'"type","([^"]+)"', obj)
            required_match = re.search(r'"required",(true|false)', obj)
            desc_match = re.search(r'"description","([^"]*)"', obj)

            if name_match:
                param = {
                    "name": name_match.group(1),
                    "type": type_match.group(1) if type_match else "string",
                    "required": required_match.group(1) == "true" if required_match else True,
                    "description": desc_match.group(1) if desc_match else "",
                }
                params.append(param)

    return params


def _extract_request_params(soup, method: str, text: str) -> list:
    """提取请求参数"""
    params = []

    # 从表格中提取
    tables = soup.find_all('table')
    for table in tables:
        rows = table.find_all('tr')
        header_row = rows[0] if rows else None
        if not header_row:
            continue

        headers = [th.get_text(strip=True) for th in header_row.find_all(['th', 'td'])]

        # 检查是否是参数表
        if not any(h in headers for h in ['参数', '参数名', '名称', 'name']):
            continue

        for row in rows[1:]:
            cells = [td.get_text(strip=True) for td in row.find_all(['td', 'th'])]
            if len(cells) >= 2:
                param = {
                    "name": cells[0],
                    "type": cells[1] if len(cells) > 1 else "string",
                    "required": "是" in cells[2] if len(cells) > 2 else True,
                    "description": cells[3] if len(cells) > 3 else "",
                }
                params.append(param)

    # 从 curl 示例中提取 (POST body)
    if method == "POST" and not params:
        curl_text = _get_curl_text(soup)
        data_match = re.search(r"--data\s+'(\{.*?\})'", curl_text, re.DOTALL)
        if data_match:
            try:
                body = json.loads(data_match.group(1))
                for key, value in body.items():
                    params.append({
                        "name": key,
                        "type": type(value).__name__,
                        "required": True,
                        "description": "",
                    })
            except json.JSONDecodeError:
                pass

    return params


def _extract_response_fields(soup) -> list:
    """提取响应字段"""
    fields = []

    # 查找 hljs 代码块
    code_blocks = soup.find_all('code', class_=re.compile(r'hljs'))
    for block in code_blocks:
        text = block.get_text()
        if '"success"' in text and '"data"' in text:
            # 这是响应示例
            attrs = block.find_all(class_='hljs-attr')
            for attr in attrs:
                field_name = attr.get_text(strip=True).strip('"')
                if field_name not in ('success', 'errorCode', 'errorMsg', 'errorData', 'errorCodeStr'):
                    fields.append({"name": field_name, "type": "unknown"})
            break

    return fields


def _extract_curl_example(soup) -> str:
    """提取 curl 示例"""
    for code in soup.find_all(['code', 'pre']):
        text = code.get_text()
        if 'curl' in text and 'open.steamdt.com' in text:
            return text.strip()
    return ""


def _extract_response_example(soup) -> str:
    """提取响应示例"""
    code_blocks = soup.find_all('code', class_=re.compile(r'hljs'))
    for block in code_blocks:
        text = block.get_text()
        if '"success"' in text:
            return text.strip()
    return ""


def _extract_notes(soup) -> list:
    """提取备注/说明"""
    notes = []
    # 查找blockquote或特定class的元素
    for bq in soup.find_all('blockquote'):
        text = bq.get_text(strip=True)
        if text:
            notes.append(text)
    return notes


def _get_curl_text(soup) -> str:
    """获取 curl 示例文本"""
    for code in soup.find_all(['code', 'pre']):
        text = code.get_text()
        if 'curl' in text or 'open.steamdt.com' in text:
            return text
    return ""


# ============================================================
# Step 5: Extract schema/DTO data
# ============================================================

def extract_schema(html: str, page: PageInfo) -> SchemaInfo:
    """从 Schema 页面提取结构化数据"""
    soup = BeautifulSoup(html, "html.parser")

    fields = []

    # 查找字段定义表格
    tables = soup.find_all('table')
    for table in tables:
        rows = table.find_all('tr')
        if not rows:
            continue

        headers = [th.get_text(strip=True) for th in rows[0].find_all(['th', 'td'])]

        # 检查是否是字段表
        if not any(h in headers for h in ['字段', '字段名', '名称', 'name', '属性']):
            continue

        for row in rows[1:]:
            cells = [td.get_text(strip=True) for td in row.find_all(['td', 'th'])]
            if len(cells) >= 2:
                field = {
                    "name": cells[0],
                    "type": cells[1],
                    "description": cells[2] if len(cells) > 2 else "",
                }
                fields.append(field)

    # 如果没有表格，尝试从代码块提取
    if not fields:
        code_blocks = soup.find_all('code', class_=re.compile(r'hljs'))
        for block in code_blocks:
            attrs = block.find_all(class_='hljs-attr')
            types = block.find_all(class_='hljs-type')
            for i, attr in enumerate(attrs):
                field_name = attr.get_text(strip=True).strip('"')
                field_type = types[i].get_text(strip=True) if i < len(types) else "unknown"
                fields.append({"name": field_name, "type": field_type})

    return SchemaInfo(
        slug=page.slug,
        name=page.title,
        doc_url=page.doc_url,
        fields=fields,
        description=page.description,
    )


# ============================================================
# Step 6: Generate comprehensive output files
# ============================================================

def save_api_endpoints_json(endpoints: list[APIEndpoint]):
    """保存 API 端点 JSON"""
    path = STRUCTURED_DIR / "api_endpoints.json"
    data = [asdict(ep) for ep in endpoints]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  💾 API 端点 JSON → {path}")


def save_schemas_json(schemas: list[SchemaInfo]):
    """保存 Schema JSON"""
    path = STRUCTURED_DIR / "schemas.json"
    data = [asdict(s) for s in schemas]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  💾 Schema JSON → {path}")


def save_pages_index(pages: list[PageInfo]):
    """保存页面索引"""
    path = STRUCTURED_DIR / "pages_index.json"
    data = [asdict(p) for p in pages]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  💾 页面索引 → {path}")


def generate_full_documentation(pages: list[PageInfo], endpoints: list[APIEndpoint], schemas: list[SchemaInfo]) -> str:
    """生成完整的 Markdown 文档"""
    lines = []
    lines.append("# SteamDT 开放平台 - 完整 API 文档")
    lines.append("")
    lines.append(f"> 自动生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"> 来源: {BASE_URL}")
    lines.append(f"> 总页面数: {len(pages)}")
    lines.append(f"> API 端点: {len(endpoints)}")
    lines.append(f"> Schema/DTO: {len(schemas)}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # 目录
    lines.append("## 目录")
    lines.append("")
    lines.append("### 文档")
    doc_pages = [p for p in pages if p.page_type == "doc"]
    for i, p in enumerate(doc_pages, 1):
        lines.append(f"{i}. [{p.title}](#{p.slug})")
    lines.append("")

    lines.append("### API 端点")
    for i, ep in enumerate(endpoints, 1):
        lines.append(f"{i}. [{ep.name}](#{ep.slug}) - `{ep.method} {ep.url}`")
    lines.append("")

    lines.append("### Schema/DTO")
    for i, s in enumerate(schemas, 1):
        lines.append(f"{i}. [{s.name}](#{s.slug})")
    lines.append("")
    lines.append("---")
    lines.append("")

    # 文档部分
    lines.append("## 文档")
    lines.append("")
    for page in doc_pages:
        lines.append(f"### {page.title}")
        lines.append("")
        lines.append(f"- **Slug**: `{page.slug}`")
        lines.append(f"- **链接**: {page.doc_url}")
        if page.description:
            lines.append(f"- **说明**: {page.description}")
        lines.append("")
        # 读取对应的 markdown 文件
        md_path = MD_DIR / f"{page.slug}.md"
        if md_path.exists():
            content = md_path.read_text(encoding="utf-8")
            # 跳过第一行标题
            content_lines = content.split("\n")[2:]
            lines.extend(content_lines)
        lines.append("")
        lines.append("---")
        lines.append("")

    # API 端点部分
    lines.append("## API 端点")
    lines.append("")
    for ep in endpoints:
        lines.append(f"### {ep.name}")
        lines.append("")
        lines.append(f"| 项目 | 说明 |")
        lines.append(f"|------|------|")
        lines.append(f"| **URL** | `{ep.method} {ep.url}` |")
        lines.append(f"| **文档页** | {ep.doc_url} |")
        if ep.category:
            lines.append(f"| **分类** | {ep.category} |")
        if ep.description:
            lines.append(f"| **说明** | {ep.description} |")
        lines.append("")

        if ep.request_params:
            lines.append("#### 请求参数")
            lines.append("")
            lines.append("| 参数 | 类型 | 必填 | 说明 |")
            lines.append("|------|------|------|------|")
            for p in ep.request_params:
                required = "✅" if p.get('required', True) else "❌"
                desc = p.get('description', '')
                lines.append(f"| `{p['name']}` | {p['type']} | {required} | {desc} |")
            lines.append("")
        else:
            lines.append("#### 请求参数")
            lines.append("")
            lines.append("无。")
            lines.append("")

        if ep.curl_example:
            lines.append("#### 请求示例")
            lines.append("")
            lines.append("```bash")
            lines.append(ep.curl_example)
            lines.append("```")
            lines.append("")

        if ep.response_fields:
            lines.append("#### 响应字段")
            lines.append("")
            lines.append("| 字段 | 类型 | 说明 |")
            lines.append("|------|------|------|")
            for f in ep.response_fields:
                lines.append(f"| `{f['name']}` | {f['type']} | |")
            lines.append("")

        if ep.response_example:
            lines.append("#### 响应示例")
            lines.append("")
            lines.append("```json")
            lines.append(ep.response_example)
            lines.append("```")
            lines.append("")

        if ep.notes:
            lines.append("#### 备注")
            lines.append("")
            for note in ep.notes:
                lines.append(f"- {note}")
            lines.append("")

        lines.append("---")
        lines.append("")

    # Schema 部分
    lines.append("## Schema/DTO 定义")
    lines.append("")
    for schema in schemas:
        lines.append(f"### {schema.name}")
        lines.append("")
        lines.append(f"- **文档页**: {schema.doc_url}")
        if schema.description:
            lines.append(f"- **说明**: {schema.description}")
        lines.append("")

        if schema.fields:
            lines.append("#### 字段")
            lines.append("")
            lines.append("| 字段名 | 类型 | 说明 |")
            lines.append("|--------|------|------|")
            for f in schema.fields:
                desc = f.get('description', '')
                lines.append(f"| `{f['name']}` | {f['type']} | {desc} |")
            lines.append("")

        lines.append("---")
        lines.append("")

    # 通用响应结构
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


# ============================================================
# Main
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="SteamDT 开放平台全量爬虫")
    parser.add_argument("--verify", action="store_true", help="仅验证已有数据完整性")
    parser.add_argument("--slug", type=str, help="只爬取指定 slug")
    args = parser.parse_args()

    # 创建输出目录
    for d in [RAW_DIR, MD_DIR, STRUCTURED_DIR]:
        d.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("SteamDT 开放平台全量爬虫")
    print("=" * 60)
    print()

    # Step 1: 获取页面列表
    llms_content = fetch_llms_txt()
    pages = parse_llms_txt(llms_content)

    print(f"📋 发现 {len(pages)} 个页面:")
    doc_count = sum(1 for p in pages if p.page_type == "doc")
    api_count = sum(1 for p in pages if p.page_type == "api")
    schema_count = sum(1 for p in pages if p.page_type == "schema")
    print(f"   - 文档: {doc_count}")
    print(f"   - API 端点: {api_count}")
    print(f"   - Schema/DTO: {schema_count}")
    print()

    if args.verify:
        print("🔍 验证模式 - 检查已有数据...")
        _verify_data(pages)
        return

    # 过滤指定 slug
    if args.slug:
        pages = [p for p in pages if p.slug == args.slug]
        if not pages:
            print(f"❌ 未找到 slug: {args.slug}")
            return

    # Step 2-3: 爬取所有页面
    print("🕷️  开始爬取页面...")
    print()

    endpoints = []
    schemas = []
    success_count = 0
    fail_count = 0

    for i, page in enumerate(pages, 1):
        print(f"  [{i}/{len(pages)}] {page.slug} - {page.title} ... ", end="", flush=True)

        # 获取 HTML
        html = fetch_page(page.slug)
        if not html:
            fail_count += 1
            continue

        # 保存原始 HTML
        save_raw_html(page.slug, html)

        # 转换为 Markdown
        md_content = html_to_markdown(html, page.title)
        save_markdown(page.slug, md_content)

        # 提取结构化数据
        if page.page_type == "api":
            endpoint = extract_api_endpoint(html, page)
            endpoints.append(endpoint)
            print(f"✅ API: {endpoint.method} {endpoint.url}")
        elif page.page_type == "schema":
            schema = extract_schema(html, page)
            schemas.append(schema)
            print(f"✅ Schema: {len(schema.fields)} fields")
        else:
            print("✅ Doc")

        success_count += 1
        time.sleep(DELAY_BETWEEN_REQUESTS)

    print()

    # Step 4: 保存结构化数据
    print("💾 保存结构化数据...")
    save_pages_index(pages)
    if endpoints:
        save_api_endpoints_json(endpoints)
    if schemas:
        save_schemas_json(schemas)

    # Step 5: 生成完整文档
    print("📝 生成完整文档...")
    full_doc = generate_full_documentation(pages, endpoints, schemas)
    doc_path = OUTPUT_DIR / "FULL_API_DOC.md"
    doc_path.write_text(full_doc, encoding="utf-8")
    print(f"  💾 完整文档 → {doc_path}")

    # 汇总
    print()
    print("=" * 60)
    print("爬取完成!")
    print(f"  成功: {success_count}")
    print(f"  失败: {fail_count}")
    print(f"  API 端点: {len(endpoints)}")
    print(f"  Schema/DTO: {len(schemas)}")
    print(f"  原始 HTML: {RAW_DIR}")
    print(f"  Markdown: {MD_DIR}")
    print(f"  结构化数据: {STRUCTURED_DIR}")
    print(f"  完整文档: {doc_path}")
    print("=" * 60)


def _verify_data(pages: list[PageInfo]):
    """验证已有数据的完整性"""
    print()

    # 检查原始 HTML
    html_files = set(f.stem for f in RAW_DIR.glob("*.html"))
    missing_html = [p.slug for p in pages if p.slug not in html_files]
    print(f"📄 原始 HTML: {len(html_files)}/{len(pages)}")
    if missing_html:
        print(f"   缺失: {', '.join(missing_html)}")

    # 检查 Markdown
    md_files = set(f.stem for f in MD_DIR.glob("*.md"))
    missing_md = [p.slug for p in pages if p.slug not in md_files]
    print(f"📝 Markdown: {len(md_files)}/{len(pages)}")
    if missing_md:
        print(f"   缺失: {', '.join(missing_md)}")

    # 检查结构化数据
    api_json = STRUCTURED_DIR / "api_endpoints.json"
    if api_json.exists():
        with open(api_json) as f:
            endpoints = json.load(f)
        print(f"🔗 API 端点: {len(endpoints)}")
        for ep in endpoints:
            print(f"   - {ep['name']}: {ep['method']} {ep['url']}")
    else:
        print("🔗 API 端点: 未找到")

    schema_json = STRUCTURED_DIR / "schemas.json"
    if schema_json.exists():
        with open(schema_json) as f:
            schemas = json.load(f)
        print(f"📋 Schema: {len(schemas)}")
    else:
        print("📋 Schema: 未找到")

    # 完整性检查
    print()
    if not missing_html and not missing_md:
        print("✅ 所有数据完整!")
    else:
        print("⚠️  部分数据缺失，请重新运行爬虫")


if __name__ == "__main__":
    main()
