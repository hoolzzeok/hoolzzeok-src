#!/usr/bin/env python3
"""코스 동네 착한가격 밥집 → 일반음식점 인허가 API로 좌표·전화번호. DATA_KEY 환경변수. 8개 동시 조회."""
import os,json,re,time,urllib.request,urllib.parse,sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from epsg5174 import to_wgs84
K=__import__('sys').path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..')) or __import__('keyfix').key('DATA_KEY'); BASE="https://apis.data.go.kr/1741000/general_restaurants/info"
def get(name):
    q=f"serviceKey={K}&pageNo=1&numOfRows=50&returnType=json&"+urllib.parse.urlencode({"cond[BPLC_NM::EQ]":name})
    for a in range(3):
        try:
            with urllib.request.urlopen(BASE+"?"+q,timeout=90) as r: d=json.loads(r.read().decode())
            it=(d["response"]["body"].get("items") or {}).get("item",[]); return it if isinstance(it,list) else [it]
        except Exception as e: err=e; time.sleep(3+a)
    raise err
def rk(a):
    m=re.search(r"([가-힣0-9A-Za-z.]+(?:로|길))\s*(\d+(?:-\d+)?)",a or ""); return (m.group(1),m.group(2)) if m else None
rows=json.load(open(sys.argv[1] if len(sys.argv)>1 else 'eat_cand.json')); out=json.load(open('eat_coords.json')) if os.path.exists('eat_coords.json') else {}
todo=[r for r in rows if r['id'] not in out or (isinstance(out[r['id']],dict) and 'err' in out[r['id']])]
def work(r):
    try: items=get(r['name'])
    except Exception as e: return r['id'],{'err':str(e)[:80]}
    k=rk(r['address'])
    for i in items:
        if "폐업" in (i.get("SALS_STTS_NM") or ""): continue
        if k and rk(i.get("ROAD_NM_ADDR"))==k and i.get("CRD_INFO_X"):
            try: lat,lon=to_wgs84(i["CRD_INFO_X"],i["CRD_INFO_Y"])
            except Exception: continue
            return r['id'],{'lat':lat,'lon':lon,'tel':(i.get('TELNO') or '').strip()}
    return r['id'],None
n=0
with ThreadPoolExecutor(12) as ex:
    for rid,v in ex.map(work,todo):
        out[rid]=v; n+=1
        if n%10==0: json.dump(out,open('eat_coords.json','w'),ensure_ascii=False); print(n,'/',len(todo),flush=True)
json.dump(out,open('eat_coords.json','w'),ensure_ascii=False)
ok=[v for v in out.values() if v and 'lat' in v]; print('done',len(out),'좌표',len(ok),'전화',sum(1 for v in ok if v['tel']))
