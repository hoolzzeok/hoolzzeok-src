#!/usr/bin/env python3
"""한국관광공사 기초지자체 중심 관광지(LocgoHubTarService1/areaBasedList1), 기준월 BASE → raw/{시군구}.json"""
import os,json,time,urllib.request,urllib.parse
K=__import__('sys').path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..')) or __import__('keyfix').key('DATA_KEY'); BASE=os.environ.get('BASE','202610'); D=os.path.dirname(os.path.abspath(__file__))
codes=json.load(open(f'{D}/../datalab/codes.json'))['locgo']; P=json.load(open(f'{D}/../datalab/placemap.json'))['map']
need=set()
for pid,(k,c) in P.items():
    if k=='l':
        subs=[x for x in codes if x[:4]==c[:4] and x!=c and x[4]!='0'] if c.endswith('0') else []
        need.update([c]+subs)
    else: need.update(x for x in codes if x[:2]==c)
print('호출',len(need))
for c in sorted(need):
    fn=f'{D}/raw/{c}.json'
    if os.path.exists(fn): continue
    u='https://apis.data.go.kr/B551011/LocgoHubTarService1/areaBasedList1?'+urllib.parse.urlencode(dict(serviceKey=K,MobileOS='ETC',MobileApp='hz',_type='json',numOfRows=100,pageNo=1,baseYm=BASE,areaCd=c[:2],signguCd=c),safe='%')
    for t in range(4):
        try:
            it=json.loads(urllib.request.urlopen(u,timeout=60).read().decode())['response']['body']['items']
            json.dump(it['item'] if it else [],open(fn,'w'),ensure_ascii=False); break
        except Exception as e: print('retry',c,e); time.sleep(3)
    time.sleep(0.15)
print('끝')
