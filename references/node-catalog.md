# FastGPT 节点目录

这份文件汇总了从 FastGPT 源码中确认过的节点类型。

确认来源：
- `packages/global/core/workflow/node/constant.ts`
- `packages/global/core/workflow/template/constants.ts`
- individual template files such as `workflowStart.ts`, `systemConfig.ts`, `assignedAnswer.ts`, `aiChat/index.ts`

## 基础应用工作流节点

这些是生成工作流时最常用、最有价值的节点：

- `userGuide` — system config node; source enum name is `systemConfig`, stored `flowNodeType` value is `"userGuide"`
- `workflowStart`
- `chatNode`
- `datasetSearchNode`
- `datasetConcatNode`
- `answerNode`
- `classifyQuestion`
- `contentExtract`
- `httpRequest468`
- `cfr` — query extension
- `tools` — tool call node
- `toolParams`
- `stopTool`
- `ifElseNode`
- `variableUpdate`
- `code`
- `textEditor`
- `customFeedback`
- `readFiles`
- `userSelect`
- `loop`
- `loopStart`
- `loopEnd`
- `formInput`
- `app`
- `tool`
- `toolSet`

## 真实模板补充节点

下面这些节点类型已经在当前内置模板中真实出现，说明导出工作流里确实会用到：

- `pluginModule`
- `comment`

处理建议：
- `pluginModule` 按真实样本做 patch，不要把它偷换成 `tool`
- `comment` 只是注释/说明节点，通常不参与主运行链路

## 特别说明

### 1. `userGuide`

FastGPT 源码里的 enum 映射为：
- `systemConfig = 'userGuide'`

因此 JSON 中应使用：

```json
{
  "nodeId": "userGuide",
  "flowNodeType": "userGuide",
  "inputs": [],
  "outputs": []
}
```

### 2. `workflowStart`

已确认的模板特征：
- unique
- non-deletable in UI
- exposes at least `userChatInput`
- can also be extended in some contexts with file input patterns

安全输出形态：

```json
{
  "key": "userChatInput",
  "type": "static",
  "valueType": "string"
}
```

### 3. `chatNode`

已确认的常见输入包括：
- model-related setting
- system prompt
- history
- dataset quote
- file link
- user chat input

已确认的常见输出包括：
- `history`
- `answerText`
- optionally `reasoningText`
- error output

对于生成场景，最安全、最小可用的模式是：
- feed user input into chat node
- optionally feed retrieval output into quote input
- connect `answerText` into `answerNode`

### 4. `datasetSearchNode`

用于 RAG / 知识库检索。

典型用途：
- take query from `workflowStart.userChatInput`
- return quoted/retrieved result to `chatNode`

### 5. `answerNode`

作为最终面向用户的输出节点使用。

典型输入：

```json
{
  "key": "text",
  "value": ["aiChatNode", "answerText"]
}
```

注意：不同模板里的 label 名称可能不同，但这个节点承担的是最终面向用户的响应出口。

### 6. `pluginModule`

虽然它没有放在上面的基础节点清单里，但真实模板已经多次出现这个类型。

当前样本里观察到的模式：
- `community-delay`
- `community-fetchUrl`
- 自定义 marketplace/plugin module

稳定特征：
- 顶层常见字段包含 `pluginId`、`toolConfig`、`catchError`
- 输入输出结构依赖具体插件，不存在一个通用输入模板
- 如果真实样本里已有 `toolConfig.systemTool.toolId`，应优先保留

## 保守生成策略

优先采用这些稳定模式：

### Plain assistant
- `userGuide` → `workflowStart` → `chatNode` → `answerNode`

### RAG assistant
- `userGuide` + `workflowStart` → `datasetSearchNode` → `chatNode` → `answerNode`

### File reader/summarizer
- `userGuide` + `workflowStart` → `readFiles` → `chatNode` → `answerNode`

### External API assistant
- `userGuide` + `workflowStart` → `httpRequest468` → `chatNode` → `answerNode`

### Plugin-based helper
- `userGuide` + `workflowStart` → `pluginModule` or `tool` → downstream node → `answerNode`

### Branching router
- `userGuide` + `workflowStart` → `classifyQuestion` or `ifElseNode` → downstream branches → `answerNode`

## 不要这样做

- Do not use node types not listed above.
- Do not rename `userGuide` to `systemConfig` in JSON output.
- Do not invent edge fields.
- Do not assume other workflow-engine conventions apply.
- Do not create loop structures unless the user truly needs iterative processing.
- Do not fabricate a universal `pluginModule` input shape.

## 基于源码的提醒

官方 FastGPT 源码确认了 enum 值和工作流 schema，但个别节点输入 key 的细节可能随版本变化。拿不准时：
- choose the smallest stable workflow
- prefer the closest real exported template over speculative reconstruction
- ask the user for missing specifics
- avoid pretending a speculative field is guaranteed
