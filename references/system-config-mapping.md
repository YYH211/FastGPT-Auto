# 系统配置映射

这份文件定义了：业务能力应该如何映射到 FastGPT 的应用级配置。

生成器不能只看 workflow 节点够不够，还必须同步配置 `chatConfig` 和相关系统设置，这样生成出来的应用才能在 FastGPT UI 里真正可用。

## 核心规则

当某项能力是工作流所必需时，在相关场景下要同时配置 **三层**：
1. workflow nodes
2. workflow start inputs/outputs
3. `chatConfig` / system configuration

不要只生成节点链路，却忘了开启对应的应用入口能力。

## 能力映射

### 1. 文件上传工作流

适用场景：
- the user uploads resumes, PDFs, Word docs, spreadsheets, or other files
- the workflow includes `readFiles`
- the workflow consumes `workflowStart.userFiles`

必需映射：
- `workflowStart.outputs` should include `userFiles`
- downstream node(s) should consume `userFiles`
- `chatConfig.fileSelectConfig.canSelectFile` must be `true`
- `chatConfig.fileSelectConfig.canSelectImg` should usually be `false` unless images are also needed

推荐默认值：

```json
"fileSelectConfig": {
  "canSelectFile": true,
  "canSelectImg": false,
  "maxFiles": 10,
  "customPdfParse": true
}
```

如果任务明确要求单文件或批量上传，可以调整 `maxFiles`。
对于简历/文档类任务，推荐设置 `customPdfParse: true`。

### 2. 图片上传工作流

适用场景：
- the workflow expects screenshots, product images, photos, or scanned image inputs

必需映射：
- `chatConfig.fileSelectConfig.canSelectImg` must be `true`

如果文件和图片都需要：

```json
"fileSelectConfig": {
  "canSelectFile": true,
  "canSelectImg": true
}
```

### 3. 定时工作流

适用场景：
- the workflow is cron-like, timed, auto-generated, or daily/weekly scheduled

必需映射：
- include scheduled trigger related configuration
- configure `chatConfig.scheduledTriggerConfig`
- ensure the workflow pattern supports scheduled prompting if needed

安全默认值：

```json
"scheduledTriggerConfig": {
  "cronString": "",
  "timezone": "Asia/Shanghai",
  "defaultPrompt": ""
}
```

### 4. 语音输入 / 语音工作流

适用场景：
- the user speaks instead of typing
- voice transcription should be enabled

必需映射：
- `chatConfig.whisperConfig.open = true`
- set `autoSend` and `autoTTSResponse` according to the use case

### 5. 引导问题 / 提示建议工作流

适用场景：
- the UI should guide the user with example questions or entry prompts

在合适时需要映射：
- `chatConfig.questionGuide`
- `chatConfig.chatInputGuide`

### 6. 变量驱动工作流

适用场景：
- the workflow requires explicit user-supplied parameters beyond a free-text question
- the app should expose named variables or configuration fields

必需映射：
- populate `chatConfig.variables`
- if the chosen template already uses `userGuide.inputs.variables`, preserve and patch them instead of replacing them blindly

## 简历工作流特殊规则

对于简历/文档筛选类工作流：
- enable file upload
- prefer `maxFiles: 15` when the template is derived from a resume/document workflow
- set `customPdfParse: true`
- ensure `workflowStart.outputs` contains `userFiles`

推荐文件配置：

```json
"fileSelectConfig": {
  "canSelectFile": true,
  "canSelectImg": false,
  "maxFiles": 15,
  "customPdfParse": true
}
```

## 校验清单

返回 JSON 之前，确认：
- if `readFiles` exists, file upload is enabled in `chatConfig`
- if `workflowStart.userFiles` is referenced, file upload is enabled in `chatConfig`
- if the task needs images, image upload is enabled
- if the task is scheduled, scheduled config exists
- if variables are required by the user task, `chatConfig.variables` is not left meaningless or empty

## 推荐思维方式

不要只盯着图结构连没连上。
更要从 FastGPT 应用 UI 的角度思考：它到底能不能接住这个工作流期望的输入。
