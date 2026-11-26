#!/usr/bin/env python3
"""v136: 외국인 딸깍 일정 확장 — 서울 쇼핑·K팝, 수원 당일치기, 제주 3코스, 전주·강릉 코스.
좌표: 관광공사 TourAPI(spots_matched) > 관광공사 중심관광지(hub, 2026-10) > 근사값(명동·성수·서울숲·동문시장, 표시 'approx').
운영시간: 관광공사 소개정보(대한민국 구석구석) 2026-11 웹 확인값. 멱등."""
import json, glob, csv
D = '.'
cdef = json.load(open('course_def.json', encoding='utf-8')); spots = json.load(open('spots.json', encoding='utf-8'))
eats = json.load(open('eat_cand.json', encoding='utf-8'))
hub = {}
for f in glob.glob('../hub/raw/*.json'):
    for x in json.load(open(f)): hub.setdefault(x['hubTatsNm'], (float(x['mapY']), float(x['mapX'])))
mt = {r['spot']: r['match'] for r in json.load(open('../tourapi/out/spots_matched.json')) if r.get('match')}

def sp(pid, key, en, src, approx=None, addr=''):
    if isinstance(src, str) and src.startswith('m:'):
        m = mt[src[2:]]; e = {"place": pid, "want": key, "cid": m['contentid'], "ct": m['contenttypeid'], "title": m['title'], "addr": m.get('addr1', ''),
             "lat": float(m['mapy']), "lon": float(m['mapx']), "img": m.get('firstimage') or '', "cpy": m.get('cpyrhtDivCd') or '', "overview": m.get('overview') or ''}
    elif isinstance(src, str) and src.startswith('h:'):
        la, lo = hub[src[2:]]; e = {"place": pid, "want": key, "cid": f"hub-{key}", "title": key, "addr": addr, "lat": la, "lon": lo, "img": "", "cpy": "", "overview": ""}
    else:
        la, lo = approx; e = {"place": pid, "want": key, "cid": f"approx-{key}", "title": key, "addr": addr, "lat": la, "lon": lo, "img": "", "cpy": "", "overview": "", "approx": True}
    spots[f"{pid}|{key}"] = e; cdef['names'][key] = [en]

