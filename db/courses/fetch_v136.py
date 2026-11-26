#!/usr/bin/env python3
"""v136 새 명소(중심관광지·근사 좌표로 넣은 것)를 TourAPI 공식 정보로 바꿈: 이름·좌표·주소·사진·소개·운영시간·쉬는날.
지금 좌표 3km 안에서 이름이 맞는 것만 받음. TOURAPI_KEY 환경변수(키는 파일에 안 씀)."""
import os, sys, json, re, time, math, html, urllib.request, urllib.parse
sys.path.insert(0, '..'); import keyfix
K = keyfix.key('TOURAPI_KEY')
def call(op, **p):
    u = f"https://apis.data.go.kr/B551011/KorService2/{op}?serviceKey={K}&MobileOS=ETC&MobileApp=hoolzzeok&_type=json&" + urllib.parse.urlencode(p)
    for a in range(6):
        try:
            with urllib.request.urlopen(u, timeout=40) as r: d = json.loads(r.read().decode())
            it = d['response']['body']['items']; it = it['item'] if isinstance(it, dict) else []
            return it if isinstance(it, list) else [it]
        except Exception as e: err = e; time.sleep(3 + a * 3)
    raise err
km = lambda a, b, c, d: 2 * 6371 * math.asin(math.sqrt(math.sin(math.radians(c - a) / 2) ** 2 + math.cos(math.radians(a)) * math.cos(math.radians(c)) * math.sin(math.radians(d - b) / 2) ** 2))
norm = lambda s: re.sub(r"[\s()\[\]·,.\-/]", "", s or "")
F = {'12': ('usetime', 'restdate', 'infocenter', 'parking'), '14': ('usetimeculture', 'restdateculture', 'infocenterculture', 'parkingculture'),
     '28': ('usetimeleports', 'restdateleports', 'infocenterleports', 'parkingleports'), '38': ('opentime', 'restdateshopping', 'infocentershopping', 'parkingshopping')}
ALIAS = {"명동거리": ["명동 쇼핑거리", "명동거리", "명동관광특구"], "성수동 카페거리": ["성수동 카페거리", "성수 카페거리", "성수동"], "홍대 걷고싶은거리": ["홍대 걷고싶은거리", "걷고싶은거리", "홍대 거리"],
         "별마당도서관": ["별마당도서관", "별마당 도서관"], "동문시장": ["동문재래시장", "동문시장"], "오설록티뮤지엄": ["오설록 티뮤지엄", "오설록"], "주상절리대": ["주상절리대", "대포주상절리"],
         "이호테우해변": ["이호테우해변", "이호테우해수욕장"], "월정리해변": ["월정리해변", "월정리해수욕장"], "경포해변": ["경포해변", "경포해수욕장"], "전주한옥마을": ["전주한옥마을", "전주 한옥마을"],
         "강릉중앙시장": ["강릉중앙시장", "강릉 중앙시장"], "오죽헌": ["오죽헌", "강릉 오죽헌"]}
sp = json.load(open('spots.json', encoding='utf-8'))
todo = [k for k, v in sp.items() if v and str(v.get('cid', '')).startswith(('hub-', 'approx-'))]
print('todo', len(todo))
for key in todo:
    v = sp[key]; pid, name = key.split('|', 1); best = None
    for kw in ALIAS.get(name, [name]):
        for i in call('searchKeyword2', keyword=kw, numOfRows=30, pageNo=1, arrange='A'):
            if i.get('contenttypeid') not in ('12', '14') and name not in ('동문시장', '강릉중앙시장'): continue   # 가게(38) 오인 방지, 시장만 예외
            if i.get('contenttypeid') not in F: continue
            try: d = km(v['lat'], v['lon'], float(i['mapy']), float(i['mapx']))
            except: continue
            if d > 3: continue
            t, w = norm(i['title']), norm(kw)
            s = 100 if t == w else 70 if (t.startswith(w) or w.startswith(t)) else 50 if (w in t or t in w) else 0
            if s >= 70 and (best is None or s - d * 5 > best[0]): best = (s - d * 5, i, d)
        time.sleep(.12)
        if best and best[0] >= 90: break
    if not best: print('NOMATCH', key); continue
    i = best[1]; cid = i['contentid']; ct = i['contenttypeid']
    c = (call('detailCommon2', contentId=cid) or [{}])[0]; r = (call('detailIntro2', contentId=cid, contentTypeId=ct) or [{}])[0]; time.sleep(.12)
    f = F[ct]; ov = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", c.get('overview', '')))).strip()
    sp[key] = {'place': pid, 'want': name, 'cid': cid, 'ct': ct, 'title': i['title'], 'addr': i.get('addr1', '') or v.get('addr', ''), 'lat': float(i['mapy']), 'lon': float(i['mapx']),
               'img': i.get('firstimage2') or i.get('firstimage') or '', 'cpy': i.get('cpyrhtDivCd') or c.get('cpyrhtDivCd', ''), 'overview': ov,
               'use': r.get(f[0], ''), 'rest': r.get(f[1], ''), 'tel': r.get(f[2], ''), 'fee': r.get('usefee', '')}
    print('OK', key, '->', i['title'], f"{best[2]:.2f}km", '|', re.sub(r'<[^>]+>', ' ', sp[key]['use'])[:60], '|', re.sub(r'<[^>]+>', ' ', sp[key]['rest'])[:40])
    json.dump(sp, open('spots.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('done')
