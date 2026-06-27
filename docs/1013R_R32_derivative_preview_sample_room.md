# R32：派生物预览样板

```text
stage_id=1013R_R32_DERIVATIVE_PREVIEW_SAMPLE_ROOM
sample_room_id=SHIWEI_DERIVATIVE_PREVIEW_SAMPLE_ROOM_R0
consumes=1013R_R31_TOOL_CONTENT_STATIC_LINKAGE
```

R32 把课件、大屏、学习单、评价表统一成同一套预览结构，避免每个工具各讲各的。

## 统一字段

```text
source
status
missing
preview
teacher_confirmation
next_suggestion
```

## 当前样板

```text
courseware_script：draft
classroom_display_screen：draft
worksheet：draft
assessment_rubric：blocked when evaluation dimension is missing
```

## 边界

```text
real_export_created=false
runtime_connected=false
provider_called=false
model_called=false
database_written=false
memory_written=false
feishu_written=false
formal_apply_performed=false
```
