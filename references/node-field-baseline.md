# 节点字段基线

这份文件不再只讲“理论最小 schema”，而是基于当前 `templates/` 目录中的 **21 个真实 FastGPT 导出模板** 提炼“导入后更容易直接可用”的运行基线。

先把丑话说前头：
- **最小 schema** 只保证 JSON 长得像工作流。
- **最小可运行模板** 才更接近“导入后不炸”。
- 有些节点能抽出稳定通用模板。
- 有些节点本质上依赖具体工具或具体业务配置，不能硬抽成一个万能模板。

## 最小 schema 字段

已确认的最小字段：
- `nodeId`
- `name`
- `flowNodeType`
- `position`
- `inputs`
- `outputs`

## 导入即用的推荐基线字段

除非有充分理由不这样做，否则建议一并保留：
- `intro`
- `avatar`
- `version`（仅当真实样本普遍存在时）
- `showStatus`（仅当真实样本普遍存在时）
- `catchError`（仅当真实样本普遍存在时）

对于输入输出项，建议尽量保留这些兼容字段：
- `key`
- `valueType`
- `renderTypeList`
- `label`
- `required`
- `description`
- `toolDescription`
- `id` on outputs

## 稳定可抽的最小可运行模板

下面这些片段是“保守运行基线”，不是数学意义上的最小字段集。

### userGuide

21/21 模板覆盖，结构最稳定。

```json
{
  "nodeId": "userGuide",
  "name": "系统配置",
  "intro": "",
  "avatar": "core/workflow/template/systemConfig",
  "flowNodeType": "userGuide",
  "position": { "x": -600, "y": -250 },
  "version": "481",
  "inputs": [],
  "outputs": []
}
```

说明：
- 真实样本里大多数 `userGuide` 带很多应用级输入项，但也存在空 `inputs` 的可运行导出。
- 生成工作流时，应用级能力仍需同步到顶层 `chatConfig`，不要以为 `userGuide.inputs` 空着就万事大吉。

### workflowStart

21/21 模板覆盖。

```json
{
  "nodeId": "workflowStart",
  "name": "common:core.module.template.work_start",
  "intro": "",
  "avatar": "core/workflow/template/workflowStart",
  "flowNodeType": "workflowStart",
  "position": { "x": 450, "y": -350 },
  "version": "481",
  "inputs": [
    {
      "key": "userChatInput",
      "label": "workflow:user_question",
      "valueType": "string",
      "required": true,
      "renderTypeList": ["reference", "textarea"],
      "toolDescription": "用户问题"
    }
  ],
  "outputs": [
    {
      "id": "userChatInput",
      "key": "userChatInput",
      "type": "static",
      "valueType": "string",
      "label": "common:core.module.input.label.user question",
      "description": ""
    }
  ]
}
```

说明：
- `userFiles` 只在需要上传文件时补。
- `workflowStart` 输出 `userChatInput` 是很多聊天链路的锚点，别省。

### chatNode

18/21 模板覆盖，是最重要的运行节点之一。

