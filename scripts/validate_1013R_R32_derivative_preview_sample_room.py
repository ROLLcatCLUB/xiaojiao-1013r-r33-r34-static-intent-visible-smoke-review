from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

STAGE_ID = "1013R_R32_DERIVATIVE_PREVIEW_SAMPLE_ROOM"
OUT_DIR = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1" / "1013R_R32_derivative_preview_sample_room"
DOC_PATH = ROOT / "docs" / "1013R_R32_derivative_preview_sample_room.md"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def validate() -> tuple[dict[str, Any], dict[str, Any], list[str]]:
    from backend.xiaobei_ai import prep_room_derivative_preview_sample_room_1013R_R32 as r32
    from backend.xiaobei_ai import prep_room_page_copy_package_binding_1013R_R21 as r21

    errors: list[str] = []
    sample_room = r32.build_derivative_preview_samples()
    page = r21.build_binding_sample_bundle()
    html = page.get("html", "")
    boundary = sample_room.get("boundary", {})
    doc = DOC_PATH.read_text(encoding="utf-8", errors="ignore") if DOC_PATH.exists() else ""

    def fail(code: str) -> None:
        errors.append(code)

    if sample_room.get("stage") != STAGE_ID:
        fail("stage_id_mismatch")
    samples = sample_room.get("samples", [])
    by_id = {sample.get("derivative_id"): sample for sample in samples}
    for derivative_id in ["courseware_script", "classroom_display_screen", "worksheet", "assessment_rubric"]:
        if derivative_id not in by_id:
            fail(f"derivative_sample_missing:{derivative_id}")
    for sample in samples:
        for field in sample_room.get("uniform_preview_fields", []):
            if field not in sample:
                fail(f"uniform_field_missing:{sample.get('derivative_id')}:{field}")
        if sample.get("teacher_confirmation", {}).get("formal_apply_allowed") is not False:
            fail(f"formal_apply_not_false:{sample.get('derivative_id')}")
    if by_id.get("assessment_rubric", {}).get("status") != "blocked":
        fail("assessment_rubric_not_blocked")
    for token in ["r32-derivative-panel", "r32-derivative-card", "data-r32-derivative-id", "assessment_rubric"]:
        if token not in html:
            fail(f"html_sample_token_missing:{token}")
    for token in ["assessment_rubric：blocked", "real_export_created=false", "formal_apply_performed=false"]:
        if token not in doc:
            fail(f"doc_token_missing:{token}")
    for flag in [
        "real_export_created",
        "runtime_connected",
        "provider_called",
        "model_called",
        "database_written",
        "memory_written",
        "feishu_written",
        "formal_apply_performed",
    ]:
        if boundary.get(flag):
            fail(f"boundary_broken:{flag}")

    evidence = {
        "stage_id": STAGE_ID,
        "sample_room_id": sample_room.get("sample_room_id"),
        "sample_count": len(samples),
        "assessment_status": by_id.get("assessment_rubric", {}).get("status"),
        "html_length": len(html),
        "boundary": boundary,
    }
    result = {
        "stage_id": STAGE_ID,
        "status": "PASS" if not errors else "FAIL",
        "validator_pass": not errors,
        "created_at": now(),
        "checks": {
            "four_derivative_samples_present": all(
                item in by_id for item in ["courseware_script", "classroom_display_screen", "worksheet", "assessment_rubric"]
            ),
            "uniform_fields_present": not any(code.startswith("uniform_field_missing") for code in errors),
            "assessment_blocked": by_id.get("assessment_rubric", {}).get("status") == "blocked",
            "html_preview_panel_present": "r32-derivative-panel" in html,
            "readonly_boundaries_intact": not any(code.startswith("boundary_broken") for code in errors),
        },
        "failed_checks": errors,
    }
    return result, evidence, errors


def write_outputs(result: dict[str, Any], evidence: dict[str, Any]) -> None:
    from backend.xiaobei_ai import prep_room_derivative_preview_sample_room_1013R_R32 as r32

    bundle = r32.build_derivative_preview_sample_bundle()
    write_json(OUT_DIR / "1013R_R32_result.json", result)
    write_json(OUT_DIR / "1013R_R32_derivative_preview_sample_room.json", bundle["derivative_preview_sample_room"])
    write_json(OUT_DIR / "1013R_R32_evidence.json", evidence)
    write_text(
        OUT_DIR / "1013R_R32_report.md",
        f"""# 1013R_R32 derivative preview sample room

```text
stage_id={STAGE_ID}
validator_pass={str(result["validator_pass"]).lower()}
failed_checks={result["failed_checks"]}
assessment_rubric_status={evidence.get("assessment_status")}
real_export_created=false
runtime_connected=false
provider_called=false
model_called=false
formal_apply_performed=false
```
""",
    )


def main() -> None:
    result, evidence, errors = validate()
    write_outputs(result, evidence)
    if errors:
        raise SystemExit("FAIL: " + ", ".join(errors))
    print("PASS: 1013R_R32 derivative preview sample room")


if __name__ == "__main__":
    main()
