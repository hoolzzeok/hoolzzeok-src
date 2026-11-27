"""경비 의견 표(cost_feedback) 확인: 시험 한 건 넣기(est=0 표시), 읽기는 막혔는지. 키 값은 출력 안 함(공개 키라도)."""
import json, os, urllib.request
c = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'supa_config.json')))
row = {"origin": "seoul", "dest": "yeosu", "nights": 1, "people": 2, "mode": "transit", "style": "standard", "est": 0, "verdict": "same", "actual": None, "lang": "ko"}
def go(req):
    try:
        r = urllib.request.urlopen(req, timeout=20); return r.status, r.read().decode()[:120]
    except Exception as e:
        return getattr(e, 'code', 'ERR'), (e.read().decode()[:160] if hasattr(e, 'read') else str(e)[:160])
print('넣기', go(urllib.request.Request(c['url'] + '/rest/v1/cost_feedback', data=json.dumps(row).encode(), method='POST', headers={'apikey': c['key'], 'Content-Type': 'application/json', 'Prefer': 'return=minimal'})))
print('읽기(막혀야 함)', go(urllib.request.Request(c['url'] + '/rest/v1/cost_feedback?select=id&limit=1', headers={'apikey': c['key']})))
bad = dict(row, verdict="wow")
print('틀린 값(거절돼야 함)', go(urllib.request.Request(c['url'] + '/rest/v1/cost_feedback', data=json.dumps(bad).encode(), method='POST', headers={'apikey': c['key'], 'Content-Type': 'application/json', 'Prefer': 'return=minimal'})))