```json
{
  "nodeId": "chatNode1",
  "name": "AI 对话",
  "intro": "AI 大模型对话",
  "avatar": "core/workflow/template/aiChat",
  "flowNodeType": "chatNode",
  "showStatus": true,
  "position": { "x": 1200, "y": -350 },
  "version": "4.9.7",
  "inputs": [
    {
      "key": "model",
      "renderTypeList": ["settingLLMModel", "reference"],
      "label": "common:core.module.input.label.aiModel",
      "valueType": "string",
      "value": "gpt-4.1-mini"
    },
    {
      "key": "temperature",
      "renderTypeList": ["hidden"],
      "label": "",
      "valueType": "number"
    },
    {
      "key": "maxToken",
      "renderTypeList": ["hidden"],
      "label": "",
      "valueType": "number"
    },
    {
      "key": "isResponseAnswerText",
      "renderTypeList": ["hidden"],
      "label": "",
      "value": true,
      "valueType": "boolean"
    },
    {
      "key": "aiChatQuoteRole",
      "renderTypeList": ["hidden"],
      "label": "",
      "valueType": "string",
      "value": "system"
    },
    {
      "key": "quoteTemplate",
      "renderTypeList": ["hidden"],
      "label": "",
      "valueType": "string"
    },
    {
      "key": "quotePrompt",
      "renderTypeList": ["hidden"],
      "label": "",
      "valueType": "string"
    },
    {
      "key": "aiChatVision",
      "renderTypeList": ["hidden"],
      "label": "",
      "valueType": "boolean",
      "value": true
    },
    {
      "key": "aiChatReasoning",
      "renderTypeList": ["hidden"],
      "label": "",
      "valueType": "boolean",
      "value": true
    },
    {
      "key": "aiChatTopP",
      "renderTypeList": ["hidden"],
      "label": "",
      "valueType": "number"
    },
    {
      "key": "aiChatStopSign",
      "renderTypeList": ["hidden"],
      "label": "",
      "valueType": "string"
    },
    {
      "key": "aiChatResponseFormat",
      "renderTypeList": ["hidden"],
      "label": "",
      "valueType": "string"
    },
    {
      "key": "aiChatJsonSchema",
      "renderTypeList": ["hidden"],
      "label": "",
      "valueType": "string"
    },
    {
      "key": "systemPrompt",
      "renderTypeList": ["textarea", "reference"],
      "valueType": "string",
      "label": "common:core.ai.Prompt",
      "value": ""
    },
    {
      "key": "history",
      "renderTypeList": ["numberInput", "reference"],
      "valueType": "chatHistory",
      "label": "common:core.module.input.label.chat history",
      "required": true,
      "min": 0,
      "max": 50,
      "value": 6
    },
    {
      "key": "quoteQA",
      "renderTypeList": ["settingDatasetQuotePrompt"],
      "label": "",
      "debugLabel": "知识库引用",
      "valueType": "datasetQuote"
    },
    {
      "key": "fileUrlList",
      "renderTypeList": ["reference", "input"],
      "label": "app:workflow.user_file_input",
      "valueType": "arrayString",
      "value": [["workflowStart", "userFiles"]]
    },
    {
      "key": "userChatInput",
      "renderTypeList": ["reference", "textarea"],
      "valueType": "string",
      "label": "workflow:user_question",
      "toolDescription": "用户问题",
      "required": true,
      "value": ["workflowStart", "userChatInput"]
    }
  ],
  "outputs": [
    {
      "id": "history",
      "key": "history",
      "required": true,
      "label": "common:core.module.output.label.New context",
      "valueType": "chatHistory",
      "type": "static"
    },
    {
      "id": "answerText",
      "key": "answerText",
      "required": true,
      "label": "common:core.module.output.label.Ai response content",
      "valueType": "string",
      "type": "static"
    },
    {
      "id": "reasoningText",
      "key": "reasoningText",
      "required": false,
      "label": "workflow:reasoning_content",
      "valueType": "string",
      "type": "static"
    },
    {
      "id": "system_error_text",
      "key": "system_error_text",
      "type": "error",
      "valueType": "string",
      "label": "workflow:error_text"
    }
  ],
  "catchError": false
}
```

强约束：
- 每个 `chatNode` 都必须显式包含 `userChatInput`。
- 默认最小可用接线是 `["workflowStart", "userChatInput"]`，但**不是唯一合法值**。
- 每个 `chatNode` 都必须显式包含 `history`。
- 默认最小可用值是 `6`，但**不是唯一合法值**。
- 真正的知识库引用输出 key 是 `quoteQA`，不是你瞎起的别名。

### answerNode

14/21 模板覆盖，结构非常简单。

