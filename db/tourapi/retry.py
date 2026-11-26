import json, re, time, sys
sys.argv=['x']; import tourapi_fetch as T
T.MAX_KM = 60
places = {p['id']: p for p in json.load(open('places_spots.json', encoding='utf-8'))}
M = json.load(open('out/spots_matched.json', encoding='utf-8'))
calls = 0; fixed = 0
for x in M:
    if x['match'] or x['place'] == 'dokdo': continue
    p = places[x['place']]; base = T.clean(x['spot'])
    variants = []
    for v in [base.replace(' ', ''), base.split(' ')[0] if ' ' in base else None, re.sub(r'(국립공원|도립공원|유적지|유적)$', '', base.replace(' ', ''))]:
        if v and len(v) >= 2 and v not in variants: variants.append(v)
    for v in variants:
        try: items = T.call('searchKeyword2', keyword=v, numOfRows=20, pageNo=1, arrange='A'); calls += 1
        except Exception as e: print('ERR', x['spot'], e); continue
        time.sleep(0.15)
        c = [(T.score(i, v, p['lat'], p['lon']), i) for i in items]; c = [k for k in c if k[0] is not None]
        if c:
            best = max(c, key=lambda k: k[0])[1]
            try: det = T.detail(best['contentid']); calls += 1
            except Exception: det = {}
            x['match'] = T.pick_fields(best, det); x['via'] = v; fixed += 1
            print('FIX', x['place'], x['spot'], '->', best['title'], best.get('contenttypeid')); break
json.dump(M, open('out/spots_matched.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('fixed', fixed, 'calls', calls, 'still', sum(1 for x in M if not x['match']))
