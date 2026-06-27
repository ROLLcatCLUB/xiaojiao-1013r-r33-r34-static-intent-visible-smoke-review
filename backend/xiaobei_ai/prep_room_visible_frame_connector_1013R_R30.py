from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from typing import Any

from . import prep_room_main_shell_fetch_adapter_1013L_R5 as l5_adapter
from . import prep_room_render_blocks_protocol_1013R_R17 as r17_blocks
from . import prep_room_tool_frame_registry_1013R_R29 as r29_tools


STAGE_ID = "1013R_R30_VISIBLE_FRAME_CONNECTOR"
CONNECTOR_ID = "SHIWEI_VISIBLE_FRAME_CONNECTOR_R0"


SLOT_SELECTOR_MAP = {
    "current_object_card": ".nb-state-bar",
    "xiaojiao_task_state": ".nb-state-bar",
    "current_lesson_prep_entry": "[data-r21-route-anchor='current_lesson_prep_entry'], .nb-hero",
    "lesson_basis": "[data-r21-route-anchor='lesson_basis'], .nb-doc-section",
    "lesson_body": ".nb-doc-section",
    "teaching_process": ".nb-flow-step",
    "big_unit_catalog": "[data-r21-route-anchor='big_unit_catalog'], .nb-panel",
    "single_lesson_catalog": "[data-r21-route-anchor='single_lesson_catalog'], [data-node^='nb-lesson'], .nb-panel",
    "teacher_demo": ".nb-flow-step",
    "courseware_entry": "[data-r21-route-anchor='courseware_entry'], .courseware-rail, .courseware-r1e-left, .courseware-r1e-screen-list, .courseware-screen-mini",
    "courseware_script": "[data-r21-route-anchor='courseware_entry'], .courseware-rail, .courseware-r1e-left, .courseware-r1e-screen-list, .courseware-screen-mini",
    "classroom_display_screen": "[data-r21-route-anchor='classroom_display_screen'], .courseware-rail, .courseware-r1e-main, .courseware-r1e-screen-frame, .courseware-r1c-screen-frame, .courseware-screen-mini",
    "worksheet": "[data-r32-derivative-id='worksheet'], [data-r21-field-anchor='derivative_linkage']",
    "assessment_rubric": "[data-r32-derivative-id='assessment_rubric'], [data-r21-route-anchor='assessment_rubric']",
    "blackboard_design": "[data-r32-derivative-id='blackboard_design'], .nb-flow-step",
    "materials_list": ".nb-drawer, .nb-right-rail",
    "source_evidence": ".nb-drawer, .nb-right-rail, details",
    "confirm_actions": "[data-r21-route-anchor='teacher_confirm_gate'], .nb-hero-actions, [data-r21-field-anchor='action_gate'], .nb-drawer, .nb-right-rail",
    "package_save_gate": "[data-r21-route-anchor='package_save_gate'], [data-r21-field-anchor='action_gate']",
    "bottom_composer": "[data-r21-route-anchor='xiaojiao_bottom_entry'], .xiaobei-chat-entry, #chatInput, #statusMain",
}


TOOL_SLOT_MAP = {
    "prep_notebook": ["current_lesson_prep_entry", "lesson_basis"],
    "prep_room_home": ["current_object_card", "xiaojiao_task_state"],
    "big_unit_design": ["big_unit_catalog", "source_evidence"],
    "single_lesson_prep": ["single_lesson_catalog", "current_lesson_prep_entry"],
    "courseware_workspace": ["courseware_entry", "classroom_display_screen"],
    "classroom_display_preview": ["classroom_display_screen"],
    "material_intake": ["materials_list", "source_evidence"],
    "schedule_context": ["source_evidence"],
    "teacher_action_gate": ["confirm_actions", "package_save_gate"],
    "source_evidence": ["source_evidence", "materials_list"],
    "xiaojiao_bottom_composer": ["bottom_composer"],
}


