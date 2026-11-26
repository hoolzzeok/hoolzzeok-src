#!/usr/bin/env python3
"""연관 관광지 → RLTE 상수: {"pid|대표관광지": [[이름, 분류(t관광지/f음식), 시군구], ...]} 순위순, 관광지 4·음식 3개까지(숙박 제외)"""
import json,re,os
need=json.load(open('need.json'))
nz=lambda s: re.sub(r'\(.*?\)|\[.*?\]|\s|·|-','',s)
out={}; hit=0
for code,keys in need.items():
    fn=f'raw/{code}.json'
    if not os.path.exists(fn): continue
    by={}
    for r in json.load(open(fn)): by.setdefault(r['tAtsNm'],[]).append(r)
    for k in keys:
        pid,sp=k.split('|',1); parts=[nz(x) for x in re.split(r'[·,/]|\(',sp) if len(nz(x))>=2]
        n=nz(sp)
        c=[t for t in by if nz(t)==n] or [t for t in by if any(p==nz(t) for p in parts)] or [t for t in by if len(n)>=3 and len(nz(t))>=3 and (n in nz(t) or nz(t) in n)]
        if not c: continue
        t=min(c,key=len); rows=sorted({(r['rlteTatsNm'],r['rlteCtgryLclsNm'],r['rlteSignguNm'],int(r['rlteRank'])) for r in by[t]},key=lambda x:x[3])
        sights=[[a,'t',g] for a,b,g,_ in rows if b=='관광지' and nz(a)!=nz(t)][:4]; eats=[[a,'f',g] for a,b,g,_ in rows if b=='음식'][:3]
        if sights or eats: out[k]=sights+eats; hit+=1
print('대표관광지',sum(len(v) for v in need.values()),'연결',hit)
js='/* 같이 많이 가는 곳: 한국관광공사 「관광지별 연관 관광지 정보」(2026-10 기준). [이름, t=관광지 f=음식, 시군구] 순위순 */\nconst RLTE = '+json.dumps(out,ensure_ascii=False,separators=(',',':'))+';\n'
open('rlte.js','w').write(js); print('JS',len(js.encode())//1024,'KB')
