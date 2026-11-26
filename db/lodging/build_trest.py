#!/usr/bin/env python3
"""관광식당(문화체육관광부 지정, 행정안전부 인허가 CSV 사용자 제공) → TREST {pid: [[이름, 영문명, 전화, 도로명주소]...]} 영업 중만"""
import csv,json,re,os
codes=json.load(open('../datalab/codes.json'))['locgo']; P=json.load(open('../datalab/placemap.json'))['map']
SIDO={'서울':'11','부산':'26','대구':'27','인천':'28','광주':'12','대전':'30','울산':'31','세종':'36','경기':'41','충청북':'43','충북':'43','충청남':'44','충남':'44','전라남':'12','전남':'12','경상북':'47','경북':'47','경상남':'48','경남':'48','제주':'50','강원':'51','전북':'52','전라북':'52'}
rows=[r for r in csv.DictReader(open('../inbox/tour_biz.csv',encoding='utf-8')) if r['영업상태명']=='영업/정상']
out={}
for r in rows:
    a=(r['도로명주소'] or r['지번주소']).split()
    if len(a)<2: continue
    sd=next((v for k,v in SIDO.items() if a[0].startswith(k)),None)
    for pid,(k,c) in P.items():
        if (k=='m' and sd==c) or (k=='l' and sd==c[:2] and a[1]==codes.get(c,'').split()[0]):
            out.setdefault(pid,[]).append([re.sub(r'\s+',' ',r['사업장명']).strip(), r['영문상호명'].strip(), r['전화번호'].strip(), re.sub(r'\s+',' ',r['도로명주소'] or r['지번주소']).split(' (')[0]])
            break
out={k:[len(v),v[:6]] for k,v in out.items()}
print(len(out), {k:v[0] for k,v in list(out.items())[:12]})
js='/* 관광식당: 문화체육관광부 지정(외국인 관광객 대상 식당, 행정안전부 인허가 자료, 2026-11 갱신). [이름, 영문 상호, 전화, 주소] */\nconst TREST = '+json.dumps(out,ensure_ascii=False,separators=(',',':'))+';\n'
open('trest.js','w').write(js); print('JS',len(js.encode())//1024,'KB')
