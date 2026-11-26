#!/usr/bin/env python3
"""관광지 집중률(향후 30일 예측, 가장 붐비는 날=100) → 코스 명소별 날짜별 값. TOURAPI_KEY 환경변수.
1) 명소 주소의 시도·시군구 → 법정동 코드(관광공사 ldongCode2)  2) 시군구별 전체 목록 받기  3) 이름으로 짝(완전일치 > 띄어쓰기 무시 > 포함)
결과: crowd.json {기준일, 명소: {tAtsNm, rates:{YYYYMMDD: 값}}}, 짝 못 찾은 명소는 unmatched에."""
import json, os, re, sys, time, urllib.parse, urllib.request
sys.path.insert(0, '..'); from keyfix import key
K = key('TOURAPI_KEY'); C = dict(MobileOS='ETC', MobileApp='hoolzzeok', _type='json')
def get(svc, op, **q):
    url = f"https://apis.data.go.kr/B551011/{svc}/{op}?serviceKey={K}&" + urllib.parse.urlencode(dict(C, **q))
    for a in range(6):
        try:
            with urllib.request.urlopen(url, timeout=60) as r: d = json.loads(r.read().decode())
            b = d['response']['body']; it = (b.get('items') or {}); it = it.get('item', []) if isinstance(it, dict) else []
            return (it if isinstance(it, list) else [it]), int(b.get('totalCount') or 0)
        except Exception as e: err = e; time.sleep(2 + a)
    raise err
cdef = json.load(open('../courses/course_def.json', encoding='utf-8')); sp = json.load(open('../courses/spots.json', encoding='utf-8'))
spots = {}
for pid, cs in cdef['courses'].items():
    for c in cs:
        for st in c['stops']:
            if st[0] == 'spot' and sp.get(f"{pid}|{st[1]}"): spots[st[1]] = sp[f"{pid}|{st[1]}"]['addr']
# 시도 코드
sido, _ = get('KorService2', 'ldongCode2', numOfRows=50, pageNo=1)
SIDO = {x['name']: x['code'] for x in sido}
ALIAS = {'서울': '서울특별시', '부산': '부산광역시', '경북': '경상북도', '경기': '경기도', '제주': '제주특별자치도', '전북': '전북특별자치도', '강원': '강원특별자치도'}
sgg_cache = {}
def sgg_code(addr):
    t = addr.split()
    a = ALIAS.get(t[0], t[0]); ac = SIDO.get(a) or next((v for k2, v in SIDO.items() if k2.startswith(a[:2])), None)
    if ac not in sgg_cache:
        it, _ = get('KorService2', 'ldongCode2', lDongRegnCd=ac, numOfRows=300, pageNo=1); sgg_cache[ac] = {x['name']: x['code'] for x in it}
    m = sgg_cache[ac]
    for n in (' '.join(t[1:3]), t[1]):
        if n in m: return ac, ac + m[n]
    return ac, None
lists = {}; out = {'base': None, 'spots': {}, 'unmatched': []}
norm = lambda s: re.sub(r'[\s()·]', '', s or '')
for nm, addr in spots.items():
    ac, sc = sgg_code(addr)
    if not sc: out['unmatched'].append([nm, addr, 'no sgg']); continue
    if sc not in lists:
        rows, p = [], 1
        while True:
            it, tot = get('TatsCnctrRateService', 'tatsCnctrRatedList', areaCd=ac, signguCd=sc, numOfRows=1000, pageNo=p); rows += it
            if len(rows) >= tot or not it: break
            p += 1
        lists[sc] = rows; print(sc, len(rows), flush=True)
    rows = lists[sc]; names = {r['tAtsNm'] for r in rows}
    OVR = {'명동거리': '명동', '홍대 걷고싶은거리': '홍대', '별마당도서관': '한국종합무역센터(코엑스)', '부평깡통시장': '부평시장(깡통시장)', '수원화성': '수원 화성 [유네스코 세계유산]', '동문시장': '동문재래시장', '경포해변': '강릉 경포해수욕장'}   # 손으로 확인한 짝(별마당도서관은 코엑스 안)
    pick = OVR[nm] if OVR.get(nm) in names else nm if nm in names else next((n for n in names if norm(n) == norm(nm)), None) or next((n for n in sorted(names, key=len) if norm(nm) in norm(n) or (len(norm(n)) >= 3 and norm(n) in norm(nm))), None)
    if not pick: out['unmatched'].append([nm, addr, sc]); continue
    rates = {r['baseYmd']: float(r['cnctrRate']) for r in rows if r['tAtsNm'] == pick}
    out['spots'][nm] = {'t': pick, 'r': rates}; out['base'] = min(rates) if rates else out['base']
json.dump(out, open('crowd.json', 'w', encoding='utf-8'), ensure_ascii=False)
json.dump({k: sorted({r['tAtsNm'] for r in v}) for k, v in lists.items()}, open('crowd_names.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('matched', len(out['spots']), 'unmatched', len(out['unmatched']))
for nm, v in out['spots'].items():
    if v['t'] != nm: print('  ', nm, '->', v['t'])
for u in out['unmatched']: print('  X', u)