```json
{
  "nodeId": "answerNode1",
  "name": "指定回复",
  "intro": "该模块可以直接回复一段指定的内容。常用于引导、提示。非字符串内容传入时，会转成字符串进行输出。",
  "avatar": "core/workflow/template/reply",
  "flowNodeType": "answerNode",
  "position": { "x": 1500, "y": -350 },
  "inputs": [
    {
      "key": "text",
      "renderTypeList": ["textarea", "reference"],
      "valueType": "any",
      "required": true,
      "label": "common:core.module.input.label.Response content",
      "value": ["chatNode1", "answerText"]
    }
  ],
  "outputs": []
}
```

### datasetSearchNode

3/21 模板覆盖，但字段高度稳定，足够作为真实基线。

```json
{
  "nodeId": "datasetSearchNode1",
  "name": "知识库搜索",
  "intro": "调用“语义检索”和“全文检索”能力，从“知识库”中查找可能与问题相关的参考内容",
  "avatar": "core/workflow/template/datasetSearch",
  "flowNodeType": "datasetSearchNode",
  "showStatus": true,
  "position": { "x": 900, "y": -500 },
  "version": "4.9.2",
  "inputs": [
    {
      "key": "datasets",
      "renderTypeList": ["selectDataset", "reference"],
      "label": "common:core.module.input.label.Select dataset",
      "value": [],
      "valueType": "selectDataset",
      "required": true
    },
    {
      "key": "similarity",
      "renderTypeList": ["selectDatasetParamsModal"],
      "label": "",
      "value": 0.4,
      "valueType": "number"
    },
    {
      "key": "limit",
      "renderTypeList": ["hidden"],
      "label": "",
      "value": 3000,
      "valueType": "number"
    },
    {
      "key": "searchMode",
      "renderTypeList": ["hidden"],
      "label": "",
      "valueType": "string",
      "value": "mixedRecall"
    },
    {
      "key": "embeddingWeight",
      "renderTypeList": ["hidden"],
      "label": "",
      "valueType": "number",
      "value": 0.25
    },
    {
      "key": "usingReRank",
      "renderTypeList": ["hidden"],
      "label": "",
      "valueType": "boolean",
      "value": false
    },
    {
      "key": "rerankModel",
      "renderTypeList": ["hidden"],
      "label": "",
      "valueType": "string",
      "value": "gpt-4.1-mini"
    },
    {
      "key": "rerankWeight",
      "renderTypeList": ["hidden"],
      "label": "",
      "valueType": "number",
      "value": 0.5
    },
    {
      "key": "datasetSearchUsingExtensionQuery",
      "renderTypeList": ["hidden"],
      "label": "",
      "valueType": "boolean",
      "value": false
    },
    {
      "key": "datasetSearchExtensionModel",
      "renderTypeList": ["hidden"],
      "label": "",
      "valueType": "string",
      "value": ""
    },
    {
      "key": "datasetSearchExtensionBg",
      "renderTypeList": ["hidden"],
      "label": "",
      "valueType": "string",
      "value": ""
    },
    {
      "key": "authTmbId",
      "renderTypeList": ["hidden"],
      "label": "",
      "valueType": "boolean",
      "value": false
    },
    {
      "key": "userChatInput",
      "renderTypeList": ["reference", "textarea"],
      "valueType": "string",
      "label": "workflow:user_question",
      "toolDescription": "需要检索的内容",
      "required": true,
      "value": ["workflowStart", "userChatInput"]
    },
    {
      "key": "collectionFilterMatch",
      "renderTypeList": ["textarea", "reference"],
      "label": "workflow:collection_metadata_filter",
      "valueType": "string"
    }
  ],
  "outputs": [
    {
      "id": "quoteQA",
      "key": "quoteQA",
      "label": "common:core.module.Dataset quote.label",
      "type": "static",
      "valueType": "datasetQuote"
    },
    {
      "id": "system_error_text",
      "key": "system_error_text",
      "type": "error",
      "valueType": "string",
      "label": "workflow:error_text"
    }
  ],
  "catchError": false
}
```

