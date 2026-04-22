# FastGPT 工作流生成器

这个目录就是 `fastgpt-workflow-generator` 的正式 skill 目录。

## 包含内容

- `SKILL.md`：主 skill 说明
- `references/`：schema、node、导入形态、规划方式、工具目录等参考资料
- `scripts/validate_fastgpt_workflow.py`：本地工作流 JSON 校验脚本
- `assets/`：内置示例工作流 JSON
- `templates/`：内置真实模板 JSON，用作 patch 基底

## 目录约定

- `references/`、`scripts/`、`assets/`、`templates/` 都视为当前 skill 的组成部分。
- 默认按当前 skill 根目录解析相对路径。
- 不要依赖无关的外部绝对路径。

## 校验方式

在 skill 根目录下，校验新生成的工作流时执行：

```bash
python3 scripts/validate_fastgpt_workflow.py --strict-generated <workflow.json>
```

如果只是想检查内置的 FastGPT 导出模板是否大体可用，而不强制套用“生成结果专用默认值”，执行：

```bash
python3 scripts/validate_fastgpt_workflow.py templates/<template>.json
```

## 校验策略

- 始终报错：会影响 JSON 解析、导入结构识别、节点定义、边连接目标、或引用源节点存在性的结构问题。
- `--strict-generated` 报错：会影响“新生成工作流导入后直接可用”的约束，这部分必须保持严格。
- 仅警告：最小默认值建议、兼容性提示，以及一些在真实 FastGPT 导出模板中可能合法、但当前校验器无法完全归一化的写法。

## 模板说明

- 这个 skill 设计上优先使用 `templates/` 中的真实模板。
- 选择模板时应检查整个 `templates/` 目录，而不只是最早那 4 个示例。
- 如果当前副本里缺少某些预期模板文件，skill 应明确说明，并保守回退，而不是假装模板存在。
- `assets/` 中的内容只是示例，不能替代真实模板库。
