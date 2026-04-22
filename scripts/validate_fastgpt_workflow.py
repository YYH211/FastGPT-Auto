#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

SUPPORTED_NODE_TYPES = {
    "workflowStart", "userGuide", "chatNode", "answerNode",
    "datasetSearchNode", "datasetConcatNode", "httpRequest468",
    "code", "ifElseNode", "loop", "loopStart", "loopEnd",
    "readFiles", "userSelect", "formInput", "variableUpdate",
    "textEditor", "agent", "contentExtract", "classifyQuestion",
    "pluginInput", "pluginOutput", "lafModule", "stopTool",
    "globalVariable", "comment", "cfr", "tools", "toolParams",
    "tool", "toolSet", "app", "customFeedback"
}

PREFERRED_NODE_FIELDS = {"intro", "avatar", "version"}
REF_RE = re.compile(r"\{\{\$(?P<node>[A-Za-z0-9_\-]+)\.(?P<key>[A-Za-z0-9_\-]+)\$\}\}")
WRONG_REF_RE = re.compile(r"(?<!\{)\{\$(?P<node>[A-Za-z0-9_\-]+)\.(?P<key>[A-Za-z0-9_\-]+)\$\}(?!\})")


def error(errors, msg):
    errors.append(msg)


def warn(warnings, msg):
    warnings.append(msg)


def report(strict, errors, warnings, msg):
    if strict:
        error(errors, msg)
    else:
        warn(warnings, msg)


def collect_output_keys(node):
    outputs = node.get("outputs", [])
    keys = set()
    for item in outputs:
        if isinstance(item, dict) and isinstance(item.get("key"), str):
            keys.add(item["key"])
    return keys


def detect_shape(data, errors):
    if not isinstance(data, dict):
        error(errors, "top level must be an object")
        return "invalid", None

    if isinstance(data.get("nodes"), list) and isinstance(data.get("edges"), list):
        return "bare-workflow", data

    workflow = data.get("workflow")
    if isinstance(workflow, dict):
        return "template-wrapper", workflow

    error(errors, "unrecognized shape: expected bare workflow or template wrapper")
    return "invalid", None


def validate_template_wrapper(data, warnings, errors):
    for field in ["id", "name", "type", "workflow"]:
        if field not in data:
            error(errors, f"template wrapper missing top-level field '{field}'")


def validate_reference(value, node_outputs, errors, warnings, context, strict):
    if isinstance(value, list):
        is_ref = len(value) == 2 and all(isinstance(x, str) for x in value)
        if not is_ref:
            return
        node_id, key = value
        if node_id == "VARIABLE_NODE_ID":
            return
        if node_id not in node_outputs:
            error(errors, f"{context}: reference source node '{node_id}' not found")
            return
        if key not in node_outputs[node_id]:
            report(strict, errors, warnings, f"{context}: reference key '{key}' not found on node '{node_id}'")
    elif isinstance(value, str):
        wrong = list(WRONG_REF_RE.finditer(value))
        if wrong:
            error(errors, f"{context}: incorrect string reference format; use {{{{$nodeId.key$}}}} not {{$nodeId.key$}}")
        for match in REF_RE.finditer(value):
            node_id = match.group("node")
            key = match.group("key")
            if node_id not in node_outputs and node_id != "VARIABLE_NODE_ID":
                error(errors, f"{context}: template reference source node '{node_id}' not found")
            elif node_id in node_outputs and key not in node_outputs[node_id]:
                report(strict, errors, warnings, f"{context}: template reference key '{key}' not found on node '{node_id}'")


def validate_system_input_config(inp, errors, warnings, context, strict):
    input_list = inp.get("inputList")
    value_obj = inp.get("value", None)

    if not isinstance(input_list, list):
        report(strict, errors, warnings, f"{context}: 'system_input_config.inputList' should be an array")
        input_list = []

    invalid_value_keys = []
    required_keys = []
    key_to_type = {}

    for item in input_list:
        if not isinstance(item, dict):
            continue
        key = item.get("key")
        if isinstance(key, str) and key:
            key_to_type[key] = item.get("inputType")
            if item.get("required") is True:
                required_keys.append(key)
        if "value" in item:
            invalid_value_keys.append(key if isinstance(key, str) and key else "<unknown>")

    if invalid_value_keys:
        error(
            errors,
            f"{context}: do not put field-level 'value' inside system_input_config.inputList ({', '.join(invalid_value_keys)}); put runtime config in system_input_config.value object",
        )

    if value_obj is not None and not isinstance(value_obj, dict):
        error(errors, f"{context}: system_input_config.value must be an object when provided")
        return

    if isinstance(value_obj, dict):
        missing_required = [k for k in required_keys if k not in value_obj]
        if missing_required:
            report(
                strict,
                errors,
                warnings,
                f"{context}: system_input_config.value is missing required keys: {', '.join(missing_required)}",
            )

        for key, expected_type in key_to_type.items():
            if key not in value_obj:
                continue
            v = value_obj[key]
            if expected_type == "numberInput" and not isinstance(v, (int, float)):
                report(
                    strict,
                    errors,
                    warnings,
                    f"{context}: system_input_config.value['{key}'] should be numeric for inputType 'numberInput'",
                )


