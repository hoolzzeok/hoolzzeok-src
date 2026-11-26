#!/usr/bin/env python3
"""훌쩍 TourAPI(국문 KorService2) 수집 스크립트 — 표준 라이브러리만 사용.

준비: apis.data.go.kr 접속이 허용된 환경에서
  TOURAPI_KEY=<일반 인증키> python3 tourapi_fetch.py places_spots.json out/
결과: out/spots_matched.json (기존 명소 265곳 매칭), out/spots_nearby.json (명소 없는 곳 주변 관광지),
      out/fetch_log.txt. 인증키는 파일에 저장하지 않는다.
근거: 한국관광공사_개방데이터_활용매뉴얼(국문)_v4.4 — searchKeyword2, locationBasedList2, detailCommon2.
호출 수: 약 265(검색) + 매칭 수(상세) + 78(주변) ≈ 600건 → 개발계정 하루 1,000건 안.
"""
import json, math, os, re, sys, time, urllib.parse, urllib.request

BASE = "https://apis.data.go.kr/B551011/KorService2/"
KEY = os.environ.get("TOURAPI_KEY", "").strip()
if KEY and "%" not in KEY: KEY = urllib.parse.quote(KEY, safe="")   # Decoding 키도 한 번만 인코딩
COMMON = {"MobileOS": "ETC", "MobileApp": "hoolzzeok", "_type": "json"}
MAX_KM = 40          # 도착지 중심에서 이 거리 넘는 검색 결과는 다른 곳으로 봄
SLEEP = 0.15

def call(op, **params):
    q = dict(COMMON, **params)
    url = BASE + op + "?serviceKey=" + KEY + "&" + urllib.parse.urlencode(q)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=20) as r:
                body = r.read().decode("utf-8")
            data = json.loads(body)
            head = data.get("response", {}).get("header", {})
            if head.get("resultCode") != "0000":
                raise RuntimeError(f"{op} {head}")
            items = data["response"]["body"].get("items") or {}
            it = items.get("item", []) if isinstance(items, dict) else []
            return it if isinstance(it, list) else [it]
        except Exception as e:
            err = e
            time.sleep(1 + attempt)
    raise err

def km(a_lat, a_lon, b_lat, b_lon):
    R, t = 6371, math.radians
    h = math.sin(t(b_lat - a_lat) / 2) ** 2 + math.cos(t(a_lat)) * math.cos(t(b_lat)) * math.sin(t(b_lon - a_lon) / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))

def clean(name):
    s = re.sub(r"\(.*?\)", " ", name)          # 괄호 설명 제거
    s = re.split(r"[·,/]", s)[0]               # "A·B"는 앞부분
    return re.sub(r"\s+", " ", s).strip()

def norm(s):
    return re.sub(r"[\s()\[\]·,.\-]", "", s)

def score(item, want, lat, lon):
    t, w = norm(item.get("title", "")), norm(want)
    try:
        d = km(lat, lon, float(item["mapy"]), float(item["mapx"]))
    except Exception:
        return None
    if d > MAX_KM:
        return None
    ct = str(item.get("contenttypeid", ""))
    market = "시장" in want
    if ct in ("15", "25", "32", "39"): return None           # 행사·여행코스·숙박·음식점은 명소가 아님
    if ct == "38" and not market: return None                # 쇼핑은 시장일 때만
    s = 0
    if t == w: s += 100
    elif t.startswith(w) or w.startswith(t): s += 70
    elif w in t or t in w: s += 50
    else: return None
    s -= abs(len(t) - len(w)) * 3                             # 덧붙은 글자가 많을수록 감점 (기념품숍 등)
    if ct in ("12", "14"): s += 10                            # 관광지·문화시설 우선
    return s - d                                              # 비슷하면 가까운 쪽

def detail(cid):
    it = call("detailCommon2", contentId=cid)
    return it[0] if it else {}

def pick_fields(item, det):
    return {
        "contentid": item.get("contentid"), "title": item.get("title"),
        "contenttypeid": item.get("contenttypeid"),
        "addr1": item.get("addr1"), "mapx": item.get("mapx"), "mapy": item.get("mapy"),
        "firstimage": item.get("firstimage") or det.get("firstimage"),
        "cpyrhtDivCd": item.get("cpyrhtDivCd") or det.get("cpyrhtDivCd"),   # Type1=출처표시, Type3=출처표시+변경금지
        "overview": (det.get("overview") or "").strip(),
        "homepage": det.get("homepage"), "tel": det.get("tel"),
        "modifiedtime": item.get("modifiedtime"),
    }

def main(src, out):
    if not KEY:
        sys.exit("TOURAPI_KEY 환경변수가 없어요")
    os.makedirs(out, exist_ok=True)
    places = json.load(open(src, encoding="utf-8"))
    log = open(os.path.join(out, "fetch_log.txt"), "w", encoding="utf-8")
    matched, nearby = [], []
    for p in places:
        for s in p["spots"]:
            want = clean(s)
            try:
                items = call("searchKeyword2", keyword=want, numOfRows=20, pageNo=1, arrange="A")
            except Exception as e:
                log.write(f"ERR search {p['id']} {s}: {e}\n"); continue
            time.sleep(SLEEP)
            cands = [(score(i, want, p["lat"], p["lon"]), i) for i in items]
            cands = [c for c in cands if c[0] is not None]
            if not cands:
                log.write(f"NOMATCH {p['id']} {s} ({len(items)} results)\n")
                matched.append({"place": p["id"], "spot": s, "match": None}); continue
            best = max(cands, key=lambda c: c[0])[1]
            try:
                det = detail(best["contentid"]); time.sleep(SLEEP)
            except Exception as e:
                det = {}; log.write(f"ERR detail {best['contentid']}: {e}\n")
            matched.append({"place": p["id"], "spot": s, "match": pick_fields(best, det)})
            log.write(f"OK {p['id']} {s} -> {best.get('title')}\n")
        if not p["spots"] and p["id"] != "dokdo":
            try:
                items = call("locationBasedList2", mapX=p["lon"], mapY=p["lat"], radius=15000,
                             contentTypeId=12, arrange="S", numOfRows=8, pageNo=1)   # S = 대표 이미지 있는 것, 거리순 (반경 최대 20km)
            except Exception as e:
                log.write(f"ERR near {p['id']}: {e}\n"); continue
            time.sleep(SLEEP)
            nearby.append({"place": p["id"], "items": [pick_fields(i, {}) for i in items]})
            log.write(f"NEAR {p['id']} {len(items)}\n")
        json.dump(matched, open(os.path.join(out, "spots_matched.json"), "w", encoding="utf-8"), ensure_ascii=False)
        json.dump(nearby, open(os.path.join(out, "spots_nearby.json"), "w", encoding="utf-8"), ensure_ascii=False)
    log.close()
    ok = sum(1 for m in matched if m["match"])
    print(f"명소 {len(matched)}곳 중 매칭 {ok}곳, 주변 관광지 받은 곳 {len(nearby)}곳")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "places_spots.json", sys.argv[2] if len(sys.argv) > 2 else "out")
