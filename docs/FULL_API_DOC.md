# SteamDT 开放平台 - 完整 API 文档

> 自动生成时间: 2026-06-27 10:11:53
> 来源: https://doc.steamdt.com
> 总页面数: 43
> API 端点: 11
> Schema/DTO: 29

---

## 目录

### 文档
1. [一分钟接入SteamDT开放平台](#6279815m0)
2. [接口权限列表(请优先查看)](#6369437m0)
3. [特殊款式对照表](#8323999m0)

### API 端点
1. [通过marketHashName查询饰品价格](#278832830e0) - `GET /open/cs2/v1/price/single`
2. [通过marketHashName批量查询饰品价格](#278832831e0) - `POST /open/cs2/v1/price/batch`
3. [查询steam饰品k线数据](#428124801e0) - `GET /open/cs2/item/v1/kline`
4. [通过MarketHashName查询所有平台近7天均价](#319748133e0) - `GET /open/cs2/v1/price/avg`
5. [通过检视链接查询磨损度相关数据](#273806087e0) - `GET /open/cs2/v1/wear`
6. [通过ASMD参数查询磨损度相关数据](#273806088e0) - `GET /open/cs2/v2/wear`
7. [通过检视链接生成检视图,前提是已经获取到饰品的磨损度](#273806089e0) - `GET /open/cs2/v1/inspect`
8. [通过ASMD参数生成检视图,前提是已经获取到饰品的磨损度](#273806090e0) - `GET /open/cs2/v2/inspect`
9. [查询大盘k线数据](#450452402e0) - `GET /open/cs2/broad/v1/kline`
10. [查询大盘最新指数数据](#450452403e0) - `GET /open/cs2/broad/v1/index`
11. [获取steam饰品基础信息](#278832832e0) - `GET /open/cs2/v1/base`

### Schema/DTO
1. [StickerWearDTO](#154220434d0)
2. [SteamStickerWearDTO](#154579830d0)
3. [PlatformPriceVO](#157024915d0)
4. [ItemPreviewDataBlockDTO](#154220435d0)
5. [SteamKeychainsDTO](#154579831d0)
6. [WebApiResListPlatformPriceVO](#157024916d0)
7. [WearResultRespDTO](#154220436d0)
8. [SteamAssetWearDTO](#154579832d0)
9. [BatchPlatformPriceVO](#157024917d0)
10. [WebApiResWearResultRespDTO](#154220437d0)
11. [WebApiResListBatchPlatformPriceVO](#157024918d0)
12. [QueryInspectByUrlAO](#154220438d0)
13. [PlatformPriceAO](#157024919d0)
14. [Object](#253951027d0)
15. [QueryInspectByAsmdAO](#154220439d0)
16. [PlatformBaseInfoVO](#157024920d0)
17. [BaseInfoVO](#157024921d0)
18. [ScreenshotDTO](#155866058d0)
19. [WebApiResListBaseInfoVO](#157024922d0)
20. [AssetScreenshotDTO](#155866059d0)
21. [InspectImageResultRespDTO](#155866060d0)
22. [WebApiResInspectImageResultRespDTO](#155866061d0)
23. [PlatformAveragePriceVO](#182841349d0)
24. [AveragePriceVO](#182841350d0)
25. [WebApiResAveragePriceVO](#182841351d0)
26. [ItemKlineAO](#253951030d0)
27. [BroadKlineAO](#269155923d0)
28. [SteamBroadIndexVO](#269155924d0)
29. [WebApiResSteamBroadIndexVO](#269155925d0)

---

## 文档

### 一分钟接入SteamDT开放平台

- **Slug**: `6279815m0`
- **链接**: https://doc.steamdt.com/6279815m0

> 来源: https://doc.steamdt.com


## 一分钟接入SteamDT开放平台


### 前期准备#


### 请求结构#

```

```

### 服务地址#


| 服务地域 | 域名 | 备注 |
| --- | --- | --- |
| 国内外 | https://open.steamdt.com | 开放平台OpenAPI接入地址 |


### 通信协议#


### 请求方式#


### 请求参数#


### 字符编码#


### 签名机制#


### 返回结果#

```
{
  "success": true,
  "data": {
  },
  "errorCode": 0,
  "errorMsg": "",
  "errorData": {},
  "errorCodeStr": ""
}
```
```
{
  "errorCode": 4001,
  "errorMsg": "请输入正确的 app-Key",
  "success": false
}
```

| 字段 | 类型 | 是否一定返回 | 说明 |
| --- | --- | --- | --- |
| success | Boolean | 是 | 本次请求是否成功,未true代表服务端流程走完,没有异常;如果为false,则需要去看errorCode字段的错误码,根据此错误码业务上进行处理 |
| errorCode | Int32 | 是 | 错误码,当success为true时,errorCode必为0;当success为false时,errorCode必非0 |
| errorMsg | String | 是 | 错误消息,当success为true时,errorMsg为空字符串;当success为false时,errorMsg错误描述 |
| errorData | Object | 否 | 发生错误时的返回数据,此结构类型不定,根据各个接口返回不同的类型 |
| errorCodeStr | String | 否 | 错误的英文简要描述,只有当success为false时, 才可能有非空字符串返回 |
| data | Object | 否 | 请求成功时返回的业务数据,结构根据每个接口不同 |


---

### 接口权限列表(请优先查看)

- **Slug**: `6369437m0`
- **链接**: https://doc.steamdt.com/6369437m0

> 来源: https://doc.steamdt.com


## 接口权限列表(请优先查看)


### 接口权限#


| url | 备注 | 权限 |
| --- | --- | --- |
| /open/cs2/v1/wear | 通过检视链接查询磨损度相关数据 | 每小时36000次 |
| /open/cs2/v2/wear | 通过ASMD参数查询磨损度相关数据 | 每小时36000次 |
| /open/cs2/v1/inspect | 通过检视链接生成检视图,前提是已经获取到饰品的磨损度 | 每日100次 |
| /open/cs2/v2/inspect | 通过ASMD参数生成检视图,前提是已经获取到饰品的磨损度 | 每日100次 |
| /open/cs2/v1/price/single | 通过marketHashName查询饰品价格 | 每分钟60次 |
| /open/cs2/v1/price/batch | 通过marketHashName批量查询饰品价格 | 每分钟1次 |
| /open/cs2/v1/base | 获取steam饰品基础信息 | 每日1次 |
| /open/cs2/item/v1/kline | 获取steam饰品K线数据 | 每分钟120次 |


---

### 特殊款式对照表

- **Slug**: `8323999m0`
- **链接**: https://doc.steamdt.com/8323999m0

> 来源: https://doc.steamdt.com


## 特殊款式对照表


| 分组 | 值 | 中文描述 |
| --- | --- | --- |
| RANK（档位） | 1st | 一档 |
| RANK（档位） | 2nd | 二档 |
| RANK（档位） | 3rd | 三档 |
| RANK（档位） | 4th | 四档 |
| RANK（档位） | 5th | 五档 |
| RANK（档位） | 6th | 六档 |
| RANK（档位） | 7th | 七档 |
| RANK（档位） | 8th | 八档 |
| RANK（档位） | 9th | 九档 |
| RANK（档位） | 10th | 十档 |
| TIER（阶段） | t1 | t1 |
| TIER（阶段） | t2 | t2 |
| TIER（阶段） | t3 | t3 |
| TIER（阶段） | t4 | t4 |
| SUN（太阳） | sun | 官图太阳 |
| PHASE（阶段） | p1 | p1 |
| PHASE（阶段） | p2 | p2 |
| PHASE（阶段） | p3 | p3 |
| PHASE（阶段） | p4 | p4 |
| PHASE（宝石） | ruby | 红宝石 |
| PHASE（宝石） | emerald | 绿宝石 |
| PHASE（宝石） | sapphire | 蓝宝石 |
| PHASE（宝石） | blackpearl | 黑珍珠 |
| SINGLEBLUE（单面全蓝） | singleblue | 单面全蓝 |
| CRIMSON_KIMONO（绯红和服） | crimson_kimono_p1 | 一档 |
| CRIMSON_KIMONO（绯红和服） | crimson_kimono_p2 | 二档 |
| CRIMSON_KIMONO（绯红和服） | crimson_kimono_p3 | 三档 |
| CRIMSON_KIMONO（绯红和服） | crimson_kimono_p4 | 四档 |
| CRIMSON_KIMONO（绯红和服） | crimson_kimono_p5 | 五档 |
| CRIMSON_KIMONO（绯红和服） | crimson_kimono_p6 | 六档 |


---

## API 端点

### 通过marketHashName查询饰品价格

| 项目 | 说明 |
|------|------|
| **URL** | `GET /open/cs2/v1/price/single` |
| **文档页** | https://doc.steamdt.com/278832830e0 |
| **分类** | CS2饰品信息 |
| **说明** | 获取全平台饰品价格、求购等数据。 |

#### 请求参数

无。

#### 请求示例

```bash
curl --location 'https://open.steamdt.com/open/cs2/v1/price/single?marketHashName=undefined'
```

#### 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `data` | unknown | |
| `platform` | unknown | |
| `platformItemId` | unknown | |
| `sellPrice` | unknown | |
| `sellCount` | unknown | |
| `biddingPrice` | unknown | |
| `biddingCount` | unknown | |
| `updateTime` | unknown | |

#### 响应示例

```json
{
  "success": false,
  "data": [
    {
      "platform": "",
      "platformItemId": "",
      "sellPrice": 0.0,
      "sellCount": 0,
      "biddingPrice": 0.0,
      "biddingCount": 0,
      "updateTime": 0
    }
  ],
  "errorCode": 0,
  "errorMsg": "",
  "errorData": {},
  "errorCodeStr": ""
}
```

---

### 通过marketHashName批量查询饰品价格

| 项目 | 说明 |
|------|------|
| **URL** | `POST /open/cs2/v1/price/batch` |
| **文档页** | https://doc.steamdt.com/278832831e0 |
| **分类** | CS2饰品信息 |
| **说明** | 批量查询饰品价格、求购等数据 |

#### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `marketHashNames` | list | ✅ |  |

#### 请求示例

```bash
curl --location 'https://open.steamdt.com/open/cs2/v1/price/batch' \
--header 'Content-Type: application/json' \
--data '{
    "marketHashNames": [
        "string"
    ]
}'
```

#### 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `data` | unknown | |
| `marketHashName` | unknown | |
| `dataList` | unknown | |
| `platform` | unknown | |
| `platformItemId` | unknown | |
| `sellPrice` | unknown | |
| `sellCount` | unknown | |
| `biddingPrice` | unknown | |
| `biddingCount` | unknown | |
| `updateTime` | unknown | |

#### 响应示例

```json
{
  "success": false,
  "data": [
    {
      "marketHashName": "",
      "dataList": [
        {
          "platform": "",
          "platformItemId": "",
          "sellPrice": 0.0,
          "sellCount": 0,
          "biddingPrice": 0.0,
          "biddingCount": 0,
          "updateTime": 0
        }
      ]
    }
  ],
  "errorCode": 0,
  "errorMsg": "",
  "errorData": {},
  "errorCodeStr": ""
}
```

---

### 查询steam饰品k线数据

| 项目 | 说明 |
|------|------|
| **URL** | `GET /open/cs2/item/v1/kline` |
| **文档页** | https://doc.steamdt.com/428124801e0 |
| **分类** | CS2饰品信息 |
| **说明** | 查询饰品K线数据(不包含成交数据) |

#### 请求参数

无。

#### 请求示例

```bash
curl --location 'https://open.steamdt.com/open/cs2/item/v1/kline' \
--header 'Content-Type: application/json' \
--data '{
    "marketHashName": "string",
    "type": 1,
    "platform": "string",
    "specialStyle": "string"
}'
```

#### 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `data` | unknown | |

#### 响应示例

```json
{
  "success": false,
  "data": [
    [
      {}
    ]
  ],
  "errorCode": 0,
  "errorMsg": "",
  "errorData": {},
  "errorCodeStr": ""
}
```

---

### 通过MarketHashName查询所有平台近7天均价

| 项目 | 说明 |
|------|------|
| **URL** | `GET /open/cs2/v1/price/avg` |
| **文档页** | https://doc.steamdt.com/319748133e0 |
| **分类** | CS2饰品信息 |
| **说明** | marketHashName 为Steam官方饰品名称，可通过获取Steam饰品基础信息接口获得 |

#### 请求参数

无。

#### 请求示例

```bash
curl --location 'https://open.steamdt.com/open/cs2/v1/price/avg?marketHashName=undefined'
```

#### 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `data` | unknown | |
| `marketHashName` | unknown | |
| `avgPrice` | unknown | |
| `dataList` | unknown | |
| `platform` | unknown | |
| `avgPrice` | unknown | |

#### 响应示例

```json
{
  "success": false,
  "data": {
    "marketHashName": "",
    "avgPrice": 0.0,
    "dataList": [
      {
        "platform": "",
        "avgPrice": 0.0
      }
    ]
  },
  "errorCode": 0,
  "errorMsg": "",
  "errorData": {},
  "errorCodeStr": ""
}
```

---

### 通过检视链接查询磨损度相关数据

| 项目 | 说明 |
|------|------|
| **URL** | `GET /open/cs2/v1/wear` |
| **文档页** | https://doc.steamdt.com/273806087e0 |
| **分类** | CS2饰品信息 |

#### 请求参数

无。

#### 请求示例

```bash
curl --location 'https://open.steamdt.com/open/cs2/v1/wear' \
--header 'Content-Type: application/json' \
--data '{
    "notifyUrl": "string",
    "inspectUrl": "string"
}'
```

#### 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `data` | unknown | |
| `sync` | unknown | |
| `taskId` | unknown | |
| `itemPreviewData` | unknown | |
| `assetId` | unknown | |
| `defindex` | unknown | |
| `paintindex` | unknown | |
| `rarity` | unknown | |
| `quality` | unknown | |
| `paintwear` | unknown | |
| `floatWear` | unknown | |
| `paintseed` | unknown | |
| `stickers` | unknown | |
| `stickerId` | unknown | |
| `slot` | unknown | |
| `wear` | unknown | |
| `keychains` | unknown | |
| `id` | unknown | |
| `pattern` | unknown | |

#### 响应示例

```json
{
  "success": false,
  "data": {
    "sync": false,
    "success": false,
    "taskId": "",
    "itemPreviewData": {
      "assetId": 0,
      "defindex": 0,
      "paintindex": 0,
      "rarity": 0,
      "quality": 0,
      "paintwear": 0,
      "floatWear": "",
      "paintseed": 0,
      "stickers": [
        {
          "stickerId": 0,
          "slot": 0,
          "wear": 0.0
        }
      ],
      "keychains": [
        {
          "id": 0,
          "pattern": 0
        }
      ]
    }
  },
  "errorCode": 0,
  "errorMsg": "",
  "errorData": {},
  "errorCodeStr": ""
}
```

---

### 通过ASMD参数查询磨损度相关数据

| 项目 | 说明 |
|------|------|
| **URL** | `GET /open/cs2/v2/wear` |
| **文档页** | https://doc.steamdt.com/273806088e0 |
| **分类** | CS2饰品信息 |

#### 请求参数

无。

#### 请求示例

```bash
curl --location 'https://open.steamdt.com/open/cs2/v2/wear' \
--header 'Content-Type: application/json' \
--data '{
    "s": 0,
    "m": 0,
    "a": 0,
    "d": "string",
    "notifyUrl": "string"
}'
```

#### 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `data` | unknown | |
| `sync` | unknown | |
| `taskId` | unknown | |
| `itemPreviewData` | unknown | |
| `assetId` | unknown | |
| `defindex` | unknown | |
| `paintindex` | unknown | |
| `rarity` | unknown | |
| `quality` | unknown | |
| `paintwear` | unknown | |
| `floatWear` | unknown | |
| `paintseed` | unknown | |
| `stickers` | unknown | |
| `stickerId` | unknown | |
| `slot` | unknown | |
| `wear` | unknown | |
| `keychains` | unknown | |
| `id` | unknown | |
| `pattern` | unknown | |

#### 响应示例

```json
{
  "success": false,
  "data": {
    "sync": false,
    "success": false,
    "taskId": "",
    "itemPreviewData": {
      "assetId": 0,
      "defindex": 0,
      "paintindex": 0,
      "rarity": 0,
      "quality": 0,
      "paintwear": 0,
      "floatWear": "",
      "paintseed": 0,
      "stickers": [
        {
          "stickerId": 0,
          "slot": 0,
          "wear": 0.0
        }
      ],
      "keychains": [
        {
          "id": 0,
          "pattern": 0
        }
      ]
    }
  },
  "errorCode": 0,
  "errorMsg": "",
  "errorData": {},
  "errorCodeStr": ""
}
```

---

### 通过检视链接生成检视图,前提是已经获取到饰品的磨损度

| 项目 | 说明 |
|------|------|
| **URL** | `GET /open/cs2/v1/inspect` |
| **文档页** | https://doc.steamdt.com/273806089e0 |
| **分类** | CS2饰品信息 |

#### 请求参数

无。

#### 请求示例

```bash
curl --location 'https://open.steamdt.com/open/cs2/v1/inspect' \
--header 'Content-Type: application/json' \
--data '{
    "notifyUrl": "string",
    "inspectUrl": "string"
}'
```

#### 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `data` | unknown | |
| `sync` | unknown | |
| `taskId` | unknown | |
| `screenshot` | unknown | |
| `itemId` | unknown | |
| `assetId` | unknown | |
| `fingerprint` | unknown | |
| `screenshots` | unknown | |
| `front` | unknown | |
| `back` | unknown | |
| `detail` | unknown | |
| `cs2Version` | unknown | |
| `clientVersion` | unknown | |
| `existSticker` | unknown | |
| `protoEncodeStr` | unknown | |
| `createTime` | unknown | |
| `updateTime` | unknown | |

#### 响应示例

```json
{
  "success": false,
  "data": {
    "sync": false,
    "success": false,
    "taskId": "",
    "screenshot": {
      "itemId": 0,
      "assetId": 0,
      "fingerprint": "",
      "screenshots": {
        "front": [
          ""
        ],
        "back": [
          ""
        ],
        "detail": [
          ""
        ]
      },
      "cs2Version": 0,
      "clientVersion": "",
      "existSticker": false,
      "protoEncodeStr": "",
      "createTime": "",
      "updateTime": ""
    }
  },
  "errorCode": 0,
  "errorMsg": "",
  "errorData": {},
  "errorCodeStr": ""
}
```

---

### 通过ASMD参数生成检视图,前提是已经获取到饰品的磨损度

| 项目 | 说明 |
|------|------|
| **URL** | `GET /open/cs2/v2/inspect` |
| **文档页** | https://doc.steamdt.com/273806090e0 |
| **分类** | CS2饰品信息 |

#### 请求参数

无。

#### 请求示例

```bash
curl --location 'https://open.steamdt.com/open/cs2/v2/inspect' \
--header 'Content-Type: application/json' \
--data '{
    "s": 0,
    "m": 0,
    "a": 0,
    "d": "string",
    "notifyUrl": "string"
}'
```

#### 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `data` | unknown | |
| `sync` | unknown | |
| `taskId` | unknown | |
| `screenshot` | unknown | |
| `itemId` | unknown | |
| `assetId` | unknown | |
| `fingerprint` | unknown | |
| `screenshots` | unknown | |
| `front` | unknown | |
| `back` | unknown | |
| `detail` | unknown | |
| `cs2Version` | unknown | |
| `clientVersion` | unknown | |
| `existSticker` | unknown | |
| `protoEncodeStr` | unknown | |
| `createTime` | unknown | |
| `updateTime` | unknown | |

#### 响应示例

```json
{
  "success": false,
  "data": {
    "sync": false,
    "success": false,
    "taskId": "",
    "screenshot": {
      "itemId": 0,
      "assetId": 0,
      "fingerprint": "",
      "screenshots": {
        "front": [
          ""
        ],
        "back": [
          ""
        ],
        "detail": [
          ""
        ]
      },
      "cs2Version": 0,
      "clientVersion": "",
      "existSticker": false,
      "protoEncodeStr": "",
      "createTime": "",
      "updateTime": ""
    }
  },
  "errorCode": 0,
  "errorMsg": "",
  "errorData": {},
  "errorCodeStr": ""
}
```

---

### 查询大盘k线数据

| 项目 | 说明 |
|------|------|
| **URL** | `GET /open/cs2/broad/v1/kline` |
| **文档页** | https://doc.steamdt.com/450452402e0 |
| **分类** | CS2饰品信息 |

#### 请求参数

无。

#### 请求示例

```bash
curl --location 'https://open.steamdt.com/open/cs2/broad/v1/kline' \
--header 'Content-Type: application/json' \
--data '{
    "type": 1
}'
```

#### 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `data` | unknown | |

#### 响应示例

```json
{
  "success": false,
  "data": [
    [
      {}
    ]
  ],
  "errorCode": 0,
  "errorMsg": "",
  "errorData": {},
  "errorCodeStr": ""
}
```

---

### 查询大盘最新指数数据

| 项目 | 说明 |
|------|------|
| **URL** | `GET /open/cs2/broad/v1/index` |
| **文档页** | https://doc.steamdt.com/450452403e0 |
| **分类** | CS2饰品信息 |

#### 请求参数

无。

#### 请求示例

```bash
curl --location 'https://open.steamdt.com/open/cs2/broad/v1/index'
```

#### 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `data` | unknown | |
| `broadMarketIndex` | unknown | |
| `updateTime` | unknown | |
| `diffYesterday` | unknown | |
| `diffYesterdayRatio` | unknown | |
| `historyMarketIndexList` | unknown | |

#### 响应示例

```json
{
  "success": false,
  "data": {
    "broadMarketIndex": 0.0,
    "updateTime": 0,
    "diffYesterday": 0.0,
    "diffYesterdayRatio": 0.0,
    "historyMarketIndexList": [
      [
        {}
      ]
    ]
  },
  "errorCode": 0,
  "errorMsg": "",
  "errorData": {},
  "errorCodeStr": ""
}
```

---

### 获取steam饰品基础信息

| 项目 | 说明 |
|------|------|
| **URL** | `GET /open/cs2/v1/base` |
| **文档页** | https://doc.steamdt.com/278832832e0 |
| **说明** | 所有接口数据都基于该接口返回的marketHashName，请优先对接该接口 |

#### 请求参数

无。

#### 请求示例

```bash
curl --location 'https://open.steamdt.com/open/cs2/v1/base'
```

#### 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `data` | unknown | |
| `name` | unknown | |
| `marketHashName` | unknown | |
| `platformList` | unknown | |
| `name` | unknown | |
| `itemId` | unknown | |

#### 响应示例

```json
{
  "success": false,
  "data": [
    {
      "name": "",
      "marketHashName": "",
      "platformList": [
        {
          "name": "",
          "itemId": ""
        }
      ]
    }
  ],
  "errorCode": 0,
  "errorMsg": "",
  "errorData": {},
  "errorCodeStr": ""
}
```

---

## Schema/DTO 定义

### StickerWearDTO

- **文档页**: https://doc.steamdt.com/154220434d0

#### 字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `slot` | unknown |  |
| `stickerId` | unknown |  |
| `wear` | unknown |  |
| `scale` | unknown |  |
| `rotation` | unknown |  |
| `tintId` | unknown |  |
| `offsetX` | unknown |  |
| `offsetY` | unknown |  |
| `offsetZ` | unknown |  |
| `pattern` | unknown |  |

---

### SteamStickerWearDTO

- **文档页**: https://doc.steamdt.com/154579830d0

#### 字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `stickerId` | unknown |  |
| `slot` | unknown |  |
| `wear` | unknown |  |

---

### PlatformPriceVO

- **文档页**: https://doc.steamdt.com/157024915d0

#### 字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `platform` | unknown |  |
| `platformItemId` | unknown |  |
| `sellPrice` | unknown |  |
| `sellCount` | unknown |  |
| `biddingPrice` | unknown |  |
| `biddingCount` | unknown |  |
| `updateTime` | unknown |  |

---

### ItemPreviewDataBlockDTO

- **文档页**: https://doc.steamdt.com/154220435d0

#### 字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `accountId` | unknown |  |
| `itemId` | unknown |  |
| `defindex` | unknown |  |
| `paintindex` | unknown |  |
| `rarity` | unknown |  |
| `quality` | unknown |  |
| `paintwear` | unknown |  |
| `paintseed` | unknown |  |
| `killEaterScoreType` | unknown |  |
| `killEaterValue` | unknown |  |
| `customName` | unknown |  |
| `inventory` | unknown |  |
| `origin` | unknown |  |
| `questId` | unknown |  |
| `dropreason` | unknown |  |
| `musicIndex` | unknown |  |
| `entIndex` | unknown |  |
| `stickers` | unknown |  |
| `slot` | unknown |  |
| `stickerId` | unknown |  |
| `wear` | unknown |  |
| `scale` | unknown |  |
| `rotation` | unknown |  |
| `tintId` | unknown |  |
| `offsetX` | unknown |  |
| `offsetY` | unknown |  |
| `offsetZ` | unknown |  |
| `pattern` | unknown |  |
| `keychains` | unknown |  |
| `slot` | unknown |  |
| `stickerId` | unknown |  |
| `wear` | unknown |  |
| `scale` | unknown |  |
| `rotation` | unknown |  |
| `tintId` | unknown |  |
| `offsetX` | unknown |  |
| `offsetY` | unknown |  |
| `offsetZ` | unknown |  |
| `pattern` | unknown |  |
| `protoEncodeStr` | unknown |  |

---

### SteamKeychainsDTO

- **文档页**: https://doc.steamdt.com/154579831d0

#### 字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `id` | unknown |  |
| `pattern` | unknown |  |

---

### WebApiResListPlatformPriceVO

- **文档页**: https://doc.steamdt.com/157024916d0

#### 字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `success` | unknown |  |
| `data` | unknown |  |
| `platform` | unknown |  |
| `platformItemId` | unknown |  |
| `sellPrice` | unknown |  |
| `sellCount` | unknown |  |
| `biddingPrice` | unknown |  |
| `biddingCount` | unknown |  |
| `updateTime` | unknown |  |
| `errorCode` | unknown |  |
| `errorMsg` | unknown |  |
| `errorData` | unknown |  |
| `errorCodeStr` | unknown |  |

---

### WearResultRespDTO

- **文档页**: https://doc.steamdt.com/154220436d0

#### 字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `sync` | unknown |  |
| `success` | unknown |  |
| `taskId` | unknown |  |
| `itemPreviewData` | unknown |  |
| `assetId` | unknown |  |
| `defindex` | unknown |  |
| `paintindex` | unknown |  |
| `rarity` | unknown |  |
| `quality` | unknown |  |
| `paintwear` | unknown |  |
| `floatWear` | unknown |  |
| `paintseed` | unknown |  |
| `stickers` | unknown |  |
| `stickerId` | unknown |  |
| `slot` | unknown |  |
| `wear` | unknown |  |
| `keychains` | unknown |  |
| `id` | unknown |  |
| `pattern` | unknown |  |

---

### SteamAssetWearDTO

- **文档页**: https://doc.steamdt.com/154579832d0

#### 字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `assetId` | unknown |  |
| `defindex` | unknown |  |
| `paintindex` | unknown |  |
| `rarity` | unknown |  |
| `quality` | unknown |  |
| `paintwear` | unknown |  |
| `floatWear` | unknown |  |
| `paintseed` | unknown |  |
| `stickers` | unknown |  |
| `stickerId` | unknown |  |
| `slot` | unknown |  |
| `wear` | unknown |  |
| `keychains` | unknown |  |
| `id` | unknown |  |
| `pattern` | unknown |  |

---

### BatchPlatformPriceVO

- **文档页**: https://doc.steamdt.com/157024917d0

#### 字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `marketHashName` | unknown |  |
| `dataList` | unknown |  |
| `platform` | unknown |  |
| `platformItemId` | unknown |  |
| `sellPrice` | unknown |  |
| `sellCount` | unknown |  |
| `biddingPrice` | unknown |  |
| `biddingCount` | unknown |  |
| `updateTime` | unknown |  |

---

### WebApiResWearResultRespDTO

- **文档页**: https://doc.steamdt.com/154220437d0

#### 字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `success` | unknown |  |
| `data` | unknown |  |
| `sync` | unknown |  |
| `success` | unknown |  |
| `taskId` | unknown |  |
| `itemPreviewData` | unknown |  |
| `assetId` | unknown |  |
| `defindex` | unknown |  |
| `paintindex` | unknown |  |
| `rarity` | unknown |  |
| `quality` | unknown |  |
| `paintwear` | unknown |  |
| `floatWear` | unknown |  |
| `paintseed` | unknown |  |
| `stickers` | unknown |  |
| `stickerId` | unknown |  |
| `slot` | unknown |  |
| `wear` | unknown |  |
| `keychains` | unknown |  |
| `id` | unknown |  |
| `pattern` | unknown |  |
| `errorCode` | unknown |  |
| `errorMsg` | unknown |  |
| `errorData` | unknown |  |
| `errorCodeStr` | unknown |  |

---

### WebApiResListBatchPlatformPriceVO

- **文档页**: https://doc.steamdt.com/157024918d0

#### 字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `success` | unknown |  |
| `data` | unknown |  |
| `marketHashName` | unknown |  |
| `dataList` | unknown |  |
| `platform` | unknown |  |
| `platformItemId` | unknown |  |
| `sellPrice` | unknown |  |
| `sellCount` | unknown |  |
| `biddingPrice` | unknown |  |
| `biddingCount` | unknown |  |
| `updateTime` | unknown |  |
| `errorCode` | unknown |  |
| `errorMsg` | unknown |  |
| `errorData` | unknown |  |
| `errorCodeStr` | unknown |  |

---

### QueryInspectByUrlAO

- **文档页**: https://doc.steamdt.com/154220438d0

#### 字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `notifyUrl` | unknown |  |
| `inspectUrl` | unknown |  |

---

### PlatformPriceAO

- **文档页**: https://doc.steamdt.com/157024919d0

#### 字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `marketHashNames` | unknown |  |

---

### Object

- **文档页**: https://doc.steamdt.com/253951027d0

---

### QueryInspectByAsmdAO

- **文档页**: https://doc.steamdt.com/154220439d0

#### 字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `s` | unknown |  |
| `m` | unknown |  |
| `a` | unknown |  |
| `d` | unknown |  |
| `notifyUrl` | unknown |  |

---

### PlatformBaseInfoVO

- **文档页**: https://doc.steamdt.com/157024920d0

#### 字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `name` | unknown |  |
| `itemId` | unknown |  |

---

### BaseInfoVO

- **文档页**: https://doc.steamdt.com/157024921d0

#### 字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `name` | unknown |  |
| `marketHashName` | unknown |  |
| `platformList` | unknown |  |
| `name` | unknown |  |
| `itemId` | unknown |  |

---

### ScreenshotDTO

- **文档页**: https://doc.steamdt.com/155866058d0

#### 字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `front` | unknown |  |
| `back` | unknown |  |
| `detail` | unknown |  |

---

### WebApiResListBaseInfoVO

- **文档页**: https://doc.steamdt.com/157024922d0

#### 字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `success` | unknown |  |
| `data` | unknown |  |
| `name` | unknown |  |
| `marketHashName` | unknown |  |
| `platformList` | unknown |  |
| `name` | unknown |  |
| `itemId` | unknown |  |
| `errorCode` | unknown |  |
| `errorMsg` | unknown |  |
| `errorData` | unknown |  |
| `errorCodeStr` | unknown |  |

---

### AssetScreenshotDTO

- **文档页**: https://doc.steamdt.com/155866059d0

#### 字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `itemId` | unknown |  |
| `assetId` | unknown |  |
| `fingerprint` | unknown |  |
| `screenshots` | unknown |  |
| `front` | unknown |  |
| `back` | unknown |  |
| `detail` | unknown |  |
| `cs2Version` | unknown |  |
| `clientVersion` | unknown |  |
| `existSticker` | unknown |  |
| `protoEncodeStr` | unknown |  |
| `createTime` | unknown |  |
| `updateTime` | unknown |  |

---

### InspectImageResultRespDTO

- **文档页**: https://doc.steamdt.com/155866060d0

#### 字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `sync` | unknown |  |
| `success` | unknown |  |
| `taskId` | unknown |  |
| `screenshot` | unknown |  |
| `itemId` | unknown |  |
| `assetId` | unknown |  |
| `fingerprint` | unknown |  |
| `screenshots` | unknown |  |
| `front` | unknown |  |
| `back` | unknown |  |
| `detail` | unknown |  |
| `cs2Version` | unknown |  |
| `clientVersion` | unknown |  |
| `existSticker` | unknown |  |
| `protoEncodeStr` | unknown |  |
| `createTime` | unknown |  |
| `updateTime` | unknown |  |

---

### WebApiResInspectImageResultRespDTO

- **文档页**: https://doc.steamdt.com/155866061d0

#### 字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `success` | unknown |  |
| `data` | unknown |  |
| `sync` | unknown |  |
| `success` | unknown |  |
| `taskId` | unknown |  |
| `screenshot` | unknown |  |
| `itemId` | unknown |  |
| `assetId` | unknown |  |
| `fingerprint` | unknown |  |
| `screenshots` | unknown |  |
| `front` | unknown |  |
| `back` | unknown |  |
| `detail` | unknown |  |
| `cs2Version` | unknown |  |
| `clientVersion` | unknown |  |
| `existSticker` | unknown |  |
| `protoEncodeStr` | unknown |  |
| `createTime` | unknown |  |
| `updateTime` | unknown |  |
| `errorCode` | unknown |  |
| `errorMsg` | unknown |  |
| `errorData` | unknown |  |
| `errorCodeStr` | unknown |  |

---

### PlatformAveragePriceVO

- **文档页**: https://doc.steamdt.com/182841349d0

#### 字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `platform` | unknown |  |
| `avgPrice` | unknown |  |

---

### AveragePriceVO

- **文档页**: https://doc.steamdt.com/182841350d0

#### 字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `marketHashName` | unknown |  |
| `avgPrice` | unknown |  |
| `dataList` | unknown |  |
| `platform` | unknown |  |
| `avgPrice` | unknown |  |

---

### WebApiResAveragePriceVO

- **文档页**: https://doc.steamdt.com/182841351d0

#### 字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `success` | unknown |  |
| `data` | unknown |  |
| `marketHashName` | unknown |  |
| `avgPrice` | unknown |  |
| `dataList` | unknown |  |
| `platform` | unknown |  |
| `avgPrice` | unknown |  |
| `errorCode` | unknown |  |
| `errorMsg` | unknown |  |
| `errorData` | unknown |  |
| `errorCodeStr` | unknown |  |

---

### ItemKlineAO

- **文档页**: https://doc.steamdt.com/253951030d0

#### 字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `marketHashName` | unknown |  |
| `type` | unknown |  |
| `platform` | unknown |  |
| `specialStyle` | unknown |  |

---

### BroadKlineAO

- **文档页**: https://doc.steamdt.com/269155923d0

#### 字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `type` | unknown |  |

---

### SteamBroadIndexVO

- **文档页**: https://doc.steamdt.com/269155924d0

#### 字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `broadMarketIndex` | unknown |  |
| `updateTime` | unknown |  |
| `diffYesterday` | unknown |  |
| `diffYesterdayRatio` | unknown |  |
| `historyMarketIndexList` | unknown |  |

---

### WebApiResSteamBroadIndexVO

- **文档页**: https://doc.steamdt.com/269155925d0

#### 字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `success` | unknown |  |
| `data` | unknown |  |
| `broadMarketIndex` | unknown |  |
| `updateTime` | unknown |  |
| `diffYesterday` | unknown |  |
| `diffYesterdayRatio` | unknown |  |
| `historyMarketIndexList` | unknown |  |
| `errorCode` | unknown |  |
| `errorMsg` | unknown |  |
| `errorData` | unknown |  |
| `errorCodeStr` | unknown |  |

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