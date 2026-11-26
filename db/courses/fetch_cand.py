#!/usr/bin/env python3
"""코스 후보 명소 → TourAPI(KorService2) 공식 이름·좌표·주소·소개·운영시간·쉬는날·사진. TOURAPI_KEY 환경변수."""
import os,json,re,time,math,urllib.request,urllib.parse,html
K=__import__('sys').path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..')) or __import__('keyfix').key('TOURAPI_KEY')
def call(op,**p):
    u=f"https://apis.data.go.kr/B551011/KorService2/{op}?serviceKey={K}&MobileOS=ETC&MobileApp=hoolzzeok&_type=json&"+urllib.parse.urlencode(p)
    for a in range(3):
        try:
            with urllib.request.urlopen(u,timeout=40) as r: d=json.loads(r.read().decode())
            it=d['response']['body']['items']; it=it['item'] if isinstance(it,dict) else []
            return it if isinstance(it,list) else [it]
        except Exception as e: err=e; time.sleep(2+a)
    raise err
def km(a,b,c,d):
    R=6371;t=math.radians;h=math.sin(t(c-a)/2)**2+math.cos(t(a))*math.cos(t(c))*math.sin(t(d-b)/2)**2;return 2*R*math.asin(math.sqrt(h))
norm=lambda s:re.sub(r"[\s()\[\]·,.\-]","",s or "")
F={'12':('usetime','restdate','infocenter','parking'),'14':('usetimeculture','restdateculture','infocenterculture','parkingculture'),
   '28':('usetimeleports','restdateleports','infocenterleports','parkingleports'),'38':('opentime','restdateshopping','infocentershopping','parkingshopping')}
cand=json.load(open('cand.json')); out=json.load(open('spots.json')) if os.path.exists('spots.json') else {}
for pid,(lat,lon,names) in cand.items():
    for n in names:
        key=f"{pid}|{n}"
        if key in out: continue
        items=call('searchKeyword2',keyword=n,numOfRows=30,pageNo=1,arrange='A'); time.sleep(.15)
        best=None
        for i in items:
            if i.get('contenttypeid') not in F: continue
            try: d=km(lat,lon,float(i['mapy']),float(i['mapx']))
            except: continue
            if d>40: continue
            t,w=norm(i['title']),norm(n)
            s=100 if t==w else 70 if (t.startswith(w) or w.startswith(t)) else 50 if (w in t or t in w) else 0
            if not s: continue
            if best is None or s-d>best[0]: best=(s-d,i)
        if not best: out[key]=None; print('NOMATCH',key); continue
        i=best[1]; cid=i['contentid']; ct=i['contenttypeid']
        c=(call('detailCommon2',contentId=cid) or [{}])[0]; time.sleep(.15)
        r=(call('detailIntro2',contentId=cid,contentTypeId=ct) or [{}])[0]; time.sleep(.15)
        f=F[ct]; ov=html.unescape(re.sub(r"<[^>]+>"," ",c.get('overview',''))); ov=re.sub(r"\s+"," ",ov).strip()
        out[key]={'place':pid,'want':n,'cid':cid,'ct':ct,'title':i['title'],'addr':i.get('addr1',''),'lat':float(i['mapy']),'lon':float(i['mapx']),
          'img':i.get('firstimage2') or i.get('firstimage') or '','cpy':i.get('cpyrhtDivCd') or c.get('cpyrhtDivCd',''),'overview':ov,
          'use':r.get(f[0],''),'rest':r.get(f[1],''),'tel':r.get(f[2],''),'park':r.get(f[3],''),'fee':r.get('usefee','')}
        print('OK',key,'->',i['title'])
        json.dump(out,open('spots.json','w'),ensure_ascii=False,indent=0)
print('done',sum(1 for v in out.values() if v),'/',len(out))
