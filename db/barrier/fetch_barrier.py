#!/usr/bin/env python3
"""한국관광공사 무장애 여행 정보(KorWithService2/detailWithTour2) — 관광지 contentId별. 사용: DATA_KEY=... python3 fetch_barrier.py"""
import os,json,time,urllib.request,urllib.parse
K=__import__('sys').path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..')) or __import__('keyfix').key('DATA_KEY'); D=os.path.dirname(os.path.abspath(__file__))
keys=json.load(open(f'{D}/keys.json'))['keys']; fn=f'{D}/barrier.json'
out=json.load(open(fn)) if os.path.exists(fn) else {}
for cid in sorted({v for v in keys.values() if v}):
    if cid in out: continue
    u='https://apis.data.go.kr/B551011/KorWithService2/detailWithTour2?'+urllib.parse.urlencode(dict(serviceKey=K,MobileOS='ETC',MobileApp='hz',_type='json',contentId=cid),safe='%')
    for t in range(3):
        try:
            d=json.loads(urllib.request.urlopen(u,timeout=40).read().decode())['response']
            it=d['body']['items']; out[cid]=(it['item'][0] if it else None); break
        except Exception as e: print('retry',cid,e); time.sleep(3)
    json.dump(out,open(fn,'w'),ensure_ascii=False); time.sleep(0.15)
print('끝',len(out),sum(1 for v in out.values() if v))
