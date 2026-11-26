import json,csv,re,os,collections
d=json.load(open('data.json'))
OUT='/home/claude/hoolzzeok_db/seed'
counts={}
def w(name, header, rows):
    rows=list(rows)
    with open(f'{OUT}/{name}.csv','w',encoding='utf-8-sig',newline='') as f:
        c=csv.writer(f); c.writerow(header); c.writerows(rows)
    counts[name]=len(rows)
B=lambda v: 1 if v else 0
# ---------- 0. 출처·정확도 ----------
SRC=[
 ('src_places','시·군 목록과 좌표','자체 정리','', '2026-11','B','바뀔 때만','좌표는 시·군청 부근 대표 좌표. 출처 주소를 남기지 않아 B. 이전 뒤 행정안전부 행정구역 코드와 대조 필요'),
 ('src_halfprice','반값여행 시범 지역 16곳','나라살림연구소·헤럴드경제','https://www.narasallim.net/report/833','2026-03','A','분기','출처 2곳 대조. 지역·조건이 바뀔 수 있어 분기마다 확인'),
 ('src_lodging','숙박 월평균 객실 요금(ADR)','야놀자리서치 2026년 3분기 국내 숙박업 동향 보고서','', '2026-3Q','B','분기','민간 통계 1곳. 1~9월은 2026년, 10~12월은 2025년 값. 평일·주말 구분 없음. 권역 10개 단위'),
 ('src_dorm','게스트하우스 침대 가격','호스텔월드 표시 최저가 표본(서울 19곳, 제주 9곳)','', '2026-11','C','분기','공식 통계 없음. 임시 값'),
 ('src_food','시·도별 외식비 8개 품목','한국소비자원 참가격(행정안전부 조사)','https://www.price.go.kr/','2026-가을','A','월 1회','공식 통계. 세종은 값이 없어 충남 값 사용'),
 ('src_coffee','커피 가격','한국소비자원 커피전문점 조사','', '2024-11','B','연 1회','2년 전 값. 갱신 필요'),
 ('src_citybus','시내버스 요금(카드)','참가격 시·도별 공공요금','https://www.price.go.kr/','2026-가을','A','반기','공식 통계'),
 ('src_taxi','택시 기본요금·거리요금','출처 1곳','', '2026-11','B','반기','출처 1곳뿐. 시·도 고시로 2차 확인 필요'),
 ('src_bus','고속·시외버스 요금 식','실제 요금 8건에 맞춘 식(고정 3,000원 + km당 73원)','', '2026-11','C','반기','실제 요금 6건과 비교 시 오차 −19%~+23%. 노선별 실제 요금표로 바꿔야 함'),
 ('src_car','자차 비용','오피넷 휘발유 평균·에너지공단 평균 연비·고속도로 통행료 식','https://www.opinet.co.kr/','2026-11-11','B','월 1회','기름값은 공식(A)이나 통행료는 식으로 추정, 도로 거리는 직선거리×1.2 가정'),
 ('src_flight','국내선 항공 운임','제주항공 공시 주중 할인운임 총액','', '2026-11','B','월 1회','항공사 1곳. 표에 없는 지방공항은 부산·청주 값으로 가정(C)'),
 ('src_ferry','여객선 운임','선사 공시 정상운임','', '2026-11','B','반기','유류할증료 별도. 제주 노선은 터미널이용료 포함'),
 ('src_events','이달 축제·체험','지자체·언론 보도 6곳','', '2026-11','B','월 1회','손으로 갱신. 날짜 지나면 자동 숨김'),
 ('src_season','제철 특산품 42종','월별 제철음식 표 2곳 대조','', '2026-11','A','연 1회','출처 간 다른 품목은 제외'),
 ('src_acts','전통체험·액티비티 73곳','각 시설 공식 안내(항목마다 주소 기록)','', '2026-11-11','B','분기','항목마다 출처 1곳. 대표 가격 없는 곳 7곳'),
 ('src_contests','접수 중 공모전','지자체 공고·언론 보도(항목마다 주소 기록)','', '2026-11','B','주 1회','마감 지나면 자동 숨김'),
 ('src_souv','기념품 실가격 22곳','온라인몰·가게 메뉴판(항목마다 주소 기록)','', '2026-11-12','B','반기','22곳만 실가격. 나머지 144곳은 중간값 12,000원(C)'),
 ('src_goodprice','착한가격업소 현황','행정안전부(사용자가 준 파일)','', '2026-09-30','A','분기','공식 자료. 이용허락범위는 공개 전 확인 필요. 500원 미만 메뉴 5건·중복 1건 제거'),
 ('src_info','도착지 소개·대표 관광지·먹거리','자체 작성','', '2026-11','B','반기','90곳만 있음(관광지 89곳). 좌표 없음 → TourAPI 연결 예정'),
 ('src_malls','지자체 공식 쇼핑몰','각 쇼핑몰 누리집','', '2026-11-12','B','반기','일부는 검색 결과 제목으로만 확인'),
 ('src_fx','환율','하나은행 매매기준율(인용 기사) + 시장 시세 대조','', '2026-11-13','B','평일 매일','하나은행 사이트 직접 조회 불가 → 인용 기사 사용'),
 ('src_assume','계산 가정값','자체 가정','', '2026-11','C','테스트 뒤','근거 자료 없음. 4060 테스트·후기 자료로 바꿔야 함'),
]
w('data_sources',['id','title','publisher','url','as_of','confidence','refresh_cycle','note'],SRC)
# ---------- 1. 지역 ----------
w('provinces',['code','name_en','lodging_region'],[(k,v,d['LODGE_REGION'].get(k,'')) for k,v in d['PROV_EN'].items()])
half=set(d['HALF'])
w('places',['id','name_ko','name_en','province','lat','lon','tier','kind','island','price_level','half_price_pilot','source_id'],
  [(p['id'],p['ko'],p['en'],p['prov'],p['lat'],p['lon'],p['tier'],p['kind'],p['island'] or '',p['lvl'],B(p['id'] in half),'src_places') for p in d['PLACES']])