强约束：
- `quoteQA` 才是当前真实样本里的正确输出 key。
- `datasets` 可以先留空数组作为占位，但如果目标是“导出即用”，最终必须绑定真实知识库。

### readFiles

6/21 模板覆盖，结构稳定。

```json
{
  "nodeId": "readFiles1",
  "name": "文档解析",
  "intro": "解析本轮对话上传的文档，并返回对应文档内容",
  "avatar": "core/workflow/template/readFiles",
  "flowNodeType": "readFiles",
  "showStatus": true,
  "position": { "x": 900, "y": -650 },
  "version": "4.9.2",
  "inputs": [
    {
      "key": "fileUrlList",
      "renderTypeList": ["reference"],
      "valueType": "arrayString",
      "label": "app:workflow.file_url",
      "required": true,
      "value": [["workflowStart", "userFiles"]]
    }
  ],
  "outputs": [
    {
      "id": "system_text",
      "key": "system_text",
      "label": "app:workflow.read_files_result",
      "valueType": "string",
      "type": "static"
    },
    {
      "id": "system_rawResponse",
      "key": "system_rawResponse",
      "label": "workflow:raw_response",
      "valueType": "arrayObject",
      "type": "static"
    },
    {
      "id": "system_error_text",
      "key": "system_error_text",
      "type": "error",
      "valueType": "string",
      "label": "workflow:error_text"
    }
  ]
}
```

### ifElseNode

12/21 模板覆盖。

```json
{
  "nodeId": "ifElse1",
  "name": "判断器",
  "intro": "根据一定的条件，执行不同的分支。",
  "avatar": "core/workflow/template/ifelse",
  "flowNodeType": "ifElseNode",
  "showStatus": true,
  "position": { "x": 900, "y": -350 },
  "inputs": [
    {
      "key": "ifElseList",
      "renderTypeList": ["hidden"],
      "valueType": "any",
      "label": "",
      "value": [
        {
          "condition": "AND",
          "list": [
            {
              "variable": ["VARIABLE_NODE_ID", "someVariable"],
              "condition": "isEmpty",
              "valueType": "input"
            }
          ]
        }
      ]
    }
  ],
  "outputs": [
    {
      "id": "ifElseResult",
      "key": "ifElseResult",
      "label": "workflow:judgment_result",
      "valueType": "string",
      "type": "static"
    }
  ]
}
```

### code

14/21 模板覆盖。这个节点能通用，但**输入参数和输出参数是动态的**。

```json
{
  "nodeId": "code1",
  "name": "代码执行",
  "intro": "执行一段简单的脚本代码，通常用于进行复杂的数据处理。",
  "avatar": "core/workflow/template/codeRun",
  "flowNodeType": "code",
  "showStatus": true,
  "position": { "x": 900, "y": -350 },
  "inputs": [
    {
      "key": "system_addInputParam",
      "renderTypeList": ["addInputParam"],
      "valueType": "dynamic",
      "label": "",
      "required": false
    },
    {
      "key": "codeType",
      "renderTypeList": ["hidden"],
      "label": "",
      "valueType": "string",
      "value": "js"
    },
    {
      "key": "code",
      "renderTypeList": ["custom"],
      "label": "",
      "valueType": "string",
      "value": "function main(){ return { result: '' }; }"
    }
  ],
  "outputs": [
    {
      "id": "system_rawResponse",
      "key": "system_rawResponse",
      "label": "workflow:full_response_data",
      "valueType": "object",
      "type": "static"
    },
    {
      "id": "error",
      "key": "error",
      "label": "workflow:error_text",
      "valueType": "string",
      "type": "error"
    },
    {
      "id": "system_addOutputParam",
      "key": "system_addOutputParam",
      "type": "dynamic",
      "valueType": "dynamic",
      "label": ""
    }
  ],
  "catchError": false
}
```

