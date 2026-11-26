#!/usr/bin/env python3
"""TAGO 열차정보 → 딸깍 도시 간 KTX 요약(하루 편수, 첫차·막차, 보통 걸리는 시간, 가장 흔한 어른 요금). DATA_KEY 환경변수.
결과 train.json {date, r: {"seoul-busan": {n, first, last, min, fare}}}"""
import json, sys, time, datetime, statistics, urllib.request, urllib.parse
from collections import Counter
sys.path.insert(0, '..'); from keyfix import key
K = key('DATA_KEY')
ST = {'seoul': 'NAT010000', 'yongsan': 'NAT010032', 'busan': 'NAT014445', 'gyeongju': 'NATH13421', 'jeonju': 'NAT040257', 'gangneung': 'NAT601936'}
ROUTES = [('seoul', 'busan'), ('seoul', 'gyeongju'), ('seoul', 'jeonju'), ('yongsan', 'jeonju'), ('seoul', 'gangneung'), ('busan', 'gyeongju')]
def get(**q):
    url = "https://apis.data.go.kr/1613000/TrainInfo/GetStrtpntAlocFndTrainInfo?serviceKey=" + K + "&" + urllib.parse.urlencode(dict(_type='json', numOfRows=300, pageNo=1, **q))
    for a in range(6):
        try:
            with urllib.request.urlopen(url, timeout=60) as r: d = json.loads(r.read().decode())
            it = (d['response']['body'].get('items') or {}); it = it.get('item', []) if isinstance(it, dict) else []
            return it if isinstance(it, list) else [it]
        except Exception as e: err = e; time.sleep(3 + a)
    raise err
today = datetime.date.today(); dt = today + datetime.timedelta(days=(2 - today.weekday()) % 7 + 7)   # 다음다음 수요일(평일 기준)
out = {'date': dt.strftime('%Y%m%d'), 'r': {}}
for a, b in ROUTES:
    for x, y in ((a, b), (b, a)):
        it = [i for i in get(depPlaceId=ST[x], arrPlaceId=ST[y], depPlandTime=out['date']) if i['traingradename'].startswith('KTX')]
        if not it: print(x, y, 'none'); continue
        mins = [(datetime.datetime.strptime(str(i['arrplandtime']), '%Y%m%d%H%M%S') - datetime.datetime.strptime(str(i['depplandtime']), '%Y%m%d%H%M%S')).seconds // 60 for i in it]
        fare = Counter(int(i['adultcharge']) for i in it if int(i['adultcharge']) > 0).most_common(1)[0][0]
        t = sorted(str(i['depplandtime'])[8:12] for i in it)
        out['r'][f'{x}-{y}'] = {'n': len(it), 'first': t[0][:2] + ':' + t[0][2:], 'last': t[-1][:2] + ':' + t[-1][2:], 'min': int(statistics.median(mins)), 'fare': fare}
        print(x, y, out['r'][f'{x}-{y}'], Counter(int(i['adultcharge']) for i in it).most_common(3))
json.dump(out, open('train.json', 'w'), ensure_ascii=False)
