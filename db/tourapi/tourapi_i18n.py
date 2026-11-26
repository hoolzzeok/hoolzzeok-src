#!/usr/bin/env python3
"""훌쩍 TourAPI 다국어(영·일·중간체) 수집 — 표준 라이브러리만 사용.

사용: TOURAPI_KEY=<일반 인증키> python3 tourapi_i18n.py <index.html> <out_dir> [en ja zh]
- 사이트에 이미 들어 있는 국문 TOUR(명소 199곳: 이름·좌표)를 기준으로
  각 언어 서비스에서 같은 장소를 찾아 [외국어 이름, 소개 첫 문장]을 받는다.
- 다국어 서비스는 콘텐츠ID가 국문과 달라서 이름·좌표로 짝을 찾는다.
  1) searchKeyword2(키워드=국문 이름) → 국문 좌표에서 3km 안, 가장 가까운 것
     (다국어 제목에 "HiKR Ground (하이커 그라운드)"처럼 한글이 같이 들어 있는 경우가 많음)
  2) 못 찾으면 locationBasedList2(반경 500m, 거리순) → 300m 안이고 제목 괄호 속 한글이 국문 이름과 맞을 때만
- 근거: 한국관광공사_개방데이터_활용매뉴얼(영문·일문·중문간체)_v4.4
  서비스 URL https://apis.data.go.kr/B551011/{EngService2|JpnService2|ChsService2}
  관광타입: 75 레포츠, 76 관광지, 77 교통, 78 문화시설, 79 쇼핑, 80 숙박, 82 음식점, 85 축제
- 호출 수: 언어마다 검색 약 200 + 상세 약 200 + 위치 보조 일부 ≈ 450건 (개발계정 서비스별 하루 1,000건 안)
- 인증키는 파일에 저장하지 않는다.
"""
import json, math, os, re, sys, time, urllib.parse, urllib.request, html

SVC = {"en": "EngService2", "ja": "JpnService2", "zh": "ChsService2"}
KEY = os.environ.get("TOURAPI_KEY", "").strip()
if KEY and "%" not in KEY: KEY = urllib.parse.quote(KEY, safe="")   # Decoding 키도 한 번만 인코딩
COMMON = {"MobileOS": "ETC", "MobileApp": "hoolzzeok", "_type": "json"}
SKIP_TYPES = {"77", "80", "82"}          # 교통·숙박·음식점은 명소 짝으로 쓰지 않음
SLEEP = 0.15

def call(svc, op, **params):
    q = dict(COMMON, **params)
    url = f"https://apis.data.go.kr/B551011/{svc}/{op}?serviceKey={KEY}&" + urllib.parse.urlencode(q)
    err = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=20) as r:
                data = json.loads(r.read().decode("utf-8"))
            head = data.get("response", {}).get("header", {})
            if head.get("resultCode") != "0000":
                raise RuntimeError(f"{op} {head}")
            items = data["response"]["body"].get("items") or {}
            it = items.get("item", []) if isinstance(items, dict) else []
            return it if isinstance(it, list) else [it]
        except Exception as e:
            err = e; time.sleep(1 + attempt)
    raise err

def km(a_lat, a_lon, b_lat, b_lon):
    R, t = 6371, math.radians
    h = math.sin(t(b_lat - a_lat) / 2) ** 2 + math.cos(t(a_lat)) * math.cos(t(b_lat)) * math.sin(t(b_lon - a_lon) / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))

def norm(s):
    return re.sub(r"[\s()\[\]·,.\-]", "", s or "")

def clean(name):
    s = re.sub(r"\(.*?\)", " ", name)
    s = re.split(r"[·,/]", s)[0]
    return re.sub(r"\s+", " ", s).strip()

def hangul_in(title):
    """다국어 제목 속 한글 부분(괄호 안 등)."""
    return "".join(re.findall(r"[가-힣0-9]+", title or ""))

def first_sentence(t, lang, n=140):
    t = html.unescape(re.sub(r"<[^>]+>", " ", t or "")); t = re.sub(r"\s+", " ", t).strip()
    if lang == "en":
        m = re.match(r"(.+?[.!?])(\s|$)", t)
    else:
        m = re.match(r"(.+?[。！？])", t)
    s = m.group(1) if m else t
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"

