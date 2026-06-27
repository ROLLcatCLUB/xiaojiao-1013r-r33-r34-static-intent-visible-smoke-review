# 1013R_R33 小教静态意图接四级框架

```text
stage_id=1013R_R33_XIAOJIAO_STATIC_INTENT_TO_VISIBLE_FRAME
status=static_fixture_only
R36_modified=false
runtime_connected=false
runtime_router_connected=false
semantic_runtime_called=false
provider_called=false
model_called=false
database_written=false
memory_written=false
feishu_written=false
formal_apply_performed=false
new_disconnected_page_created=false
```

## 目标

把 R27 的静态意图判断接到 R30/R31/R32 已定义的四级框架、工具区、内容槽和派生物预览上。

这一步不是 runtime，不调用模型，不真实生成课件、大屏、学习单或评价表。页面只显示“小教判断”，并在现有 R21 页面内做红色审核态定位和高亮。

## 静态输入

```text
课件入口找不到
这段教案太乱
帮我生成大屏
评价表怎么没有
我要保存这个课包
```

每条输入必须输出：

```text
intent
frame_level
room_id=prep_room
tool_id
slot_id
action_gate_required
visible_result
preview_only=true
formal_apply_allowed=false
```

## 红色审核生成物规则

R33 页面注入物必须标记：

```text
data-shiwei-generated-visual=true
data-shiwei-hide-after-review=true
data-shiwei-generated-source-stage=1013R_R33_XIAOJIAO_STATIC_INTENT_TO_VISIBLE_FRAME
```

这些节点是为了当前审核临时显性化，未来产品态可以隐藏或收进调试/审核层。