I=d['INFO']
w('place_profiles',['place_id','desc_ko','desc_en','note_ko','note_en','festival_ko','festival_en','source_id'],
  [(k,v['desc']['ko'],v['desc']['en'],(v.get('note') or {}).get('ko',''),(v.get('note') or {}).get('en',''),(v.get('fest') or {}).get('ko',''),(v.get('fest') or {}).get('en',''),'src_info') for k,v in I.items()])
w('place_spots',['place_id','seq','name_ko','name_en','is_night_view','lat','lon','tour_api_id'],
  [(k,i+1,s[0],s[1],B('야경' in s[0]),'','','') for k,v in I.items() for i,s in enumerate(v.get('spots') or [])])
w('place_foods',['place_id','seq','name_ko','name_en'],[(k,i+1,s[0],s[1]) for k,v in I.items() for i,s in enumerate(v.get('musts') or [])])
ev=[(f"fest{i+1}",f['place'],'festival',f['ko'],f['en'],f['start'],f['end'],f.get('whereKo',''),f.get('whereEn',''),'src_events') for i,f in enumerate(d['FESTS'])]
ev+=[(f"exp{i+1}",e['place'],'experience',e['ko'],e['en'],'','',e.get('noteKo',''),e.get('noteEn',''),'src_events') for i,e in enumerate(d['EXPS'])]
w('events',['id','place_id','kind','name_ko','name_en','start_date','end_date','detail_ko','detail_en','source_id'],ev)
pk=[(f"ko{i+1}",'ko',r['place'],r.get('until',''),'',r.get('ko',''),r.get('en',''),r.get('ja',''),r.get('zh','')) for i,r in enumerate(d['RECS'])]
pk+=[(f"fr{i+1}",'foreign',r['place'],r.get('until',''),r.get('tag',''),r.get('ko',''),r.get('en',''),r.get('ja',''),r.get('zh','')) for i,r in enumerate(d['FOREIGN_RECS'])]
w('agent_picks',['id','audience','place_id','until','tag','text_ko','text_en','text_ja','text_zh'],pk)
w('season_products',['id','name_ko','name_en','source_id'],[(i+1,s[0],s[1],'src_season') for i,s in enumerate(d['SEASON'])])
w('season_months',['product_id','month'],[(i+1,m) for i,s in enumerate(d['SEASON']) for m in s[2]])
w('season_places',['product_id','place_id'],[(i+1,p) for i,s in enumerate(d['SEASON']) for p in s[3]])
w('activities',['id','place_id','kind','type_ko','type_en','name_ko','price_text','duration_text','note','source_url','source_as_of','rep_price'],
  [(i+1,a[0],'traditional' if a[1]=='t' else 'activity',a[2],d['ACT_TYPE_EN'].get(a[2],''),a[3],a[4],a[5],a[6],a[7],a[8],a[9] or '') for i,a in enumerate(d['ACTS'])])
