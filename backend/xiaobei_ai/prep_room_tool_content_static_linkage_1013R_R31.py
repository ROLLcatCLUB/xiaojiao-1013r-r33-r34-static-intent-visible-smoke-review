from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from typing import Any

from . import prep_room_visible_frame_connector_1013R_R30 as r30_connector


STAGE_ID = "1013R_R31_TOOL_CONTENT_STATIC_LINKAGE"
LINKAGE_ID = "SHIWEI_TOOL_CONTENT_STATIC_LINKAGE_R0"


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def boundary_flags() -> dict[str, bool]:
    flags = dict(r30_connector.boundary_flags())
    flags.update(
        {
            "stage": STAGE_ID,
            "tool_content_static_linkage_defined": True,
            "tool_click_highlight_only": True,
            "navigation_creates_new_page": False,
            "real_generation_performed": False,
            "runtime_connected": False,
            "provider_called": False,
            "model_called": False,
            "database_written": False,
            "memory_written": False,
            "feishu_written": False,
            "formal_apply_performed": False,
        }
    )
    return flags


def build_static_linkage_map() -> dict[str, Any]:
    connector = r30_connector.build_connector_map()
    links = []
    for item in connector.get("tool_content_connectors", []):
        slots = item.get("content_slots", [])
        primary = slots[0] if slots else {}
        links.append(
            {
                "tool_id": item.get("tool_id"),
                "tool_label": item.get("tool_label"),
                "room_id": item.get("room_id"),
                "tool_group_id": item.get("tool_group_id"),
                "primary_slot_id": primary.get("slot_id"),
                "target_selectors": [slot.get("visible_selector") for slot in slots if slot.get("visible_selector")],
                "highlight_mode": "scroll_into_view_and_soft_outline",
                "blocked": not bool(slots),
                "blocked_reason": "" if slots else "no_visible_content_slot_registered",
                "preview_only": True,
                "formal_apply_allowed": False,
            }
        )
    return {
        "ok": True,
        "stage": STAGE_ID,
        "linkage_id": LINKAGE_ID,
        "generated_at": _now(),
        "consumes": {
            "r30_stage": connector.get("stage"),
            "r30_connector_id": connector.get("connector_id"),
        },
        "tool_links": links,
        "interaction_contract": {
            "click_tool_scrolls_to_content": True,
            "click_tool_highlights_content": True,
            "new_page_navigation_allowed": False,
            "real_generation_allowed": False,
            "save_export_archive_allowed": False,
        },
        "boundary": boundary_flags(),
        "next_stage_recommendation": {
            "stage": "1013R_R32_DERIVATIVE_PREVIEW_SAMPLE_ROOM",
            "why": "Tools can locate content slots; next normalize derivative previews for courseware, display, worksheet, and assessment.",
        },
    }


def build_static_linkage_sample_bundle() -> dict[str, Any]:
    linkage = build_static_linkage_map()
    return {
        "ok": True,
        "stage": STAGE_ID,
        "static_linkage_map": linkage,
        "tool_links": deepcopy(linkage["tool_links"]),
        "boundary": deepcopy(linkage["boundary"]),
    }
