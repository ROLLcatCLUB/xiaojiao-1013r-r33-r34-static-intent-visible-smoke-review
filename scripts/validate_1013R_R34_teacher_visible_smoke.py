from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

STAGE_ID = "1013R_R34_TEACHER_VISIBLE_SMOKE"
OUT_DIR = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1" / "1013R_R34_teacher_visible_smoke"
R21_HTML = (
    ROOT
    / "outputs"
    / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
    / "1013R_R21_page_copy_binds_unified_package"
    / "prep_room_page_copy_binds_unified_package_1013R_R21.html"
)
DOC_PATH = ROOT / "docs" / "1013R_R34_teacher_visible_smoke.md"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def validate() -> tuple[dict[str, Any], dict[str, Any], list[str]]:
    from backend.xiaobei_ai import prep_room_teacher_visible_smoke_1013R_R34 as r34

    errors: list[str] = []
    smoke = r34.build_teacher_visible_smoke()
    dom = smoke.get("dom_smoke", {})
    screenshot = smoke.get("screenshot_smoke", {})
    boundary = smoke.get("boundary", {})
    walkthrough = smoke.get("teacher_walkthrough", "")
    gpt_note = smoke.get("gpt_review_note", "")
    doc = DOC_PATH.read_text(encoding="utf-8", errors="ignore") if DOC_PATH.exists() else ""

    def fail(code: str) -> None:
        errors.append(code)

    if smoke.get("stage") != STAGE_ID:
        fail("stage_id_mismatch")
    if not dom.get("pass"):
        fail("dom_textual_smoke_failed")
    for key, value in dom.get("checks", {}).items():
        if not value:
            fail(f"dom_check_failed:{key}")
    if "当前页面是" not in walkthrough or "备课室" not in walkthrough:
        fail("teacher_walkthrough_missing_room_explanation")
    for token in ["右侧红色", "小教判断", "评价表", "formal_apply_allowed=false", "data-shiwei-generated-visual=true"]:
        if token not in walkthrough:
            fail(f"teacher_walkthrough_token_missing:{token}")
    for token in ["FINAL_STATUS=PASS_R33_R34_XIAOJIAO_STATIC_INTENT_VISIBLE_SMOKE", "R36_RUNTIME_PROVIDER_STAGE=HOLD"]:
        if token not in gpt_note:
            fail(f"gpt_review_note_token_missing:{token}")
    if screenshot.get("available"):
        if not screenshot.get("screenshot_files"):
            fail("screenshot_available_but_files_missing")
    else:
        if screenshot.get("mode") != "html_textual_smoke_fallback" or not screenshot.get("fallback_reason"):
            fail("screenshot_fallback_reason_missing")
    routes = smoke.get("fixture_route_matrix", [])
    if len(routes) < 5:
        fail("fixture_route_matrix_too_small")
    if not any(route.get("input") == "评价表怎么没有" and route.get("blocked") for route in routes):
        fail("assessment_blocked_route_missing")
    if not any(route.get("input") == "我要保存这个课包" and route.get("action_gate_required") for route in routes):
        fail("save_action_gate_route_missing")
    if doc and "R36_modified=false" not in doc:
        fail("doc_boundary_token_missing:R36_modified=false")
    for flag in [
        "real_generation_performed",
        "runtime_connected",
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
        "smoke_id": smoke.get("smoke_id"),
        "dom_smoke_pass": dom.get("pass"),
        "dom_smoke_mode": dom.get("mode"),
        "marker_counts": dom.get("marker_counts"),
        "screenshot_available": screenshot.get("available"),
        "screenshot_mode": screenshot.get("mode"),
        "screenshot_fallback_reason": screenshot.get("fallback_reason"),
        "fixture_route_count": len(routes),
        "boundary": boundary,
    }
    result = {
        "stage_id": STAGE_ID,
        "status": "PASS" if not errors else "FAIL",
        "validator_pass": not errors,
        "created_at": now(),
        "checks": {
            "dom_smoke_json_present": bool(dom),
            "dom_smoke_pass": dom.get("pass") is True,
            "teacher_walkthrough_present": "备课室" in walkthrough and "小教判断" in walkthrough,
            "fixture_route_matrix_present": len(routes) >= 5,
            "assessment_rubric_blocked": not any(code == "assessment_blocked_route_missing" for code in errors),
            "save_export_enters_teacher_gate": not any(code == "save_action_gate_route_missing" for code in errors),
            "screenshot_or_textual_smoke_present": screenshot.get("available") is True
            or screenshot.get("mode") == "html_textual_smoke_fallback",
            "gpt_review_note_present": "FINAL_STATUS=PASS_R33_R34_XIAOJIAO_STATIC_INTENT_VISIBLE_SMOKE" in gpt_note,
            "readonly_boundaries_intact": not any(code.startswith("boundary_broken") for code in errors),
        },
        "failed_checks": errors,
    }
    return result, evidence, errors


def write_outputs(result: dict[str, Any], evidence: dict[str, Any]) -> None:
    from backend.xiaobei_ai import prep_room_page_copy_package_binding_1013R_R21 as r21
    from backend.xiaobei_ai import prep_room_teacher_visible_smoke_1013R_R34 as r34

    bundle = r34.build_teacher_visible_smoke_sample_bundle()
    smoke = bundle["teacher_visible_smoke"]
    page = r21.build_binding_sample_bundle()
    write_json(OUT_DIR / "1013R_R34_result.json", result)
    write_json(OUT_DIR / "1013R_R34_dom_smoke.json", smoke["dom_smoke"])
    write_json(OUT_DIR / "1013R_R34_screenshot_smoke.json", smoke["screenshot_smoke"])
    write_json(OUT_DIR / "1013R_R34_fixture_route_matrix.json", smoke["fixture_route_matrix"])
    write_json(OUT_DIR / "1013R_R34_evidence.json", evidence)
    write_text(OUT_DIR / "teacher_walkthrough.md", smoke["teacher_walkthrough"])
    write_text(OUT_DIR / "GPT_REVIEW_NOTE_1013R_R34.md", smoke["gpt_review_note"])
    write_text(OUT_DIR / "prep_room_page_copy_binds_unified_package_1013R_R21.html", page["html"])
    write_text(R21_HTML, page["html"])
    write_text(
        OUT_DIR / "1013R_R34_report.md",
        f"""# 1013R_R34 teacher visible smoke

```text
stage_id={STAGE_ID}
validator_pass={str(result["validator_pass"]).lower()}
failed_checks={result["failed_checks"]}
dom_smoke_mode={evidence["dom_smoke_mode"]}
screenshot_mode={evidence["screenshot_mode"]}
screenshot_fallback_reason={evidence["screenshot_fallback_reason"]}
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
    print("PASS: 1013R_R34 teacher visible smoke")


if __name__ == "__main__":
    main()
