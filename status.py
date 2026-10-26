import json, os, time, urllib.request, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
UA = os.environ.get("FEED_UA") or "CMiraiItemFeed/1.0 (+https://github.com/cmiraitem)"
VIDEO_WORDS = ("video", "youtube", "yt-dlp", "ytdlp", "player", "stream", "avpro")

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return json.loads(urllib.request.urlopen(req, timeout=20).read())

def main():
    os.makedirs(OUT, exist_ok=True)
    now = datetime.datetime.now(datetime.timezone.utc)
    lines = ["CMI-STATUS|1|%s" % now.strftime("%Y-%m-%dT%H:%MZ")]
    alerts = []
    try:
        d = fetch("https://status.vrchat.com/api/v2/summary.json")
        for inc in d.get("incidents", []):
            if inc.get("status") in ("resolved", "postmortem"): continue
            name = inc.get("name", "")
            video = any(w in name.lower() for w in VIDEO_WORDS)
            alerts.append({"id": inc.get("id", ""), "name": name, "video": video, "url": inc.get("shortlink") or "https://status.vrchat.com"})
    except Exception as e:
        print("status page error", e)
    if any(a["video"] for a in alerts):
        lines.append("msg|cinema|2|VRChat 側で動画の不具合が起きています（%s）。直るまで再生できないことがあります。|VRChat is having video playback problems (%s). Videos may not play until it is fixed.|VRChat 쪽에서 영상 재생 장애가 발생했습니다 (%s). 복구될 때까지 재생이 안 될 수 있습니다.|VRChat 方面出现视频播放故障（%s）。修复前可能无法播放。" % tuple([next(a["name"] for a in alerts if a["video"])] * 4))
    elif alerts:
        lines.append("msg|all|1|VRChat 側で障害が起きています（%s）。|VRChat is having an incident (%s).|VRChat 쪽에서 장애가 발생했습니다 (%s).|VRChat 方面发生故障（%s）。" % tuple([alerts[0]["name"]] * 4))
    manual = os.path.join(HERE, "status_manual.txt")
    if os.path.exists(manual):
        for l in open(manual, encoding="utf-8"):
            l = l.strip()
            if l and not l.startswith("#") and (l.startswith("msg|") or l.startswith("flag|")): lines.append(l)
    open(os.path.join(OUT, "status.txt"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    json.dump(alerts, open(os.path.join(OUT, "alerts.json"), "w"), ensure_ascii=False)
    print("\n".join(lines))

if __name__ == "__main__":
    main()
