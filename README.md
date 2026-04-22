# FastGPT Workflow Generator

`fastgpt-workflow-generator` 是一个面向 FastGPT 的 workflow JSON 生成 skill。
它把自然语言需求或已有 workflow 草稿，约束性地落成可导入 FastGPT 的工作流 JSON。

## Public Release Scope

这个公开版仓库只保留适合对外复用的模板、参考资料和校验脚本。

- 已移除明显偏内部业务流程的合同审批模板。
- 已清理明文密钥、Webhook、固定实例地址和默认业务配置。
- 仍保留部分集成类模板，但这类模板需要用户自行补充 API 地址、变量和鉴权信息。

## Repository Layout

- `SKILL.md`: skill 主说明与生成约束
- `references/`: schema、节点目录、导入结构、patch 策略、system config 映射等资料
- `scripts/validate_fastgpt_workflow.py`: 本地 workflow JSON 校验器
- `assets/`: 最小示例和 wrapper 示例
- `templates/`: 对外公开模板库

所有相对路径默认相对当前 skill 根目录解析。

## Requirements

- Python 3
- 可导入 FastGPT workflow JSON 的运行环境
- 用户自行提供可用模型、API 凭证和外部服务配置

## Validation

在 skill 根目录下校验新生成的 workflow：

```bash
python3 scripts/validate_fastgpt_workflow.py --strict-generated <workflow.json>
```

检查模板文件是否满足基础结构：

```bash
python3 scripts/validate_fastgpt_workflow.py templates/<template>.json
```

校验策略：

- 结构错误：直接报错
- `--strict-generated` 约束：面向“生成结果可直接导入”的更严格检查
- 兼容性或推荐项：警告

## Template Categories

公开版模板分为三类，详见 `templates/README.md`：

- `core`: 通用场景，可作为优先基底
- `integration`: 依赖外部 API、变量或第三方平台配置
- `experimental`: 更偏参考或环境相关，不保证开箱即用

## Known Limitations

- 模板中的模型名仅为示例，不保证在所有部署环境可直接使用。
- 部分模板保留了 FastGPT 云端资源地址或平台字段命名，用于兼容导入结构，不代表这些域名是唯一依赖。
- 校验器内置了一个基于当前资料整理的节点白名单，若 FastGPT 后续新增节点类型，可能需要同步更新。

## Notes

- 这是一个社区整理的 skill 仓库，不是 FastGPT 官方仓库。
- 如果当前公开模板库缺少你需要的场景，skill 应保守回退，而不是假设模板存在。
