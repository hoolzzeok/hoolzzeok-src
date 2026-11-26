#!/usr/bin/env python3
"""반려동물 동반여행 → PET {pid: [[관광지·체험 이름..5], [숙소..3], [식당..3], 전체 수, 쇼핑 수]}"""
import json,glob,re,os
out={}
clean=lambda t: re.sub(r'\s*\[[^\]]*\]','',t).strip()
for f in glob.glob('raw/*.json'):
    pid=os.path.basename(f)[:-5]; it=json.load(open(f))['items']
    if not it: continue
    by=lambda ts: [clean(r['title']) for r in it if r['contenttypeid'] in ts]
    sights=list(dict.fromkeys(by(('12','14','28'))))[:5]; stays=list(dict.fromkeys(by(('32',))))[:3]; eats=list(dict.fromkeys(by(('39',))))[:3]
    out[pid]=[sights,stays,eats,len(it),sum(1 for r in it if r['contenttypeid']=='38')]
print(len(out)); print(out.get('gyeongju')); print(out.get('seoul')[3:],out.get('seoul')[0])
js='/* 반려동물 동반여행: 한국관광공사 「반려동물 동반여행 서비스」(KorPetTourService2, 2026-11 조회). [관광·체험, 숙소, 식당, 전체 수, 쇼핑 수] */\nconst PET = '+json.dumps(out,ensure_ascii=False,separators=(',',':'))+';\n'
open('pet.js','w').write(js); print('JS',len(js.encode())//1024,'KB')
