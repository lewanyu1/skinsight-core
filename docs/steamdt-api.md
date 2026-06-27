
# SteamDT 开放平台 API 文档

> 来源: https://doc.steamdt.com
> 基础域名: `https://open.steamdt.com`
> 数据格式: JSON
> 鉴权方式: 待确认
> 生成方式: scraper.py 自动爬取

---

## 目录

1. [获取steam饰品基础信息](#1-获取steam饰品基础信息)
2. [通过marketHashName查询饰品价格](#2-通过marketHashName查询饰品价格)
3. [通过marketHashName批量查询饰品价格](#3-通过marketHashName批量查询饰品价格)
4. [查询steam饰品k线数据](#4-查询steam饰品k线数据)
5. [通过MarketHashName查询所有平台近7天均价](#5-通过MarketHashName查询所有平台近7天均价)
6. [通过检视链接查询磨损度相关数据](#6-通过检视链接查询磨损度相关数据)
7. [通过ASMD参数查询磨损度相关数据](#7-通过ASMD参数查询磨损度相关数据)
8. [通过检视链接生成检视图](#8-通过检视链接生成检视图)
9. [通过ASMD参数生成检视图](#9-通过ASMD参数生成检视图)
10. [查询大盘k线数据](#10-查询大盘k线数据)
11. [查询大盘最新指数数据](#11-查询大盘最新指数数据)
12. [通用响应结构](#通用响应结构)

---

## 1. 获取steam饰品基础信息

| 项目 | 说明 |
|------|------|
| **URL** | `GET /open/cs2/v1/base` |
| **文档页** | https://doc.steamdt.com/278832832e0 |

### 请求参数

无。

### 响应字段

| `data` | array | |
| `  data.name` | string | |
| `  data.marketHashName` | string | |
| `  data.platformList` | array | |
| `    data.platformList.name` | string | |
| `    data.platformList.itemId` | string | |

---

## 2. 通过marketHashName查询饰品价格

| 项目 | 说明 |
|------|------|
| **URL** | `GET /open/cs2/v1/price/single` |
| **文档页** | https://doc.steamdt.com/278832830e0 |

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `marketHashName` | string | ✅ | |

### 响应字段

| `data` | array | |
| `  data.platform` | string | |
| `  data.platformItemId` | string | |
| `  data.sellPrice` | number | |
| `  data.sellCount` | number | |
| `  data.biddingPrice` | number | |
| `  data.biddingCount` | number | |
| `  data.updateTime` | number | |

---

## 3. 通过marketHashName批量查询饰品价格

| 项目 | 说明 |
|------|------|
| **URL** | `POST /open/cs2/v1/price/batch` |
| **文档页** | https://doc.steamdt.com/278832831e0 |

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `marketHashNames` | array | ✅ | |

### 响应字段

| `data` | array | |
| `  data.marketHashName` | string | |
| `  data.dataList` | array | |
| `    data.dataList.platform` | string | |
| `    data.dataList.platformItemId` | string | |
| `    data.dataList.sellPrice` | number | |
| `    data.dataList.sellCount` | number | |
| `    data.dataList.biddingPrice` | number | |
| `    data.dataList.biddingCount` | number | |
| `    data.dataList.updateTime` | number | |

---

## 4. 查询steam饰品k线数据

| 项目 | 说明 |
|------|------|
| **URL** | `POST /open/cs2/item/v1/kline` |
| **文档页** | https://doc.steamdt.com/428124801e0 |

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `marketHashName` | string | ✅ | |
| `type` | number | ✅ | |
| `platform` | string | ✅ | |
| `specialStyle` | string | ✅ | |

### 响应字段

| `data` | array | |

---

## 5. 通过MarketHashName查询所有平台近7天均价

| 项目 | 说明 |
|------|------|
| **URL** | `GET /open/cs2/v1/price/avg` |
| **文档页** | https://doc.steamdt.com/319748133e0 |

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `marketHashName` | string | ✅ | |

### 响应字段

| `data` | object | |
| `  data.marketHashName` | string | |
| `  data.avgPrice` | number | |
| `  data.dataList` | array | |
| `    data.dataList.platform` | string | |
| `    data.dataList.avgPrice` | number | |

---

## 6. 通过检视链接查询磨损度相关数据

| 项目 | 说明 |
|------|------|
| **URL** | `POST /open/cs2/v1/wear` |
| **文档页** | https://doc.steamdt.com/273806087e0 |

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `notifyUrl` | string | ✅ | |
| `inspectUrl` | string | ✅ | |

### 响应字段

| `data` | object | |
| `  data.sync` | boolean | |
| `  data.taskId` | string | |
| `  data.itemPreviewData` | object | |
| `    data.itemPreviewData.assetId` | number | |
| `    data.itemPreviewData.defindex` | number | |
| `    data.itemPreviewData.paintindex` | number | |
| `    data.itemPreviewData.rarity` | number | |
| `    data.itemPreviewData.quality` | number | |
| `    data.itemPreviewData.paintwear` | number | |
| `    data.itemPreviewData.floatWear` | string | |
| `    data.itemPreviewData.paintseed` | number | |
| `    data.itemPreviewData.stickers` | array | |
| `      data.itemPreviewData.stickers.stickerId` | number | |
| `      data.itemPreviewData.stickers.slot` | number | |
| `      data.itemPreviewData.stickers.wear` | number | |
| `  data.keychains` | array | |
| `    data.keychains.id` | number | |
| `    data.keychains.pattern` | number | |

---

## 7. 通过ASMD参数查询磨损度相关数据

| 项目 | 说明 |
|------|------|
| **URL** | `POST /open/cs2/v2/wear` |
| **文档页** | https://doc.steamdt.com/273806088e0 |

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `s` | number | ✅ | |
| `m` | number | ✅ | |
| `a` | number | ✅ | |
| `d` | string | ✅ | |
| `notifyUrl` | string | ✅ | |

### 响应字段

| `data` | object | |
| `  data.sync` | boolean | |
| `  data.taskId` | string | |
| `  data.itemPreviewData` | object | |
| `    data.itemPreviewData.assetId` | number | |
| `    data.itemPreviewData.defindex` | number | |
| `    data.itemPreviewData.paintindex` | number | |
| `    data.itemPreviewData.rarity` | number | |
| `    data.itemPreviewData.quality` | number | |
| `    data.itemPreviewData.paintwear` | number | |
| `    data.itemPreviewData.floatWear` | string | |
| `    data.itemPreviewData.paintseed` | number | |
| `    data.itemPreviewData.stickers` | array | |
| `      data.itemPreviewData.stickers.stickerId` | number | |
| `      data.itemPreviewData.stickers.slot` | number | |
| `      data.itemPreviewData.stickers.wear` | number | |
| `  data.keychains` | array | |
| `    data.keychains.id` | number | |
| `    data.keychains.pattern` | number | |

---

## 8. 通过检视链接生成检视图

| 项目 | 说明 |
|------|------|
| **URL** | `POST /open/cs2/v1/inspect` |
| **文档页** | https://doc.steamdt.com/273806089e0 |

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `notifyUrl` | string | ✅ | |
| `inspectUrl` | string | ✅ | |

### 响应字段

| `data` | object | |
| `  data.sync` | boolean | |
| `  data.taskId` | string | |
| `  data.screenshot` | object | |
| `    data.screenshot.itemId` | number | |
| `    data.screenshot.assetId` | number | |
| `    data.screenshot.fingerprint` | string | |
| `    data.screenshot.screenshots` | object | |
| `      data.screenshot.screenshots.front` | array | |
| `      data.screenshot.screenshots.back` | array | |
| `      data.screenshot.screenshots.detail` | array | |
| `    data.screenshot.cs2Version` | number | |
| `    data.screenshot.clientVersion` | string | |
| `    data.screenshot.existSticker` | boolean | |
| `    data.screenshot.protoEncodeStr` | string | |
| `    data.screenshot.createTime` | string | |
| `    data.screenshot.updateTime` | string | |

---

## 9. 通过ASMD参数生成检视图

| 项目 | 说明 |
|------|------|
| **URL** | `POST /open/cs2/v2/inspect` |
| **文档页** | https://doc.steamdt.com/273806090e0 |

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `s` | number | ✅ | |
| `m` | number | ✅ | |
| `a` | number | ✅ | |
| `d` | string | ✅ | |
| `notifyUrl` | string | ✅ | |

### 响应字段

| `data` | object | |
| `  data.sync` | boolean | |
| `  data.taskId` | string | |
| `  data.screenshot` | object | |
| `    data.screenshot.itemId` | number | |
| `    data.screenshot.assetId` | number | |
| `    data.screenshot.fingerprint` | string | |
| `    data.screenshot.screenshots` | object | |
| `      data.screenshot.screenshots.front` | array | |
| `      data.screenshot.screenshots.back` | array | |
| `      data.screenshot.screenshots.detail` | array | |
| `    data.screenshot.cs2Version` | number | |
| `    data.screenshot.clientVersion` | string | |
| `    data.screenshot.existSticker` | boolean | |
| `    data.screenshot.protoEncodeStr` | string | |
| `    data.screenshot.createTime` | string | |
| `    data.screenshot.updateTime` | string | |

---

## 10. 查询大盘k线数据

| 项目 | 说明 |
|------|------|
| **URL** | `POST /open/cs2/broad/v1/kline` |
| **文档页** | https://doc.steamdt.com/450452402e0 |

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `type` | number | ✅ | |

### 响应字段

| `data` | array | |

---

## 11. 查询大盘最新指数数据

| 项目 | 说明 |
|------|------|
| **URL** | `GET /open/cs2/broad/v1/index` |
| **文档页** | https://doc.steamdt.com/450452403e0 |

### 请求参数

无。

### 响应字段

| `data` | object | |
| `  data.broadMarketIndex` | number | |
| `  data.updateTime` | number | |
| `  data.diffYesterday` | number | |
| `  data.diffYesterdayRatio` | number | |
| `  data.historyMarketIndexList` | array | |

---

## 通用响应结构

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