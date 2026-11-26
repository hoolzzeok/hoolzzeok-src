#!/usr/bin/env python3
"""한국관광공사 반려동물 동반여행(KorPetTourService2/areaBasedList2) 장소별 목록 → raw/{pid}.json"""
import os,json,time,urllib.request,urllib.parse
K=__import__('sys').path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..')) or __import__('keyfix').key('DATA_KEY'); D=os.path.dirname(os.path.abspath(__file__))
P=json.load(open(f'{D}/../datalab/placemap.json'))['map']
for pid,(k,c) in sorted(P.items()):
    fn=f'{D}/raw/{pid}.json'
    if os.path.exists(fn): continue
    q=dict(serviceKey=K,MobileOS='ETC',MobileApp='hz',_type='json',numOfRows=1000,pageNo=1,arrange='C',lDongRegnCd=c[:2])
    if k=='l': q['lDongSignguCd']=c[2:]
    u='https://apis.data.go.kr/B551011/KorPetTourService2/areaBasedList2?'+urllib.parse.urlencode(q,safe='%')
    for t in range(4):
        try:
            b=json.loads(urllib.request.urlopen(u,timeout=60).read().decode())['response']['body']; it=b['items']
            json.dump({'total':b.get('totalCount'),'items':it['item'] if it else []},open(fn,'w'),ensure_ascii=False); break
        except Exception as e: print('retry',pid,e); time.sleep(3)
    time.sleep(0.15)
print('끝')
