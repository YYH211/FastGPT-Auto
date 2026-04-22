# 歧义检查清单

在生成 FastGPT 工作流之前，先使用这份清单检查需求是否仍有歧义。

目标是找出 **用户任务本身** 里还不清楚的地方，而不是纠结工作流实现细节。

## 高优先级歧义类型

### 1. 目标歧义

检查以下内容是否清楚：
- What exact problem is the workflow solving?
- What counts as a successful result?
- Is the workflow for generation, retrieval, extraction, routing, transformation, or automation?

如果不清楚，可追问：
- **这个工作流成功运行后，最理想的结果是什么？**
- **你希望它主要是回答、提取、分类、生成，还是调用外部能力去完成任务？**

### 2. 用户歧义

检查以下内容是否清楚：
- Who is the end user?
- Is this for internal staff, customers, operators, or an automated process?
- Does the user's role affect output style or permissions?

如果不清楚，可追问：
- **这个工作流是给谁用的？**
- **不同用户是否需要不同处理方式？**

### 3. 输入歧义

检查以下内容是否清楚：
- What does the user provide?
- Is the input a question, structured form, uploaded file, list of items, or API payload?
- Are there required fields?

如果不清楚，可追问：
- **用户触发时会输入什么，或者上传什么？**
- **哪些输入是必填的，哪些是可选的？**

### 4. 输出歧义

检查以下内容是否清楚：
- What should the workflow return?
- Is the output free text, JSON, summary, extraction result, classification label, or downstream action?
- Is there a strict format?

如果不清楚，可追问：
- **最后希望返回什么结果？**
- **结果有没有固定格式、字段或示例？**

### 5. 知识/数据源歧义

检查以下内容是否清楚：
- Does the workflow need knowledge base retrieval?
- Does it need live web/API data?
- What source is authoritative?

如果不清楚，可追问：
- **这个任务需要依赖知识库、联网数据，还是外部系统接口？**
- **如果有多个数据来源，哪个优先？**

### 6. 决策逻辑歧义

检查以下内容是否清楚：
- Does the workflow branch by condition, classification, or confidence?
- Are there multiple business cases?
- Are there fallback paths?

如果不清楚，可追问：
- **这个任务会不会因为不同情况走不同处理路径？**
- **有没有需要兜底或升级处理的情况？**

### 7. 规模/处理流程歧义

检查以下内容是否清楚：
- Is this single-turn, multi-turn, or batch processing?
- Does it process one item or many?
- Does it need loops or repeated handling?

如果不清楚，可追问：
- **一次只处理一条，还是会批量处理多条内容？**
- **有没有逐条处理、循环处理的需求？**

### 8. 约束歧义

检查以下内容是否清楚：
- 语言要求
- 合规要求
- 语气/风格约束
- 模型行为要求
- 哪些字段不能凭空补

如果不清楚，可追问：
- **输出时有没有必须遵守的规则、语气、语言或合规要求？**
- **哪些内容必须严格依据输入，不能补充猜测？**

## 提问策略

- 只问那些真正会阻塞生成的问题。
- 用业务/任务语言提问，不要用节点语言提问。
- 优先问 2 到 5 个简洁问题，不要一上来甩一整张问卷。
- 如果用户已经暗示了默认值，就直接采用，并记录到 assumptions。

## 可开始构建的判断标准

当下面这些条件都满足时，说明需求已经足够清晰，可以开始构建：
- 目标已清晰
- 输入已经足够清晰
- 输出已经足够清晰
- 所需外部依赖已经足够清晰
- 特殊业务规则已经足够清晰
- 已经可以在不猜业务意图的前提下选择内部工作流模式