S = [  # (pid, 한국어 이름, 영어 이름, 출처, 근사 좌표, 주소)
 ('seoul', '명동거리', 'Myeong-dong shopping street', None, (37.5637, 126.9857), '서울특별시 중구 명동길 일대'),
 ('seoul', '성수동 카페거리', 'Seongsu-dong cafés & pop-up stores', None, (37.5443, 127.0558), '서울특별시 성동구 연무장길 일대'),
 ('seoul', '서울숲', 'Seoul Forest', None, (37.5444, 127.0374), '서울특별시 성동구 뚝섬로 273'),
 ('seoul', '별마당도서관', 'Starfield Library (COEX Mall)', 'h:스타필드/코엑스몰', None, '서울특별시 강남구 영동대로 513 코엑스몰'),
 ('seoul', '봉은사', 'Bongeunsa Temple', 'h:봉은사', None, '서울특별시 강남구 봉은사로 531'),
 ('seoul', '홍대 걷고싶은거리', 'Hongdae street (shops & buskers)', 'h:홍대클럽거리', None, '서울특별시 마포구 어울마당로 일대'),
 ('suwon', '화성행궁', 'Hwaseong Haenggung Palace', 'm:화성행궁', None, ''),
 ('suwon', '수원화성', 'Suwon Hwaseong Fortress wall walk', 'm:수원화성 (유네스코 세계유산)', None, ''),
 ('suwon', '행리단길', 'Haengridan-gil café streets', 'm:행리단길', None, ''),
 ('suwon', '통닭거리', 'Suwon Fried Chicken Street', 'm:통닭거리', None, ''),
 ('jeju', '성산일출봉', 'Seongsan Ilchulbong (Sunrise Peak)', 'm:성산일출봉 (유네스코 세계유산)', None, ''),
 ('jeju', '성읍민속마을', 'Seongeup Folk Village', 'h:성읍민속마을', None, '제주특별자치도 서귀포시 표선면 성읍리'),
 ('jeju', '월정리해변', 'Woljeong-ri Beach', 'h:월정리해변', None, '제주특별자치도 제주시 구좌읍 월정리'),
 ('jeju', '함덕해수욕장', 'Hamdeok Beach', 'h:함덕해수욕장', None, '제주특별자치도 제주시 조천읍 함덕리'),
 ('jeju', '오설록티뮤지엄', "O'sulloc Tea Museum", 'h:오설록티뮤지엄', None, '제주특별자치도 서귀포시 안덕면 신화역사로 15'),
 ('jeju', '카멜리아힐', 'Camellia Hill', 'h:카멜리아힐', None, '제주특별자치도 서귀포시 안덕면 병악로 166'),
 ('jeju', '주상절리대', 'Jusangjeolli Cliff (Daepo)', 'h:주상절리대', None, '제주특별자치도 서귀포시 이어도로 36-24'),
 ('jeju', '천지연폭포', 'Cheonjiyeon Waterfall', 'm:천지연폭포', None, ''),
 ('jeju', '용두암', 'Yongduam (Dragon Head Rock)', 'm:용두암', None, ''),
 ('jeju', '이호테우해변', 'Iho Tewoo Beach', 'h:이호테우해변', None, '제주특별자치도 제주시 이호일동'),
 ('jeju', '협재해수욕장', 'Hyeopjae Beach', 'm:협재해수욕장', None, ''),
 ('jeju', '동문시장', 'Dongmun Market', None, (33.5126, 126.5266), '제주특별자치도 제주시 관덕로14길 20'),
 ('jeonju', '경기전', 'Gyeonggijeon Shrine', 'm:경기전', None, ''),
 ('jeonju', '전동성당', 'Jeondong Catholic Church', 'm:전동성당', None, ''),
 ('jeonju', '전주한옥마을', 'Jeonju Hanok Village', 'h:전주한옥마을', None, '전북특별자치도 전주시 완산구 기린대로 99'),
 ('jeonju', '오목대', 'Omokdae Pavilion', 'h:오목대', None, '전북특별자치도 전주시 완산구 기린대로 55'),
 ('jeonju', '남부시장', 'Nambu Market', 'm:남부시장 야시장', None, ''),
 ('gangneung', '오죽헌', 'Ojukheon House', 'h:오죽헌', None, '강원특별자치도 강릉시 율곡로3139번길 24'),
 ('gangneung', '경포대', 'Gyeongpodae Pavilion', 'm:경포대 · 경포해변', None, ''),
 ('gangneung', '경포해변', 'Gyeongpo Beach', 'h:경포해변', None, '강원특별자치도 강릉시 강문동'),
 ('gangneung', '안목해변 커피거리', 'Anmok Beach Coffee Street', 'm:안목해변 커피거리', None, ''),
 ('gangneung', '강릉중앙시장', 'Gangneung Jungang Market', 'h:강릉중앙시장', None, '강원특별자치도 강릉시 금성로 21'),
]
for pid, k, en, src, ap, ad in S: sp(pid, k, en, src, ap, ad)

