from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

STAGE_ID = "1013R_R30_VISIBLE_FRAME_CONNECTOR"
OUT_DIR = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1" / "1013R_R30_visible_frame_connector"
DOC_PATH = ROOT / "docs" / "1013R_R30_visible_frame_connector.md"


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
    from backend.xiaobei_ai import prep_room_visible_frame_connector_1013R_R30 as r30

    errors: list[str] = []
    connector = r30.build_connector_map()
    page = r21.build_binding_sample_bundle()
    html = page.get("html", "")
    boundary = connector.get("boundary", {})
    doc = DOC_PATH.read_text(encoding="utf-8", errors="ignore") if DOC_PATH.exists() else ""

    def fail(code: str) -> None:
        errors.append(code)

    if connector.get("stage") != STAGE_ID:
        fail("stage_id_mismatch")
    if connector.get("active_room", {}).get("room_id") != "prep_room":
        fail("active_room_not_prep_room")
    if len(connector.get("visible_frame_labels", [])) != 4:
        fail("four_visible_frame_labels_missing")
    if len(connector.get("tool_groups", [])) < 4:
        fail("tool_groups_too_few")
    if len(connector.get("tool_content_connectors", [])) < 9:
        fail("tool_connectors_too_few")
    for token in ["courseware_workspace", "classroom_display_preview", "material_intake", "teacher_action_gate"]:
        if token not in json.dumps(connector, ensure_ascii=False):
            fail(f"connector_token_missing:{token}")
    for token in ["data-shiwei-room-id", "data-shiwei-tool-id", "data-shiwei-slot-id", "r30-tool-panel", "renderVisibleToolPanel"]:
        if token not in html:
            fail(f"html_token_missing:{token}")
    for token in ["R36_modified=false", "provider_called=false", "formal_apply_performed=false"]:
        if token not in doc:
            fail(f"doc_boundary_token_missing:{token}")
    for flag in [
        "R36_modified",
        "main_shell_modified",
        "route_registered",
        "endpoint_registered",
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
        "connector_id": connector.get("connector_id"),
        "active_room": connector.get("active_room"),
        "tool_group_count": len(connector.get("tool_groups", [])),
        "tool_connector_count": len(connector.get("tool_content_connectors", [])),
        "html_length": len(html),
        "boundary": boundary,
    }
    result = {
        "stage_id": STAGE_ID,
        "status": "PASS" if not errors else "FAIL",
        "validator_pass": not errors,
        "created_at": now(),
        "checks": {
            "visible_frame_labels": len(connector.get("visible_frame_labels", [])) == 4,
            "tool_groups_present": len(connector.get("tool_groups", [])) >= 4,
            "room_tool_slot_data_attributes_present": all(
                token in html for token in ["data-shiwei-room-id", "data-shiwei-tool-id", "data-shiwei-slot-id"]
            ),
            "current_R21_page_copy_used": "script-1013R-R21-internal-prototype-binding" in html,
            "readonly_boundaries_intact": not any(code.startswith("boundary_broken") for code in errors),
        },
        "failed_checks": errors,
    }
    return result, evidence, errors


def write_outputs(result: dict[str, Any], evidence: dict[str, Any]) -> None:
    from backend.xiaobei_ai import prep_room_visible_frame_connector_1013R_R30 as r30

    bundle = r30.build_visible_connector_sample_bundle()
    write_json(OUT_DIR / "1013R_R30_result.json", result)
    write_json(OUT_DIR / "1013R_R30_connector_map.json", bundle["connector_map"])
    write_json(OUT_DIR / "1013R_R30_evidence.json", evidence)
    write_text(
        OUT_DIR / "1013R_R30_report.md",
        f"""# 1013R_R30 visible frame connector

```text
stage_id={STAGE_ID}
validator_pass={str(result["validator_pass"]).lower()}
failed_checks={result["failed_checks"]}
R36_modified=false
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
    print("PASS: 1013R_R30 visible frame connector")


if __name__ == "__main__":
    main()
