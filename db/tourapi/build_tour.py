#!/usr/bin/env python3
"""TourAPI 수집 결과 → 사이트용 JS 상수(TOUR, TOUR_NEAR) + 썸네일(공공누리 1유형만, 축소 JPEG data URI).
사용: python3 build_tour.py out/ tour.js
- 1유형(Type1, 출처표시): 축소·압축 허용 → 220px 폭 JPEG
- 3유형(Type3, 변경금지): 사진을 바꾸지 않기 위해 넣지 않음(카카오맵 '사진·지도 보기'로 대신)
- 소개 글: HTML 태그 제거 후 첫 문장(최대 110자)
"""
import base64, html, io, json, os, re, sys, urllib.request
from PIL import Image

src, dst = sys.argv[1], sys.argv[2]
CACHE = os.path.join(src, "img"); os.makedirs(CACHE, exist_ok=True)

def first_sentence(t, n=110):
    t = html.unescape(re.sub(r"<[^>]+>", " ", t or "")); t = re.sub(r"\s+", " ", t).strip()
    m = re.match(r"(.+?[다요]\.)(\s|$)", t)
    s = m.group(1) if m else t
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"

def thumb(url, cid):
    if not url: return ""
    url = url.replace("http://", "https://", 1)
    p = os.path.join(CACHE, f"{cid}.jpg")
    if not os.path.exists(p):
        try:
            with urllib.request.urlopen(url, timeout=20) as r: raw = r.read()
            im = Image.open(io.BytesIO(raw)).convert("RGB")
            w = 220; h = round(im.height * w / im.width)
            im = im.resize((w, h), Image.LANCZOS)
            im.save(p, "JPEG", quality=62, optimize=True, progressive=True)
        except Exception as e:
            print("img fail", cid, e); return ""
    return "data:image/jpeg;base64," + base64.b64encode(open(p, "rb").read()).decode()

def row(m, with_img=True):
    t1 = m.get("cpyrhtDivCd") == "Type1"
    img = "" if not with_img else thumb(m.get("firstimage2") or m.get("firstimage"), m["contentid"]) if t1 else ""
    return [m["contentid"], m["title"], first_sentence(m.get("overview")), img, "1" if t1 else ("3" if m.get("cpyrhtDivCd") == "Type3" else ""),
            round(float(m["mapx"]), 5) if m.get("mapx") else None, round(float(m["mapy"]), 5) if m.get("mapy") else None]

matched = json.load(open(os.path.join(src, "spots_matched.json"), encoding="utf-8"))
nearby = json.load(open(os.path.join(src, "spots_nearby.json"), encoding="utf-8"))
TOUR = {}
for x in matched:
    if x["match"]: TOUR.setdefault(x["place"], {})[x["spot"]] = row(x["match"])
NEAR = {}
for x in nearby:
    NEAR[x["place"]] = [row(i, False) for i in x["items"][:4]]   # 주변 목록은 이름만(용량 절약)
js = ("/* 한국관광공사 TourAPI(국문 관광정보 서비스) 2026-11-13 수집. [콘텐츠ID, 공식 이름, 소개 첫 문장, 썸네일(1유형만), 공공누리 유형, 경도, 위도]\n"
      "   사진 출처: 한국관광공사. 1유형만 축소해 넣음(3유형은 변경금지라 넣지 않음) */\n"
      f"const TOUR = {json.dumps(TOUR, ensure_ascii=False, separators=(',', ':'))};\n"
      f"const TOUR_NEAR = {json.dumps(NEAR, ensure_ascii=False, separators=(',', ':'))};\n")
open(dst, "w", encoding="utf-8").write(js)
n_img = sum(1 for p in TOUR.values() for r in p.values() if r[3]) + sum(1 for p in NEAR.values() for r in p if r[3])
print(f"TOUR {sum(len(v) for v in TOUR.values())}개, NEAR {len(NEAR)}곳, 썸네일 {n_img}장, JS {len(js.encode())/1024:.0f}KB")