说明：
- 真实样本里几乎所有业务输入，比如 `data1`、`input`、`url`，都是在这个基线之上动态追加的。
- 真正要输出什么字段，取决于 `code` 里的 `return` 对象。

### httpRequest468

8/21 模板覆盖。这个节点之前最容易瞎猜字段，现在已经有稳定基线。

```json
{
  "nodeId": "httpRequest1",
  "name": "HTTP 请求",
  "intro": "可以发出一个 HTTP 请求，实现更为复杂的操作（联网搜索、数据库查询等）",
  "avatar": "core/workflow/template/httpRequest",
  "flowNodeType": "httpRequest468",
  "showStatus": true,
  "position": { "x": 900, "y": -350 },
  "inputs": [
    {
      "key": "system_addInputParam",
      "renderTypeList": ["addInputParam"],
      "valueType": "dynamic",
      "label": "",
      "required": false
    },
    {
      "key": "system_httpMethod",
      "renderTypeList": ["custom"],
      "valueType": "string",
      "label": "",
      "value": "GET",
      "required": true
    },
    {
      "key": "system_httpTimeout",
      "renderTypeList": ["custom"],
      "valueType": "number",
      "label": "",
      "value": 30,
      "min": 5,
      "max": 600,
      "required": true
    },
    {
      "key": "system_httpReqUrl",
      "renderTypeList": ["hidden"],
      "valueType": "string",
      "label": "",
      "value": ""
    },
    {
      "key": "system_header_secret",
      "renderTypeList": ["hidden"],
      "valueType": "object",
      "label": ""
    },
    {
      "key": "system_httpHeader",
      "renderTypeList": ["custom"],
      "valueType": "any",
      "value": [],
      "label": ""
    },
    {
      "key": "system_httpParams",
      "renderTypeList": ["hidden"],
      "valueType": "any",
      "value": [],
      "label": ""
    },
    {
      "key": "system_httpJsonBody",
      "renderTypeList": ["hidden"],
      "valueType": "any",
      "value": "",
      "label": ""
    },
    {
      "key": "system_httpFormBody",
      "renderTypeList": ["hidden"],
      "valueType": "any",
      "value": [],
      "label": ""
    },
    {
      "key": "system_httpContentType",
      "renderTypeList": ["hidden"],
      "valueType": "string",
      "value": "json",
      "label": ""
    }
  ],
  "outputs": [
    {
      "id": "httpRawResponse",
      "key": "httpRawResponse",
      "required": true,
      "label": "workflow:raw_response",
      "valueType": "any",
      "type": "static"
    },
    {
      "id": "error",
      "key": "error",
      "label": "workflow:error_text",
      "valueType": "string",
      "type": "error"
    },
    {
      "id": "system_addOutputParam",
      "key": "system_addOutputParam",
      "type": "dynamic",
      "valueType": "dynamic",
      "label": "输出字段提取"
    }
  ],
  "catchError": false
}
```

说明：
- 业务输出字段如 `msg`、`code`、`tenant_access_token` 都是在 `system_addOutputParam` 基线之上动态追加的。
- 这玩意儿别再手搓半截了，少一个系统字段就可能前端读取 `includes` 直接炸。

### formInput

4/21 模板覆盖。

```json
{
  "nodeId": "formInput1",
  "name": "表单输入",
  "intro": "该模块可以配置多种输入，引导用户输入特定内容。",
  "avatar": "core/workflow/template/formInput",
  "flowNodeType": "formInput",
  "position": { "x": 900, "y": -350 },
  "inputs": [
    {
      "key": "description",
      "renderTypeList": ["textarea"],
      "valueType": "string",
      "label": "app:workflow.select_description",
      "value": ""
    },
    {
      "key": "userInputForms",
      "renderTypeList": ["custom"],
      "valueType": "any",
      "label": "",
      "value": []
    }
  ],
  "outputs": [
    {
      "id": "formInputResult",
      "key": "formInputResult",
      "required": true,
      "label": "workflow:form_input_result",
      "valueType": "object",
      "type": "static"
    }
  ]
}
```

