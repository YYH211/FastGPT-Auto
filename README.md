# FastGPT Workflow Generator

Generate import-ready FastGPT workflow JSON from natural-language requirements or existing workflow drafts.

This repository is the public edition of the `fastgpt-workflow-generator` skill. It packages the skill spec, a curated template library, supporting references, and a local validator so others can reuse the workflow generation process instead of rebuilding FastGPT flows from scratch.

## What This Repo Is For

- Turn product or business requirements into FastGPT workflow JSON that is closer to import-ready.
- Reuse real templates first, then patch them with the minimum necessary changes.
- Validate workflow structure locally before importing into FastGPT.
- Provide a safer public starting point without embedded secrets, internal webhooks, or fixed business defaults.

## Who Should Use It

- Engineers building FastGPT applications or agents
- Workflow designers who need importable JSON instead of screenshots or vague node descriptions
- Teams maintaining reusable FastGPT templates
- Users who want to inspect, patch, validate, and version workflow JSON locally

## What Is Included

- `SKILL.md`: the core skill instructions and generation constraints
- `templates/`: public workflow template library
- `references/`: schema notes, import shapes, node catalog, patching guidance, and config mapping
- `scripts/validate_fastgpt_workflow.py`: local validator for workflow JSON
- `assets/`: minimal examples and wrapper examples

All relative paths are resolved from the skill root directory.

## How To Use

### Option 1: Use It As a Codex Skill

1. Put this repository in your local Codex skills directory.
2. Let Codex load [`SKILL.md`](./SKILL.md).
3. Ask for a FastGPT workflow to be created, modified, repaired, or validated.
4. Validate the generated JSON locally before importing it into FastGPT.

### Option 2: Use It As a Template and Validation Repo

1. Pick the closest template from `templates/`.
2. Patch the workflow for your own use case.
3. Run the validator on the result.
4. Import it into your FastGPT environment and fill in runtime-specific configuration.

## Quick Validation

Validate a generated workflow with stricter import-oriented checks:

```bash
python3 scripts/validate_fastgpt_workflow.py --strict-generated <workflow.json>
```

Validate a template file for base structure:

```bash
python3 scripts/validate_fastgpt_workflow.py templates/<template>.json
```

Validation behavior:

- Structural errors fail immediately
- `--strict-generated` applies tighter checks for generated import targets
- Compatibility or recommended-field issues are reported as warnings

## Template Library

The public templates are grouped into three categories. See [`templates/README.md`](./templates/README.md) for the current list.

- `core`: general-purpose templates that are suitable starting points
- `integration`: templates that depend on external APIs, third-party platforms, or extra variables
- `experimental`: templates mainly kept as structural references and not guaranteed to be plug-and-play

## Public Release Scope

This public edition keeps only the parts that are suitable for external reuse.

- Internal contract-approval workflows were removed from the public release.
- Plain-text secrets, webhooks, fixed instance URLs, and default business-specific configuration were cleaned out.
- Some integration templates are still included, but users must provide their own API endpoints, variables, credentials, and environment-specific settings.

## Requirements

- Python 3
- A FastGPT environment that can import workflow JSON
- Your own model configuration, credentials, and external service settings where required

## Known Limitations

- Model names in templates are examples only and may not exist in your deployment.
- Some templates retain FastGPT-specific field naming or cloud resource references for import compatibility.
- The validator uses a node whitelist based on the current reference set and may need updates when FastGPT adds new node types.

## Notes

- This is a community-maintained skill repository, not an official FastGPT repository.
- If no public template is a good match, the workflow should be rebuilt conservatively instead of pretending a template already exists.

## License

MIT
