---
name: fastgpt-workflow-generator
description: 从自然语言需求或已有 workflow 草稿生成可导入 FastGPT 的 workflow JSON。适用于用户要求创建、设计、生成、修改、修复或校验 FastGPT 工作流，或者表达“给我生成一个工作流 / create a workflow / generate workflow JSON / FastGPT 工作流”这类需求，或明确想要可直接复制导入 FastGPT 的 JSON 内容。
---

# FastGPT 工作流生成器

生成 **可直接导入 FastGPT 的 workflow JSON**。把这个 skill 当成一个受 schema 约束的构造器，而不是用来发散 brainstorming 的助手。

## 路径约定

- 把当前 `SKILL.md` 所在目录视为这个 skill 的根目录。
- 默认按 skill 根目录解析 `references/`、`scripts/`、`assets/`、`templates/` 下的相对路径。
- 不要依赖外部绝对路径来补 skill 自己该带的内容。

## 先读取这些参考资料

1. 读取 `references/requirement-template.md`
2. 读取 `references/ambiguity-checklist.md`
3. 读取 `references/workflow-schema.md`
4. 读取 `references/import-shapes.md`
5. 读取 `references/node-catalog.md`
6. 读取 `references/node-field-baseline.md`
7. 读取 `references/template-library.md`
8. 读取 `references/patching-strategy.md`
9. 读取 `references/system-config-mapping.md`
10. 读取 `references/workflow-patterns.md`
11. 如果工作流可能使用内置系统工具，读取 `references/system-tool-catalog.md`
12. 如果需要精确的 tool id、子工具结构或节点配置形态，按需检查 `references/system-tool-index.json`，不要一次性全读进上下文

不要跳过。这些文件里整理了真正的工作约束，来源包括：
- 用户要求参考的 skill
- FastGPT 公开仓库源码和工作流模板

## 工作模式

每次都按这个顺序执行：

1. **澄清用户任务，消除歧义**
2. **产出结构化需求工件**
3. **先选最接近的真实模板**
4. **对该模板做最小必要 patch**
5. **把所需能力映射到 system config 和应用入口设置**
6. **只有当模板 patch 明显不合适时，才直接拼节点**
7. **当内置系统工具相关时，优先使用真实的 tool/toolSet/pluginModule 配置，而不是伪造 HTTP 占位**
8. **按正确的导入形态生成 workflow JSON**
9. **从 schema、引用语法、连接规则、system-config 联动、tool-config 联动几个方面做自校验**
10. **有条件时运行本地校验器**
11. **返回可直接复制粘贴的 JSON 文件**

如果用户只说了很宽泛的话，比如“给我生成一个工作流”，**不要瞎猜**。先围绕业务任务本身提几个聚焦问题。

## 阶段 1：需求采集

使用 `requirement-template.md` 中的问题集，以及 `ambiguity-checklist.md` 中的检查项。

目标：在没有隐藏假设的前提下，采集出足够构建工作流的细节。

重要：澄清阶段关注的是 **用户真实要做的任务**，不是让用户决定 FastGPT 要用什么节点。除非用户明确要求掌控技术实现，否则不要让用户去选 node type、edge 结构或实现细节。

至少要提取出这些信息：
- workflow purpose
- who the end user is and what they are trying to accomplish
- interaction mode: chat / form / file processing / tool workflow
- user inputs
- expected final output
- whether knowledge base retrieval is needed
- whether external HTTP/API calls are needed
- whether conditional branching is needed
- whether loop/batch processing is needed
- whether file upload/reading is needed
- any fixed prompts, output format, or business rules

如果关键字段缺失，只问最少的一组补充问题。
用产品/业务语言提问，不要用节点语言提问。

## 阶段 2：需求工件

当需求已经足够清晰后，在生成 workflow 之前，先整理一份简洁的需求工件，可以用 Markdown 或 JSON。

推荐结构：

```json
{
  "name": "workflow name",
  "goal": "what the workflow achieves",
  "interactionMode": "chat|form|file|tool",
  "inputs": [],
  "outputs": [],
  "requiredNodes": [],
  "optionalNodes": [],
  "integrations": [],
  "constraints": [],
  "assumptions": []
}
```

如果用户要求直接给最终工作流，而需求此时也已经清晰，那这份工件可以简短一点，然后继续往下做。

## 阶段 3：模板优先规划

先读 `template-library.md`，优先挑出最接近的真实模板。

然后读 `patching-strategy.md`，对这个模板做最小必要 patch。

接着读 `system-config-mapping.md`，确保所需业务能力也同步体现在应用级配置里，比如 `chatConfig`、文件上传设置、定时设置、变量暴露等。

`workflow-patterns.md` 只作为次级规划辅助，在比较模板或没有合适模板时再用。

只使用这个 skill 参考资料里确认支持的 node type。

