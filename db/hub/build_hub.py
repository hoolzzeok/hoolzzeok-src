#!/usr/bin/env python3
"""중심 관광지 → HUB 상수 {pid: [[관광지명, 중분류약호, 경도, 위도]...6, [[숙소명]...3]]} (광역시 7곳은 기존 소개가 있어 제외)"""
import json,os,re
D=os.path.dirname(os.path.abspath(__file__))
codes=json.load(open(f'{D}/../datalab/codes.json'))['locgo']; P=json.load(open(f'{D}/../datalab/placemap.json'))['map']
SKIP=re.compile(r'역$|역\(|터미널|휴게소|주차장|IC$|나들목|톨게이트|공항|정류장|정류소|마트|아울렛|백화점|CC$|골프|병원|청사|시청|군청|구청|대학교|학교|주유소|여객선|선착장$|항여객|버스|모텔|교차로|사거리|아파트|행정복지센터|우체국|은행')
MC={'문화관광':'c','자연관광':'n','역사관광':'h','레저스포츠':'l','체험관광':'x','쇼핑':'s','기타관광':'o'}
out={}
for pid,(k,c) in P.items():
    if k!='l': continue
    subs=[x for x in codes if x[:4]==c[:4] and x!=c and x[4]!='0'] if c.endswith('0') else []
    rows=[]
    for x in [c]+subs:
        fn=f'{D}/raw/{x}.json'
        if os.path.exists(fn): rows+=json.load(open(fn))
    rows.sort(key=lambda r:int(r['hubRank']))
    seen=set(); t=[]; s=[]
    for r in rows:
        n=r['hubTatsNm'].strip()
        if n in seen: continue
        seen.add(n)
        if r['hubCtgryLclsNm']=='관광지' and not SKIP.search(n) and (r['hubCtgryMclsNm']!='쇼핑' or re.search(r'시장|거리|골목|마을',n)) and len(t)<6: t.append([n,MC.get(r['hubCtgryMclsNm'],'o'),round(float(r['mapX']),5),round(float(r['mapY']),5)])
        elif r['hubCtgryLclsNm']=='숙박' and len(s)<3: s.append(n)
    if t: out[pid]=[t,s]
print('장소',len(out),'빈 곳',[p for p,(k,c) in P.items() if k=='l' and p not in out])
js='/* 요즘 많이 찾는 곳: 한국관광공사 「기초지자체 중심 관광지 정보」(2026-10 기준) 순위순. [[이름, 분류 c문화 n자연 h역사 l레저 x체험 s쇼핑 o기타, 경도, 위도]..., [숙소..]] */\nconst HUB = '+json.dumps(out,ensure_ascii=False,separators=(',',':'))+';\n'
open(f'{D}/hub.js','w').write(js); print('JS',len(js.encode())//1024,'KB'); print(out.get('yeongwol')); print(out.get('suwon'))
