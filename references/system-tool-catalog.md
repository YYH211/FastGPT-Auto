# FastGPT 系统工具目录参考

## 文件定位

- 本文档是当前 skill 自带的工具目录摘要。
- 详细结构索引见同目录下的 `system-tool-index.json`。
- 这不是可直接导入 FastGPT 的 workflow JSON。
- 它是一份系统工具目录元数据，适合给 skill 当作“预选工具索引”和“节点构造参考源”。

## 统计概览

- 工具总条目：`122`
- 顶层工具：`48`
- 子工具：`74`

## 构造规则

- 顶层工具且存在子工具：默认映射为 `toolSet` 节点。
- 顶层工具且没有子工具：默认映射为 `tool` 节点。
- 子工具：运行时通常映射为 `tool` 节点，并挂在父级 `toolSet` 下面。
- 源文件里的 `toolId` 是原始 ID，写入 FastGPT 节点 `toolConfig` 时通常需要转成 `systemTool-{toolId}`。
- 父子关系同理，`parentId` 进入节点配置时也要带上 `systemTool-` 前缀。

## 工作流节点映射示例

### 单工具

```json
{
  "flowNodeType": "tool",
  "toolConfig": {
    "systemTool": {
      "toolId": "systemTool-fetchUrl"
    }
  }
}
```

### 工具集

```json
{
  "flowNodeType": "toolSet",
  "toolConfig": {
    "systemToolSet": {
      "toolId": "systemTool-metaso",
      "toolList": [
        {
          "toolId": "systemTool-metaso/metasoSearch",
          "name": "秘塔搜索",
          "description": "基于秘塔 API 的智能搜索工具"
        }
      ]
    }
  }
}
```

## 意图推荐

- `search`: metaso, perplexity, bocha, searchXNG, searchApi, google, duckduckgo, tavily, firecrawl, fetchUrl, dailyHot, wiki, youtube, arxiv, jinaAi, searchInfinity
- `publish_and_notify`: wechatOfficialAccount, WeWorkWebhook, DingTalkWebhook, feishu, smtpEmail
- `image_generation`: dalle3, blackForestLab, gptImage, stability, seedream, aliModelStudio, minimax, silliconFlow
- `document_and_ppt`: chatPPT, markdownTransform, Doc2X, mineru, docDiff, base64Decode, drawing
- `data_and_storage`: databaseConnection, dbops, redis, feishuBitable
- `utility`: getTime, delay, mathExprVal, whisper

## 顶层工具总表

| 工具名 | rawToolId | 节点类型 | 子工具数 | 密钥 | 最新版本 |
| --- | --- | --- | --- | --- | --- |
| 钉钉 webhook | `DingTalkWebhook` | `tool` | 0 | 否 | `0.1.0` |
| Doc2X 服务 | `Doc2X` | `toolSet` | 1 | 是 | - |
| 企业微信 webhook | `WeWorkWebhook` | `tool` | 0 | 否 | `0.1.0` |
| 阿里云百炼 | `aliModelStudio` | `toolSet` | 3 | 是 | - |
| ArXiv 工具集 | `arxiv` | `toolSet` | 5 | 否 | - |
| Base64 解析 | `base64Decode` | `toolSet` | 3 | 否 | - |
| Flux 绘图 | `blackForestLab` | `toolSet` | 2 | 是 | - |
| 博查搜索 | `bocha` | `tool` | 0 | 是 | `0.1.0` |
| 必优ChatPPT | `chatPPT` | `tool` | 0 | 是 | `0.1.0` |
| 热榜工具 | `dailyHot` | `tool` | 0 | 否 | `0.1.0` |
| Dalle3 绘图 | `dalle3` | `tool` | 0 | 是 | `0.1.0` |
| 数据库连接 | `databaseConnection` | `tool` | 0 | 是 | `0.1.0` |
| 数据库操作 | `dbops` | `toolSet` | 5 | 否 | - |
| 流程等待 | `delay` | `tool` | 0 | 否 | `1.0` |
| 文档对比工具 | `docDiff` | `tool` | 0 | 否 | `1.0.0` |
| BI图表功能 | `drawing` | `toolSet` | 1 | 否 | - |
| DuckDuckGo服务 | `duckduckgo` | `toolSet` | 4 | 否 | - |
| 飞书 webhook | `feishu` | `tool` | 0 | 否 | `0.1.0` |
| 飞书多维表格 | `feishuBitable` | `toolSet` | 13 | 是 | - |
| 网页内容抓取 | `fetchUrl` | `tool` | 0 | 否 | `0.1.0` |
| Firecrawl | `firecrawl` | `toolSet` | 1 | 是 | - |
| 获取当前时间 | `getTime` | `tool` | 0 | 否 | `0.1.0` |
| GitHub 工具集 | `github` | `toolSet` | 2 | 是 | - |
| Google 搜索 | `google` | `tool` | 0 | 是 | `0.1.0` |
| gpt-image 绘图 | `gptImage` | `toolSet` | 2 | 是 | - |
| Jina AI 工具集 | `jinaAi` | `toolSet` | 2 | 是 | - |
| libulibu 工具集 | `libulibu` | `toolSet` | 1 | 是 | - |
| Markdown 转文件 | `markdownTransform` | `tool` | 0 | 否 | `0.1.0` |
| 数学公式执行 | `mathExprVal` | `tool` | 0 | 否 | `0.1.0` |
| 秘塔搜索工具集 | `metaso` | `toolSet` | 1 | 是 | - |
| MinerU | `mineru` | `toolSet` | 2 | 是 | - |
| minimax 工具集 | `minimax` | `toolSet` | 1 | 是 | - |
| 墨迹天气 | `mojiWeather` | `toolSet` | 1 | 是 | - |
| OpenRouter 多模态 | `openrouterMultiModal` | `toolSet` | 1 | 是 | - |
| Perplexity 工具集 | `perplexity` | `toolSet` | 1 | 是 | - |
| Redis 缓存 | `redis` | `toolSet` | 3 | 是 | - |
| SearchApi | `searchApi` | `toolSet` | 5 | 是 | - |
| 融合信息搜索 | `searchInfinity` | `tool` | 0 | 是 | `0.1.0` |
| SearXNG 搜索 | `searchXNG` | `tool` | 0 | 否 | `0.1.0` |
| Seedream 4.0 绘图 | `seedream` | `tool` | 0 | 是 | `0.1.0` |
| 硅基流动 | `silliconFlow` | `toolSet` | 4 | 是 | - |
| Email 邮件发送 | `smtpEmail` | `tool` | 0 | 否 | `0.1.0` |
| Stability AI 图像生成 | `stability` | `toolSet` | 1 | 是 | - |
| Tavily 搜索 | `tavily` | `toolSet` | 4 | 是 | - |
| 微信公众号工具集 | `wechatOfficialAccount` | `toolSet` | 4 | 是 | - |
| Whisper 语音转文字 | `whisper` | `tool` | 0 | 是 | `0.1.0` |
| Wiki搜索 | `wiki` | `tool` | 0 | 否 | `0.1.0` |
| YouTube 工具集 | `youtube` | `toolSet` | 1 | 否 | - |

