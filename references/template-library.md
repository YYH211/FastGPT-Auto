# 模板库

这个 skill 应优先基于真实模板做 patch，而不是从零拼工作流。

## 模板来源

使用当前 skill 本地 `templates/` 目录中的公开模板。
把这个目录视为当前 skill 的标准模板位置。
不要只盯着下面前 4 个示例。应检查 `templates/` 里的全部公开模板 JSON，并选择最接近的真实基底。

核心锚点模板：

1. `document-translation-assistant.json`
   - domain: document
   - complexity: simple
   - features: readFiles, aiChat, answerNode
   - pattern: linear processing

2. `sales-coaching-master.json`
   - domain: conversation / guided interaction
   - complexity: medium
   - features: formInput, chatNode, multi-stage guidance
   - pattern: conversational flow

3. `resume-screening-assistant-feishu.json`
   - domain: data processing + external integration
   - complexity: complex
   - features: readFiles, chatNode, httpRequest, filtering, external integration
   - pattern: ETL / analysis flow

4. `ai-finance-daily.json`
   - domain: scheduled / aggregation / multi-stage generation
   - complexity: complex
   - features: scheduled trigger, multiple chat nodes, aggregation
   - pattern: parallel-ish aggregation flow

匹配时也应纳入考虑的其他公开模板：

- `flux-kontext-image-generation.json`
- `ppt-generation-assistant-jijyun.json`
- `invoice-recognition-assistant.json`
- `travel-budget-monitor-assistant.json`
- `resume-screening-assistant-excel.json`
- `interview-assistance-expert.json`
- `it-operations-qa-assistant.json`
- `smart-question-generation-assistant.json`

公开版不包含内部合同审批类模板。
如果当前副本的 `templates/` 目录中缺少这些文件，应明确说明这一限制；只有在确有必要时，才退回到直接构造或使用 `assets/` 中的示例。

## 生成策略

默认规则：
- Do **not** start from a blank JSON unless no template is even remotely suitable.
- First choose the closest real template.
- Then patch it with the minimum necessary changes.

## 模板优先匹配启发式

根据以下因素判断哪个模板最接近：
- task domain
- interaction mode
- whether file input is needed
- whether external API/http is needed
- whether multi-stage generation is needed
- whether the workflow is linear, conversational, ETL-like, or aggregation-like

## 实用匹配提示

- content generation / guided authoring / multi-step article production → usually start from `sales-coaching-master.json` or `ai-finance-daily.json`
- file processing → start from `document-translation-assistant.json`
- complex pipeline with API + analysis → start from `resume-screening-assistant-feishu.json`
- scheduled or multi-branch aggregation → start from `ai-finance-daily.json`
- external API driven review / audit → prefer an `integration` template and clearly surface required variables
- environment-specific workflow examples should be treated as references, not default anchors

## Patch 策略

相比整套重建，更优先使用这些 patch 操作：
- modify node prompts
- rename nodes
- add a small number of nodes
- remove obviously irrelevant nodes
- reconnect edges
- update `chatConfig.welcomeText`
- update input/output references

避免无意义的大改：
- keep original node field structure where possible
- keep original renderTypeList / labels / output shapes when compatible
- preserve template-specific fields unless they conflict with the user's task
- normalize all generated string references to the skill-wide required format: `{{$nodeId.key$}}`

## 最后手段

只有在以下情况下才从零生成：
- all template match scores are clearly poor
- patching would require replacing most of the template anyway
- the user explicitly asks for a blank/custom build
