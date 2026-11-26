#!/usr/bin/env python3
"""숙박업 인허가 CSV(행정안전부, 사용자 제공, 2026-11-16 갱신) →
 1) STAY_SUPPLY {pid: [호텔, 여관·모텔, 여인숙, 생활숙박, 콘도]} 영업 중인 곳 수
 2) GOOD_STAY 확인: {"pid|이름": ["o"영업/"c"폐업, 전화]}
펜션·민박·게스트하우스(농어촌민박·외국인관광도시민박 등)는 다른 신고라 이 자료에 없음"""
import csv,json,re,os
D=os.path.dirname(os.path.abspath(__file__))
codes=json.load(open(f'{D}/../datalab/codes.json'))['locgo']; P=json.load(open(f'{D}/../datalab/placemap.json'))['map']
SIDO={'서울':'11','부산':'26','대구':'27','인천':'28','광주':'12','대전':'30','울산':'31','세종':'36','경기':'41','충청북':'43','충북':'43','충청남':'44','충남':'44','전라남':'12','전남':'12','경상북':'47','경북':'47','경상남':'48','경남':'48','제주':'50','강원':'51','전북':'52','전라북':'52'}
GROUP={'일반호텔':0,'관광호텔':0,'여관업':1,'숙박업 기타':1,'여인숙업':2,'숙박업(생활)':3,'휴양콘도미니엄업':4}
rows=list(csv.DictReader(open(f'{D}/../inbox/lodging.csv',encoding='utf-8')))
def loc(r):
    a=(r['도로명주소'] or r['지번주소']).split()
    if len(a)<2: return None,None
    sd=next((v for k,v in SIDO.items() if a[0].startswith(k)),None)
    return sd,a[1]
idx={}
for r in rows:
    sd,sg=loc(r)
    if sd: idx.setdefault(sd,[]).append((sg,r))
sup={}
for pid,(k,c) in P.items():
    nm=codes.get(c,'') if k=='l' else None
    pool=[r for sg,r in idx.get(c[:2],[]) if (k=='m' or sg==nm or sg==nm.split()[0])]
    if k=='m' and c=='28': pool=[r for sg,r in idx.get('28',[])]
    v=[0]*5
    for r in pool:
        if r['영업상태명']=='영업/정상' and r['업태구분명'] in GROUP: v[GROUP[r['업태구분명']]]+=1
    sup[pid]=v
# 광주: 통합 뒤 시군구 이름(동구 등)이 겹쳐서 광주 5개 구만
sup['gwangju']=[0]*5
for sg,r in idx.get('12',[]):
    a=(r['도로명주소'] or r['지번주소'])
    if a.startswith('광주') or re.match(r'전남광주통합특별시 (동구|서구|남구|북구|광산구)',a):
        if r['영업상태명']=='영업/정상' and r['업태구분명'] in GROUP: sup['gwangju'][GROUP[r['업태구분명']]]+=1
# 착한가격 숙소 확인
s=open('/home/claude/hoolzzeok_site/index.html',encoding='utf-8').read()
i=s.index('const GOOD_STAY = ')+18; j=s.index(';\n',i); GS=json.loads(s[i:j])
nz=lambda x: re.sub(r'\(.*?\)|㈜|주식회사|\s|[-·.]','',x)
gsv={}; stat={'o':0,'c':0,'?':0}
for pid,lst in GS.items():
    k,c=P.get(pid,('l','00'))
    for g in lst:
        nm=nz(g[0]); cand=[r for sg,r in idx.get(c[:2] if pid!='gwangju' else '12',[]) if nm and (nz(r['사업장명'])==nm or (len(nm)>=3 and (nm in nz(r['사업장명']) or nz(r['사업장명']) in nm) and len(nz(r['사업장명']))>=3))]
        # 주소 앞부분 겹치는 곳 우선
        road=re.sub(r'\s+',' ',g[2]).split(' (')[0]
        cand.sort(key=lambda r:(0 if road.split()[-2:]==(r['도로명주소'] or '').split(' (')[0].split()[-2:] else 1, 0 if r['영업상태명']=='영업/정상' else 1))
        ok=lambda r: road.split()[-2:]==(r['도로명주소'] or '').split(' (')[0].split(',')[0].split()[-2:] or (nz(r['사업장명'])==nm and any(t in (r['도로명주소']+r['지번주소']) for t in road.split()[:2] if len(t)>=2))
        cand=[r for r in cand if ok(r)]
        if not cand: stat['?']+=1; continue
        r=cand[0]; st='o' if r['영업상태명']=='영업/정상' else 'c'; stat[st]+=1
        gsv[f'{pid}|{g[0]}']=[st,r['전화번호'].strip()]
print('공급',len(sup),'예',sup.get('yeongwol'),sup.get('gyeongju'),sup.get('seoul'),sup.get('gwangju'))
print('착한가격 숙소 확인',stat, [k for k,v in gsv.items() if v[0]=='c'])
js=('/* 숙박업 인허가(행정안전부 지방행정 인허가 자료, 2026-11-16 갱신). 영업 중 [호텔, 여관·모텔, 여인숙, 생활숙박, 콘도] — 펜션·민박·게스트하우스는 다른 신고라 빠짐 */\n'
    'const STAY_SUPPLY = '+json.dumps(sup,separators=(',',':'))+';\n'
    '/* 착한가격 숙소를 같은 자료로 확인: ["o"영업 중 | "c"폐업, 전화] */\nconst GSV = '+json.dumps(gsv,ensure_ascii=False,separators=(',',':'))+';\n')
open(f'{D}/lodging.js','w').write(js); print('JS',len(js.encode())//1024,'KB')