w('contests',['id','place_id','province','hub_place_id','nationwide','end_date','name_ko','name_en','type_ko','type_en','prize_ko','prize_en','who_ko','who_en','url'],
  [(i+1,c.get('place',''),c.get('prov',''),c.get('hub',''),B(c.get('all')),c['end'],c['ko'],c['en'],c.get('typeKo',''),c.get('typeEn',''),c.get('prizeKo',''),c.get('prizeEn',''),c.get('whoKo',''),c.get('whoEn',''),c.get('url','')) for i,c in enumerate(d['CONTESTS'])])
w('souvenirs',['place_id','name_ko','name_en','price','basis','source_url'],[(k,v[0],v[1],v[2],v[3],v[4] or '') for k,v in d['SOUV'].items()])
# ---------- 2. 가격 ----------
LNAME={'motel':'모텔','hotel':'호텔','pension':'펜션'}
w('lodging_rates',['lodging_type','region','month','adr_krw','data_year','source_id'],
  [(t,r,m+1,a[m],2026 if m<9 else 2025,'src_lodging') for t,v in d['LODGE'].items() for r,a in v.items() for m in range(12)])
w('dorm_bed_rates',['region_key','price','source_id'],[(k,v,'src_dorm') for k,v in d['DORM_BED'].items()])
ITEMS=['냉면','비빔밥','김치찌개백반','삼겹살 200g','자장면','삼계탕','칼국수','김밥']
fp=[(p,ITEMS[i],v[i],'src_food') for p,v in d['FOOD_PRICE'].items() for i in range(8)]
fp+=[('전국','아메리카노',d['COFFEE']['americano'],'src_coffee'),('전국','카페라떼',d['COFFEE']['latte'],'src_coffee')]
w('food_prices',['province','item','price','source_id'],fp)
w('meal_baskets',['style','item','qty','source_id'],[
 ('budget','자장면',1,'src_assume'),('budget','칼국수',1,'src_assume'),('budget','김치찌개백반',1,'src_assume'),('budget','아메리카노',1,'src_assume'),
 ('standard','김치찌개백반',1,'src_assume'),('standard','냉면',1,'src_assume'),('standard','삼겹살 200g',1,'src_assume'),('standard','아메리카노',2,'src_assume'),
 ('comfort','냉면',1,'src_assume'),('comfort','삼겹살 200g',1.5,'src_assume'),('comfort','삼계탕',1,'src_assume'),('comfort','카페라떼',2,'src_assume')])
w('city_bus_fares',['province','fare','source_id'],[(k,v,'src_citybus') for k,v in d['CITY_BUS'].items()])
w('taxi_fares',['province','base_fare','base_km','meters_per_100won','source_id'],[(k,v[0],v[1],v[2],'src_taxi') for k,v in d['TAXI'].items()])
w('flight_fares',['from_place','to_place','fare','basis','source_id'],
  [(k,'jeju',v,'공시 운임','src_flight') for k,v in d['FLIGHT_JEJU'].items()]+[(k.split('-')[0],k.split('-')[1],v,'공시 운임','src_flight') for k,v in d['FLIGHT_MAIN'].items()])
w('ferry_fares',['island_group','port_place_id','fare','source_id'],[(g,p,f,'src_ferry') for g,v in d['FERRY'].items() for p,f in v.items()])
A=[('bus_fixed',d['BUS']['fix'],'원','고속·시외버스 요금 식의 고정분','src_bus'),('bus_per_km',d['BUS']['perKm'],'원/km','고속·시외버스 요금 식의 거리분','src_bus'),
 ('road_factor',d['ROAD_FACTOR'],'배','직선거리 → 도로거리 환산','src_assume'),
 ('fuel_per_l',d['CAR']['fuelPerL'],'원/L','휘발유 전국 평균','src_car'),('km_per_l',d['CAR']['kmPerL'],'km/L','평균 연비','src_car'),
 ('toll_base',d['CAR']['tollBase'],'원','고속도로 기본요금(1종)','src_car'),('toll_per_km',d['CAR']['tollPerKm'],'원/km','고속도로 주행요금(1종)','src_car'),
 ('car_share',d['CAR']['share'],'명','자차 비용을 나누는 인원','src_assume'),
 ('flight_jeju_default',d['FLIGHT_JEJU_EST'],'원','표에 없는 공항의 제주 노선 운임','src_assume'),
 ('half_cap_per_person',d['HALF_CAP_PER_PERSON'],'원','반값여행 1인 환급 한도','src_halfprice'),
 ('taxi_ride_km',d['TAXI_RIDE_KM'],'km','택시 한 번 타는 거리(2명 탑승)','src_assume'),('local_drive_km',d['LOCAL_DRIVE_KM'],'km/일','자차 현지 주행','src_assume'),
 ('souvenir_default',d['SOUV_DEFAULT'],'원','실가격 없는 지역의 기념품 값','src_assume')]
