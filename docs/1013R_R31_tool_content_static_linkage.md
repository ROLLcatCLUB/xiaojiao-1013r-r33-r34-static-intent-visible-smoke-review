# R31：工具区与内容区静态联动

```text
stage_id=1013R_R31_TOOL_CONTENT_STATIC_LINKAGE
linkage_id=SHIWEI_TOOL_CONTENT_STATIC_LINKAGE_R0
consumes=1013R_R30_VISIBLE_FRAME_CONNECTOR
```

R31 只做页面内定位和高亮：点击右侧工具，滚动到对应内容槽，并标记当前仍是 `preview_only=true`。

## 映射

```text
课件 -> courseware_script / classroom_display_screen
大屏 -> classroom_display_screen
资料 -> materials_list / source_evidence
评价 -> assessment_rubric
确认门 -> confirm_actions
编辑 -> 修改前 / 修改后 / 小教建议
```

## 不做

```text
real_generation_performed=false
new_page_navigation_allowed=false
save_export_archive_allowed=false
formal_apply_allowed=false
```

## 边界

```text
runtime_connected=false
provider_called=false
model_called=false
database_written=false
memory_written=false
feishu_written=false
formal_apply_performed=false
```
