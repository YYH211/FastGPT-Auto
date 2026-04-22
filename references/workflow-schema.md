# FastGPT 工作流 Schema 约束

这份参考资料汇总了从 FastGPT 源码树中确认过的工作流结构。

## 已确认的顶层结构

FastGPT 工作流核心结构如下：

```json
{
  "nodes": [],
  "edges": [],
  "chatConfig": {}
}
```

不过从导入角度看，也要参考 `import-shapes.md`。在某些导入入口里，可能还需要包装后的模板对象。

源码 schema 确认来源：
- `packages/global/core/workflow/type/index.ts`
- `packages/global/core/app/type.ts`
- `packages/global/core/workflow/type/edge.ts`
- `packages/global/core/workflow/type/node.ts`

## 节点结构

每个存储下来的 workflow 节点，本质上都会受到 `StoreNodeItemTypeSchema` 和通用 node schema 的约束。

使用下面这个最小安全结构：

```json
{
  "nodeId": "aiChatNode",
  "name": "AI 对话",
  "flowNodeType": "chatNode",
  "position": { "x": 200, "y": 0 },
  "inputs": [],
  "outputs": []
}
```

### 已确认的通用字段

- `nodeId`: string
- `name`: string
- `flowNodeType`: enum value
- `position.x`: number
- `position.y`: number
- `inputs`: array
- `outputs`: array

可选字段当然也可能存在，但除非确有必要，否则不要乱加。

## Edge 结构

每条 edge 使用下面这个已确认结构：

```json
{
  "source": "workflowStart",
  "sourceHandle": "workflowStart-source-right",
  "target": "aiChatNode",
  "targetHandle": "aiChatNode-target-left"
}
```

必填字段：
- `source`
- `sourceHandle`
- `target`
- `targetHandle`

## chatConfig 结构

`chatConfig` 中已确认安全可用的字段包括：
- `welcomeText`
- `variables`
- `instruction`
- optional advanced config sections such as `autoExecute`, `questionGuide`, `ttsConfig`, `whisperConfig`, `scheduledTriggerConfig`, `chatInputGuide`, `fileSelectConfig`

对大多数生成工作流来说，`chatConfig` 保持精简即可：

```json
{
  "welcomeText": "",
  "variables": []
}
```

## 必要基线节点

对于普通应用工作流，始终应包含：
- `userGuide` node (`flowNodeType: "userGuide"`)
- `workflowStart` node (`flowNodeType: "workflowStart"`)

对于面向用户响应的工作流，通常还应包含：
- `answerNode`

## 引用格式

只使用以下两种引用方式：

### 直接数组引用

```json
["workflowStart", "userChatInput"]
```

### 字符串中的模板插值

```json
"请根据用户问题回答：{{$workflowStart.userChatInput$}}"
```

重要：在这个 skill 里，要求的字符串引用格式是：
- `{{$nodeId.key$}}`

不要输出 `{$nodeId.key$}` 这种单花括号引用。
也不要发明别的占位符语法。

## 安全布局默认值

使用简单的从左到右布局。

推荐位置：
- `userGuide`: `{ "x": -600, "y": -250 }`
- `workflowStart`: `{ "x": -150, "y": 100 }`
- then increment x by about 300~400 per major node
- stack parallel/branch nodes vertically with ~120~180 y gap

## 校验清单

返回 JSON 之前，确认：
- all node ids are unique
- all edges refer to real nodes
- `workflowStart` can reach the processing path
- the final answer/output node is connected
- there are no orphan nodes
- all references point to plausible upstream outputs
- only supported `flowNodeType` values are used
- every `chatNode` must include a `userChatInput` input item
- the minimal default wiring for `userChatInput` is `["workflowStart", "userChatInput"]`, but other intentional sources are allowed
- every `chatNode` must include a `history` input item
- the minimal default for `history` is `6`, but other intentional values are allowed
- if the workflow expects file inputs, `chatConfig.fileSelectConfig.canSelectFile` is enabled
- if the workflow expects image inputs, `chatConfig.fileSelectConfig.canSelectImg` is enabled
