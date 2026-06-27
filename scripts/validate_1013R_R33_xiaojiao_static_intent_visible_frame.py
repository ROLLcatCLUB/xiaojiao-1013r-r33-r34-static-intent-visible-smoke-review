from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

STAGE_ID = "1013R_R33_XIAOJIAO_STATIC_INTENT_TO_VISIBLE_FRAME"
OUT_DIR = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1" / "1013R_R33_xiaojiao_static_intent_visible_frame"
DOC_PATH = ROOT / "docs" / "1013R_R33_xiaojiao_static_intent_visible_frame.md"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def validate() -> tuple[dict[str, Any], dict[str, Any], list[str]]:
    from backend.xiaobei_ai import prep_room_page_copy_package_binding_1013R_R21 as r21
    from backend.xiaobei_ai import prep_room_xiaojiao_static_intent_visible_frame_1013R_R33 as r33

    errors: list[str] = []
    mapping = r33.build_static_intent_visible_frame_map()
    page = r21.build_binding_sample_bundle()
    html = page.get("html", "")
    boundary = mapping.get("boundary", {})
    doc = DOC_PATH.read_text(encoding="utf-8", errors="ignore") if DOC_PATH.exists() else ""

    def fail(code: str) -> None:
        errors.append(code)

    if mapping.get("stage") != STAGE_ID:
        fail("stage_id_mismatch")
    routes = mapping.get("visible_routes", [])
    by_input = {route.get("input"): route for route in routes}
    for fixture in ["课件入口找不到", "这段教案太乱", "帮我生成大屏", "评价表怎么没有", "我要保存这个课包"]:
        if fixture not in by_input:
            fail(f"fixture_missing:{fixture}")
    for route in routes:
        for field in ["intent", "frame_level", "room_id", "tool_id", "slot_id", "action_gate_required", "visible_result"]:
            if field not in route:
                fail(f"route_field_missing:{route.get('input')}:{field}")
        if route.get("room_id") != "prep_room":
            fail(f"route_room_not_prep_room:{route.get('input')}")
        if route.get("preview_only") is not True:
            fail(f"route_preview_not_true:{route.get('input')}")
        if route.get("formal_apply_allowed") is not False:
            fail(f"route_formal_apply_not_false:{route.get('input')}")
        if route.get("model_call_allowed") is not False or route.get("runtime_call_allowed") is not False:
            fail(f"route_runtime_or_model_allowed:{route.get('input')}")
    if by_input.get("评价表怎么没有", {}).get("blocked") is not True:
        fail("assessment_fixture_not_blocked")
    if by_input.get("我要保存这个课包", {}).get("tool_id") != "teacher_action_gate":
        fail("save_fixture_not_routed_to_teacher_gate")
    if by_input.get("课件入口找不到", {}).get("slot_id") != "courseware_entry":
        fail("courseware_entry_fixture_not_routed_to_right_entry")
    if by_input.get("帮我生成大屏", {}).get("slot_id") != "classroom_display_screen":
        fail("display_fixture_not_routed_to_right_preview")
    if by_input.get("评价表怎么没有", {}).get("slot_id") != "assessment_rubric":
        fail("assessment_fixture_not_routed_to_rubric_preview")
    if by_input.get("我要保存这个课包", {}).get("slot_id") != "package_save_gate":
        fail("save_fixture_not_routed_to_package_save_gate")
    for route in routes:
        if route.get("tool_id") in {"courseware_workspace", "classroom_display_preview"}:
            if any("derivative_linkage" in str(selector) for selector in route.get("target_selectors", [])):
                fail(f"derivative_linkage_still_primary_target:{route.get('input')}")
    for token in [
        "r33-intent-panel",
        "data-r33-xiaojiao-judgement",
        "bindXiaojiaoStaticIntent",
        "activateStaticIntentRoute",
        "data-1013r-r33-static-intent-visible-frame",
        "小教判断",
        "data-shiwei-generated-visual=\"true\"",
        "data-shiwei-hide-after-review=\"true\"",
    ]:
        if token not in html:
            fail(f"html_token_missing:{token}")
    if doc and "R36_modified=false" not in doc:
        fail("doc_boundary_token_missing:R36_modified=false")
    for flag in [
        "real_generation_performed",
        "runtime_connected",
        "runtime_router_connected",
        "semantic_runtime_called",
        "provider_called",
        "model_called",
        "database_written",
        "memory_written",
        "feishu_written",
        "formal_apply_performed",
        "R36_modified",
        "main_shell_modified",
        "route_registered",
        "endpoint_registered",
        "new_disconnected_page_created",
    ]:
        if boundary.get(flag):
            fail(f"boundary_broken:{flag}")

    evidence = {
        "stage_id": STAGE_ID,
        "intent_visible_id": mapping.get("intent_visible_id"),
        "fixture_count": len(routes),
        "route_inputs": [route.get("input") for route in routes],
        "html_length": len(html),
        "boundary": boundary,
    }
    result = {
        "stage_id": STAGE_ID,
        "status": "PASS" if not errors else "FAIL",
        "validator_pass": not errors,
        "created_at": now(),
        "checks": {
            "five_static_inputs_pass": len(routes) >= 5 and not any(code.startswith("fixture_missing") for code in errors),
            "required_route_fields_present": not any(code.startswith("route_field_missing") for code in errors),
            "xiaojiao_judgement_visible": "r33-intent-panel" in html and "小教判断" in html,
            "each_input_targets_tool_or_slot": all(route.get("tool_id") and route.get("slot_id") for route in routes),
            "assessment_blocked": by_input.get("评价表怎么没有", {}).get("blocked") is True,
            "save_enters_teacher_gate": by_input.get("我要保存这个课包", {}).get("tool_id") == "teacher_action_gate",
            "courseware_routes_to_right_entry": by_input.get("课件入口找不到", {}).get("slot_id") == "courseware_entry",
            "display_routes_to_right_preview": by_input.get("帮我生成大屏", {}).get("slot_id")
            == "classroom_display_screen",
            "save_routes_to_package_save_gate": by_input.get("我要保存这个课包", {}).get("slot_id")
            == "package_save_gate",
            "flow_relation_not_primary_target": not any(
                "derivative_linkage" in str(selector)
                for route in routes
                if route.get("tool_id") in {"courseware_workspace", "classroom_display_preview"}
                for selector in route.get("target_selectors", [])
            ),
            "generated_visuals_marked_red": "data-shiwei-generated-visual=\"true\"" in html and "#b42323" in html,
            "readonly_boundaries_intact": not any(code.startswith("boundary_broken") for code in errors),
        },
        "failed_checks": errors,
    }
    return result, evidence, errors