def load_tour(index_html):
    s = open(index_html, encoding="utf-8").read()
    m = re.search(r"^const TOUR = (\{.*?\});\s*$", s, re.M)
    if not m:
        sys.exit("index.html에서 const TOUR 줄을 못 찾음")
    return json.loads(m.group(1))

def pick(items, ko, lat, lon, max_km, need_name):
    best = None
    shop_ok = bool(re.search(r"시장|거리|골목|아울렛|몰", ko))
    for i in items:
        ct = i.get("contenttypeid")
        if ct in SKIP_TYPES or (ct == "79" and not shop_ok) or "免税" in (i.get("title") or "") or "Tax Refund" in (i.get("title") or ""):
            continue
        try:
            d = km(lat, lon, float(i["mapy"]), float(i["mapx"]))
        except Exception:
            continue
        if d > max_km:
            continue
        h, w = hangul_in(i.get("title")), norm(clean(ko))
        if not h:
            nm = 0
        elif h == w:
            nm = 100
        elif h.startswith(w) or w.startswith(h):
            nm = 70
        elif len(w) >= 3 and (w in h or h in w):
            nm = 50
        else:
            nm = 0
        name_ok = nm > 0
        if need_name and not name_ok:
            continue
        if not need_name and not name_ok and d > 0.3:
            continue          # 이름이 안 맞으면 300m 안일 때만
        score = nm - d
        if best is None or score > best[0]:
            best = (score, i, d, name_ok)
    return best

def main(index_html, out, langs):
    if not KEY:
        sys.exit("TOURAPI_KEY 환경변수가 없어요")
    os.makedirs(out, exist_ok=True)
    tour = load_tour(index_html)
    spots = [(p, k, r) for p, d in tour.items() for k, r in d.items() if r[5] and r[6]]
    print(f"국문 명소 {len(spots)}곳")
    for lang in langs:
        svc = SVC[lang]; res = {}; log = open(os.path.join(out, f"i18n_{lang}_log.txt"), "w", encoding="utf-8")
        ok = 0; calls = 0
        for p, k, r in spots:
            ko, lon, lat = r[1], float(r[5]), float(r[6])
            best = None
            try:
                items = call(svc, "searchKeyword2", keyword=clean(ko), numOfRows=50, pageNo=1, arrange="A"); calls += 1
                best = pick(items, ko, lat, lon, 3.0, False)
            except Exception as e:
                log.write(f"ERR search {p} {k}: {e}\n")
            time.sleep(SLEEP)
            if not best:
                try:
                    items = call(svc, "locationBasedList2", mapX=lon, mapY=lat, radius=500, arrange="E", numOfRows=20, pageNo=1); calls += 1
                    best = pick(items, ko, lat, lon, 0.3, True)
                except Exception as e:
                    log.write(f"ERR near {p} {k}: {e}\n")
                time.sleep(SLEEP)
            if not best:
                log.write(f"NOMATCH {p} {k}\n"); continue
            _, it, d, name_ok = best
            intro = ""
            try:
                det = call(svc, "detailCommon2", contentId=it["contentid"]); calls += 1
                intro = first_sentence((det[0] if det else {}).get("overview"), lang)
            except Exception as e:
                log.write(f"ERR detail {it['contentid']}: {e}\n")
            time.sleep(SLEEP)
            title = re.sub(r"\s*[(（][^)）]*[가-힣][^)）]*[)）]\s*", " ", it.get("title", "")).strip()   # 괄호 속 한글은 뺌
            res.setdefault(p, {})[k] = [title, intro, it["contentid"], round(d, 2), "name" if name_ok else "near"]
            ok += 1
            log.write(f"OK {p} {k} -> {it.get('title')} ({d:.2f}km, {'name' if name_ok else 'near'})\n")
        json.dump(res, open(os.path.join(out, f"i18n_{lang}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
        log.close()
        print(f"{lang}: {ok}/{len(spots)}곳 매칭, 호출 {calls}건")

if __name__ == "__main__":
    a = sys.argv[1:]
    main(a[0] if a else "index.html", a[1] if len(a) > 1 else "out_i18n", a[2:] or ["en", "ja", "zh"])