F = {
 "명동거리": {"h": "상시 (가게마다 다름)"}, "성수동 카페거리": {"h": "상시 (가게마다 다름)"}, "서울숲": {"h": "상시"},
 "별마당도서관": {"h": "10:30~22:00 · 무료", "open": "10:30"}, "봉은사": {"h": "09:00~18:00 · 무료"}, "홍대 걷고싶은거리": {"h": "상시 (가게마다 다름)"},
 "화성행궁": {"h": "11~2월 09:00~17:00 · 3~10월 09:00~18:00", "close": "17:00"}, "수원화성": {"h": "상시 (성곽길)"}, "행리단길": {"h": "상시 (가게마다 다름)"}, "통닭거리": {"h": "가게마다 다름"},
 "성산일출봉": {"h": "11~2월 06:00~18:00 (매표 17:00) · 매월 첫째 월요일 휴무", "close": "17:00", "offNth": [[1, 1]]},
 "성읍민속마을": {"h": "상시 · 무료 (주민이 사는 마을)"}, "월정리해변": {"h": "상시"}, "함덕해수욕장": {"h": "상시"},
 "오설록티뮤지엄": {"h": "동절기 09:00~18:00 · 무료", "open": "09:00", "close": "18:00"},
 "카멜리아힐": {"h": "11~2월 08:30~18:00 (입장 17:00) · 유료", "open": "08:30", "close": "17:00"},
 "주상절리대": {"h": "09:00~17:30 · 성인 2,000원", "open": "09:00", "close": "17:30"},
 "천지연폭포": {"h": "09:00~22:00 (입장 21:20)", "close": "21:20"}, "용두암": {"h": "상시"}, "이호테우해변": {"h": "상시"}, "협재해수욕장": {"h": "상시"},
 "동문시장": {"h": "08:00~21:00 · 야시장은 저녁"},
 "경기전": {"h": "11~2월 09:00~18:00 (입장 17:00)", "open": "09:00", "close": "17:00"}, "전동성당": {"h": "09:00~17:00", "close": "17:00"},
 "전주한옥마을": {"h": "상시"}, "오목대": {"h": "상시"}, "남부시장": {"h": "점포마다 다름 · 야시장은 금·토 저녁"},
 "오죽헌": {"h": "09:00~18:00 (매표 17:00) · 성인 3,000원", "open": "09:00", "close": "17:00"},
 "경포대": {"h": "상시"}, "경포해변": {"h": "상시"}, "안목해변 커피거리": {"h": "상시 (카페마다 다름)"}, "강릉중앙시장": {"h": "점포마다 다름"},
}
cdef['facts'].update(F)

def C(id, emoji, t, d, start, stops, tags, go, walk=2):
    return {"id": id, "emoji": emoji, "t": dict(zip(["ko", "en", "ja", "zh"], t)), "d": dict(zip(["ko", "en", "ja", "zh"], d)), "walk": walk, "start": start, "stops": stops, "tags": tags, "go": go}