如果任务涉及搜索、发布、图像生成、通知、数据库操作、工具函数等内置能力，在发明 `httpRequest468` 兜底方案之前，先检查 `system-tool-catalog.md`。只要工具目录里有，就优先用真实的 `tool`、`toolSet` 或 `pluginModule` 配置。

这是内部设计步骤。除非用户明确想控制节点，否则不用让用户去指定节点。

如果所选模板里已经有，通常应保留这些节点：
- `userGuide` node (`flowNodeType: "userGuide"`)
- `workflowStart` node

通常也应保留或以此结束：
- `answerNode`

patch 要保守。优先选择基于真实模板做小而有效的改动，不要炫技式重建。

### 必做的规划检查

在开始写 JSON 前，先明确这些点：
- which real template is the best base
- which nodes can be kept as-is
- which nodes should be repurposed by patching prompts/labels/config
- which nodes must be added or removed
- whether any built-in system tool should be used instead of a hand-made HTTP node
- whether the chosen tool should be represented as `tool` or `toolSet`
- whether the tool requires `systemTool` or `systemToolSet` config
- whether the raw `toolId` from the catalog must be converted to `systemTool-...` runtime ids
- which outputs feed which later inputs
- whether references should use array form `["nodeId", "key"]`
- whether any text concatenation requires `{{$nodeId.key$}}` template syntax
- whether `chatConfig.variables` is needed
- whether file/image upload must be enabled in `chatConfig`
- whether scheduled config must be enabled
- where the output for the user is produced
- whether every `chatNode.userChatInput` exists explicitly
- the minimal default for `chatNode.userChatInput` is `["workflowStart", "userChatInput"]`, but other intentional sources are allowed
- whether every `chatNode.history` exists explicitly
- the minimal default for `chatNode.history` is `6`, but other intentional history settings are allowed

## 阶段 4：JSON 生成规则

严格遵循 `workflow-schema.md`。

### 硬性要求

- Output valid JSON, not JSON5
- 除非用户明确要求 template-wrapper 包装，否则默认采用 `import-shapes.md` 中的 **bare workflow shape**
- The top level should usually contain:
  - `nodes`
  - `edges`
  - `chatConfig`
- If wrapper format is explicitly requested, the nested `workflow` object must contain `nodes`, `edges`, and `chatConfig`
- Every node must have at least:
  - `nodeId`
  - `name`
  - `flowNodeType`
  - `position`
  - `inputs`
  - `outputs`
- For import-oriented output, prefer also including compatibility fields from `node-field-baseline.md`, especially:
  - `intro`
  - `avatar`
  - `version`
- Every edge must have at least:
  - `source`
  - `sourceHandle`
  - `target`
  - `targetHandle`
- `flowNodeType` must be one of the supported values in `node-catalog.md`
- `position.x` 和 `position.y` 使用数值
- `nodeId` 使用唯一值

### NodeId 规则

使用可读的、camelCase 风格的英文 id。

Reserved ids:
- `userGuide`
- `workflowStart`

推荐示例：
- `aiChatNode`
- `datasetSearchNode1`
- `httpRequestNode`
- `metasoToolSet`
- `wechatOfficialAccountToolSet`
- `answerNode`

如果同类型节点有多个，加稳定后缀区分。

### Edge-handle 规则

默认连接 handle：
- `sourceHandle`: `"<sourceNodeId>-source-right"`
- `targetHandle`: `"<targetNodeId>-target-left"`

除非工作流明确需要特殊的分支/输出 handle，否则都按这个规则走。

### 内置工具规则

当 `system-tool-catalog.md` 中存在内置系统工具时：

- Prefer `tool` for a single tool with no children
- Prefer `toolSet` for a built-in tool folder / tool collection
- 使用精确的运行时 tool id 形态 `systemTool-{rawToolId}`
- For child tools, use `systemTool-{rawChildToolId}`
- Do not invent unofficial tool ids
- Do not replace an available built-in search/publish/drawing tool with `httpRequest468` unless the user explicitly wants a custom external API
- If a top-level catalog entry has no direct `versionList` but has child tools, treat it as a `toolSet`
- When a tool requires secrets, surface them through app variables or clearly-marked configuration fields rather than hardcoding them into the workflow
- If the exact child tool is unclear, ask the user or choose the smallest plausible child tool and state the assumption

对于体积较大的 `system-tool-index.json`，按 `rawToolId`、`runtimeToolId` 或 category 选择性查看，不要把整个文件全塞进上下文。

#### `system_input_config`（secretInputs）硬性规则

当 `tool`/`pluginModule` 节点存在输入 `key: "system_input_config"` 时，必须遵守：

- `inputList` 只用于声明字段 schema，不要在 `inputList` 子项里写 `value`。
- 需要预填连接参数时，只能写在 `system_input_config.value` 顶层对象中，key 必须与 `inputList[].key` 对齐。
- `numberInput` 类型（例如 `port`）在 `system_input_config.value` 中必须是数字，不能是字符串。
- 如果不确定部署环境是否允许导入密钥，优先把 `system_input_config.value` 留空并在说明里提示用户导入后在 UI 手工填写。

