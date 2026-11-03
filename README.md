# 财报日历

主要上市公司财报发布日程（北京时间），每个日程附投资者关系页链接。

iPhone 订阅地址：

https://raw.githubusercontent.com/ZiS1234/earnings-calendar/main/earnings.ics

订阅方法：设置 → 日历 → 日历账户 → 添加账户 → 其他 → 添加已订阅的日历，粘贴上面的地址。

## 维护

- `watchlist.json`：关注的公司名单，定时任务只跟踪这里的公司。
- 在 `events.json` 某个日程里加 `"locked": true`，自动更新就不会改动它。

- `events.json`：日程数据（北京时间）。修改后运行 `python3 build.py` 重新生成 `earnings.ics`。
- 每个日程的 `id` 设定后不要改，iPhone 靠它识别同一个日程，改了会出现重复。
