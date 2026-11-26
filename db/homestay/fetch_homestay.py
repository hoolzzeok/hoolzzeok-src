#!/usr/bin/env python3
"""행정안전부 외국인관광도시민박업 → 영업 중인 곳을 도시·구별로 셈. DATA_KEY 환경변수. 결과 homestay.json"""
import json, sys, time, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, '..'); from keyfix import key
K = key('DATA_KEY'); BASE = "https://apis.data.go.kr/1741000/foreigner_city_homestays/info"
def page(p):
    q = f"serviceKey={K}&pageNo={p}&numOfRows=100&returnType=json"
    for a in range(6):
        try:
            with urllib.request.urlopen(BASE + "?" + q, timeout=120) as r: d = json.loads(r.read().decode())
            it = (d['response']['body'].get('items') or {}).get('item', []); return it if isinstance(it, list) else [it]
        except Exception as e: err = e; time.sleep(3 + a)
    raise err
with ThreadPoolExecutor(8) as ex: rows = [x for ps in ex.map(page, range(1, 158)) for x in ps]
act = [r for r in rows if (r.get('SALS_STTS_NM') or '').startswith('영업')]
from collections import Counter
city = Counter(); gu = Counter()
for r in act:
    a = (r.get('ROAD_NM_ADDR') or r.get('LOTNO_ADDR') or '').split()
    if len(a) >= 2: city[a[0] + ' ' + a[1]] += 1; gu[' '.join(a[:3])] += 1
sido = Counter(); [sido.update({(r.get('ROAD_NM_ADDR') or r.get('LOTNO_ADDR') or '?').split()[0]: 1}) for r in act]
json.dump({'rows': len(rows), 'active': len(act), 'sido': sido, 'city': city, 'updated': max(r.get('DAT_UPDT_PNT') or '' for r in rows)}, open('homestay.json', 'w'), ensure_ascii=False, indent=0)
print(len(rows), len(act)); print(sido.most_common(20))
for k in ['서울특별시', '부산광역시', '경상북도 경주시', '경기도 수원시', '제주특별자치도 제주시', '제주특별자치도 서귀포시', '전북특별자치도 전주시', '강원특별자치도 강릉시']:
    print(k, sum(v for c, v in city.items() if c.startswith(k)))
