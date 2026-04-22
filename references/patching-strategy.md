# 模板 Patch 策略

在选出最接近的模板之后，使用这份策略。

## 目标

以 **最小且有效的 diff**，把真实模板改造成目标工作流。

## Patch 顺序

1. Keep required system nodes if already present
   - `userGuide`
   - `workflowStart` (or template start node id if preserving ids is safer)

2. Keep structurally useful processing nodes
   - chat nodes
   - file nodes
   - API nodes
   - branch nodes
   - output nodes

3. Modify before deleting
   - If a node is structurally similar, repurpose it by changing name, prompt, and references.

4. Delete only clearly irrelevant nodes
   - remove task-specific leftovers that would cause wrong behavior

5. Add only the minimum new nodes needed

6. Reconnect edges carefully
   - preserve stable edge patterns where possible

7. Re-check all references
   - array references: `["nodeId", "key"]`
   - string references: `{{$nodeId.key$}}`

## 节点 patch 指南

### 对于 `chatNode`

通常 patch 这些内容：
- `name`
- `intro`
- `inputs[].value` for `systemPrompt`
- optional model/temperature/maxToken
- user input wiring

关键默认接线规则：
- every generated `chatNode` must include an explicit input with `key: "userChatInput"`
- it must not be left unwired
- the minimal default source is:
  ```json
  ["workflowStart", "userChatInput"]
  ```
- other upstream sources are allowed when the workflow intentionally routes user input through another stage
- if extra synthesized context is needed, place that context in other inputs or in prompt text; keep the minimal default above unless the workflow design clearly requires another source
- every generated `chatNode` must include an explicit input with `key: "history"`
- the minimal default value is:
  ```json
  6
  ```
- other history values are allowed when the workflow intentionally needs them

约束意图：
- explicit `userChatInput` and `history` are generation-time requirements for minimum usability
- the specific default values above are recommended safe defaults, not the only valid values
- when a workflow intentionally rewires these values, preserve the design instead of forcing a meaningless reset to defaults

如果现有结构已经有效，不要把所有字段都重写一遍。

### 对于 `datasetSearchNode`

通常 patch：
- selected dataset fields
- search query input wiring
- keep output shape if already usable

### 对于 HTTP 节点

通常 patch：
- URL
- headers
- body
- content type
- preserve the template's IO envelope where possible

### 对于 `answerNode`

通常 patch：
- response text source
- prompt or message text only if needed

## ID 策略

除非有充分理由，否则优先保留原模板节点 ID。

原因：
- fewer broken references
- fewer edge rewrites
- closer to known-good template structure

只有在这些情况下才改名：
- the original names/ids become too confusing
- new inserted nodes would be ambiguous
- the user explicitly wants cleaner ids

## 位置策略

优先保留保留节点的原始位置。
只有在这些情况下才调整位置：
- newly inserted nodes
- nodes whose old position becomes visually misleading

## Patch 后校验

完成 patch 后，确认：
- all kept references still point to existing nodes/outputs
- all new references use the correct syntax
- removed nodes are not still referenced
- every node on the main path is reachable
- output path still ends at an output node

## 推荐思维方式

把自己当成在 patch 一个已经能工作的系统的维护者，而不是凭空发明新系统的生成器。