错误示例（禁止）：

```json
{
  "key": "system_input_config",
  "inputList": [
    { "key": "host", "inputType": "input", "value": "db.example.com" }
  ]
}
```

正确示例（允许）：

```json
{
  "key": "system_input_config",
  "inputList": [
    { "key": "host", "inputType": "input", "required": true },
    { "key": "port", "inputType": "numberInput", "required": true }
  ],
  "value": {
    "host": "db.example.com",
    "port": 3306
  }
}
```

### 引用规则

只允许两种格式：

1. 直接引用：
```json
["workflowStart", "userChatInput"]
```

2. 内嵌模板字符串：
```json
"问题：{{$workflowStart.userChatInput$}}"
```

在这个 skill 里，不要输出 `{$nodeId.key$}` 这种单花括号引用。
也不要发明别的插值语法。

## 阶段 5：自校验

回复前先做心智校验。

### 结构校验

检查：
- JSON parses
- determine whether the output is a bare workflow or a template wrapper
- by default, prefer bare workflow and ensure top level contains `nodes`, `edges`, and `chatConfig`
- if template wrapper was explicitly requested, ensure `id`, `name`, `type`, and `workflow` are present
- ensure the actual workflow object contains `nodes`, `edges`, and `chatConfig`
- every edge source/target refers to an existing node
- every referenced `[nodeId, key]` points to a real node output or start output
- app-level configuration is present when required by the workflow capability set

### 工作流校验

检查：
- `userGuide` exists
- `workflowStart` exists
- at least one user-visible output path exists
- no orphan nodes
- no impossible cycles unless using loop nodes
- every nontrivial node receives the inputs it needs

### 导入兼容性校验

检查：
- the output still resembles a patched real template, not an invented foreign structure
- important nodes include compatibility-oriented fields such as `avatar`, `intro`, and `version`
- outputs include `id` when appropriate
- no fake fields copied from other workflow engines
- preserved template fields were not unnecessarily stripped away
- every `chatNode` includes a `userChatInput` selector
- that selector is not blank
- 其最小默认值是 workflow start → user question（`["workflowStart", "userChatInput"]`），但也允许工作流有意使用其他来源
- every `chatNode` includes a `history` input
- 其最小默认值是 `6`，但也允许工作流有意使用其他值
- required app entry capabilities are enabled, e.g. file upload for `readFiles` workflows
- for any `system_input_config` input:
  - `inputList` items must not contain field-level `value`
  - runtime config must be placed at `system_input_config.value` (object) if prefilled
  - numeric fields such as `port` must be numeric in `system_input_config.value`

### 最小化校验

检查：
- no extra nodes that do not contribute to the result
- no unsupported node types

## 响应风格

### 如果需求不完整

提简洁的澄清问题，然后停止。

## 阶段 6：本地校验

如果你能写临时 JSON 文件，并且当前就在 skill 根目录下，那么对生成结果执行严格校验：

```bash
python3 scripts/validate_fastgpt_workflow.py --strict-generated <workflow.json>
```

校验器支持两种模式：
- default mode：兼容当前 skill 内置的 FastGPT 导出模板
- `--strict-generated`：推荐用于校验这个 skill 新生成的工作流结果；它会强约束必需结构，但把“最小默认值”视为推荐，而不是唯一合法值

校验策略：
- always-error constraints：会破坏解析、导入形态、顶层结构、节点结构、edge 目标存在性、或引用源节点存在性的规则，一律报错
- strict-generated errors：为了保证“新生成的工作流导入后直接可用”而必须成立的规则，例如必需聊天输入、明确输出路径检查、能力与配置的联动检查
- warnings only：最小默认值建议、兼容性字段、看起来不常见但可能合法的 handle，以及某些可能依赖 FastGPT 运行时扩展输出、当前校验器暂时看不全的引用

校验器默认必须能校验 bare workflow 形态。
如果是有意生成 template wrapper，也可以支持对应校验。

在返回最终结果前，必须修掉所有 validator errors。
warning 也要认真复查，尤其是 unreachable nodes 或缺少可见输出这种提示。

## 响应风格

### 如果需求不完整

提简洁的澄清问题，然后停止。

### 如果需求完整

按这个顺序返回：
1. 一句很短的工作流设计摘要
2. 最终 JSON，放在一个代码块里
3. 只有确实需要时，才补一两句简短导入说明

如果用户明确想要可直接复制粘贴导入的内容，优先只返回 **一个 JSON 代码块**，外加最多一两行说明。

## 质量标准

输出结果应尽量做到：导入 FastGPT 时只需要极少甚至不需要手工修改。

避免：
- placeholder pseudo-fields
- unsupported nodes
- speculative schema sections
- long explanations before the JSON

如果有些值没法仅凭 prompt 确定，可以采用这些策略之一：
- ask the user
- leave a clearly marked editable empty value only where FastGPT normally expects user configuration

宁可诚实说明，也不要硬编。
