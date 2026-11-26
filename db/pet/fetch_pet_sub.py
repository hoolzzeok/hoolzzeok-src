import os,json,time,urllib.request,urllib.parse
K=__import__('sys').path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..')) or __import__('keyfix').key('DATA_KEY')
P=json.load(open('../datalab/placemap.json'))['map']; L=json.load(open('../names/ldong.json'))['KorService2']['sgg']
def get(rc,sc=None):
    q=dict(serviceKey=K,MobileOS='ETC',MobileApp='hz',_type='json',numOfRows=1000,pageNo=1,arrange='C',lDongRegnCd=rc)
    if sc: q['lDongSignguCd']=sc
    u='https://apis.data.go.kr/B551011/KorPetTourService2/areaBasedList2?'+urllib.parse.urlencode(q,safe='%')
    for t in range(4):
        try:
            it=json.loads(urllib.request.urlopen(u,timeout=60).read().decode())['response']['body']['items']; return it['item'] if it else []
        except Exception as e: time.sleep(3)
    return []
for pid,(k,c) in P.items():
    fn=f'raw/{pid}.json'; d=json.load(open(fn))
    if d['items']: continue
    rows=[]
    if pid=='sejong': rows=get('36110')
    elif c.endswith('0'):
        for s in [x for x in L.get(c[:2],{}) if x[:2]==c[2:4] and x!=c[2:]]: rows+=get(c[:2],s); time.sleep(0.15)
    if rows: json.dump({'total':len(rows),'items':rows},open(fn,'w'),ensure_ascii=False); print(pid,len(rows))
