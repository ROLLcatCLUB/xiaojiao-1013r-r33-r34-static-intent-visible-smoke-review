from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from typing import Any

from . import prep_room_tool_content_static_linkage_1013R_R31 as r31_linkage
from . import prep_room_unified_package_readonly_export_1013R_R20 as r20_package


STAGE_ID = "1013R_R32_DERIVATIVE_PREVIEW_SAMPLE_ROOM"
SAMPLE_ROOM_ID = "SHIWEI_DERIVATIVE_PREVIEW_SAMPLE_ROOM_R0"


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def boundary_flags() -> dict[str, bool]:
    flags = dict(r31_linkage.boundary_flags())
    flags.update(
        {
            "stage": STAGE_ID,
            "derivative_preview_sample_room_defined": True,
            "courseware_preview_sample_defined": True,
            "display_preview_sample_defined": True,
            "worksheet_preview_sample_defined": True,
            "assessment_preview_blocked_if_dimension_missing": True,
            "real_export_created": False,
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


def _first_courseware_screen(package: dict[str, Any]) -> dict[str, Any]:
    screens = package.get("lesson_viewmodel", {}).get("courseware_screens", [])
    return deepcopy(screens[0]) if screens else {}


def _first_process_link(package: dict[str, Any]) -> dict[str, Any]:
    links = package.get("derivative_linkage", {}).get("process_derivative_links", [])
    return deepcopy(links[0]) if links else {}


def build_derivative_preview_samples(package: dict[str, Any] | None = None) -> dict[str, Any]:
    if package is None:
        package = r20_package.build_unified_package()
    linkage = r31_linkage.build_static_linkage_map()
    screen = _first_courseware_screen(package)
    process_link = _first_process_link(package)
    missing = package.get("task_state", {}).get("missing_materials", [])
    assessment_missing_dimension = any(
        "评价" in str(item.get("label") or item.get("id") or "") or "维度" in str(item.get("label") or item.get("id") or "")
        for item in missing
    )
    samples = [
        {
            "derivative_id": "courseware_script",
            "label": "课件预览",
            "source_slot_id": "courseware_script",
            "source": "lesson_viewmodel.courseware_screens",
            "status": "draft",
            "missing": [],
            "preview": {
                "title": screen.get("title") or "渐变观察导入",
                "summary": screen.get("role") or "把教学过程转成课堂屏幕提示。",
            },
            "teacher_confirmation": {
                "preview_only": True,
                "formal_apply_allowed": False,
            },
            "next_suggestion": "先检查屏幕与教学环节是否对应，再决定是否继续精修。",
        },
        {
            "derivative_id": "classroom_display_screen",
            "label": "大屏预览",
            "source_slot_id": "classroom_display_screen",
            "source": "render_block_linkage_index.classroom_display_screen",
            "status": "draft",
            "missing": [],
            "preview": {
                "title": "课堂大屏短句",
                "summary": process_link.get("classroom_display", {}).get("student_visible_prompt")
                or "让学生看到本环节要观察和表达的重点。",
            },
            "teacher_confirmation": {
                "preview_only": True,
                "formal_apply_allowed": False,
            },
            "next_suggestion": "大屏文字保持短句，确认前不导出到课堂展示。",
        },
        {
            "derivative_id": "worksheet",
            "label": "学习单预览",
            "source_slot_id": "worksheet",
            "source": "render_block_linkage_index.worksheet",
            "status": "draft",
            "missing": ["学生记录版式待确认"],
            "preview": {
                "title": "试色记录",
                "summary": process_link.get("worksheet", {}).get("capture_prompt")
                or "记录 3 到 5 格渐变试色过程。",
            },
            "teacher_confirmation": {
                "preview_only": True,
                "formal_apply_allowed": False,
            },
            "next_suggestion": "先确认学生记录方式，再决定是否生成完整学习单。",
        },
        {
            "derivative_id": "assessment_rubric",
            "label": "评价表预览",
            "source_slot_id": "assessment_rubric",
            "source": "task_state.missing_materials + render_block_linkage_index.assessment_rubric",
            "status": "blocked" if assessment_missing_dimension else "draft",
            "missing": ["评价维度需教师确认"] if assessment_missing_dimension else [],
            "preview": {
                "title": "评价维度",
                "summary": "评价表必须等教师确认维度后才能进入预览。",
            },
            "teacher_confirmation": {
                "preview_only": True,
                "formal_apply_allowed": False,
            },
            "next_suggestion": "先补齐评价维度；不能假装评价表已经生成。",
        },
    ]
    return {
        "ok": True,
        "stage": STAGE_ID,
        "sample_room_id": SAMPLE_ROOM_ID,
        "generated_at": _now(),
        "consumes": {
            "r31_stage": linkage.get("stage"),
            "r20_stage": package.get("stage"),
        },
        "samples": samples,
        "uniform_preview_fields": [
            "source",
            "status",
            "missing",
            "preview",
            "teacher_confirmation",
            "next_suggestion",
        ],
        "boundary": boundary_flags(),
        "next_stage_recommendation": {
            "stage": "1013R_R33_XIAOJIAO_STATIC_INTENT_TO_VISIBLE_FRAME",
            "why": "Derivative previews are now normalized; next may connect bottom input to static intent routing after review.",
        },
    }


def build_derivative_preview_sample_bundle() -> dict[str, Any]:
    sample_room = build_derivative_preview_samples()
    return {
        "ok": True,
        "stage": STAGE_ID,
        "derivative_preview_sample_room": sample_room,
        "samples": deepcopy(sample_room["samples"]),
        "boundary": deepcopy(sample_room["boundary"]),
    }
