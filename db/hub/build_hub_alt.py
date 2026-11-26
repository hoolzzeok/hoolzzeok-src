#!/usr/bin/env python3
"""v114: 광역시(서울·부산 등)는 소개 명소가 적어 '맘에 안들어요' 바꿀 거리가 모자람 → 구·군별 중심 관광지 상위 3곳씩 모아 순위순 12곳.
HUB_ALT = {pid: [[이름, 분류, 경도, 위도]...]}  (출처: 한국관광공사 「기초지자체 중심 관광지 정보」, raw/ 와 같은 기준월)"""
import json,os,re
D=os.path.dirname(os.path.abspath(__file__))
src=open(f'{D}/build_hub.py',encoding='utf-8').read()
SKIP=eval(re.search(r'^SKIP=(re\.compile\(.*\))$',src,re.M).group(1))
EXTRA=re.compile(r'시네마|CGV|메가박스|경기장|야구장|체육관|영화관|아레나|볼파크|도매시장|부두|EXCO|컨벤션|아카데미하우스')
MC={'문화관광':'c','자연관광':'n','역사관광':'h','레저스포츠':'l','체험관광':'x','쇼핑':'s','기타관광':'o'}
P=json.load(open(f'{D}/../datalab/placemap.json'))['map']
out={}
for pid,(k,c) in P.items():
    if k!='m': continue
    rows=[]
    for fn in sorted(os.listdir(f'{D}/raw')):
        if not fn.startswith(c): continue
        per=[r for r in json.load(open(f'{D}/raw/{fn}')) if r['hubCtgryLclsNm']=='관광지']
        per.sort(key=lambda r:int(r['hubRank']))
        got=0
        for r in per:
            n=r['hubTatsNm'].strip()
            if SKIP.search(n) or EXTRA.search(n) or (r['hubCtgryMclsNm']=='쇼핑' and not re.search(r'시장|거리|골목|마을',n)): continue
            rows.append((int(r['hubRank']),n,MC.get(r['hubCtgryMclsNm'],'o'),round(float(r['mapX']),5),round(float(r['mapY']),5))); got+=1
            if got>=3: break
    rows.sort(key=lambda r:r[0]); seen=set(); t=[]
    for _,n,m,x,y in rows:
        if n in seen: continue
        seen.add(n); t.append([n,m,x,y])
        if len(t)>=12: break
    if t: out[pid]=t
js='/* 광역시 바꿀 거리: 한국관광공사 「기초지자체 중심 관광지 정보」 구·군별 상위 3곳을 모아 순위순 12곳. [이름, 분류, 경도, 위도] */\nconst HUB_ALT = '+json.dumps(out,ensure_ascii=False,separators=(',',':'))+';'
open(f'{D}/hub_alt.js','w').write(js)
for k,v in out.items(): print(k,len(v),', '.join(x[0] for x in v))
