#!/usr/bin/env python3
"""한국관광공사 관광지별 연관 관광지(TarRlteTarService1/areaBasedList1), 기준월 BASE.
우리 대표 관광지가 있는 시군구마다 1번 호출 → raw/{code}.json"""
import os,json,re,time,urllib.request,urllib.parse
K=__import__('sys').path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..')) or __import__('keyfix').key('DATA_KEY'); BASE=os.environ.get('BASE','202610'); D=os.path.dirname(os.path.abspath(__file__)); os.makedirs(f'{D}/raw',exist_ok=True)
codes=json.load(open(f'{D}/../datalab/codes.json'))['locgo']
P=json.load(open(f'{D}/../datalab/placemap.json'))['map']
M=json.load(open(f'{D}/../tourapi/out/spots_matched.json'))
SIDO={'서울':'11','부산':'26','대구':'27','인천':'28','광주':'12','대전':'30','울산':'31','세종':'36','경기':'41','충청북':'43','충북':'43','충청남':'44','충남':'44','전라남':'12','전남':'12','경상북':'47','경북':'47','경상남':'48','경남':'48','제주':'50','강원':'51','전북':'52','전라북':'52'}
need={}
for r in M:
    a=(r.get('match') or {}).get('addr1','') or ''
    sd=next((v for k,v in SIDO.items() if a.startswith(k)),None); parts=a.split()
    code=None
    if sd and len(parts)>1:
        nm=parts[1]; cands=[k for k,v in codes.items() if k[:2]==sd and v==nm]
        if not cands and len(parts)>2: cands=[k for k,v in codes.items() if k[:2]==sd and v==f'{parts[1]} {parts[2]}']
        if len(cands)==1: code=cands[0]
    if not code and P.get(r['place'],[''])[0]=='l': code=P[r['place']][1]
    if code: need.setdefault(code,[]).append(f"{r['place']}|{r['spot']}")
json.dump(need,open(f'{D}/need.json','w'),ensure_ascii=False); print('시군구',len(need),'관광지',sum(len(v) for v in need.values()))
for code in sorted(need):
    fn=f'{D}/raw/{code}.json'
    if os.path.exists(fn): continue
    u='https://apis.data.go.kr/B551011/TarRlteTarService1/areaBasedList1?'+urllib.parse.urlencode(dict(serviceKey=K,MobileOS='ETC',MobileApp='hz',_type='json',numOfRows=2000,pageNo=1,baseYm=BASE,areaCd=code[:2],signguCd=code),safe='%')
    for t in range(3):
        try:
            d=json.loads(urllib.request.urlopen(u,timeout=60).read().decode())['response']
            it=d['body']['items']; json.dump(it['item'] if it else [],open(fn,'w'),ensure_ascii=False); break
        except Exception as e: print('retry',code,e); time.sleep(3)
    time.sleep(0.2)
print('끝')