NEW = {
 "seoul": [
  C("shop", "🛍️", ["쇼핑·뷰티", "Shopping & beauty", "ショッピングとビューティー", "购物与美妆"],
    ["명동 화장품 거리에서 성수 팝업까지", "From Myeong-dong beauty shops to Seongsu pop-ups", "明洞のコスメ街から聖水のポップアップまで", "从明洞美妆街到圣水快闪店"], "11:00",
    [["spot", "명동거리", 120], ["meal", "lunch", 60, "명동\\d가|충무로\\d가|을지로\\d가|남산동|회현동|저동"], ["spot", "성수동 카페거리", 120], ["spot", "서울숲", 60], ["meal", "dinner", 60, "성수동\\d가"]],
    ["shop", "food"], {"en": "Subway Line 4 to Myeong-dong Station", "ja": "地下鉄4号線 明洞駅", "zh": "地铁4号线 明洞站", "ko": "지하철 4호선 명동역"}),
  C("kpop", "🎤", ["K팝·젊은 서울", "K-pop & young Seoul", "K-POPと若者のソウル", "K-pop与年轻首尔"],
    ["코엑스 K팝 광장과 별마당도서관, 저녁엔 홍대 거리", "COEX K-pop square and Starfield Library, Hongdae in the evening", "COEXのK-POP広場と図書館、夜は弘大", "COEX K-pop广场与星空图书馆，晚上去弘大"], "10:30",
    [["spot", "별마당도서관", 70], ["spot", "봉은사", 50], ["meal", "lunch", 60, "삼성동|대치동"], ["spot", "홍대 걷고싶은거리", 150], ["meal", "dinner", 60, "서교동|동교동|합정동|연남동"]],
    ["kpop", "shop"], {"en": "Subway Line 2 to Samseong Station (COEX)", "ja": "地下鉄2号線 三成駅（COEX）", "zh": "地铁2号线 三成站（COEX）", "ko": "지하철 2호선 삼성역(코엑스)"}),
 ],
 "suwon": [
  C("fort", "🏰", ["수원 화성 당일치기", "Suwon fortress day trip", "水原華城 日帰り", "水原华城一日游"],
    ["세계유산 성곽길을 걷고 수원 통닭으로 마무리", "Walk the UNESCO fortress wall, end with Suwon fried chicken", "世界遺産の城壁を歩き、水原チキンで締め", "走世界遗产城墙，最后吃水原炸鸡"], "10:30",
    [["spot", "화성행궁", 60], ["meal", "lunch", 60, "남창동|신풍동|장안동|북수동|남수동|팔달로\\d가"], ["spot", "수원화성", 120], ["spot", "행리단길", 60], ["meal", "dinner", 60, ">팔달로\\d가|남수동|영동|교동|매산로\\d가"], ["spot", "통닭거리", 20]],
    ["history", "food"], {"en": "Subway Line 1 or train to Suwon Station (about 1 hour), then taxi 10 min", "ja": "地下鉄1号線か列車で水原駅（約1時間）、タクシー10分", "zh": "坐地铁1号线或火车到水原站（约1小时），再打车10分钟", "ko": "지하철 1호선·열차로 수원역(약 1시간), 택시 10분"}),
 ],
 "jeju": [
  C("east", "🌅", ["성산·동쪽 바다", "Seongsan & east coast", "城山と東の海", "城山与东海岸"],
    ["일출봉에 오르고 돌담 마을, 에메랄드빛 해변으로", "Climb Sunrise Peak, then a stone-wall village and emerald beaches", "日の出峰に登り、石垣の村とエメラルドの海へ", "登日出峰，再去石墙村和翡翠色海滩"], "09:00",
    [["spot", "성산일출봉", 100], ["meal", "lunch", 60, "성산읍"], ["spot", "성읍민속마을", 60], ["spot", "월정리해변", 40], ["spot", "함덕해수욕장", 60], ["meal", "dinner", 60, "조천읍"]],
    ["nature", "history"], {"en": "No subway in Jeju. Taxi, a day taxi tour, or slower buses", "ja": "済州に地下鉄はありません。タクシー・貸切タクシー、または時間のかかるバス", "zh": "济州没有地铁。打车、包车一日游，或较慢的巴士", "ko": "제주는 지하철이 없어요. 택시·택시 투어, 또는 느린 버스"}),
  C("south", "🍵", ["차밭·남쪽 절경", "Tea fields & south coast", "茶畑と南の絶景", "茶园与南部海岸"],
    ["녹차밭과 동백 정원, 주상절리와 폭포", "Green tea fields, a camellia garden, lava cliffs and a waterfall", "緑茶畑と椿の庭、柱状節理と滝", "绿茶园、山茶花园、柱状节理和瀑布"], "09:30",
    [["spot", "오설록티뮤지엄", 60], ["spot", "카멜리아힐", 80], ["meal", "lunch", 60, "안덕면|대정읍"], ["spot", "주상절리대", 40], ["spot", "천지연폭포", 50], ["meal", "dinner", 60, "서귀동|천지동|서홍동|송산동|정방동|중앙동|동홍동"]],
    ["nature", "rest"], {"en": "No subway in Jeju. Taxi, a day taxi tour, or slower buses", "ja": "済州に地下鉄はありません。タクシー・貸切タクシー、または時間のかかるバス", "zh": "济州没有地铁。打车、包车一日游，或较慢的巴士", "ko": "제주는 지하철이 없어요. 택시·택시 투어, 또는 느린 버스"}),
  C("city", "🐟", ["제주 시내·서쪽 해변", "Jeju City & west beaches", "済州市内と西のビーチ", "济州市区与西部海滩"],
    ["용두암과 해변, 저녁은 동문시장 먹거리", "Dragon Head Rock and beaches, dinner at Dongmun Market", "龍頭岩とビーチ、夜は東門市場グルメ", "龙头岩和海滩，晚上去东门市场吃"], "10:00",
    [["spot", "용두암", 30], ["spot", "이호테우해변", 40], ["meal", "lunch", 60, "이호|도두|외도"], ["spot", "협재해수욕장", 90], ["spot", "동문시장", 70], ["meal", "dinner", 60, "일도|이도|삼도|건입동|용담"]],
    ["food", "nature", "shop"], {"en": "No subway in Jeju. Taxi, a day taxi tour, or slower buses", "ja": "済州に地下鉄はありません。タクシー・貸切タクシー、または時間のかかるバス", "zh": "济州没有地铁。打车、包车一日游，或较慢的巴士", "ko": "제주는 지하철이 없어요. 택시·택시 투어, 또는 느린 버스"}),
 ],
 "jeonju": [
  C("hanok", "🏮", ["한옥마을·비빔밥", "Hanok village & bibimbap", "韓屋村とビビンバ", "韩屋村与拌饭"],
    ["왕의 초상을 모신 경기전과 한옥 골목, 오래된 시장", "A royal portrait shrine, hanok lanes and the old market", "王の肖像を祀る慶基殿と韓屋の路地、市場", "供奉国王画像的庆基殿、韩屋小巷和老市场"], "09:30",
    [["spot", "경기전", 60], ["spot", "전동성당", 30], ["meal", "lunch", 60, "풍남동|교동|전동|경원동|중앙동|태평동"], ["spot", "전주한옥마을", 90], ["spot", "오목대", 30], ["spot", "남부시장", 60], ["meal", "dinner", 60, "전동|풍남동|중앙동|경원동|다가동|태평동"]],
    ["history", "food"], {"en": "KTX to Jeonju Station, then taxi 15 min to the Hanok Village", "ja": "KTXで全州駅、韓屋村までタクシー15分", "zh": "坐KTX到全州站，再打车15分钟到韩屋村", "ko": "KTX 전주역, 한옥마을까지 택시 15분"}),
 ],
 "gangneung": [
  C("sea", "☕", ["바다·커피의 도시", "Sea & coffee town", "海とコーヒーの街", "海与咖啡之城"],
    ["오죽헌과 경포 바다, 안목 커피거리, 중앙시장", "Ojukheon, Gyeongpo beach, Anmok coffee street and the market", "烏竹軒と鏡浦の海、安木のコーヒー通り、中央市場", "乌竹轩、镜浦海滩、安木咖啡街和中央市场"], "09:30",
    [["spot", "오죽헌", 70], ["spot", "경포대", 30], ["spot", "경포해변", 40], ["meal", "lunch", 60, "초당동|강문동|포남동|저동"], ["spot", "안목해변 커피거리", 90], ["spot", "강릉중앙시장", 60], ["meal", "dinner", 60, "성남동|임당동|금학동|옥천동|중앙동"]],
    ["nature", "food", "rest"], {"en": "KTX to Gangneung Station, then taxi 10 min", "ja": "KTXで江陵駅、タクシー10分", "zh": "坐KTX到江陵站，再打车10分钟", "ko": "KTX 강릉역, 택시 10분"}),
 ],
}
# 기존 코스에 테마·가는 법 붙이기
OLD = {("seoul", "history"): (["history"], {"en": "Subway Line 3 to Gyeongbokgung Station", "ja": "地下鉄3号線 景福宮駅", "zh": "地铁3号线 景福宫站", "ko": "지하철 3호선 경복궁역"}),
       ("seoul", "market"): (["food", "shop"], {"en": "Subway Line 3 to Gyeongbokgung Station, then a 10-min walk to Tongin Market", "ja": "地下鉄3号線 景福宮駅から通仁市場へ徒歩10分", "zh": "地铁3号线 景福宫站，步行10分钟到通仁市场", "ko": "지하철 3호선 경복궁역, 통인시장까지 걸어서 10분"}),
       ("seoul", "easy"): (["rest", "history"], {"en": "Subway Line 1 or 2 to City Hall Station", "ja": "地下鉄1・2号線 市庁駅", "zh": "地铁1号线或2号线 市厅站", "ko": "지하철 1·2호선 시청역"}),
       ("busan", "sea"): (["nature", "rest"], {"en": "Taxi to Haedong Yonggungsa (about 30 min from Haeundae)", "ja": "海東龍宮寺へタクシー（海雲台から約30分）", "zh": "打车去海东龙宫寺（从海云台约30分钟）", "ko": "해동용궁사까지 택시(해운대에서 약 30분)"}),
       ("busan", "oldtown"): (["food", "shop", "history"], {"en": "Subway Line 1 to Toseong Station, then a short bus or taxi up to Gamcheon", "ja": "地下鉄1号線 土城駅からバスかタクシーで甘川へ", "zh": "地铁1号线 土城站，再坐公交或打车上甘川", "ko": "지하철 1호선 토성역, 감천까지 마을버스·택시"}),
       ("busan", "easy"): (["rest", "nature"], {"en": "Taxi or bus to Songdo Beach (cable car)", "ja": "松島海水浴場（ケーブルカー）へタクシーかバス", "zh": "打车或坐公交到松岛海水浴场（缆车）", "ko": "송도해수욕장(케이블카)까지 택시·버스"}),
       ("gyeongju", "history"): (["history"], {"en": "Bus 10 or 11, or taxi, to Bulguksa", "ja": "仏国寺へバス10・11番かタクシー", "zh": "坐10路、11路公交或打车到佛国寺", "ko": "불국사까지 10·11번 버스 또는 택시"}),
       ("gyeongju", "night"): (["history", "food"], {"en": "Taxi or walk to the Gyeongju National Museum", "ja": "国立慶州博物館へタクシーか徒歩", "zh": "打车或步行到国立庆州博物馆", "ko": "국립경주박물관까지 택시·걷기"})}
