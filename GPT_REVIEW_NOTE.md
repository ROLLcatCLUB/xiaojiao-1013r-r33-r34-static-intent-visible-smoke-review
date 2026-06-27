# GPT Review Note

Please review this compact R33-R34 package, not the full `xiaobei-core` repository.

Expected status:

```text
FINAL_STATUS=PASS_R33_R34_XIAOJIAO_STATIC_INTENT_VISIBLE_SMOKE
NEXT_STAGE=R35_COMPACT_TEACHER_EXPERIENCE_REVIEW_PACKAGE
R36_RUNTIME_PROVIDER_STAGE=HOLD
```

Focus:

1. Does the teacher-visible Xiaojiao judgement make sense for the five static inputs?
2. Does every input map to `intent -> frame_level -> room_id -> tool_id -> slot_id -> visible_result`?
3. Are delete/hide-after-review overlays visibly red and machine-searchable, while retained product content keeps normal color?
4. Does assessment remain blocked until dimensions are confirmed?
5. Does save/export/archive stay behind the teacher confirmation gate with `formal_apply_allowed=false`?
6. Does the package still avoid runtime/provider/model/database/Feishu/memory/R36/formal apply?
