"""고캠핑·두루누비·오디 전체 목록 → db/pull/{gocamping,durunubi,odii}.json"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(__file__))
from _api import call, items, total, header
B = "https://apis.data.go.kr/B551011"
HERE = os.path.dirname(__file__)
ROWS = 1000

def pull_all(svc, op, **kw):
    out, page, tot = [], 1, None
    while True:
        for _ in range(4):  # 일시 오류·빈 페이지면 다시
            r = call(f"{B}/{svc}", op, numOfRows=ROWS, pageNo=page, **kw)
            if items(r) or (total(r) is not None and len(out) >= total(r)): break
            time.sleep(3)
        if tot is None:
            tot = total(r)
            if tot is None: return None, header(r)
        got = items(r)
        out += got
        if not got or len(out) >= tot: break
        page += 1
    return out, tot

def save(name, data):
    json.dump(data, open(os.path.join(HERE, name), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

def main(which):
    if "gocamping" in which:
        it, t = pull_all("GoCamping", "basedList")
        save("gocamping.json", {"source": "GoCamping basedList", "total": t, "items": it or []})
        print("gocamping", len(it or []), t)
    if "durunubi" in which:
        it, t = pull_all("Durunubi", "courseList")
        save("durunubi.json", {"source": "Durunubi courseList", "total": t, "items": it or []})
        print("durunubi", len(it or []), t)
    if "odii" in which:
        res = {"source": "Odii themeBasedList / storyBasedList", "langs": {}}
        for lg, code in (("ko", "ko"), ("en", "en"), ("ja", "jp"), ("zh_cn", "cn1"), ("zh_tw", "cn2")):
            th, tt = pull_all("Odii", "themeBasedList", langCode=code)
            st, ts = pull_all("Odii", "storyBasedList", langCode=code)
            res["langs"][lg] = {"langCode": code, "theme_total": tt, "themes": th or [], "story_total": ts, "stories": st or []}
            print("odii", lg, len(th or []), tt, len(st or []), ts, flush=True)
        save("odii.json", res)

if __name__ == "__main__":
    main(sys.argv[1:] or ["gocamping", "durunubi", "odii"])
