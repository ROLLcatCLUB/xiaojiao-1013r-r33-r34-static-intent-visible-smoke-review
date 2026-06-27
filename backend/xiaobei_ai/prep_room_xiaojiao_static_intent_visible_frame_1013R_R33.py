from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from typing import Any

from . import prep_room_derivative_preview_sample_room_1013R_R32 as r32_derivative_preview
from . import prep_room_tool_content_static_linkage_1013R_R31 as r31_static_linkage
from . import prep_room_visible_frame_connector_1013R_R30 as r30_connector
from . import prep_room_xiaojiao_intent_frame_router_1013R_R27 as r27_router


STAGE_ID = "1013R_R33_XIAOJIAO_STATIC_INTENT_TO_VISIBLE_FRAME"
INTENT_VISIBLE_ID = "SHIWEI_XIAOJIAO_STATIC_INTENT_VISIBLE_FRAME_R0"


FIXTURE_INPUTS = [
    "课件入口找不到",
    "这段教案太乱",
    "帮我生成大屏",
    "评价表怎么没有",
    "我要保存这个课包",
]


INTENT_RULES = {
    "课件入口找不到": {
        "intent": "find_courseware_entry",
        "frame_level": 3,
        "tool_id": "courseware_workspace",
        "slot_id": "courseware_script",
        "visible_result": "高亮课堂派生物里的课件工具，并定位到课件/大屏草稿内容区。",
        "blocked": False,
        "blocked_reason": "",
    },
    "这段教案太乱": {
        "intent": "diagnose_lesson_body_structure",
        "frame_level": 4,
        "tool_id": "prep_notebook",
        "slot_id": "teaching_process",
        "visible_result": "定位到备课本正文和教学过程内容区，只提示结构问题，不改写正文。",
        "blocked": False,
        "blocked_reason": "",
    },
    "帮我生成大屏": {
        "intent": "preview_classroom_display",
        "frame_level": 3,
        "tool_id": "classroom_display_preview",
        "slot_id": "classroom_display_screen",
        "visible_result": "高亮大屏工具和大屏预览草稿；只展示预览态，不导出、不生成正式课件。",
        "blocked": False,
        "blocked_reason": "",
    },
    "评价表怎么没有": {
        "intent": "assessment_rubric_missing",
        "frame_level": 3,
        "tool_id": "source_evidence",
        "slot_id": "assessment_rubric",
        "visible_result": "定位到评价表预览，并显示 blocked：评价维度需教师确认。",
        "blocked": True,
        "blocked_reason": "评价维度需教师确认",
    },
    "我要保存这个课包": {
        "intent": "save_package_requires_confirmation",
        "frame_level": 3,
        "tool_id": "teacher_action_gate",
        "slot_id": "confirm_actions",
        "visible_result": "进入教师确认门；当前只能预览，不能保存、导出或写入正式课包。",
        "blocked": True,
        "blocked_reason": "保存/导出/归档需要教师确认，formal_apply_allowed=false",
    },
}


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def boundary_flags() -> dict[str, bool]:
    flags = dict(r32_derivative_preview.boundary_flags())
    flags.update(
        {
            "stage": STAGE_ID,
            "xiaojiao_static_intent_visible_frame_defined": True,
            "bottom_composer_static_fixture_bound": True,
            "intent_fixture_only": True,
            "static_fixture_count": len(FIXTURE_INPUTS),
            "tool_highlight_only": True,
            "real_generation_performed": False,
            "runtime_connected": False,
            "runtime_router_connected": False,
            "semantic_runtime_called": False,
            "provider_called": False,
            "model_called": False,
            "database_written": False,
            "memory_written": False,
            "vector_index_written": False,
            "feishu_written": False,
            "formal_apply_performed": False,
            "R36_modified": False,
            "main_shell_modified": False,
            "route_registered": False,
            "endpoint_registered": False,
            "new_disconnected_page_created": False,
        }
    )
    return flags


def _link_index() -> dict[str, dict[str, Any]]:
    linkage = r31_static_linkage.build_static_linkage_map()
    return {str(link.get("tool_id")): link for link in linkage.get("tool_links", [])}


def _group_index() -> dict[str, dict[str, Any]]:
    connector = r30_connector.build_connector_map()
    return {str(group.get("group_id")): group for group in connector.get("tool_groups", [])}


def _tool_group_id(tool_id: str, link_index: dict[str, dict[str, Any]]) -> str:
    return str(link_index.get(tool_id, {}).get("tool_group_id") or "other")