说明：
- 真实样本里通常还会为每个表单字段追加一个同名 output。
- 如果目标是“导出即用”，建议同步生成这些字段级 outputs。

### userSelect

4/21 模板覆盖。

```json
{
  "nodeId": "userSelect1",
  "name": "用户选择",
  "intro": "该模块可配置多个选项，以供对话时选择。不同选项可导向不同工作流支线",
  "avatar": "core/workflow/template/userSelect",
  "flowNodeType": "userSelect",
  "position": { "x": 900, "y": -350 },
  "inputs": [
    {
      "key": "description",
      "renderTypeList": ["textarea"],
      "valueType": "string",
      "label": "app:workflow.select_description",
      "value": ""
    },
    {
      "key": "userSelectOptions",
      "renderTypeList": ["custom"],
      "valueType": "any",
      "label": "",
      "value": [
        { "value": "选项1", "key": "option1" },
        { "value": "选项2", "key": "option2" }
      ]
    }
  ],
  "outputs": [
    {
      "id": "selectResult",
      "key": "selectResult",
      "required": true,
      "label": "app:workflow.select_result",
      "valueType": "string",
      "type": "static"
    }
  ]
}
```

### classifyQuestion

3/21 模板覆盖，样本虽少但字段统一。

```json
{
  "nodeId": "classify1",
  "name": "问题分类",
  "intro": "根据用户的历史记录和当前问题判断该次提问的类型。",
  "avatar": "core/workflow/template/questionClassify",
  "flowNodeType": "classifyQuestion",
  "showStatus": true,
  "position": { "x": 900, "y": -350 },
  "version": "4.9.2",
  "inputs": [
    {
      "key": "model",
      "renderTypeList": ["selectLLMModel", "reference"],
      "label": "common:core.module.input.label.aiModel",
      "required": true,
      "valueType": "string",
      "llmModelType": "classify",
      "value": "gpt-4.1"
    },
    {
      "key": "systemPrompt",
      "renderTypeList": ["textarea", "reference"],
      "valueType": "string",
      "label": "common:core.module.input.label.Background",
      "value": ""
    },
    {
      "key": "history",
      "renderTypeList": ["numberInput", "reference"],
      "valueType": "chatHistory",
      "label": "common:core.module.input.label.chat history",
      "required": true,
      "min": 0,
      "max": 50,
      "value": 6
    },
    {
      "key": "userChatInput",
      "renderTypeList": ["reference", "textarea"],
      "valueType": "string",
      "label": "workflow:user_question",
      "required": true,
      "value": ["workflowStart", "userChatInput"]
    },
    {
      "key": "agents",
      "renderTypeList": ["custom"],
      "valueType": "any",
      "label": "",
      "value": [
        { "value": "分类1", "key": "type1" },
        { "value": "分类2", "key": "type2" }
      ]
    }
  ],
  "outputs": [
    {
      "id": "cqResult",
      "key": "cqResult",
      "required": true,
      "label": "workflow:classification_result",
      "valueType": "string",
      "type": "static"
    }
  ]
}
```

### variableUpdate

8/21 模板覆盖。

```json
{
  "nodeId": "variableUpdate1",
  "name": "变量更新",
  "intro": "可以更新指定节点的输出值或更新全局变量",
  "avatar": "core/workflow/template/variableUpdate",
  "flowNodeType": "variableUpdate",
  "showStatus": false,
  "position": { "x": 900, "y": -350 },
  "inputs": [
    {
      "key": "updateList",
      "valueType": "any",
      "label": "",
      "renderTypeList": ["hidden"],
      "value": [
        {
          "variable": ["VARIABLE_NODE_ID", "someVariable"],
          "value": ["", ""],
          "valueType": "string",
          "renderType": "input"
        }
      ]
    }
  ],
  "outputs": []
}
```