TOOL_GROUPS = [
    {
        "group_id": "prep_design",
        "label": "备课设计",
        "tool_ids": ["prep_notebook", "big_unit_design", "single_lesson_prep"],
    },
    {
        "group_id": "derivatives",
        "label": "课堂派生物",
        "tool_ids": ["courseware_workspace", "classroom_display_preview"],
    },
    {
        "group_id": "evidence_and_assessment",
        "label": "依据与评价",
        "tool_ids": ["material_intake", "source_evidence"],
    },
    {
        "group_id": "action_gate",
        "label": "动作门",
        "tool_ids": ["teacher_action_gate", "xiaojiao_bottom_composer"],
    },
]


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def boundary_flags() -> dict[str, bool]:
    flags = dict(r29_tools.boundary_flags())
    flags.update(
        {
            "stage": STAGE_ID,
            "visible_frame_connector_defined": True,
            "room_tool_slot_mapping_defined": True,
            "current_R21_page_copy_generator_targeted": True,
            "new_disconnected_page_created": False,
            "R36_modified": False,
            "main_shell_modified": False,
            "route_registered": False,
            "endpoint_registered": False,
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


def _tool_index() -> dict[str, dict[str, Any]]:
    tools = [
        {
            "tool_id": "prep_notebook",
            "tool_label": "备课本",
            "room_id": "prep_room",
            "source_state_id": "prep_notebook",
            "render_slot": "stage_body",
            "fetch_policy": "l0_state_static_mapping",
        }
    ]
    for adapter in l5_adapter.state_fetch_adapters():
        tools.append(
            {
                "tool_id": adapter.get("active_capability"),
                "tool_label": adapter.get("teacher_label"),
                "room_id": "prep_room",
                "source_state_id": adapter.get("state_id"),
                "render_slot": adapter.get("render_slot"),
                "fetch_policy": adapter.get("fetch_policy"),
            }
        )
    tools.extend(
        [
            {
                "tool_id": "teacher_action_gate",
                "tool_label": "教师确认门",
                "room_id": "prep_room",
                "source_state_id": "confirm_actions",
                "render_slot": "governance",
                "fetch_policy": "render_block_slot_mapping",
            },
            {
                "tool_id": "source_evidence",
                "tool_label": "资料来源与依据",
                "room_id": "prep_room",
                "source_state_id": "source_evidence",
                "render_slot": "governance",
                "fetch_policy": "render_block_slot_mapping",
            },
            {
                "tool_id": "xiaojiao_bottom_composer",
                "tool_label": "小教推进入口",
                "room_id": "prep_room",
                "source_state_id": "bottom_composer",
                "render_slot": "global_bottom",
                "fetch_policy": "composer_prompt_mapping",
            },
        ]
    )
    return {str(tool["tool_id"]): tool for tool in tools if tool.get("tool_id")}


def _render_block_index() -> dict[str, dict[str, Any]]:
    protocol = r17_blocks.build_render_blocks_protocol()
    return {str(block["slot_id"]): block for block in protocol.get("render_blocks", [])}


def _group_for_tool(tool_id: str) -> str:
    for group in TOOL_GROUPS:
        if tool_id in group["tool_ids"]:
            return group["group_id"]
    return "other"


def build_connector_map() -> dict[str, Any]:
    tool_index = _tool_index()
    block_index = _render_block_index()
    connector_items: list[dict[str, Any]] = []
    for tool_id, slot_ids in TOOL_SLOT_MAP.items():
        tool = tool_index.get(tool_id, {})
        slot_links = []
        for slot_id in slot_ids:
            block = block_index.get(slot_id, {})
            slot_links.append(
                {
                    "slot_id": slot_id,
                    "block_type": block.get("block_type"),
                    "title": block.get("title"),
                    "visible_selector": SLOT_SELECTOR_MAP.get(slot_id, "[data-shiwei-frame-level='4']"),
                    "gate_type": block.get("gate_type") or "preview_then_confirm",
                    "formal_apply_allowed": False,
                }
            )
        connector_items.append(
            {
                "tool_id": tool_id,
                "tool_label": tool.get("tool_label") or tool_id,
                "tool_group_id": _group_for_tool(tool_id),
                "room_id": tool.get("room_id") or "prep_room",
                "source_state_id": tool.get("source_state_id"),
                "render_slot": tool.get("render_slot"),
                "fetch_policy": tool.get("fetch_policy"),
                "confirmation_gate": {
                    "preview_only": True,
                    "teacher_confirmation_required": True,
                    "formal_apply_allowed": False,
                },
                "content_slots": slot_links,
            }
        )
    return {
        "ok": True,
        "stage": STAGE_ID,
        "connector_id": CONNECTOR_ID,
        "generated_at": _now(),
        "active_room": {
            "room_id": "prep_room",
            "room_label": "备课室",
            "source": "R21 body[data-active-view='prepNotebook']",
        },
        "visible_frame_labels": [
            {"level": 1, "label": "平台壳层", "teacher_hint": "顶部导航和底部小教入口"},
            {"level": 2, "label": "备课室", "teacher_hint": "当前工作空间"},
            {"level": 3, "label": "工具区", "teacher_hint": "备课本、大单元、单课、课件、大屏、资料、确认门"},
            {"level": 4, "label": "内容区", "teacher_hint": "正文、教学过程、课件草稿、大屏草稿、来源依据"},
        ],
        "tool_groups": deepcopy(TOOL_GROUPS),
        "tool_content_connectors": connector_items,
        "data_attributes": [
            "data-shiwei-room-id",
            "data-shiwei-tool-id",
            "data-shiwei-slot-id",
            "data-shiwei-tool-group-id",
        ],
        "boundary": boundary_flags(),
        "next_stage_recommendation": {
            "stage": "1013R_R31_TOOL_CONTENT_STATIC_LINKAGE",
            "why": "R21 can now expose room, tool, and slot ids; next bind tool clicks to in-page highlighting.",
        },
    }


def build_visible_connector_sample_bundle() -> dict[str, Any]:
    connector = build_connector_map()
    return {
        "ok": True,
        "stage": STAGE_ID,
        "connector_map": connector,
        "tool_content_connectors": deepcopy(connector["tool_content_connectors"]),
        "boundary": deepcopy(connector["boundary"]),
    }
