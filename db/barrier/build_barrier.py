#!/usr/bin/env python3
"""무장애 정보 → ACC 상수: {"pid|관광지": ["기호들", "한국어 설명"]}
기호 w 휠체어 대여, s 턱 없는 입구, e 엘리베이터, r 장애인 화장실, p 장애인 주차, b 유모차 대여, n 수유실, a 음성 안내, d 보조견 동반"""
import json,re
K=json.load(open('keys.json'))['keys']; B=json.load(open('barrier.json'))
clean=lambda s: re.sub(r'_(무장애|시각장애인|청각장애인|영유아가족) 편의시설','',(s or '').strip())
def flags(v):
    f=''
    if v.get('wheelchair','').strip() and re.search(r'대여|이용 ?가능|비치',v['wheelchair']): f+='w'
    if re.search(r'턱이 없|경사로|접근 ?가능',(v.get('exit') or '')+(v.get('route') or '')): f+='s'
    if re.search(r'있음|운영',v.get('elevator') or ''): f+='e'
    if re.search(r'있음',v.get('restroom') or ''): f+='r'
    if re.search(r'있음',v.get('parking') or ''): f+='p'
    if re.search(r'대여',v.get('stroller') or ''): f+='b'
    if re.search(r'있음',v.get('lactationroom') or ''): f+='n'
    if (v.get('audioguide') or '').strip(): f+='a'
    if re.search(r'가능',v.get('helpdog') or ''): f+='d'
    return f
LAB=[('wheelchair','휠체어'),('exit','출입구'),('route','가는 길'),('elevator','엘리베이터'),('restroom','화장실'),('parking','주차'),('publictransport','대중교통'),('stroller','유모차'),('lactationroom','수유실'),('audioguide','음성 안내'),('helpdog','보조견')]
out={}
for k,cid in K.items():
    v=B.get(cid)
    if not v: continue
    f=flags(v)
    if not f: continue
    txt=' / '.join(f'{lab}: {clean(v.get(fld))}' for fld,lab in LAB if clean(v.get(fld)))
    out[k]=[f,txt[:400]]
print('관광지',len(K),'무장애 정보',len(out))
js='/* 무장애 여행 정보: 한국관광공사 「무장애 여행 정보」(KorWithService2, 2026-11 조회). ["기호", "한국어 설명"] w휠체어대여 s턱없는입구 e엘리베이터 r장애인화장실 p장애인주차 b유모차대여 n수유실 a음성안내 d보조견 */\nconst ACC = '+json.dumps(out,ensure_ascii=False,separators=(',',':'))+';\n'
open('acc.js','w').write(js); print('JS',len(js.encode())//1024,'KB')
from collections import Counter; print(Counter(c for v in out.values() for c in v[0]))