for st,v in d['LOCAL_RIDES'].items(): A+=[(f'bus_rides_{st}',v['bus'],'회/일','하루 버스 횟수','src_assume'),(f'taxi_rides_{st}',v['taxi'],'회/일','하루 택시 횟수','src_assume')]
for st,v in d['SOUV_QTY'].items(): A.append((f'souvenir_qty_{st}',v,'개','여행 한 번 기념품 개수','src_assume'))
w('cost_params',['key','value','unit','note','source_id'],A)
# ---------- 3. 착한가격 ----------
MEAT=re.compile(r'삼겹|갈비|목살|항정|등심|안심|막창|곱창|불고기|흑돼지|생고기|숯불|오리구이|소금구이|양념구이|한우')
NOTG=re.compile(r'탕|찜|국(?!산|내)|만두|도넛|빵|버거|덮밥|비빔')
NOT_MEAL=re.compile(r'김밥|공기밥|공깃밥|사리|추가|음료|커피|아메리카노|라떼|소주|맥주|막걸리|떡볶|튀김|어묵|빵|토스트|핫도그|호떡|와플|도넛|도너츠|아이스|빙수|에이드|주스|쥬스|만두\s*\(?\d*개|떡(?!국|갈비|만둣?국)')
MEAT2=re.compile(r'오리|주물럭|로스|구이|대창|육회|족발|보쌈|수육|양곱창|갈매기살|닭발')
SUB=[('고기구이',None),
 ('국밥·탕·찌개',re.compile(r'국밥|해장국|설렁탕|곰탕|갈비탕|삼계탕|추어탕|감자탕|순대국|육개장|찌개|찌게|청국장|순두부|전골|매운탕|탕$|탕\(|백숙|국$')),
 ('면',re.compile(r'칼국수|국수|냉면|밀면|막국수|우동|라면|쫄면|수제비|짬뽕|짜장|자장|파스타|스파게티|소바')),
 ('백반·정식',re.compile(r'백반|정식|비빔밥|덮밥|볶음밥|쌈밥|한정식|뷔페|도시락|돌솥|보리밥|가정식|제육')),
 ('해산물',re.compile(r'물회|모듬회|생선회|회덮밥|회$|회\(|횟|광어|우럭|생선|조개|해물|아구|아귀|낙지|장어|굴(?!비)|초밥|오징어|주꾸미|쭈꾸미|꼬막|전복|게장|굴비|고등어|갈치')),
 ('치킨·돈가스',re.compile(r'치킨|닭강정|통닭|돈가스|돈까스|닭갈비|찜닭|닭볶음')),
 ('분식',re.compile(r'김밥|떡볶|순대(?!국)|튀김|만두|어묵|토스트|핫도그')),
 ('카페·디저트',re.compile(r'커피|아메리카노|라떼|빵|케이크|와플|빙수|에이드|주스|쥬스|도넛|쿠키|샌드위치|샐러드|스콘|마들렌|마끼아또|쌍화차|[가-힣]차$|스무디|떡(?!국|갈비|볶|만두)'))]
CAT={'k':'한식','c':'중식','j':'일식','w':'양식','e':'기타요식','b':'베이커리'}
def subcat(g):
    menus=[m[0] for m in g[3]]
    if g[1]=='c': return '중식'
    if g[1]=='j': return '일식'
    if g[1]=='w': return '양식'
    if g[1]=='b': return '카페·디저트'
    if g[1]=='e' and any(SUB[-1][1].search(x) for x in menus) and not any(SUB[1][1].search(x) or SUB[2][1].search(x) or SUB[3][1].search(x) for x in menus): return '카페·디저트'
    if any(MEAT.search(x) and not NOTG.search(x) for x in menus) and sum(1 for x in menus if MEAT.search(x) and not NOTG.search(x))*2>=len(menus): return '고기구이'
    sc=collections.Counter()
    for x in menus:
        for name,rx in SUB[1:]:
            if rx.search(x): sc[name]+=1; break
    if not sc: return '고기구이' if any((MEAT.search(x) and not NOTG.search(x)) or MEAT2.search(x) for x in menus) else '기타'
    order=[n for n,_ in SUB]
    return sorted(sc.items(), key=lambda kv:(-kv[1],order.index(kv[0])))[0][0]
