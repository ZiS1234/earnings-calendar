"""Generate earnings.ics from events.json. Run: python3 build.py"""
import json, hashlib
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
data = json.loads((ROOT / "events.json").read_text(encoding="utf-8"))

def esc(s):
    return s.replace("\\", "\\\\").replace(",", "\\,").replace(";", "\\;").replace("\n", "\\n")

def fold(line):
    b = line.encode("utf-8"); out = []
    while len(b) > 73:
        cut = 73
        while (b[cut] & 0xC0) == 0x80:
            cut -= 1
        out.append(b[:cut]); b = b[cut:]
    out.append(b)
    return "\r\n ".join(x.decode("utf-8") for x in out)

now = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
L = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//earnings-calendar//ZH", "CALSCALE:GREGORIAN",
     "METHOD:PUBLISH", "X-WR-CALNAME:财报日历", "X-WR-TIMEZONE:Asia/Shanghai",
     "REFRESH-INTERVAL;VALUE=DURATION:PT12H", "X-PUBLISHED-TTL:PT12H"]
for e in sorted(data["events"], key=lambda x: x["start"]):
    links = "\n".join(f'{l["name"]}：{l["url"]}' for l in e["links"])
    desc = e["note"] + ("\n\n财报与直播入口：\n" + links if links else "")
    uid = hashlib.md5(e["id"].encode()).hexdigest() + "@earnings-calendar"
    ev = ["BEGIN:VEVENT", f"UID:{uid}", f"DTSTAMP:{now}", f"SUMMARY:{esc(e['title'])}", f"DESCRIPTION:{esc(desc)}"]
    if e["links"]:
        ev.append(f'URL:{e["links"][0]["url"]}')
    if e["minutes"] is None:
        d = datetime.strptime(e["start"], "%Y-%m-%d")
        ev += [f"DTSTART;VALUE=DATE:{d:%Y%m%d}", f"DTEND;VALUE=DATE:{d + timedelta(days=1):%Y%m%d}"]
    else:
        st = datetime.strptime(e["start"], "%Y-%m-%d %H:%M") - timedelta(hours=8)
        ev += [f"DTSTART:{st:%Y%m%dT%H%M%SZ}", f"DTEND:{st + timedelta(minutes=e['minutes']):%Y%m%dT%H%M%SZ}"]
    ev += ["TRANSP:TRANSPARENT", "END:VEVENT"]
    L += [fold(x) for x in ev]
L.append("END:VCALENDAR")
(ROOT / "earnings.ics").write_text("\r\n".join(L) + "\r\n", encoding="utf-8", newline="")
print(f"wrote {len(data['events'])} events")
