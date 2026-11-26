"""공공데이터포털 호출 도우미 (키는 환경변수에서만 읽음, 출력·저장 안 함)."""
import json, sys, time, urllib.request, urllib.parse, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from keyfix import key
GAP = 0.15
_last = [0.0]
def call(base, op, keyname="TOURAPI_KEY", **params):
    wait = GAP - (time.time() - _last[0])
    if wait > 0: time.sleep(wait)
    p = {"MobileOS": "ETC", "MobileApp": "hoolzzeok", "_type": "json"}
    p.update({k: v for k, v in params.items() if v is not None})
    url = f"{base}/{op}?serviceKey={key(keyname)}&" + urllib.parse.urlencode(p)
    for i in range(3):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                raw = r.read().decode("utf-8", "replace")
            break
        except Exception as e:
            err = type(e).__name__ + ":" + str(getattr(e, "code", ""))
            raw = None
            time.sleep(1 + i)
        finally:
            _last[0] = time.time()
    if raw is None:
        return {"_error": err}
    try:
        return json.loads(raw)
    except Exception:
        return {"_error": "nonjson", "_raw": raw[:300].replace(key(keyname), "***")}
def items(res):
    try:
        it = res["response"]["body"]["items"]
        if not it: return []
        it = it["item"]
        return it if isinstance(it, list) else [it]
    except Exception:
        return []
def total(res):
    try: return int(res["response"]["body"]["totalCount"])
    except Exception: return None
def header(res):
    try: return res["response"]["header"]
    except Exception: return res.get("_error") or res.get("_raw") or str(res)[:200]
