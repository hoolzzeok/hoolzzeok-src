#!/usr/bin/env python3
"""관광공사 고캠핑·두루누비·오디(Odii) → 사이트용 작은 상수 3개(CAMP, WALK, ODII)를 site/index.html 에 넣음.

- CAMP: 도착지 중심 20km 안, 운영 중인 캠핑장 가까운 순 3곳 [이름, 종류, 주소(시군구까지), 전화, 예약·홈페이지 주소, km]
- WALK: 코리아둘레길(두루누비) 코스 중 시군 이름이 도착지와 같은 것 최대 3개 [코스명, km, 분, 난이도 1~3, 시작점]
- ODII: 언어별(ko·en·ja·zh·zt) 도착지 중심 10km 안 음성 해설 이야기 가까운 순 3개 [제목, mp3 주소, 초]
  mp3는 관광공사 서버 주소로 링크만 함(파일을 복사해 두지 않음).
사용: python3 db/pull/build_extras.py   (db/pull/*.json 은 Default 환경 세션에서 받은 원본)
"""
import json, math, os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PULL = os.path.join(ROOT, "db", "pull")
SITE = os.path.join(ROOT, "site", "index.html")

def km(a, b, c, d):
    R, t = 6371, math.radians
    h = math.sin(t(c - a) / 2) ** 2 + math.cos(t(a)) * math.cos(t(c)) * math.sin(t(d - b) / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))

def places():
    s = open(SITE, encoding="utf-8").read()
    raw = re.search(r"^const RAW = (\[.*?\]);", s, re.M | re.S)
    return s, raw

def load_places():
    # RAW 행: [id, ko, en, prov, lat, lon, ...] 형식 확인 후 사용
    import subprocess
    js = "const fs=require('fs');const s=fs.readFileSync(process.argv[1],'utf8');" \
         "const i=s.indexOf('const RAW = ');const j=s.indexOf('];',i);const R=eval(s.slice(i+12,j+1));" \
         "console.log(JSON.stringify(R))"
    out = subprocess.check_output(["node", "-e", js, SITE]).decode()
    return json.loads(out)

HEX64 = re.compile(r"[0-9a-fA-F]{64}")
def url_ok(u):
    """예약 주소에 64자리 해시가 들어 있으면 저장소 키 검사(pre-commit)에 걸리므로 링크를 빼고 전화번호만 보여 줌"""
    return "" if HEX64.search(u) else u

def clean(t, n=40):
    t = re.sub(r"<[^>]+>", " ", t or ""); t = re.sub(r"\s+", " ", t).strip()
    return t if len(t) <= n else t[: n - 1] + "…"

def main():
    rows = load_places()
    # RAW 열 위치 찾기: 숫자 두 개(위도 33~39, 경도 124~132)
    P = []
    for r in rows:
        nums = [x for x in r if isinstance(x, (int, float))]
        lat = next((x for x in nums if 32 < x < 40), None); lon = next((x for x in nums if 124 < x < 132), None)
        if lat and lon: P.append({"id": r[0], "ko": r[1], "lat": lat, "lon": lon})
    camp = {}
    G = [g for g in json.load(open(os.path.join(PULL, "gocamping.json"), encoding="utf-8"))["items"] if g.get("manageSttus") == "운영" and g.get("mapX") and g.get("mapY")]
    for p in P:
        near = []
        for g in G:
            d = km(p["lat"], p["lon"], float(g["mapY"]), float(g["mapX"]))
            if d <= 20: near.append((d, g))
        # 전화나 예약·홈페이지 주소가 있는 곳만 (연락할 길이 없는 곳은 뺌), 가까운 순
        near = [x for x in near if (x[1].get("tel") or x[1].get("resveUrl") or x[1].get("homepage"))]
        near.sort(key=lambda x: x[0])
        if near:
            camp[p["id"]] = [[clean(g["facltNm"], 30), clean((g.get("induty") or "").replace(",", "·"), 24),
                              " ".join((g.get("addr1") or "").split()[:2]), g.get("tel") or "",
                              url_ok((g.get("resveUrl") or g.get("homepage") or "").strip()), round(d, 1)] for d, g in near[:3]]
    walk = {}
    W = json.load(open(os.path.join(PULL, "durunubi.json"), encoding="utf-8"))["items"]
    for p in P:
        base = re.sub(r"\(.*\)", "", p["ko"]).strip()
        hit = []
        for w in W:
            sg = (w.get("sigun") or "").split()
            names = [re.sub(r"(특별자치시|특별자치도|광역시|특별시|시|군|구)$", "", x) for x in sg]
            if base in names:
                m = re.search(r"시점\s*:\s*([^<(\n]+)", w.get("travelerinfo") or "")
                hit.append([w["crsKorNm"], float(w.get("crsDstnc") or 0), int(w.get("crsTotlRqrmHour") or 0), int(w.get("crsLevel") or 0), clean(m.group(1) if m else "", 24)])
        if hit: walk[p["id"]] = hit[:3]
    odii = {}
    O = json.load(open(os.path.join(PULL, "odii.json"), encoding="utf-8"))["langs"]
    for key, lg in (("ko", "ko"), ("en", "en"), ("ja", "ja"), ("zh_cn", "zh"), ("zh_tw", "zt")):
        st = [x for x in O[key]["stories"] if x.get("audioUrl", "").startswith("https://") and x.get("mapX") and x.get("mapY")]
        # 한 관광지(theme)에 이야기가 여러 개 → 관광지마다 첫 이야기 하나만, 제목은 관광지 이름
        tt = {t["tid"]: clean(t.get("title"), 40) for t in O[key]["themes"]}
        first = {}
        for x in st:
            k = x["tid"]
            if k not in first or int(x.get("stid") or 0) < int(first[k].get("stid") or 0): first[k] = x
        st = [dict(x, title=tt.get(x["tid"]) or x.get("title")) for x in first.values()]
        m = {}
        for p in P:
            near = []
            for x in st:
                try: d = km(p["lat"], p["lon"], float(x["mapY"]), float(x["mapX"]))
                except ValueError: continue
                if d <= 10: near.append((d, x))
            near.sort(key=lambda z: z[0]); seen, pick = set(), []
            for d, x in near:
                t = clean(x.get("title"), 40)
                if t in seen: continue
                seen.add(t); pick.append([t, x["audioUrl"], int(x.get("playTime") or 0)])
                if len(pick) >= 3: break
            if pick: m[p["id"]] = pick
        odii[lg] = m
    s = open(SITE, encoding="utf-8").read()
    for name, obj in (("CAMP", camp), ("WALK", walk), ("ODII", odii)):
        line = f"const {name} = " + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + ";"
        if re.search(rf"^const {name} = .*$", s, re.M): s = re.sub(rf"^const {name} = .*$", lambda _: line, s, count=1, flags=re.M)
        else:
            mm = re.search(r"^const HUB78 = .*$", s, re.M); s = s[: mm.end()] + "\n" + line + s[mm.end():]
    open(SITE, "w", encoding="utf-8").write(s)
    print(f"캠핑 {len(camp)}곳 / 걷기 {len(walk)}곳 / 음성해설 " + ", ".join(f"{k} {len(v)}" for k, v in odii.items()))
    print("크기(KB):", {n: round(len(json.dumps(o, ensure_ascii=False)) / 1024) for n, o in (("CAMP", camp), ("WALK", walk), ("ODII", odii))})

if __name__ == "__main__":
    main()