def addr_parts(a):
    gu=re.search(r'(?:^|\s)([가-힣]+(?:구|군))\s',a+' '); 
    dong=re.search(r'\(([가-힣0-9]+(?:동|가|리))[,)]',a) or re.search(r'\s([가-힣]+[0-9]?(?:읍|면|동|리))(?=\s|,|$)',a)
    road=re.search(r'([가-힣0-9]+(?:대로|로|길)(?:[0-9]+번?길)?)',a)
    return (gu.group(1) if gu else '', dong.group(1) if dong else '', road.group(1) if road else '')
def band(p):
    return '' if p is None else '5천 원 이하' if p<=5000 else '8천 원 이하' if p<=8000 else '1만 2천 원 이하' if p<=12000 else '1만 2천 원 초과'
E=[];M=[];eid=0
for pid,v in d['GOOD'].items():
    for g in v:
        eid+=1; meals=[m[1] for m in g[3] if m[1]>=3000 and not NOT_MEAL.search(m[0])]
        mm=min(meals) if meals else None; gu,dong,road=addr_parts(g[2])
        grill=any(MEAT.search(m[0]) and not NOTG.search(m[0]) for m in g[3])
        E.append((eid,pid,g[0],CAT[g[1]],subcat(g),g[2],gu,dong,road,mm if mm is not None else '',band(mm),B(any(m[1]>=5000 and not NOT_MEAL.search(m[0]) for m in g[3])),B(grill),'src_goodprice'))
        for i,m in enumerate(g[3]): M.append((eid,i+1,m[0],m[1],B(m[1]>=3000 and not NOT_MEAL.search(m[0]))))
w('goodprice_eateries',['id','place_id','name','category','subcategory','address','district','neighborhood','road','min_meal_price','price_band','is_full_meal','has_grill','source_id'],E)
w('goodprice_menus',['eatery_id','seq','menu','price','is_meal'],M)
S=[];R=[];sid=0
for pid,v in d['GOOD_STAY'].items():
    for s in v:
        sid+=1; gu,dong,road=addr_parts(s[2])
        S.append((sid,pid,s[0],s[1],s[2],gu,dong,road,'src_goodprice'))
        for i,m in enumerate(s[3]): R.append((sid,i+1,m[0],m[1]))
w('goodprice_stays',['id','place_id','name','min_night_price','address','district','neighborhood','road','source_id'],S)
w('goodprice_stay_rates',['stay_id','seq','item','price'],R)
# ---------- 4. 그 밖 ----------
w('official_malls',['scope','scope_key','name','description','url','source_id'],[('province',k,v[0],v[1],v[2],'src_malls') for k,v in d['MALL'].items()]+[('place',k,v[0],v[1],v[2],'src_malls') for k,v in d['MALL_PLACE'].items()])
w('checklist_items',['key','audience','name','reason','partner','affiliate_url'],[(k,'ko',v[0],v[1],'coupang','') for k,v in d['SHOP_KO'].items()]+[(k,'foreign',v[0],v[1],'klook','') for k,v in d['SHOP_EN'].items()])
fx=d['FX']; w('fx_rates',['rate_date','currency','krw_per_unit','source'],[(fx['date'],'USD',fx['usd'],fx['src']),(fx['date'],'JPY',round(fx['jpy100']/100,4),fx['src']),(fx['date'],'CNY',fx['cny'],fx['src'])])
json.dump(counts,open('counts.json','w'),ensure_ascii=False)
for k,v in counts.items(): print(f'{k:24}{v:>7}')
sub=collections.Counter(e[4] for e in E); print('세부 분류',sub.most_common())
print('구·군 파싱',sum(1 for e in E if e[6]),'동 파싱',sum(1 for e in E if e[7]),'도로 파싱',sum(1 for e in E if e[8]),'/',len(E))
print('가격대',collections.Counter(e[10] for e in E).most_common())