for pid, cs in cdef['courses'].items():
    for c in cs:
        if (pid, c['id']) in OLD: c['tags'], c['go'] = OLD[(pid, c['id'])]
for pid, cs in NEW.items():
    have = {c['id'] for c in cdef['courses'].get(pid, [])}
    cdef['courses'].setdefault(pid, []).extend([c for c in cs if c['id'] not in have])
    for c in cs:   # 다시 돌려도 최신 정의로
        cdef['courses'][pid] = [c if x['id'] == c['id'] else x for x in cdef['courses'][pid]]

# 밥집 후보: 착한가격업소 중 새 동네(제주는 서귀포 포함 'jeju'로)
have = {r['id'] for r in eats}
AREAS = {"seoul": r"명동|충무로|을지로|남산동|회현동|저동|성수동|삼성동|대치동|서교동|동교동|합정동|연남동", "suwon": ".", "jeju": ".", "seogwipo": ".", "jeonju": ".", "gangneung": "."}
import re
for r in csv.DictReader(open('../seed/goodprice_eateries.csv', encoding='utf-8-sig')):
    p = r['place_id']
    if p in AREAS and r['id'] not in have and re.search(AREAS[p], r['address'] + ' ' + r['neighborhood']):
        r = dict(r); r['place_id'] = 'jeju' if p == 'seogwipo' else p; eats.append(r); have.add(r['id'])
json.dump(cdef, open('course_def.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(spots, open('spots.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(eats, open('eat_cand.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('spots', len(spots), 'eats', len(eats), {p: len(c) for p, c in cdef['courses'].items()})
