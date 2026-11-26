#!/usr/bin/env python3
"""서울 출발은 터미널(경부·센트럴·동서울, ID 여러 개)마다 요금이 달라 전부 조회해 가장 싼 값으로 다시 잡음. 고속 + 시외 둘 다."""
import json,os,sys,time
sys.argv=['x','20261118']; src=open('tago_fetch.py',encoding='utf-8').read()
exec(src[:src.index('if not KEY:')])
def allmin(svc,op,deps,arrs):
    best=None
    for a in deps:
        for b in arrs:
            try: it=call(svc,op,depTerminalId=a,arrTerminalId=b,depPlandTime=DATE,numOfRows=200,pageNo=1)
            except Exception as e: continue
            time.sleep(SLEEP)
            ch=[int(i['charge']) for i in it if str(i.get('charge','')).isdigit() and int(i['charge'])>0]
            if ch and (best is None or min(ch)<best[0]): best=(min(ch),a,b)
    return best
n=0
for p in places:
    d=p['id']
    if d=='seoul': continue
    t=TERM[d]; cands=[]
    if t['exp']: r=allmin('ExpBusInfo','GetStrtpntAlocFndExpbusInfo',TERM['seoul']['exp'],t['exp'][:2]); r and cands.append((r[0],'exp',r[1],r[2]))
    if t['sub']: r=allmin('SuburbsBusInfo','GetStrtpntAlocFndSuberbsBusInfo',TERM['seoul']['sub'],t['sub'][:2]); r and cands.append((r[0],'sub',r[1],r[2]))
    old=fares.get(f'seoul-{d}')
    if cands:
        b=min(cands); fares[f'seoul-{d}']=[b[0],b[1],b[2],b[3]]
        if old and b[0]<old[0]: n+=1
    save()
print('다시 잡음, 더 싼 값 찾은 곳',n,'호출',calls)
