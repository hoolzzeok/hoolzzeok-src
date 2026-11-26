import os,json,time,urllib.request,urllib.parse
K=__import__('sys').path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..')) or __import__('keyfix').key('DATA_KEY'); BASE='202610'
codes=json.load(open('../datalab/codes.json'))['locgo']; need=json.load(open('need.json'))
def get(code):
    u='https://apis.data.go.kr/B551011/TarRlteTarService1/areaBasedList1?'+urllib.parse.urlencode(dict(serviceKey=K,MobileOS='ETC',MobileApp='hz',_type='json',numOfRows=2000,pageNo=1,baseYm=BASE,areaCd=code[:2],signguCd=code),safe='%')
    for t in range(4):
        try:
            it=json.loads(urllib.request.urlopen(u,timeout=60).read().decode())['response']['body']['items']; return it['item'] if it else []
        except Exception as e: print('retry',code,e); time.sleep(3)
    return None
for code in need:
    fn=f'raw/{code}.json'
    cur=json.load(open(fn)) if os.path.exists(fn) else None
    if cur: continue
    subs=[c for c in codes if c[:4]==code[:4] and c!=code and c[4]!='0'] if code.endswith('0') else []
    rows=[]
    for c in ([code] if cur is None else [])+subs:
        r=get(c); rows+= r or []; time.sleep(0.2)
    json.dump(rows,open(fn,'w'),ensure_ascii=False); print(code,subs,len(rows))
