from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

STAGE_ID = "1013R_R31_TOOL_CONTENT_STATIC_LINKAGE"
OUT_DIR = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1" / "1013R_R31_tool_content_static_linkage"
DOC_PATH = ROOT / "docs" / "1013R_R31_tool_content_static_linkage.md"


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
    from backend.xiaobei_ai import prep_room_tool_content_static_linkage_1013R_R31 as r31

    errors: list[str] = []
    linkage = r31.build_static_linkage_map()
    page = r21.build_binding_sample_bundle()
    html = page.get("html", "")
    boundary = linkage.get("boundary", {})
    doc = DOC_PATH.read_text(encoding="utf-8", errors="ignore") if DOC_PATH.exists() else ""

    def fail(code: str) -> None:
        errors.append(code)

    if linkage.get("stage") != STAGE_ID:
        fail("stage_id_mismatch")
    links = linkage.get("tool_links", [])
    if len(links) < 9:
        fail("tool_links_too_few")
    if any(link.get("blocked") for link in links):
        fail("unexpected_blocked_tool_link")
    for token in ["activateToolContent", "r31-content-highlight", "scrollIntoView", "__PREP_ROOM_R31_ACTIVE_TOOL_LINK__"]:
        if token not in html:
            fail(f"html_linkage_token_missing:{token}")
    for token in ["new_page_navigation_allowed=false", "formal_apply_allowed=false"]:
        if token not in doc:
            fail(f"doc_token_missing:{token}")
    for flag in [
        "navigation_creates_new_page",
        "real_generation_performed",
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
        "linkage_id": linkage.get("linkage_id"),
        "tool_link_count": len(links),
        "html_length": len(html),
        "boundary": boundary,
    }
    result = {
        "stage_id": STAGE_ID,
        "status": "PASS" if not errors else "FAIL",
        "validator_pass": not errors,
        "created_at": now(),
        "checks": {
            "tool_links_present": len(links) >= 9,
            "all_tools_have_targets": not any(link.get("blocked") for link in links),
            "click_highlight_script_present": "activateToolContent" in html and "r31-content-highlight" in html,
            "readonly_boundaries_intact": not any(code.startswith("boundary_broken") for code in errors),
        },
        "failed_checks": errors,
    }
    return result, evidence, errors


def write_outputs(result: dict[str, Any], evidence: dict[str, Any]) -> None:
    from backend.xiaobei_ai import prep_room_tool_content_static_linkage_1013R_R31 as r31

    bundle = r31.build_static_linkage_sample_bundle()
    write_json(OUT_DIR / "1013R_R31_result.json", result)
    write_json(OUT_DIR / "1013R_R31_static_linkage_map.json", bundle["static_linkage_map"])
    write_json(OUT_DIR / "1013R_R31_evidence.json", evidence)
    write_text(
        OUT_DIR / "1013R_R31_report.md",
        f"""# 1013R_R31 tool content static linkage

```text
stage_id={STAGE_ID}
validator_pass={str(result["validator_pass"]).lower()}
failed_checks={result["failed_checks"]}
navigation_creates_new_page=false
real_generation_performed=false
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
    print("PASS: 1013R_R31 tool content static linkage")


if __name__ == "__main__":
    main()