def _frame_level_path(route: dict[str, Any], chosen_level: int) -> list[dict[str, Any]]:
    path = deepcopy(route.get("level_path") or [])
    if not any(item.get("level") == chosen_level for item in path):
        frame = r27_router.FRAME_LEVELS[chosen_level]
        path.append(
            {
                "level": chosen_level,
                "level_key": frame["level_key"],
                "teacher_name": frame["teacher_name"],
                "target_marker": frame["target_marker"],
            }
        )
    return sorted(path, key=lambda item: int(item.get("level") or 0))


def route_static_intent_to_visible_frame(message: str) -> dict[str, Any]:
    text = str(message or "").strip()
    rule = INTENT_RULES.get(text)
    if rule is None:
        rule = {
            "intent": "fallback_current_lesson_question",
            "frame_level": 4,
            "tool_id": "prep_notebook",
            "slot_id": "lesson_body",
            "visible_result": "定位到当前备课正文；保持静态预览，不调用模型。",
            "blocked": False,
            "blocked_reason": "",
        }
    route = r27_router.route_intent_static(text)
    link_index = _link_index()
    group_id = _tool_group_id(rule["tool_id"], link_index)
    link = link_index.get(rule["tool_id"], {})
    action_gate_required = (
        rule["tool_id"] == "teacher_action_gate"
        or rule["blocked"]
        or any(token in text for token in ["保存", "导出", "归档", "写入", "正式"])
    )
    return {
        "input": text,
        "intent": rule["intent"],
        "frame_level": rule["frame_level"],
        "frame_level_key": r27_router.FRAME_LEVELS[rule["frame_level"]]["level_key"],
        "frame_level_path": _frame_level_path(route, rule["frame_level"]),
        "room_id": "prep_room",
        "tool_group_id": group_id,
        "tool_group_label": _group_index().get(group_id, {}).get("label") or group_id,
        "tool_id": rule["tool_id"],
        "tool_label": link.get("tool_label") or rule["tool_id"],
        "slot_id": rule["slot_id"],
        "target_selectors": deepcopy(link.get("target_selectors") or []),
        "action_gate_required": action_gate_required,
        "blocked": rule["blocked"],
        "blocked_reason": rule["blocked_reason"],
        "visible_result": rule["visible_result"],
        "preview_only": True,
        "formal_apply_allowed": False,
        "runtime_call_allowed": False,
        "model_call_allowed": False,
        "source_route": {
            "r27_operation": route.get("operation"),
            "r27_command_type": route.get("command_type"),
            "r27_route_reasons": deepcopy(route.get("route_reasons", [])),
        },
    }


def build_static_intent_visible_frame_map() -> dict[str, Any]:
    routes = [route_static_intent_to_visible_frame(message) for message in FIXTURE_INPUTS]
    return {
        "ok": True,
        "stage": STAGE_ID,
        "intent_visible_id": INTENT_VISIBLE_ID,
        "generated_at": _now(),
        "consumes": {
            "r27_stage": r27_router.STAGE_ID,
            "r30_stage": r30_connector.STAGE_ID,
            "r31_stage": r31_static_linkage.STAGE_ID,
            "r32_stage": r32_derivative_preview.STAGE_ID,
        },
        "fixture_inputs": deepcopy(FIXTURE_INPUTS),
        "visible_routes": routes,
        "interaction_contract": {
            "bottom_input_static_fixture_only": True,
            "submit_shows_xiaojiao_judgement": True,
            "submit_highlights_tool_or_slot": True,
            "save_export_archive_enters_teacher_gate": True,
            "real_generation_allowed": False,
            "runtime_call_allowed": False,
            "model_call_allowed": False,
            "formal_apply_allowed": False,
        },
        "generated_visual_policy": {
            "marked_red_for_review": True,
            "hide_after_review": True,
            "machine_marker": "data-shiwei-generated-visual=true",
        },
        "boundary": boundary_flags(),
        "next_stage_recommendation": {
            "stage": "1013R_R34_TEACHER_VISIBLE_SMOKE",
            "why": "Static intent routes can now point to frame/tool/slot; next prove the teacher can see and understand it.",
        },
    }


def build_static_intent_visible_frame_sample_bundle() -> dict[str, Any]:
    mapping = build_static_intent_visible_frame_map()
    return {
        "ok": True,
        "stage": STAGE_ID,
        "static_intent_visible_frame": mapping,
        "visible_routes": deepcopy(mapping["visible_routes"]),
        "boundary": deepcopy(mapping["boundary"]),
    }
