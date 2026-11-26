#!/usr/bin/env python3
"""한국천문연구원 특일 정보 → 공휴일 목록 holidays.json [[YYYYMMDD, 이름], ...]. DATA_KEY 환경변수(같은 계정 키)."""
import json, sys, time, urllib.request, urllib.parse
sys.path.insert(0, '..'); from keyfix import key
K = key('DATA_KEY'); out = []
for y in sys.argv[1:] or ['2026', '2027']:
    for m in range(1, 13):
        url = f"https://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo?serviceKey={K}&" + urllib.parse.urlencode(dict(solYear=y, solMonth=f"{m:02d}", _type='json', numOfRows=50))
        for a in range(5):
            try:
                with urllib.request.urlopen(url, timeout=60) as r: d = json.loads(r.read().decode()); break
            except Exception as e: err = e; time.sleep(2 + a)
        else: raise err
        it = (d['response']['body'].get('items') or {}); it = it.get('item', []) if isinstance(it, dict) else []
        for x in (it if isinstance(it, list) else [it]):
            if x.get('isHoliday') == 'Y': out.append([str(x['locdate']), x['dateName']])
out = sorted({tuple(x) for x in out}); json.dump(out, open('holidays.json', 'w'), ensure_ascii=False)
print(len(out)); [print(*x) for x in out]
