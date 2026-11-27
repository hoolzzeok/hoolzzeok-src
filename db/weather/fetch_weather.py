#!/usr/bin/env python3
"""기상청 단기예보(오늘~3일 뒤, 5km 격자) + 중기 육상예보(4~10일 뒤, 권역) → 코스 도시별 날짜별 날씨.
DATA_KEY 환경변수. 결과 weather.json {at, d: {pid: {YYYYMMDD: [종류, 강수확률, 최저, 최고]}}}
종류: c 맑음, p 구름많음, o 흐림, r 비, s 눈.  최저·최고는 단기예보에만 있음(중기는 null)."""
import json, math, sys, time, datetime, urllib.request, urllib.parse
sys.path.insert(0, '..'); from keyfix import key
K = key('DATA_KEY')
CITY = {  # 시청 근처 좌표, 중기 육상예보 구역
  'seoul': (37.5665, 126.9780, '11B00000'), 'suwon': (37.2636, 127.0286, '11B00000'), 'busan': (35.1796, 129.0756, '11H20000'),
  'gyeongju': (35.8562, 129.2247, '11H10000'), 'jeonju': (35.8242, 127.1480, '11F10000'), 'gangneung': (37.7519, 128.8761, '11D20000'),
  'jeju': (33.4996, 126.5312, '11G00000')}
def grid(lat, lon):   # 기상청 격자 변환(Lambert Conformal Conic, 기상청 단기예보 활용가이드 식)
    RE, GRID, S1, S2, OLON, OLAT, XO, YO = 6371.00877, 5.0, 30.0, 60.0, 126.0, 38.0, 43, 136
    D = math.pi / 180; re = RE / GRID; s1, s2, olon, olat = S1 * D, S2 * D, OLON * D, OLAT * D
    sn = math.log(math.cos(s1) / math.cos(s2)) / math.log(math.tan(math.pi / 4 + s2 / 2) / math.tan(math.pi / 4 + s1 / 2))
    sf = math.tan(math.pi / 4 + s1 / 2) ** sn * math.cos(s1) / sn; ro = re * sf / math.tan(math.pi / 4 + olat / 2) ** sn
    ra = re * sf / math.tan(math.pi / 4 + lat * D / 2) ** sn; th = lon * D - olon
    th = th - 2 * math.pi if th > math.pi else th + 2 * math.pi if th < -math.pi else th; th *= sn
    return int(ra * math.sin(th) + XO + 0.5), int(ro - ra * math.cos(th) + YO + 0.5)
def get(path, **q):
    url = f"https://apis.data.go.kr/1360000/{path}?serviceKey={K}&" + urllib.parse.urlencode(dict(dataType='JSON', pageNo=1, **q))
    for a in range(6):
        try:
            with urllib.request.urlopen(url, timeout=60) as r: d = json.loads(r.read().decode())
            if d['response']['header']['resultCode'] == '03': raise LookupError(d['response']['header'])
            if d['response']['header']['resultCode'] != '00': raise RuntimeError(d['response']['header'])
            it = d['response']['body']['items']['item']; return it if isinstance(it, list) else [it]
        except LookupError: raise
        except Exception as e: err = e; time.sleep(3 + a)
    raise err
KST = datetime.timezone(datetime.timedelta(hours=9)); now = datetime.datetime.now(KST)
# 단기: 가장 최근 발표(02·05·08·11·14·17·20·23시, 발표 10분 뒤부터)
bt = max([h for h in (2, 5, 8, 11, 14, 17, 20, 23) if now >= now.replace(hour=h, minute=15, second=0)] or [None]) if now.hour >= 2 else None
bd = now if bt is not None else now - datetime.timedelta(days=1); bt = 23 if bt is None else bt
# 중기: 06·18시 발표
mt = now.replace(hour=18) if now.hour >= 18 else now.replace(hour=6) if now.hour >= 6 else (now - datetime.timedelta(days=1)).replace(hour=18)
def kind_short(sky, pty):
    return {1: 'r', 2: 'r', 3: 's', 4: 'r'}.get(pty) or {1: 'c', 3: 'p', 4: 'o'}.get(sky, 'p')
def kind_mid(t):
    return 's' if '눈' in t else 'r' if ('비' in t or '소나기' in t) else 'o' if '흐' in t else 'p' if '구름' in t else 'c'
out = {'at': now.strftime('%Y%m%d%H'), 'short': bd.strftime('%Y%m%d') + f'{bt:02d}', 'mid': mt.strftime('%Y%m%d%H'), 'd': {}}
for pid, (lat, lon, reg) in CITY.items():
    nx, ny = grid(lat, lon); days = {}
    rows = get('VilageFcstInfoService_2.0/getVilageFcst', numOfRows=1200, base_date=bd.strftime('%Y%m%d'), base_time=f'{bt:02d}00', nx=nx, ny=ny)
    by = {}
    for r in rows: by.setdefault(r['fcstDate'], []).append(r)
    for dte, rs in by.items():
        day = [r for r in rs if '0900' <= r['fcstTime'] <= '1800']
        pop = max([int(r['fcstValue']) for r in day if r['category'] == 'POP'] or [0])
        pty = [int(r['fcstValue']) for r in day if r['category'] == 'PTY' and r['fcstValue'] != '0']
        sky = [int(r['fcstValue']) for r in day if r['category'] == 'SKY']
        tmn = next((float(r['fcstValue']) for r in rs if r['category'] == 'TMN'), None); tmx = next((float(r['fcstValue']) for r in rs if r['category'] == 'TMX'), None)
        if not day: continue
        k = kind_short(max(set(sky), key=sky.count) if sky else 1, max(set(pty), key=pty.count) if pty else 0)
        days[dte] = [k, pop, None if tmn is None else round(tmn), None if tmx is None else round(tmx)]
    m = {}; mtu = mt
    for tm in (mt, mt - datetime.timedelta(hours=12)):   # 최신 발표가 아직 안 올라왔으면(NO_DATA) 바로 전 발표를 씀
        try: m = get('MidFcstInfoService/getMidLandFcst', numOfRows=1, regId=reg, tmFc=tm.strftime('%Y%m%d%H00'))[0]; mtu = tm; break
        except Exception as e: print(pid, reg, tm.strftime('%m%d%H'), '중기예보 없음:', str(e)[:60], flush=True)
    out.setdefault('mid_used', {})[pid] = mtu.strftime('%Y%m%d%H')
    for n in range(4, 11):
        dte = (mtu + datetime.timedelta(days=n)).strftime('%Y%m%d')
        if dte in days: continue
        if f'rnSt{n}Am' in m: pop = max(m[f'rnSt{n}Am'], m[f'rnSt{n}Pm']); wf = m[f'wf{n}Am'] + ' ' + m[f'wf{n}Pm']
        elif f'rnSt{n}' in m: pop = m[f'rnSt{n}']; wf = m[f'wf{n}']
        else: continue
        days[dte] = [kind_mid(wf), int(pop), None, None]
    out['d'][pid] = dict(sorted(days.items())); print(pid, nx, ny, len(days), list(days.items())[:2], flush=True)
json.dump(out, open('weather.json', 'w'), ensure_ascii=False)
print('at', out['at'], 'short', out['short'], 'mid', out['mid'], '중기 쓴 발표', sorted(set(out.get('mid_used', {}).values())), '5일 넘게 있는 도시', sum(len(v) > 4 for v in out['d'].values()), '/', len(out['d']))
