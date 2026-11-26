#!/usr/bin/env python3
"""코스 명소 이름을 일본어·중국어(간체)로: 관광공사 일문·중문간체 서비스에서 같은 장소를 찾아 제목을 받음.
짝 찾기 규칙은 ../tourapi/tourapi_i18n.py 와 같음(국문 이름 검색 3km → 안 되면 반경 500m에서 괄호 속 한글이 맞는 것).
결과: names_i18n.json {국문이름: {ja, zh}}. 멱등(이미 있는 이름은 건너뜀). TOURAPI_KEY 환경변수."""
import json, re, sys, time, os
sys.path.insert(0, '../tourapi'); import tourapi_i18n as T
LANGS = [tuple(x.split(':')) for x in os.environ.get('LANGS', 'ja:JpnService2,zh:ChsService2').split(',')]
out = json.load(open('names_i18n.json', encoding='utf-8')) if os.path.exists('names_i18n.json') else {}
cdef = json.load(open('course_def.json', encoding='utf-8')); sp = json.load(open('spots.json', encoding='utf-8'))
def tidy(t):
    t = re.sub(r"[（(][^）)]*[가-힣][^）)]*[）)]", "", t or "")   # 괄호 속 한글 표기 빼기
    return re.sub(r"\s+", " ", t).strip(" ·")
todo = []
for pid, cs in cdef['courses'].items():
    for c in cs:
        for st in c['stops']:
            if st[0] == 'spot':
                s = sp.get(f"{pid}|{st[1]}")
                if s and st[1] not in [x[0] for x in todo]: todo.append((st[1], s['lat'], s['lon']))
for ko, lat, lon in todo:
    cur = out.setdefault(ko, {})
    for lg, svc in LANGS:
        if cur.get(lg) is not None: continue
        try:
            b = T.pick(T.call(svc, 'searchKeyword2', keyword=T.clean(ko), numOfRows=30, pageNo=1, arrange='A'), ko, lat, lon, 3, True); time.sleep(T.SLEEP)
            if not b:
                b = T.pick(T.call(svc, 'locationBasedList2', mapX=lon, mapY=lat, radius=500, arrange='E', numOfRows=30, pageNo=1), ko, lat, lon, 0.5, False); time.sleep(T.SLEEP)
        except Exception as e:
            print('ERR', ko, lg, str(e)[:80]); continue
        cur[lg] = tidy(b[1]['title']) if b else ''
        print(lg, ko, '->', cur[lg] or '(없음)')
    json.dump(out, open('names_i18n.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('done', len(out))