def validate_workflow_core(workflow, warnings, errors, strict):
    nodes = workflow.get("nodes")
    edges = workflow.get("edges")
    chat_config = workflow.get("chatConfig")

    if not isinstance(nodes, list):
        error(errors, "'nodes' must be an array")
        nodes = []
    if not isinstance(edges, list):
        error(errors, "'edges' must be an array")
        edges = []
    if not isinstance(chat_config, dict):
        error(errors, "'chatConfig' must be an object")
        chat_config = {}

    if len(nodes) == 0:
        error(errors, "'nodes' must be a non-empty array")

    node_ids = set()
    node_outputs = {}
    node_types = {}

    for i, node in enumerate(nodes):
        ctx = f"nodes[{i}]"
        if not isinstance(node, dict):
            error(errors, f"{ctx} must be an object")
            continue

        node_id = node.get("nodeId")
        name = node.get("name")
        flow_node_type = node.get("flowNodeType")
        position = node.get("position")
        inputs = node.get("inputs")
        outputs = node.get("outputs")

        if not isinstance(node_id, str) or not node_id:
            error(errors, f"{ctx}.nodeId must be a non-empty string")
            continue
        if node_id in node_ids:
            error(errors, f"duplicate nodeId: '{node_id}'")
        node_ids.add(node_id)

        if not isinstance(name, str) or not name:
            error(errors, f"{ctx}.name must be a non-empty string")
        if not isinstance(flow_node_type, str) or flow_node_type not in SUPPORTED_NODE_TYPES:
            warn(warnings, f"{ctx}.flowNodeType '{flow_node_type}' is not in validator allowlist; may still be valid in FastGPT")
        else:
            node_types[node_id] = flow_node_type

        if not isinstance(position, dict):
            error(errors, f"{ctx}.position must be an object")
        else:
            if not isinstance(position.get("x"), (int, float)):
                error(errors, f"{ctx}.position.x must be numeric")
            if not isinstance(position.get("y"), (int, float)):
                error(errors, f"{ctx}.position.y must be numeric")

        if not isinstance(inputs, list):
            error(errors, f"{ctx}.inputs must be an array")
            inputs = []
        if not isinstance(outputs, list):
            error(errors, f"{ctx}.outputs must be an array")
            outputs = []

        missing_preferred = sorted(field for field in PREFERRED_NODE_FIELDS if field not in node)
        if missing_preferred:
            warn(warnings, f"{ctx} missing preferred compatibility fields: {', '.join(missing_preferred)}")

        for j, out in enumerate(outputs):
            if isinstance(out, dict) and isinstance(out.get("key"), str) and "id" not in out:
                warn(warnings, f"{ctx}.outputs[{j}] has key '{out.get('key')}' but no 'id'; compatibility may be lower")

        if flow_node_type == "chatNode":
            user_inputs = [inp for inp in inputs if isinstance(inp, dict) and inp.get("key") == "userChatInput"]
            if not user_inputs:
                report(strict, errors, warnings, f"{ctx} is chatNode but missing required input key 'userChatInput'")
            else:
                user_input = user_inputs[0]
                expected = ["workflowStart", "userChatInput"]
                if user_input.get("value") != expected:
                    warn(warnings, f"{ctx}.inputs userChatInput is not using the minimal default {expected}; this is allowed when the workflow intentionally uses another source")

            history_inputs = [inp for inp in inputs if isinstance(inp, dict) and inp.get("key") == "history"]
            if not history_inputs:
                report(strict, errors, warnings, f"{ctx} is chatNode but missing preferred input key 'history'")
            else:
                history_input = history_inputs[0]
                if history_input.get("value") != 6:
                    warn(warnings, f"{ctx}.inputs history is not using the minimal default 6; this is allowed when the workflow intentionally uses another history setting")

        node_outputs[node_id] = collect_output_keys(node)

    has_workflow_start = any(v == "workflowStart" for v in node_types.values())
    has_user_guide = any(v == "userGuide" for v in node_types.values())
    has_output = any(v in {"answerNode", "pluginOutput"} for v in node_types.values())
    has_read_files = any(v == "readFiles" for v in node_types.values())

    if not has_workflow_start:
        error(errors, "missing required node type 'workflowStart'")
    if not has_user_guide:
        warn(warnings, "recommended node type 'userGuide' is missing")
    if not has_output:
        report(strict, errors, warnings, "no explicit output node detected: answerNode or pluginOutput")

    adjacency = {nid: set() for nid in node_ids}
    edge_pairs = set()

    for i, edge in enumerate(edges):
        ctx = f"edges[{i}]"
        if not isinstance(edge, dict):
            error(errors, f"{ctx} must be an object")
            continue
        for field in ["source", "sourceHandle", "target", "targetHandle"]:
            if not isinstance(edge.get(field), str) or not edge.get(field):
                error(errors, f"{ctx}.{field} must be a non-empty string")

        source = edge.get("source")
        target = edge.get("target")
        if isinstance(source, str) and source not in node_ids:
            error(errors, f"{ctx}.source '{source}' not found")
        if isinstance(target, str) and target not in node_ids:
            error(errors, f"{ctx}.target '{target}' not found")

        if isinstance(edge.get("sourceHandle"), str) and source and not re.match(rf"^{re.escape(source)}-source-(left|right|top|bottom)$", edge["sourceHandle"]):
            warn(warnings, f"{ctx}.sourceHandle format looks unusual: {edge['sourceHandle']}")
        if isinstance(edge.get("targetHandle"), str) and target and not re.match(rf"^{re.escape(target)}-target-(left|right|top|bottom)$", edge["targetHandle"]):
            warn(warnings, f"{ctx}.targetHandle format looks unusual: {edge['targetHandle']}")

        if isinstance(source, str) and isinstance(target, str):
            pair = (source, target, edge.get("sourceHandle"), edge.get("targetHandle"))
            if pair in edge_pairs:
                error(errors, f"{ctx} duplicates an existing edge")
            edge_pairs.add(pair)
            if source in adjacency:
                adjacency[source].add(target)
            if source == target:
                error(errors, f"{ctx} contains self-loop on '{source}'")

    for i, node in enumerate(nodes):
        if not isinstance(node, dict) or not isinstance(node.get("nodeId"), str):
            continue
        node_id = node["nodeId"]
        for j, inp in enumerate(node.get("inputs", [])):
            if not isinstance(inp, dict):
                continue
            if inp.get("key") == "system_input_config":
                validate_system_input_config(inp, errors, warnings, f"node '{node_id}' input[{j}]", strict)
            if "value" in inp:
                validate_reference(inp.get("value"), node_outputs, errors, warnings, f"node '{node_id}' input[{j}]", strict)

    workflow_start_ids = [nid for nid, typ in node_types.items() if typ == "workflowStart"]
    if workflow_start_ids:
        start_id = workflow_start_ids[0]
        reachable = set()
        stack = [start_id]
        while stack:
            cur = stack.pop()
            if cur in reachable:
                continue
            reachable.add(cur)
            stack.extend(adjacency.get(cur, []))
        ignored = {nid for nid, typ in node_types.items() if typ == "userGuide"}
        orphaned = [nid for nid in node_ids if nid not in reachable and nid not in ignored]
        if orphaned:
            report(strict, errors, warnings, "unreachable nodes from workflowStart: " + ", ".join(sorted(orphaned)))

    start_output_keys = set()
    if workflow_start_ids:
        start_output_keys = node_outputs.get(workflow_start_ids[0], set())

    needs_file_upload = has_read_files or ("userFiles" in start_output_keys)
    file_cfg = chat_config.get("fileSelectConfig") if isinstance(chat_config, dict) else None
    if needs_file_upload:
        if not isinstance(file_cfg, dict):
            report(strict, errors, warnings, "workflow expects file input but chatConfig.fileSelectConfig is missing")
        else:
            if file_cfg.get("canSelectFile") is not True:
                report(strict, errors, warnings, "workflow expects file input but chatConfig.fileSelectConfig.canSelectFile is not true")

    needs_image_upload = False
    if needs_image_upload:
        if not isinstance(file_cfg, dict) or file_cfg.get("canSelectImg") is not True:
            report(strict, errors, warnings, "workflow expects image input but chatConfig.fileSelectConfig.canSelectImg is not true")


def main():
    strict = False
    args = sys.argv[1:]

    if args and args[0] == "--strict-generated":
        strict = True
        args = args[1:]

    if len(args) != 1:
        print("Usage: validate_fastgpt_workflow.py [--strict-generated] <workflow.json>", file=sys.stderr)
        return 2

    path = Path(args[0])
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as e:
        print(f"JSON parse error: {e}", file=sys.stderr)
        return 1

    errors = []
    warnings = []

    shape, workflow = detect_shape(data, errors)
    if shape == "invalid":
        print_report(shape, errors, warnings)
        return 1

    if shape == "template-wrapper":
        validate_template_wrapper(data, warnings, errors)

    validate_workflow_core(workflow, warnings, errors, strict)

    print_report(shape, strict, errors, warnings)
    return 1 if errors else 0


def print_report(shape, strict, errors, warnings):
    report = {
        "ok": not errors,
        "shape": shape,
        "mode": "strict-generated" if strict else "default",
        "errors": errors,
        "warnings": warnings
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    raise SystemExit(main())
