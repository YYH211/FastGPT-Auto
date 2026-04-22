# 需求采集模板

在生成 FastGPT 工作流之前，先用这份文件采集最基本、最真实的需求。

目标是澄清 **任务本身**，而不是让用户替你设计工作流实现。

## 第一轮问题集

只问当前缺失的信息。

1. **这个工作流要帮谁解决什么问题？**
   - one-sentence goal and target user
2. **用户会怎样发起这个任务？**
   - chat input / form input / uploaded files / scheduled trigger / tool call
3. **用户会提供哪些信息或材料？**
   - text, files, form fields, options
4. **你希望最后产出什么结果？**
   - answer text, structured JSON, extracted fields, generated content, routing result
5. **过程中需要查知识库、联网查数据，还是调用外部系统吗？**
   - yes/no; if yes, what business purpose
6. **这个任务有没有分情况处理的逻辑？**
   - yes/no; if yes, what kinds of cases
7. **这个任务是不是要批量处理、循环处理，或者逐个处理多条内容？**
   - yes/no
8. **是否需要读取用户上传的文件或附件？**
   - yes/no
9. **输出有没有固定格式或必须遵守的规则？**
   - prompt 规则、JSON schema、语言、格式、合规要求
10. **有没有什么你没说但我不能默认替你决定的地方？**
   - 把隐藏歧义一起挖出来

## 需求工件结构

澄清完成后，汇总成下面这种结构：

```json
{
  "name": "",
  "goal": "",
  "interactionMode": "chat|form|file|tool|scheduled",
  "userInputs": [],
  "finalOutputs": [],
  "knowledgeBase": {
    "enabled": false,
    "purpose": ""
  },
  "httpRequests": {
    "enabled": false,
    "purpose": ""
  },
  "branching": false,
  "looping": false,
  "fileRead": false,
  "toolUsage": false,
  "constraints": [],
  "assumptions": []
}
```

## 内部映射提示

这些提示只用于需求明确后的内部工作流构建。除非用户明确要求，否则不要把这套映射逻辑直接甩给用户。

- plain Q&A assistant → `workflowStart` + `chatNode` + `answerNode`
- RAG assistant → add `datasetSearchNode` before `chatNode`
- file summarizer/extractor → add `readFiles`
- external-data workflow → add `httpRequest468`
- branch by category/intent → add `classifyQuestion` or `ifElseNode`
- iterative processing → add `loop`, `loopStart`, `loopEnd`
- collect structured user fields before processing → add `formInput` or `userSelect`

## 停止条件

在这些点没有明确之前，不要生成最终 JSON：
- what the user inputs
- what the workflow outputs
- what the business task actually is
- what the main processing path should accomplish
- which special capabilities are actually required