## 与文章自动发布工作流最相关的工具

### Flux 绘图 (`blackForestLab`)

- 运行时 ID：`systemTool-blackForestLab`
- 默认节点类型：`toolSet`
- 是否需要密钥：是
- 密钥字段：`apiKey`
- 子工具：`blackForestLab/kontextGeneration`, `blackForestLab/kontextEditing`

### 热榜工具 (`dailyHot`)

- 运行时 ID：`systemTool-dailyHot`
- 默认节点类型：`tool`
- 是否需要密钥：否
- 最新版本：`0.1.0`
- 输入字段：`sources`
- 输出字段：`hotNewsList`

### Dalle3 绘图 (`dalle3`)

- 运行时 ID：`systemTool-dalle3`
- 默认节点类型：`tool`
- 是否需要密钥：是
- 密钥字段：`url`, `authorization`
- 最新版本：`0.1.0`
- 输入字段：`prompt`
- 输出字段：`link`, `system_error`

### 流程等待 (`delay`)

- 运行时 ID：`systemTool-delay`
- 默认节点类型：`tool`
- 是否需要密钥：否
- 最新版本：`1.0`
- 输入字段：`ms`
- 输出字段：-

### 网页内容抓取 (`fetchUrl`)

- 运行时 ID：`systemTool-fetchUrl`
- 默认节点类型：`tool`
- 是否需要密钥：否
- 最新版本：`0.1.0`
- 输入字段：`url`
- 输出字段：`title`, `result`

### 获取当前时间 (`getTime`)

- 运行时 ID：`systemTool-getTime`
- 默认节点类型：`tool`
- 是否需要密钥：否
- 最新版本：`0.1.0`
- 输入字段：-
- 输出字段：`time`

### 秘塔搜索工具集 (`metaso`)

- 运行时 ID：`systemTool-metaso`
- 默认节点类型：`toolSet`
- 是否需要密钥：是
- 密钥字段：`apiKey`
- 子工具：`metaso/metasoSearch`

### Perplexity 工具集 (`perplexity`)

- 运行时 ID：`systemTool-perplexity`
- 默认节点类型：`toolSet`
- 是否需要密钥：是
- 密钥字段：`apiKey`
- 子工具：`perplexity/findResults`

### 微信公众号工具集 (`wechatOfficialAccount`)

- 运行时 ID：`systemTool-wechatOfficialAccount`
- 默认节点类型：`toolSet`
- 是否需要密钥：是
- 密钥字段：`appId`, `secret`
- 子工具：`wechatOfficialAccount/uploadMarkdownToDraft`, `wechatOfficialAccount/getAuthToken`, `wechatOfficialAccount/publishDraft`, `wechatOfficialAccount/uploadPermanentMaterial`

## 接入 skill 的建议

- 把 `references/system-tool-index.json` 当作精确字段和工具 ID 的结构化来源。
- 在 `SKILL.md` 里补一条规则：涉及系统工具时，先查 rawToolId，再生成带 `systemTool-` 前缀的 `toolConfig`。
- 搜索、发布、绘图、通知这几类优先做显式工具映射，不要让模型自由脑补。
- 如果某个顶层工具 `versionList` 为空但有子工具，优先按 `toolSet` 处理；真正的输入输出从子工具版本里取。
