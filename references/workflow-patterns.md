# 任务到工作流模式的映射

在需求明确之后再使用这份文件。

用户应该描述任务本身，然后在内部把它映射到最小、最合适的 FastGPT 工作流模式。

## 模式 1：普通对话助手

适用场景：
- user asks questions
- workflow should answer directly
- no retrieval or external data required

典型结构：
- `userGuide`
- `workflowStart`
- `chatNode`
- `answerNode`

## 模式 2：RAG / 知识库助手

适用场景：
- the answer must rely on internal knowledge
- retrieval should happen before generation
- answer should cite or condition on retrieved context

典型结构：
- `userGuide`
- `workflowStart`
- `datasetSearchNode`
- `chatNode`
- `answerNode`

## 模式 3：文件读取 / 总结 / 提取

适用场景：
- user uploads files
- workflow must read attachments before responding
- output is summary, extraction, translation, or structured result

典型结构：
- `userGuide`
- `workflowStart`
- `readFiles`
- `chatNode` or `contentExtract`
- `answerNode`

## 模式 4：外部 API / 数据助手

适用场景：
- workflow needs real-time external data
- output depends on HTTP/API response

典型结构：
- `userGuide`
- `workflowStart`
- `httpRequest468`
- optional `textEditor` or `chatNode`
- `answerNode`

## 模式 5：分类 / 路由工作流

适用场景：
- task outcome depends on category or condition
- different cases need different prompts or paths

典型结构：
- `userGuide`
- `workflowStart`
- `classifyQuestion` or `ifElseNode`
- branch-specific node chains
- `answerNode`

## 模式 6：批量 / 迭代处理器

适用场景：
- many items must be handled one by one
- repeated logic applies to each item

典型结构：
- `userGuide`
- `workflowStart`
- `loop`
- `loopStart`
- processing nodes
- `loopEnd`
- `answerNode`

## 模式 7：表单驱动的结构化工作流

适用场景：
- the task depends on collecting fixed structured fields
- free-form chat is not enough

典型结构：
- `userGuide`
- `workflowStart`
- `formInput` or `userSelect`
- processing node(s)
- `answerNode`

## 模式 8：工具编排型助手

适用场景：
- task requires calling tools/apps/plugins
- the core value is orchestration rather than a single model answer

典型结构：
- `userGuide`
- `workflowStart`
- `tools` / `toolParams` / `tool` / `toolSet` / `app`
- optional `chatNode`
- `answerNode`

## 模式组合规则

- 优先选择一个主模式；只有业务任务真的需要时，才组合多个模式。
- 常见组合：
  - RAG + classification
  - file reading + extraction
  - API + chat synthesis
  - form input + external API
- 简单任务不要过度组合。

## 选择启发式

选择能满足以下条件的最小模式：
- the user input type
- the required data dependencies
- the output type
- any conditional or batch behavior

如果两个模式都能满足需求，优先选更简单的那个，除非用户明确需要更复杂的行为。
