"""군 지역 명소(HUB78)의 외국어 이름: 관광공사 영·일·중(간체·번체) 서비스에서 좌표 300m 안 가장 가까운 같은 곳을 찾음.
입력: site/index.html 의 HUB78(t = [contentid, 제목, 소개, 사진, 종류, 경도, 위도]). 출력: $OUT_DIR/hub78_i18n.json
키 값은 출력하지 않음."""
import json, os, sys, math, time, re, urllib.request, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from keyfix import key
K = key('TOURAPI_KEY') if os.environ.get('TOURAPI_KEY') else key('DATA_KEY')
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'site', 'index.html')
s = open(SRC, encoding='utf-8').read(); i = s.index('const HUB78 = '); j = s.index('\n', i)
HUB = json.loads(s[i + len('const HUB78 = '):j].rstrip(';'))
SVC = {'en': 'EngService2', 'ja': 'JpnService2', 'zh': 'ChsService2', 'zt': 'ChtService2'}
def call(svc, x, y):
    q = dict(MobileOS='ETC', MobileApp='hoolzzeok', _type='json', mapX=x, mapY=y, radius=400, numOfRows=20, pageNo=1, arrange='E')
    url = f"https://apis.data.go.kr/B551011/{svc}/locationBasedList2?serviceKey={K}&" + urllib.parse.urlencode(q)
    for a in range(4):
        try:
            with urllib.request.urlopen(url, timeout=40) as r: d = json.loads(r.read().decode())
            b = d.get('response', {}).get('body', {}); it = (b.get('items') or {}) if isinstance(b.get('items'), dict) else {}
            it = it.get('item', []); return it if isinstance(it, list) else [it]
        except Exception as e: err = e; time.sleep(2 + a)
    print('오류', svc, str(err)[:80], flush=True); return []
def dist(a, b): return math.hypot((a[0] - b[0]) * 88.0, (a[1] - b[1]) * 111.0)
out = {L: {} for L in SVC}; hit = {L: 0 for L in SVC}; n = 0
for pid, v in HUB.items():
    for ko, t in v['t'].items():
        x, y = t[5], t[6]
        if not x or not y: continue
        n += 1
        for L, svc in SVC.items():
            best = None
            for r in call(svc, x, y):
                if str(r.get('contenttypeid')) in ('77', '80', '82', '85'): continue   # 교통·숙박·음식점·행사는 빼고
                try: dd = dist((float(r['mapx']), float(r['mapy'])), (x, y))
                except Exception: continue
                if dd <= 0.3 and (best is None or dd < best[0]): best = (dd, r.get('title', '').strip())
            if best and best[1]:
                out[L].setdefault(pid, {})[ko] = [re.sub(r'\s+', ' ', best[1])]; hit[L] += 1
            time.sleep(0.05)
od = os.environ.get('OUT_DIR', '.'); os.makedirs(od, exist_ok=True)
json.dump(out, open(os.path.join(od, 'hub78_i18n.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print('명소', n, '찾음', hit)