def write_outputs(result: dict[str, Any], evidence: dict[str, Any]) -> None:
    from backend.xiaobei_ai import prep_room_xiaojiao_static_intent_visible_frame_1013R_R33 as r33

    bundle = r33.build_static_intent_visible_frame_sample_bundle()
    write_json(OUT_DIR / "1013R_R33_result.json", result)
    write_json(OUT_DIR / "1013R_R33_static_intent_visible_frame.json", bundle["static_intent_visible_frame"])
    write_json(OUT_DIR / "1013R_R33_evidence.json", evidence)
    write_text(
        OUT_DIR / "1013R_R33_report.md",
        f"""# 1013R_R33 Xiaojiao static intent to visible frame

```text
stage_id={STAGE_ID}
validator_pass={str(result["validator_pass"]).lower()}
failed_checks={result["failed_checks"]}
fixture_count={evidence["fixture_count"]}
real_generation_performed=false
runtime_connected=false
provider_called=false
model_called=false
formal_apply_performed=false
R36_modified=false
```
""",
    )


def main() -> None:
    result, evidence, errors = validate()
    write_outputs(result, evidence)
    if errors:
        raise SystemExit("FAIL: " + ", ".join(errors))
    print("PASS: 1013R_R33 Xiaojiao static intent visible frame")


if __name__ == "__main__":
    main()