### textEditor

5/21 模板覆盖。

```json
{
  "nodeId": "textEditor1",
  "name": "文本拼接",
  "intro": "可对固定或传入的文本进行加工后输出，非字符串类型数据最终会转成字符串类型。",
  "avatar": "core/workflow/template/textConcat",
  "flowNodeType": "textEditor",
  "position": { "x": 900, "y": -350 },
  "inputs": [
    {
      "key": "system_textareaInput",
      "renderTypeList": ["textarea"],
      "valueType": "string",
      "required": true,
      "label": "workflow:concatenation_text",
      "value": "{{$chatNode1.answerText$}}"
    }
  ],
  "outputs": [
    {
      "id": "system_text",
      "key": "system_text",
      "label": "workflow:concatenation_result",
      "type": "static",
      "valueType": "string"
    }
  ]
}
```

### loop / loopStart / loopEnd

8/21 模板覆盖。这个家族字段稳定，但**必须成套出现**。

`loop`

```json
{
  "nodeId": "loop1",
  "name": "循环",
  "intro": "输入一个数组，遍历数组并将每一个数组元素作为输入元素，执行工作流。",
  "avatar": "core/workflow/template/loop",
  "flowNodeType": "loop",
  "showStatus": true,
  "position": { "x": 900, "y": -350 },
  "inputs": [
    {
      "key": "loopInputArray",
      "renderTypeList": ["reference"],
      "valueType": "arrayObject",
      "required": true,
      "label": "workflow:loop_input_array",
      "value": [["someNode", "arrayField"]]
    },
    {
      "key": "childrenNodeIdList",
      "renderTypeList": ["hidden"],
      "valueType": "arrayString",
      "label": "",
      "value": ["loopStart1", "loopEnd1"]
    },
    {
      "key": "nodeWidth",
      "renderTypeList": ["hidden"],
      "valueType": "number",
      "label": "",
      "value": 1200
    },
    {
      "key": "nodeHeight",
      "renderTypeList": ["hidden"],
      "valueType": "number",
      "label": "",
      "value": 800
    },
    {
      "key": "loopNodeInputHeight",
      "renderTypeList": ["hidden"],
      "valueType": "number",
      "label": "",
      "value": 83
    }
  ],
  "outputs": [
    {
      "id": "loopArray",
      "key": "loopArray",
      "label": "workflow:loop_result",
      "type": "static",
      "valueType": "arrayObject"
    }
  ]
}
```

`loopStart`

```json
{
  "nodeId": "loopStart1",
  "parentNodeId": "loop1",
  "name": "开始",
  "avatar": "core/workflow/template/loopStart",
  "flowNodeType": "loopStart",
  "showStatus": false,
  "position": { "x": 1200, "y": -300 },
  "inputs": [
    {
      "key": "loopStartInput",
      "renderTypeList": ["hidden"],
      "valueType": "any",
      "label": "",
      "required": true,
      "value": ""
    },
    {
      "key": "loopStartIndex",
      "renderTypeList": ["hidden"],
      "valueType": "number",
      "label": "workflow:Array_element_index"
    }
  ],
  "outputs": [
    {
      "id": "loopStartIndex",
      "key": "loopStartIndex",
      "label": "workflow:Array_element_index",
      "type": "static",
      "valueType": "number"
    },
    {
      "id": "loopStartInput",
      "key": "loopStartInput",
      "label": "数组元素",
      "type": "static",
      "valueType": "object"
    }
  ]
}
```

`loopEnd`

```json
{
  "nodeId": "loopEnd1",
  "parentNodeId": "loop1",
  "name": "结束",
  "avatar": "core/workflow/template/loopEnd",
  "flowNodeType": "loopEnd",
  "showStatus": false,
  "position": { "x": 1800, "y": -300 },
  "inputs": [
    {
      "key": "loopEndInput",
      "renderTypeList": ["reference"],
      "valueType": "any",
      "label": "",
      "required": true,
      "value": ["loopStart1", "loopStartInput"]
    }
  ],
  "outputs": []
}
```

