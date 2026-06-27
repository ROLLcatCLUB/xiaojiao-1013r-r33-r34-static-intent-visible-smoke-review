# R30：四级框架可见连接器

```text
stage_id=1013R_R30_VISIBLE_FRAME_CONNECTOR
connector_id=SHIWEI_VISIBLE_FRAME_CONNECTOR_R0
current_surface=1013R_R21 page copy
```

R30 把 R25-R29 的协议轻连接到当前 R21 页面副本。它不新开页面，不接 runtime，只定义教师可见的房间、工具和内容槽映射。

## 可见层

```text
1级：平台壳层
2级：备课室
3级：工具区
4级：内容区
```

## 工具分组

```text
备课设计：备课本 / 大单元 / 单课
课堂派生物：课件 / 大屏
依据与评价：资料 / 来源依据
动作门：教师确认门 / 小教推进入口
```

## 页面标记

```text
data-shiwei-room-id
data-shiwei-tool-id
data-shiwei-slot-id
data-shiwei-tool-group-id
```

## 边界

```text
R36_modified=false
main_shell_modified=false
new_disconnected_page_created=false
route_registered=false
endpoint_registered=false
runtime_connected=false
provider_called=false
model_called=false
database_written=false
memory_written=false
feishu_written=false
formal_apply_performed=false
```
