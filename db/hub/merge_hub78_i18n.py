"""HUB78 외국어 이름(fetch_hub78_names.py 결과)을 site/index.html 의 `const HUB78_I18N = …;` 한 줄로 넣음.
화면에서는 TOUR_I18N(일·중 이름)과 지역 명소 목록의 영어 이름(s[1])에 합쳐서 씀. 자료가 없으면 빈 객체."""
import json, sys, os, re
src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), 'hub78_i18n.json')
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'site', 'index.html')
d = json.load(open(src, encoding='utf-8')) if os.path.exists(src) else {}
def clean(t):
    """한글 표기 괄호를 지움: '海印寺（陜川）（해인사（합천））' → '海印寺（陜川）'"""
    for _ in range(3): t = re.sub(r'[(（][^()（）]*[가-힣][^()（）]*[)）]', '', t)
    t = re.sub(r'[가-힣][가-힣0-9 ·]*', '', t)
    t = re.sub(r'[(（]\s*[)）]', '', t); t = re.sub(r'\s+', ' ', t).strip(' -·')
    return t
out = {L: {pid: {k: clean(v[0]) for k, v in m.items() if clean(v[0])} for pid, m in d.get(L, {}).items()} for L in ('en', 'ja', 'zh')}
line = 'const HUB78_I18N = ' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';'
s = open(P, encoding='utf-8').read()
if re.search(r'^const HUB78_I18N = .*;$', s, re.M): s = re.sub(r'^const HUB78_I18N = .*;$', lambda m: line, s, count=1, flags=re.M)
else:
    i = s.index('const TOUR_I18N = '); j = s.index('\n', i) + 1
    s = s[:j] + line + '\n' + '''/* v148: 군 지역 명소(HUB78) 외국어 이름 — 관광공사 영·일·중 서비스에서 좌표 300m 안 같은 곳(교통·숙박·음식점·행사 제외) */
for (const [L, m] of Object.entries(HUB78_I18N)) for (const [pid, names] of Object.entries(m)) {
  if (L === "en") { const sp = (INFO[pid] || {}).spots || []; sp.forEach(a => { if (names[a[0]] && a[1] === a[0]) a[1] = names[a[0]]; }); continue; }
  TOUR_I18N[L] = TOUR_I18N[L] || {}; TOUR_I18N[L][pid] = TOUR_I18N[L][pid] || {};
  for (const [ko, nm] of Object.entries(names)) if (!TOUR_I18N[L][pid][ko]) TOUR_I18N[L][pid][ko] = [nm, ""];
}
''' + s[j:]
open(P, 'w', encoding='utf-8').write(s)
print('HUB78_I18N', {L: sum(len(x) for x in out[L].values()) for L in out})
