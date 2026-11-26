#!/usr/bin/env python3
"""명소 운영시간·쉬는 날·문의전화·주차 (KorService2 detailIntro2). TOURAPI_KEY 환경변수. 결과 out/spots_intro.json"""
import os,json,time,urllib.request,urllib.parse
K=__import__('sys').path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..')) or __import__('keyfix').key('TOURAPI_KEY')
def call(op,**p):
    u=f"https://apis.data.go.kr/B551011/KorService2/{op}?serviceKey={K}&MobileOS=ETC&MobileApp=hoolzzeok&_type=json&"+urllib.parse.urlencode(p)
    for a in range(3):
        try:
            with urllib.request.urlopen(u,timeout=40) as r: d=json.loads(r.read().decode())
            it=d['response']['body']['items']; it=it['item'] if isinstance(it,dict) else []
            return it[0] if it else {}
        except Exception as e: err=e; time.sleep(2+a)
    raise err
F={'12':('usetime','restdate','infocenter','parking'),'14':('usetimeculture','restdateculture','infocenterculture','parkingculture'),
   '28':('usetimeleports','restdateleports','infocenterleports','parkingleports'),'38':('opentime','restdateshopping','infocentershopping','parkingshopping')}
m=json.load(open('out/spots_matched.json')); out={}
p='out/spots_intro.json'
if os.path.exists(p): out=json.load(open(p))
for x in m:
    if not x['match']: continue
    cid=x['match']['contentid']; ct=x['match']['contenttypeid']
    if cid in out: continue
    try: r=call('detailIntro2',contentId=cid,contentTypeId=ct)
    except Exception as e: print('ERR',cid,e); continue
    f=F.get(ct,F['12']); out[cid]={'place':x['place'],'spot':x['spot'],'ct':ct,'use':r.get(f[0],''),'rest':r.get(f[1],''),'tel':r.get(f[2],''),'park':r.get(f[3],''),'fee':r.get('usefee','')}
    json.dump(out,open(p,'w'),ensure_ascii=False); time.sleep(.15)
print('done',len(out))
