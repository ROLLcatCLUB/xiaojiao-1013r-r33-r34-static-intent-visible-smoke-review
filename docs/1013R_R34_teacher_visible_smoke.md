# 1013R_R34 教师可见 Smoke

```text
stage_id=1013R_R34_TEACHER_VISIBLE_SMOKE
status=teacher_visible_smoke_only
R36_modified=false
runtime_connected=false
provider_called=false
model_called=false
database_written=false
memory_written=false
feishu_written=false
formal_apply_performed=false
new_disconnected_page_created=false
```

## 目标

R30-R33 已经把四级框架、工具、内容槽、派生物预览和小教静态意图接入现有 R21 页面。R34 的目标不是继续扩功能，而是补足教师可见证据。

## 必须输出

```text
teacher_walkthrough.md
1013R_R34_dom_smoke.json
1013R_R34_screenshot_smoke.json
1013R_R34_fixture_route_matrix.json
GPT_REVIEW_NOTE_1013R_R34.md
更新后的 R21 HTML
```

## 截图策略

如果本机有 Playwright 和浏览器 CLI，则输出 2K 截图：

```text
默认备课室
点击课件工具后
输入“评价表怎么没有”后
```

如果不可用，必须明确报告原因，并输出 HTML textual smoke。不可假装截图成功。

## 通过条件

```text
页面源码/可渲染脚本中存在当前空间：备课室
存在工具区标签
存在内容区标签
存在小教判断区
存在 preview_only / formal_apply_allowed=false
assessment_rubric 保持 blocked
审核生成物红色标记可检索
```
