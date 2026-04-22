# FastGPT 导入形态

这个项目应把 **裸工作流对象** 作为主要生成目标。

## 主要形态：裸工作流对象

```json
{
  "nodes": [],
  "edges": [],
  "chatConfig": {}
}
```

根据参考 skill 中的 `json_structure_spec.md`，这是标准的工作流 JSON 结构。

## 可选形态：包装后的模板对象

某些导入路径下可能会使用包装后的模板对象，但除非用户明确要求 template-wrapper 包装，否则它**不应**成为默认生成目标。

```json
{
  "id": "template-id",
  "name": "Template Name",
  "type": "workflow",
  "workflow": {
    "nodes": [],
    "edges": [],
    "chatConfig": {}
  }
}
```

## 实际生成规则

默认生成 **bare workflow JSON**。

只有当用户明确要求以下形式时，才生成 wrapper：
- template package
- wrapped import object
- template market style object

## 校验策略

始终优先校验 bare workflow 形态。
如果是有意生成 wrapper，也要继续校验其中嵌套的 workflow 对象。
