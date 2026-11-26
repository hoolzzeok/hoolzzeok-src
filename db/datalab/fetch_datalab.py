#!/usr/bin/env python3
"""한국관광공사 빅데이터 지역별 방문자수(DataLabService) → raw/locgo.json, raw/metco.json
사용: DATA_KEY=<일반 인증키> python3 fetch_datalab.py 20251001 20261019
값: {code: {yyyymmdd: [현지인, 외지인, 외국인]}}"""
import os,sys,json,time,urllib.request,urllib.parse,datetime as dt
K=__import__('sys').path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..')) or __import__('keyfix').key('DATA_KEY'); A,B=sys.argv[1],sys.argv[2]
D=os.path.dirname(os.path.abspath(__file__)); os.makedirs(f'{D}/raw',exist_ok=True)
def call(op,s,e,rows):
    p=dict(serviceKey=K,MobileOS='ETC',MobileApp='hz',_type='json',numOfRows=rows,pageNo=1,startYmd=s,endYmd=e)
    u=f'https://apis.data.go.kr/B551011/DataLabService/{op}?'+urllib.parse.urlencode(p,safe='%')
    for t in range(4):
        try:
            d=json.loads(urllib.request.urlopen(u,timeout=120).read().decode())['response']
            if d['header']['resultCode']!='0000': raise RuntimeError(d['header'])
            it=d['body']['items']; return it['item'] if it else []
        except Exception as ex:
            print('retry',op,s,ex); time.sleep(3+t*3)
    raise SystemExit('실패 '+s)
def run(op,key,step,rows,fn):
    out=json.load(open(fn)) if os.path.exists(fn) else {}
    d=dt.date(int(A[:4]),int(A[4:6]),int(A[6:])); end=dt.date(int(B[:4]),int(B[4:6]),int(B[6:]))
    while d<=end:
        e=min(end,d+dt.timedelta(days=step-1)); s,ee=d.strftime('%Y%m%d'),e.strftime('%Y%m%d')
        if all(s2 in next(iter(out.values()),{}) for s2 in [s,ee]) : d=e+dt.timedelta(days=1); continue
        for r in call(op,s,ee,rows):
            v=out.setdefault(r[key],{}).setdefault(r['baseYmd'],[None,None,None]); v[int(r['touDivCd'])-1]=round(float(r['touNum']))
        json.dump(out,open(fn,'w'),separators=(',',':')); print(op,s,ee,len(out)); d=e+dt.timedelta(days=1); time.sleep(0.3)
run('metcoRegnVisitrDDList','areaCode',90,10000,f'{D}/raw/metco.json')
run('locgoRegnVisitrDDList','signguCode',7,10000,f'{D}/raw/locgo.json')
print('끝')
