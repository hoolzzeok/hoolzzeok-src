#!/usr/bin/env python3
"""착한가격 밥집 ↔ 행정안전부 일반음식점 인허가(지방행정 인허가 Open API) 짝짓기 → 전화번호.
사용: DATA_KEY=<일반 인증키> python3 rest_phone.py goodprice_eateries.csv out.json [표본수]
- API: https://apis.data.go.kr/1741000/general_restaurants/info  (cond[BPLC_NM::EQ]=가게이름 로 검색)
- 같은 이름 중 도로명 주소의 '도로명 + 건물번호'가 같은 영업 중 업소만 인정
- 응답 TELNO(전화번호)가 빈 곳이 많음 → 실제로 채워진 비율을 함께 기록
- 인증키는 파일에 저장하지 않는다.
"""
import csv, json, os, re, sys, time, urllib.parse, urllib.request

KEY = os.environ.get("DATA_KEY", "").strip()
BASE = "https://apis.data.go.kr/1741000/general_restaurants/info"
calls = 0

def get(name):
    global calls
    q = f"serviceKey={KEY}&pageNo=1&numOfRows=50&returnType=json&" + urllib.parse.urlencode({"cond[BPLC_NM::EQ]": name})
    err = None
    for a in range(3):
        try:
            calls += 1
            with urllib.request.urlopen(BASE + "?" + q, timeout=60) as r:
                d = json.loads(r.read().decode())
            if "response" not in d:
                raise RuntimeError(str(d)[:200])
            it = (d["response"]["body"].get("items") or {}).get("item", [])
            return it if isinstance(it, list) else [it]
        except Exception as e:
            err = e; time.sleep(2 + a)
    raise err

def road_key(addr):
    """'성북구 오패산로19길 46 (하월곡동) 1층' → ('오패산로19길', '46')"""
    m = re.search(r"([가-힣0-9A-Za-z.]+(?:로|길))\s*(\d+(?:-\d+)?)", addr or "")
    return (m.group(1), m.group(2)) if m else None

def main(src, out, n=None):
    if not KEY:
        sys.exit("DATA_KEY 환경변수가 없어요")
    rows = list(csv.DictReader(open(src, encoding="utf-8-sig")))
    if n:
        rows = rows[:: max(1, len(rows) // n)][:n]
    res = json.load(open(out, encoding="utf-8")) if os.path.exists(out) else {}
    stat = {"rows": 0, "matched": 0, "tel": 0}
    for r in rows:
        if r["id"] in res:
            continue
        stat["rows"] += 1
        try:
            items = get(r["name"])
        except Exception as e:
            print("ERR", r["id"], e); continue
        rk = road_key(r["address"])
        hit = None
        for i in items:
            if i.get("SALS_STTS_CD") not in ("01", None) and "영업" not in (i.get("SALS_STTS_NM") or ""):
                continue
            if rk and road_key(i.get("ROAD_NM_ADDR")) == rk:
                hit = i; break
        if hit:
            stat["matched"] += 1
            tel = (hit.get("TELNO") or "").strip()
            if tel: stat["tel"] += 1
            res[r["id"]] = {"tel": tel, "mng": hit.get("MNG_NO"), "x": hit.get("CRD_INFO_X"), "y": hit.get("CRD_INFO_Y")}
        else:
            res[r["id"]] = None
        json.dump(res, open(out, "w", encoding="utf-8"), ensure_ascii=False)
        time.sleep(0.1)
    print(json.dumps(stat, ensure_ascii=False), "호출", calls)

if __name__ == "__main__":
    a = sys.argv[1:]
    main(a[0], a[1], int(a[2]) if len(a) > 2 else None)