## 必须按实例分型的节点

这些节点不能抽成一个“所有场景都适用”的输入模板，只能抽“外壳 + 具体工具配置”。

### tool

当前样本里至少有 4 种形态：
- `systemTool-getTime`：无输入，输出 `time`
- `systemTool-markdownTransform`：输入 `markdown`、`format`、`filename`
- `systemTool-databaseConnection` / `systemTool-dbops/mysql`：输入 `system_input_config`、`sql`
- 自定义插件工具：输入 `toolData` + 业务参数，且不一定有 `toolConfig.systemTool`

最小稳定外壳：

```json
{
  "nodeId": "tool1",
  "name": "获取当前时间",
  "intro": "获取当前时间",
  "avatar": "tool-icon",
  "flowNodeType": "tool",
  "showStatus": true,
  "position": { "x": 900, "y": -350 },
  "version": "",
  "inputs": [],
  "outputs": [
    {
      "id": "system_error_text",
      "key": "system_error_text",
      "type": "error",
      "valueType": "string",
      "label": "错误信息"
    }
  ],
  "pluginId": "systemTool-getTime",
  "toolConfig": {
    "systemTool": {
      "toolId": "systemTool-getTime"
    }
  },
  "catchError": false
}
```

规则：
- `pluginId` 必填。
- 如果是系统工具，优先保留 `toolConfig.systemTool.toolId`。
- 业务输入输出要跟具体工具样本走，别想当然复用别的工具字段。

### pluginModule

当前样本里至少有 3 种形态：
- `community-fetchUrl`：输入 `url` 或 `system_forbid_stream + url`
- `community-delay`：输入 `ms`
- 自定义插件模块：输入输出完全按插件自己的 schema

最小稳定外壳：

```json
{
  "nodeId": "pluginModule1",
  "name": "流程等待",
  "intro": "让工作流等待指定时间后运行",
  "avatar": "core/workflow/template/sleep",
  "flowNodeType": "pluginModule",
  "showStatus": true,
  "position": { "x": 900, "y": -350 },
  "version": "",
  "inputs": [
    {
      "key": "ms",
      "label": "延迟时长(毫秒)",
      "defaultValue": 1000,
      "renderTypeList": ["numberInput", "reference"],
      "valueType": "number",
      "value": 1000
    }
  ],
  "outputs": [
    {
      "id": "system_error_text",
      "key": "system_error_text",
      "type": "error",
      "valueType": "string",
      "label": "workflow:error_text"
    }
  ],
  "pluginId": "community-delay",
  "toolConfig": {
    "systemTool": {
      "toolId": "systemTool-delay"
    }
  },
  "catchError": false
}
```

规则：
- `pluginId` 必填。
- 如果样本里存在 `toolConfig.systemTool`，尽量保留。
- 输入输出必须跟具体插件实例对齐，不要跨插件复用字段。

## 仍缺真实样本的节点

当前 `templates/` 目录里还没覆盖到这些节点，暂时别把它们当“可稳定直生”的类型：
- `datasetConcatNode`
- `contentExtract`
- `cfr`
- `tools`
- `toolParams`
- `stopTool`
- `customFeedback`
- `app`
- `toolSet`

## 实际规则

当你生成的是“准备导入”的工作流时，应优先采用这里的 **真实样本运行基线**，而不是只满足理论最小值。

不过，除非用户明确要求 wrapper，顶层 JSON 默认仍应保持 bare workflow object。

## 校验规则

校验器应当：
- accept the minimum schema
- accept real exported templates even when they do not use this document's recommended defaults
- warn when compatibility-oriented fields are missing
- treat bare workflow as the default target shape
- optionally support a stricter wrapper mode only when explicitly requested
