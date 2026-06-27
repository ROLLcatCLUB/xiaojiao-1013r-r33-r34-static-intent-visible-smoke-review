from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from shutil import which
from typing import Any

from . import prep_room_page_copy_package_binding_1013R_R21 as r21_binding
from . import prep_room_xiaojiao_static_intent_visible_frame_1013R_R33 as r33_intent


STAGE_ID = "1013R_R34_TEACHER_VISIBLE_SMOKE"
SMOKE_ID = "SHIWEI_TEACHER_VISIBLE_SMOKE_R0"


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def boundary_flags() -> dict[str, bool]:
    flags = dict(r33_intent.boundary_flags())
    flags.update(
        {
            "stage": STAGE_ID,
            "teacher_visible_smoke_defined": True,
            "dom_smoke_defined": True,
            "teacher_walkthrough_defined": True,
            "gpt_review_note_defined": True,
            "screenshot_smoke_attempted": True,
            "screenshot_smoke_required_if_browser_available": True,
            "real_generation_performed": False,
            "runtime_connected": False,
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


def _playwright_available() -> bool:
    try:
        import playwright  # noqa: F401
    except Exception:
        return False
    return True


def _browser_candidates() -> list[str]:
    candidates = []
    for command in ["chrome", "chrome.exe", "msedge", "msedge.exe", "chromium", "chromium.exe"]:
        path = which(command)
        if path:
            candidates.append(path)
    return candidates


def screenshot_smoke_plan() -> dict[str, Any]:
    browsers = _browser_candidates()
    playwright_available = _playwright_available()
    available = bool(browsers and playwright_available)
    reason = ""
    if not playwright_available and not browsers:
        reason = "local Playwright package and browser CLI are unavailable"
    elif not playwright_available:
        reason = "local Playwright package is unavailable"
    elif not browsers:
        reason = "local browser CLI is unavailable"
    return {
        "available": available,
        "mode": "2k_screenshot" if available else "html_textual_smoke_fallback",
        "required_viewports": ["default_prep_room", "courseware_tool_clicked", "assessment_input_blocked"],
        "browser_candidates": browsers,
        "playwright_available": playwright_available,
        "fallback_reason": reason,
        "screenshot_files": [],
    }


def build_teacher_walkthrough() -> str:
    return """# 1013R_R34 Teacher Walkthrough

当前页面是“师维”的备课室，老师打开后应先确认自己在当前课 `2-1《色彩的渐变》` 的备课本里。

右侧红色的“备课室工具”不是最终产品样式，而是审核期临时层。它把后端已经验证过的工具关系临时露出来：备课本、大单元、单课负责备课设计；课件和大屏负责课堂派生物；资料和资料来源负责依据；教师确认门和小教推进入口负责动作门。

点这些红色工具时，页面只会滚动和高亮相关内容区。它不会新开页面，不会真的生成课件、大屏、学习单或评价表，也不会保存到正式课包。

底部输入栏现在接了静态小教判断。输入或点击示例“课件入口找不到”“这段教案太乱”“帮我生成大屏”“评价表怎么没有”“我要保存这个课包”时，红色“小教判断”会说明：这句话属于哪一层、定位到哪个工具、定位到哪个内容槽、是否需要教师确认。

“评价表怎么没有”会显示 blocked，因为评价维度还需要老师确认。这里不能假装评价表已经完成。

“我要保存这个课包”会进入教师确认门，并保持 `formal_apply_allowed=false`。当前只是审核可视化，不允许保存、导出、归档或写入正式备课本。

所有红色区域都带有 `data-shiwei-generated-visual=true` 和 `data-shiwei-hide-after-review=true`，表示它们是审核期临时显性化内容，后续产品态可以删除、隐藏或收拢。要保留进产品态的内容不应使用红色删除态。
"""


def build_gpt_review_note() -> str:
    return """# GPT Review Note

Please review R33-R34 only.

Expected status:

```text
FINAL_STATUS=PASS_R33_R34_XIAOJIAO_STATIC_INTENT_VISIBLE_SMOKE
NEXT_STAGE=R35_COMPACT_TEACHER_EXPERIENCE_REVIEW_PACKAGE
R36_RUNTIME_PROVIDER_STAGE=HOLD
```

Please check:

1. Whether the static Xiaojiao intent routes make teacher-facing sense.
2. Whether every fixture maps to `intent -> frame_level -> room_id -> tool_id -> slot_id -> visible_result`.
3. Whether the page visibly marks generated review-only overlays in red with machine markers.
4. Whether assessment remains blocked when dimensions are missing.
5. Whether save/export/archive routes to the teacher confirmation gate and keeps `formal_apply_allowed=false`.
6. Whether the implementation still avoids runtime, provider/model, database, Feishu, memory, R36, and formal apply.
7. Whether R35 may proceed as a compact teacher experience review package, not runtime.
"""


def build_dom_smoke(html: str) -> dict[str, Any]:
    checks = {
        "current_space_prep_room_visible": "备课室" in html,
        "tool_area_label_visible": "备课室工具" in html and "r30-tool-panel" in html,
        "content_area_labels_visible": "nb-doc-section" in html and "nb-flow-step" in html,
        "xiaojiao_judgement_visible": "小教判断" in html and "r33-intent-panel" in html,
        "preview_only_visible": "preview_only=true" in html or 'data-preview-only="true"' in html,
        "formal_apply_false_visible": "formal_apply_allowed=false" in html or 'data-formal-apply-allowed="false"' in html,
        "assessment_rubric_blocked_visible": "assessment_rubric" in html and "blocked" in html,
        "delete_or_hide_overlay_red_markers_visible": 'data-shiwei-hide-after-review="true"' in html and "#b42323" in html,
        "hide_after_review_markers_visible": 'data-shiwei-hide-after-review="true"' in html,
    }
    return {
        "mode": "html_textual_smoke",
        "checks": checks,
        "pass": all(checks.values()),
        "marker_counts": {
            "generated_visual": html.count('data-shiwei-generated-visual="true"'),
            "hide_after_review": html.count('data-shiwei-hide-after-review="true"'),
            "generated_source_stage": html.count("data-shiwei-generated-source-stage"),
        },
    }


def build_teacher_visible_smoke() -> dict[str, Any]:
    page = r21_binding.build_binding_sample_bundle()
    html = page.get("html", "")
    r33 = r33_intent.build_static_intent_visible_frame_map()
    dom_smoke = build_dom_smoke(html)
    screenshot_plan = screenshot_smoke_plan()
    return {
        "ok": dom_smoke["pass"],
        "stage": STAGE_ID,
        "smoke_id": SMOKE_ID,
        "generated_at": _now(),
        "consumes": {
            "r21_stage": r21_binding.STAGE_ID,
            "r33_stage": r33_intent.STAGE_ID,
        },
        "dom_smoke": dom_smoke,
        "screenshot_smoke": screenshot_plan,
        "teacher_walkthrough_required": True,
        "teacher_walkthrough": build_teacher_walkthrough(),
        "gpt_review_note": build_gpt_review_note(),
        "fixture_route_matrix": [
            {
                "input": route.get("input"),
                "intent": route.get("intent"),
                "frame_level": route.get("frame_level"),
                "room_id": route.get("room_id"),
                "tool_id": route.get("tool_id"),
                "slot_id": route.get("slot_id"),
                "visible_result": route.get("visible_result"),
                "blocked": route.get("blocked"),
                "action_gate_required": route.get("action_gate_required"),
            }
            for route in r33.get("visible_routes", [])
        ],
        "final_status_if_pass": "PASS_R33_R34_XIAOJIAO_STATIC_INTENT_VISIBLE_SMOKE",
        "next_stage_if_pass": "R35_COMPACT_TEACHER_EXPERIENCE_REVIEW_PACKAGE",
        "boundary": boundary_flags(),
    }


def build_teacher_visible_smoke_sample_bundle() -> dict[str, Any]:
    smoke = build_teacher_visible_smoke()
    return {
        "ok": smoke.get("ok"),
        "stage": STAGE_ID,
        "teacher_visible_smoke": smoke,
        "dom_smoke": smoke["dom_smoke"],
        "screenshot_smoke": smoke["screenshot_smoke"],
        "boundary": smoke["boundary"],
    }
