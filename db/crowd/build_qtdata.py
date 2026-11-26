#!/usr/bin/env python3
"""공휴일(holiday/holidays.json)과 명소 혼잡 예측(crowd/crowd.json)을 index.html의 두 줄로 넣음.
const KR_HOL = {YYYYMMDD: 이름}; const SPOT_CROWD = {base: 'YYYYMMDD', n: 일수, s: {명소: [값...]}}  (값은 정수, 그날 자료 없으면 null)"""
import json, datetime, sys
SRC = '/home/claude/hoolzzeok_site/index.html'
hol = dict(json.load(open('/home/claude/hoolzzeok_db/holiday/holidays.json', encoding='utf-8')))
cr = json.load(open('/home/claude/hoolzzeok_db/crowd/crowd.json', encoding='utf-8'))
days = sorted({d for v in cr['spots'].values() for d in v['r']})
base = days[0]; b = datetime.datetime.strptime(base, '%Y%m%d'); n = (datetime.datetime.strptime(days[-1], '%Y%m%d') - b).days + 1
ds = [(b + datetime.timedelta(i)).strftime('%Y%m%d') for i in range(n)]
s = {k: [round(v['r'][d]) if d in v['r'] else None for d in ds] for k, v in cr['spots'].items()}
wx = json.load(open('/home/claude/hoolzzeok_db/weather/weather.json', encoding='utf-8'))
tr = json.load(open('/home/claude/hoolzzeok_db/train/train.json', encoding='utf-8'))
lines = {'const TRAIN = ': 'const TRAIN = ' + json.dumps(tr, ensure_ascii=False, separators=(',', ':')) + ';   // 국토교통부 TAGO 열차정보(평일 하루, KTX만)',
         'const WX = ': 'const WX = ' + json.dumps(wx, ensure_ascii=False, separators=(',', ':')) + ';   // 기상청 단기·중기 예보(빌드할 때 받은 값)',
         'const KR_HOL = ': 'const KR_HOL = ' + json.dumps(hol, ensure_ascii=False, separators=(',', ':')) + ';   // 한국천문연구원 특일 정보(공휴일)',
         'const SPOT_CROWD = ': 'const SPOT_CROWD = ' + json.dumps({'base': base, 'n': n, 's': s}, ensure_ascii=False, separators=(',', ':')) + ';   // 한국관광공사 관광지 집중률(향후 30일, 가장 붐비는 날=100)'}
L = open(SRC, encoding='utf-8').read().split('\n')
for pre, new in lines.items():
    idx = [i for i, l in enumerate(L) if l.startswith(pre)]
    if idx: L[idx[0]] = new
    else:
        j = [i for i, l in enumerate(L) if l.startswith('const COURSES = ')][0]; L.insert(j + 1, new)
open(SRC, 'w', encoding='utf-8').write('\n'.join(L)); print('base', base, 'days', n, 'spots', len(s), 'holidays', len(hol))
