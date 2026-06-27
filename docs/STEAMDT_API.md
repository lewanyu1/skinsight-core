# SteamDT 开放平台 API 文档

> **基础域名**: `https://open.steamdt.com`
> **数据格式**: JSON
> **鉴权方式**: API Key (待确认)
> **文档来源**: https://doc.steamdt.com/6279815m0
> **最后验证**: 2026-06-27

---

## 快速开始

所有接口返回统一格式：

```json
{
  "success": true,
  "data": {},
  "errorCode": 0,
  "errorMsg": "",
  "errorData": {},
  "errorCodeStr": ""
}
```

---

## API 目录

### 饰品价格相关
| # | 接口 | 方法 | 路径 | 说明 |
|---|------|------|------|------|
| 1 | [获取饰品基础信息](#1-获取steam饰品基础信息) | GET | `/open/cs2/v1/base` | 获取所有饰品的 marketHashName |
| 2 | [查询饰品价格](#2-通过markethashname查询饰品价格) | GET | `/open/cs2/v1/price/single` | 单个饰品全平台价格 |
| 3 | [批量查询价格](#3-通过markethashname批量查询饰品价格) | POST | `/open/cs2/v1/price/batch` | 批量饰品价格 |
| 4 | [查询K线数据](#4-查询steam饰品k线数据) | POST | `/open/cs2/item/v1/kline` | 饰品K线数据 |
| 5 | [查询7天均价](#5-通过markethashname查询所有平台近7天均价) | GET | `/open/cs2/v1/price/avg` | 全平台7天均价 |

### 饰品磨损及检视图
| # | 接口 | 方法 | 路径 | 说明 |
|---|------|------|------|------|
| 6 | [查询磨损(链接)](#6-通过检视链接查询磨损度) | POST | `/open/cs2/v1/wear` | 通过检视链接查询磨损 |
| 7 | [查询磨损(ASMD)](#7-通过asmd参数查询磨损度) | POST | `/open/cs2/v2/wear` | 通过ASMD参数查询磨损 |
| 8 | [生成检视图(链接)](#8-通过检视链接生成检视图) | POST | `/open/cs2/v1/inspect` | 通过检视链接生成检视图 |
| 9 | [生成检视图(ASMD)](#9-通过asmd参数生成检视图) | POST | `/open/cs2/v2/inspect` | 通过ASMD参数生成检视图 |

### 大盘数据
| # | 接口 | 方法 | 路径 | 说明 |
|---|------|------|------|------|
| 10 | [大盘K线](#10-查询大盘k线数据) | POST | `/open/cs2/broad/v1/kline` | 大盘K线数据 |
| 11 | [大盘指数](#11-查询大盘最新指数) | GET | `/open/cs2/broad/v1/index` | 大盘最新指数 |

---

## 1. 获取Steam饰品基础信息

> 所有接口数据都基于该接口返回的 `marketHashName`，**请优先对接该接口**

```
GET /open/cs2/v1/base
```

**请求参数**: 无

**响应示例**:
```json
{
  "success": true,
  "data": [
    {
      "name": "AK-47 | 二西莫夫 (崭新出厂)",
      "marketHashName": "AK-47 | Asiimov (Factory New)",
      "platformList": [
        {
          "name": "BUFF",
          "itemId": "123456"
        },
        {
          "name": "C5",
          "itemId": "789012"
        }
      ]
    }
  ],
  "errorCode": 0,
  "errorMsg": ""
}
```

**响应字段**:
| 字段 | 类型 | 说明 |
|------|------|------|
| `data` | array | 饰品列表 |
| `data[].name` | string | 饰品中文名 |
| `data[].marketHashName` | string | 饰品英文名(用于其他接口) |
| `data[].platformList` | array | 支持的平台列表 |
| `data[].platformList[].name` | string | 平台名称 |
| `data[].platformList[].itemId` | string | 平台商品ID |

**cURL**:
```bash
curl --location 'https://open.steamdt.com/open/cs2/v1/base'
```

---

## 2. 通过marketHashName查询饰品价格

```
GET /open/cs2/v1/price/single?marketHashName={name}
```

**请求参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `marketHashName` | string | ✅ | 饰品英文名 |

**响应示例**:
```json
{
  "success": true,
  "data": [
    {
      "platform": "BUFF",
      "platformItemId": "123456",
      "sellPrice": 1234.56,
      "sellCount": 100,
      "biddingPrice": 1200.00,
      "biddingCount": 50,
      "updateTime": 1719500000
    }
  ],
  "errorCode": 0,
  "errorMsg": ""
}
```

**响应字段**:
| 字段 | 类型 | 说明 |
|------|------|------|
| `data` | array | 各平台价格数据 |
| `data[].platform` | string | 平台名称 |
| `data[].platformItemId` | string | 平台商品ID |
| `data[].sellPrice` | number | 在售价格 |
| `data[].sellCount` | number | 在售数量 |
| `data[].biddingPrice` | number | 求购价格 |
| `data[].biddingCount` | number | 求购数量 |
| `data[].updateTime` | number | 更新时间戳 |

**cURL**:
```bash
curl --location 'https://open.steamdt.com/open/cs2/v1/price/single?marketHashName=AK-47%20%7C%20Asiimov%20(Factory%20New)'
```

---

## 3. 通过marketHashName批量查询饰品价格

```
POST /open/cs2/v1/price/batch
Content-Type: application/json
```

**请求体**:
```json
{
  "marketHashNames": [
    "AK-47 | Asiimov (Factory New)",
    "AWP | Dragon Lore (Factory New)"
  ]
}
```

**请求参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `marketHashNames` | array | ✅ | 饰品英文名数组 |

**响应示例**:
```json
{
  "success": true,
  "data": [
    {
      "marketHashName": "AK-47 | Asiimov (Factory New)",
      "dataList": [
        {
          "platform": "BUFF",
          "platformItemId": "123456",
          "sellPrice": 1234.56,
          "sellCount": 100,
          "biddingPrice": 1200.00,
          "biddingCount": 50,
          "updateTime": 1719500000
        }
      ]
    }
  ],
  "errorCode": 0,
  "errorMsg": ""
}
```

**响应字段**:
| 字段 | 类型 | 说明 |
|------|------|------|
| `data` | array | 结果列表 |
| `data[].marketHashName` | string | 饰品英文名 |
| `data[].dataList` | array | 各平台价格数据 |
| `data[].dataList[].platform` | string | 平台名称 |
| `data[].dataList[].sellPrice` | number | 在售价格 |
| `data[].dataList[].biddingPrice` | number | 求购价格 |

**cURL**:
```bash
curl --location 'https://open.steamdt.com/open/cs2/v1/price/batch' \
--header 'Content-Type: application/json' \
--data '{
    "marketHashNames": [
        "AK-47 | Asiimov (Factory New)",
        "AWP | Dragon Lore (Factory New)"
    ]
}'
```

---

## 4. 查询steam饰品K线数据

```
POST /open/cs2/item/v1/kline
Content-Type: application/json
```

**请求体**:
```json
{
  "marketHashName": "AK-47 | Asiimov (Factory New)",
  "type": 1,
  "platform": "BUFF",
  "specialStyle": ""
}
```

**请求参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `marketHashName` | string | ✅ | 饰品英文名 |
| `type` | number | ✅ | K线类型 (1=日K, 2=周K, 3=月K) |
| `platform` | string | ✅ | 平台名称 |
| `specialStyle` | string | ✅ | 特殊款式 (无特殊款式传空字符串) |

**响应示例**:
```json
{
  "success": true,
  "data": [
    [1719500000, 1234.56, 1250.00, 1260.00, 1220.00]
  ],
  "errorCode": 0,
  "errorMsg": ""
}
```

**响应字段**:
| 字段 | 类型 | 说明 |
|------|------|------|
| `data` | array | K线数据数组 |
| `data[]` | array | [时间戳, 开盘价, 收盘价, 最高价, 最低价] |

**cURL**:
```bash
curl --location 'https://open.steamdt.com/open/cs2/item/v1/kline' \
--header 'Content-Type: application/json' \
--data '{
    "marketHashName": "AK-47 | Asiimov (Factory New)",
    "type": 1,
    "platform": "BUFF",
    "specialStyle": ""
}'
```

---

## 5. 通过marketHashName查询所有平台近7天均价

```
GET /open/cs2/v1/price/avg?marketHashName={name}
```

**请求参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `marketHashName` | string | ✅ | 饰品英文名 |

**响应示例**:
```json
{
  "success": true,
  "data": {
    "marketHashName": "AK-47 | Asiimov (Factory New)",
    "avgPrice": 1250.00,
    "dataList": [
      {
        "platform": "BUFF",
        "avgPrice": 1260.00
      },
      {
        "platform": "C5",
        "avgPrice": 1240.00
      }
    ]
  },
  "errorCode": 0,
  "errorMsg": ""
}
```

**响应字段**:
| 字段 | 类型 | 说明 |
|------|------|------|
| `data.marketHashName` | string | 饰品英文名 |
| `data.avgPrice` | number | 全平台平均价格 |
| `data.dataList` | array | 各平台均价 |
| `data.dataList[].platform` | string | 平台名称 |
| `data.dataList[].avgPrice` | number | 该平台7天均价 |

**cURL**:
```bash
curl --location 'https://open.steamdt.com/open/cs2/v1/price/avg?marketHashName=AK-47%20%7C%20Asiimov%20(Factory%20New)'
```

---

## 6. 通过检视链接查询磨损度

> 异步接口，需要提供回调地址

```
POST /open/cs2/v1/wear
Content-Type: application/json
```

**请求体**:
```json
{
  "notifyUrl": "https://your-server.com/callback",
  "inspectUrl": "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20S76561198253243553A1234567890D1234567890"
}
```

**请求参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `notifyUrl` | string | ✅ | 回调通知地址 |
| `inspectUrl` | string | ✅ | 检视链接 |

**响应示例**:
```json
{
  "success": true,
  "data": {
    "sync": true,
    "taskId": "task_123456",
    "itemPreviewData": {
      "assetId": 1234567890,
      "defindex": 7,
      "paintindex": 280,
      "rarity": 6,
      "quality": 4,
      "paintwear": 1050685696,
      "floatWear": "0.045678",
      "paintseed": 123,
      "stickers": [
        {
          "stickerId": 1234,
          "slot": 0,
          "wear": 0.01
        }
      ],
      "keychains": [
        {
          "id": 5678,
          "pattern": 42
        }
      ]
    }
  },
  "errorCode": 0,
  "errorMsg": ""
}
```

**响应字段**:
| 字段 | 类型 | 说明 |
|------|------|------|
| `data.sync` | boolean | 是否同步返回结果 |
| `data.taskId` | string | 任务ID |
| `data.itemPreviewData.assetId` | number | 饰品资产ID |
| `data.itemPreviewData.defindex` | number | 饰品定义索引 |
| `data.itemPreviewData.paintindex` | number | 皮肤索引 |
| `data.itemPreviewData.rarity` | number | 稀有度 |
| `data.itemPreviewData.quality` | number | 品质 |
| `data.itemPreviewData.paintwear` | number | 磨损值(原始) |
| `data.itemPreviewData.floatWear` | string | 磨损值(浮点) |
| `data.itemPreviewData.paintseed` | number | 图案种子 |
| `data.itemPreviewData.stickers` | array | 贴纸列表 |
| `data.itemPreviewData.stickers[].stickerId` | number | 贴纸ID |
| `data.itemPreviewData.stickers[].slot` | number | 贴纸位置 |
| `data.itemPreviewData.stickers[].wear` | number | 贴纸磨损 |
| `data.itemPreviewData.keychains` | array | 挂件列表 |

**cURL**:
```bash
curl --location 'https://open.steamdt.com/open/cs2/v1/wear' \
--header 'Content-Type: application/json' \
--data '{
    "notifyUrl": "https://your-server.com/callback",
    "inspectUrl": "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20S76561198253243553A1234567890D1234567890"
}'
```

---

## 7. 通过ASMD参数查询磨损度

```
POST /open/cs2/v2/wear
Content-Type: application/json
```

**请求体**:
```json
{
  "s": 76561198253243553,
  "m": 730,
  "a": 1234567890,
  "d": 1234567890,
  "notifyUrl": "https://your-server.com/callback"
}
```

**请求参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `s` | number | ✅ | Steam ID |
| `m` | number | ✅ | 游戏ID (CS2=730) |
| `a` | number | ✅ | 资产ID |
| `d` | string | ✅ | D参数 |
| `notifyUrl` | string | ✅ | 回调通知地址 |

**响应**: 同 [接口6](#6-通过检视链接查询磨损度)

**cURL**:
```bash
curl --location 'https://open.steamdt.com/open/cs2/v2/wear' \
--header 'Content-Type: application/json' \
--data '{
    "s": 76561198253243553,
    "m": 730,
    "a": 1234567890,
    "d": 1234567890,
    "notifyUrl": "https://your-server.com/callback"
}'
```

---

## 8. 通过检视链接生成检视图

> 前提：已获取到饰品的磨损度数据

```
POST /open/cs2/v1/inspect
Content-Type: application/json
```

**请求体**:
```json
{
  "notifyUrl": "https://your-server.com/callback",
  "inspectUrl": "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20S76561198253243553A1234567890D1234567890"
}
```

**请求参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `notifyUrl` | string | ✅ | 回调通知地址 |
| `inspectUrl` | string | ✅ | 检视链接 |

**响应示例**:
```json
{
  "success": true,
  "data": {
    "sync": true,
    "taskId": "task_123456",
    "screenshot": {
      "itemId": 123456,
      "assetId": 1234567890,
      "fingerprint": "abc123def456",
      "screenshots": {
        "front": ["https://cdn.steamdt.com/front.png"],
        "back": ["https://cdn.steamdt.com/back.png"],
        "detail": ["https://cdn.steamdt.com/detail.png"]
      },
      "cs2Version": 1,
      "clientVersion": "1.0.0",
      "existSticker": true,
      "protoEncodeStr": "...",
      "createTime": "2026-06-27T00:00:00Z",
      "updateTime": "2026-06-27T00:00:00Z"
    }
  },
  "errorCode": 0,
  "errorMsg": ""
}
```

**响应字段**:
| 字段 | 类型 | 说明 |
|------|------|------|
| `data.sync` | boolean | 是否同步返回 |
| `data.taskId` | string | 任务ID |
| `data.screenshot.itemId` | number | 物品ID |
| `data.screenshot.assetId` | number | 资产ID |
| `data.screenshot.fingerprint` | string | 指纹 |
| `data.screenshot.screenshots.front` | array | 正面图URL |
| `data.screenshot.screenshots.back` | array | 背面图URL |
| `data.screenshot.screenshots.detail` | array | 详情图URL |
| `data.screenshot.cs2Version` | number | CS2版本 |
| `data.screenshot.existSticker` | boolean | 是否有贴纸 |

**cURL**:
```bash
curl --location 'https://open.steamdt.com/open/cs2/v1/inspect' \
--header 'Content-Type: application/json' \
--data '{
    "notifyUrl": "https://your-server.com/callback",
    "inspectUrl": "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20S76561198253243553A1234567890D1234567890"
}'
```

---

## 9. 通过ASMD参数生成检视图

```
POST /open/cs2/v2/inspect
Content-Type: application/json
```

**请求体**:
```json
{
  "s": 76561198253243553,
  "m": 730,
  "a": 1234567890,
  "d": 1234567890,
  "notifyUrl": "https://your-server.com/callback"
}
```

**请求参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `s` | number | ✅ | Steam ID |
| `m` | number | ✅ | 游戏ID (CS2=730) |
| `a` | number | ✅ | 资产ID |
| `d` | string | ✅ | D参数 |
| `notifyUrl` | string | ✅ | 回调通知地址 |

**响应**: 同 [接口8](#8-通过检视链接生成检视图)

**cURL**:
```bash
curl --location 'https://open.steamdt.com/open/cs2/v2/inspect' \
--header 'Content-Type: application/json' \
--data '{
    "s": 76561198253243553,
    "m": 730,
    "a": 1234567890,
    "d": 1234567890,
    "notifyUrl": "https://your-server.com/callback"
}'
```

---

## 10. 查询大盘K线数据

```
POST /open/cs2/broad/v1/kline
Content-Type: application/json
```

**请求体**:
```json
{
  "type": 1
}
```

**请求参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `type` | number | ✅ | K线类型 (1=日K, 2=周K, 3=月K) |

**响应示例**:
```json
{
  "success": true,
  "data": [
    [1719500000, 1000.00, 1050.00, 1060.00, 990.00]
  ],
  "errorCode": 0,
  "errorMsg": ""
}
```

**响应字段**:
| 字段 | 类型 | 说明 |
|------|------|------|
| `data` | array | K线数据数组 |
| `data[]` | array | [时间戳, 开盘指数, 收盘指数, 最高指数, 最低指数] |

**cURL**:
```bash
curl --location 'https://open.steamdt.com/open/cs2/broad/v1/kline' \
--header 'Content-Type: application/json' \
--data '{
    "type": 1
}'
```

---

## 11. 查询大盘最新指数

```
GET /open/cs2/broad/v1/index
```

**请求参数**: 无

**响应示例**:
```json
{
  "success": true,
  "data": {
    "broadMarketIndex": 1050.00,
    "updateTime": 1719500000,
    "diffYesterday": 10.00,
    "diffYesterdayRatio": 0.0096,
    "historyMarketIndexList": [
      [1719400000, 1040.00],
      [1719300000, 1030.00]
    ]
  },
  "errorCode": 0,
  "errorMsg": ""
}
```

**响应字段**:
| 字段 | 类型 | 说明 |
|------|------|------|
| `data.broadMarketIndex` | number | 当前大盘指数 |
| `data.updateTime` | number | 更新时间戳 |
| `data.diffYesterday` | number | 较昨日变化 |
| `data.diffYesterdayRatio` | number | 较昨日变化率 |
| `data.historyMarketIndexList` | array | 历史指数列表 |

**cURL**:
```bash
curl --location 'https://open.steamdt.com/open/cs2/broad/v1/index'
```

---

## 附录

### 特殊款式对照表

查询K线数据时，`specialStyle` 参数需要传入特殊款式标识。常见款式：

| 款式 | 值 |
|------|-----|
| 无特殊款式 | `""` |
| 暗金 | `"StatTrak™"` |
| 纪念品 | `"Souvenir"` |

### 错误码

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| 其他 | 失败，参考 `errorMsg` |

### 数据源平台

| 平台 | 说明 |
|------|------|
| BUFF | 网易BUFF |
| C5 | C5game |
| Steam | Steam社区市场 |
| UU | 悠悠有品 |

---

## Schema/DTO 参考

详见 [schemas.json](structured/schemas.json)

### 主要 Schema 列表

| Schema | 说明 |
|--------|------|
| PlatformPriceVO | 平台价格数据 |
| BatchPlatformPriceVO | 批量平台价格 |
| BaseInfoVO | 饰品基础信息 |
| AveragePriceVO | 均价数据 |
| WearResultRespDTO | 磨损查询结果 |
| InspectImageResultRespDTO | 检视图结果 |
| SteamBroadIndexVO | 大盘指数 |
| ItemKlineAO | K线请求参数 |
| QueryInspectByUrlAO | 检视链接请求 |
| QueryInspectByAsmdAO | ASMD参数请求 |

---

> **文档生成时间**: 2026-06-27
> **数据来源**: https://doc.steamdt.com/llms.txt
> **原始数据**: [raw/](raw/) | [structured/](structured/)
