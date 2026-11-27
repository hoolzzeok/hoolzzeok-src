"""중기예보 진단: 어떤 조합에서 자료가 오는지 결과 코드만 출력(키는 출력 안 함)."""
import json, datetime, urllib.request, urllib.parse, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from keyfix import key
K = key('DATA_KEY')
def call(path, **q):
    url = f"https://apis.data.go.kr/1360000/{path}?serviceKey={K}&" + urllib.parse.urlencode(dict(dataType='JSON', pageNo=1, numOfRows=10, **q))
    try:
        with urllib.request.urlopen(url, timeout=40) as r: raw = r.read().decode()
        try:
            d = json.loads(raw); h = d['response']['header']; n = d['response'].get('body', {}).get('totalCount')
            it = d['response'].get('body', {}).get('items', {}) or {}
            it = it.get('item') if isinstance(it, dict) else it
            keys = sorted((it[0] if isinstance(it, list) else it or {}).keys())[:12] if it else []
            return f"{h['resultCode']} {h['resultMsg']} n={n} keys={keys}"
        except Exception: return 'RAW ' + raw[:160].replace('\n', ' ')
    except Exception as e: return 'ERR ' + str(e)[:120]
KST = datetime.timezone(datetime.timedelta(hours=9)); now = datetime.datetime.now(KST)
d0 = now.strftime('%Y%m%d'); d1 = (now - datetime.timedelta(days=1)).strftime('%Y%m%d')
for tm in (d0 + '0600', d1 + '1800', d1 + '0600'):
    print('Land 11B00000', tm, call('MidFcstInfoService/getMidLandFcst', regId='11B00000', tmFc=tm))
    print('Ta 11B10101', tm, call('MidFcstInfoService/getMidTa', regId='11B10101', tmFc=tm))
    print('Fcst 108', tm, call('MidFcstInfoService/getMidFcst', stnId='108', tmFc=tm))
