#!/usr/bin/env python3
"""착한가격 메뉴 이름 → 영·일·중 표기.
1순위: 한식진흥원 「한식메뉴 외국어표기 길라잡이 800선」(2023-06-01) 파일
2순위: 부산광역시 올랭 메뉴 외국어 표기사전 API(MenuLangService, 800선 + 부산 27개)
3순위: 같은 음식의 다른 표기(짜장면→자장면 등)는 공식 항목으로 연결(ALIAS)
4순위: 한식이 아닌 흔한 메뉴(커피·우동·돈가스 등)만 훌쩍 자체 표기(OWN). 그 밖은 번역하지 않음
"""
import json,re,sys
from collections import Counter
H=json.load(open('hansik800.json')); B=json.load(open('busan_menu.json'))
D={}
for x in H: D.setdefault(x['ko'].replace(' ',''),[x['en'].strip(),x['ja'].strip(),x['zh'].strip()])
for x in B: D.setdefault(x['menuNm'].replace(' ',''),[x['menuEngNm'].strip(),x['menuJpnsNm'].strip(),x['menuZhhansNm'].strip()])
# 붙어 있는 영어 단어 띄우기(원문 오타: DumplingSoup, KimchiNoodles)
for k,v in D.items(): v[0]=re.sub(r'([a-z])([A-Z])',r'\1 \2',v[0])
ALIAS={'짜장면':'자장면','짜장':'자장면','순대국':'순댓국','아구찜':'아귀찜','아구탕':'아귀탕','떡만두국':'떡만둣국','만두국':'만둣국','모듬회':'모둠회',
 '청국장':'청국장찌개','순두부':'순두부찌개','손칼국수':'칼국수','손수제비':'수제비','생삼겹살':'삼겹살','생삼겹':'삼겹살','냉동삼겹살':'삼겹살','삼겹':'삼겹살',
 '돼지갈비':'돼지갈비구이','냉면':'물냉면','물밀면':'밀면','가정식백반':'백반','원조김밥':'김밥','야채김밥':'김밥','한우등심':'등심구이','등심':'등심구이',
 '소갈비':'소갈비구이','된장':'된장찌개','김치찌게':'김치찌개','된장찌게':'된장찌개','순두부찌게':'순두부찌개','부대찌게':'부대찌개'}
OWN={'아메리카노':['Americano','アメリカーノ','美式咖啡'],'아이스아메리카노':['Iced Americano','アイスアメリカーノ','冰美式咖啡'],
 '카페라떼':['Caffè Latte','カフェラテ','拿铁咖啡'],'바닐라라떼':['Vanilla Latte','バニララテ','香草拿铁'],'카푸치노':['Cappuccino','カプチーノ','卡布奇诺'],
 '에스프레소':['Espresso','エスプレッソ','意式浓缩咖啡'],'커피':['Coffee','コーヒー','咖啡'],'아이스티':['Iced Tea','アイスティー','冰茶'],
 '우동':['Udon','うどん','乌冬面'],'라면':['Ramyeon (Instant Noodles)','ラーメン（インスタント）','拉面（方便面）'],'볶음밥':['Fried Rice','チャーハン','炒饭'],
 '돈가스':['Pork Cutlet','トンカツ','炸猪排'],'돈까스':['Pork Cutlet','トンカツ','炸猪排'],'탕수육':['Sweet and Sour Pork','酢豚（タンスユク）','糖醋肉'],
 '짬뽕':['Spicy Seafood Noodle Soup','チャンポン','韩式海鲜辣汤面'],'치킨':['Fried Chicken','フライドチキン','炸鸡'],'후라이드치킨':['Fried Chicken','フライドチキン','炸鸡'],
 '후라이드':['Fried Chicken','フライドチキン','炸鸡'],'국수':['Noodles','麺料理','面条'],'정식':['Set Meal','定食','套餐'],'한식뷔페':['Korean Buffet','韓国料理ビュッフェ','韩式自助餐'],
 '목살':['Pork Neck','豚肩ロース','猪颈肉'],'생목살':['Pork Neck','豚肩ロース','猪颈肉'],'단팥빵':['Red Bean Bun','あんパン','红豆面包'],'팥빵':['Red Bean Bun','あんパン','红豆面包'],
 '소금빵':['Salt Bread','塩パン','盐面包'],'꽈배기':['Twisted Doughnut','ねじりドーナツ','麻花甜甜圈'],'멸치국수':['Anchovy Broth Noodles','煮干しだしの麺','鳀鱼汤面'],
 '간짜장':['Dry Black Bean Sauce Noodles','汁なしジャージャー麺','干炸酱面']}
PREFIX=['원조','옛날','수제','국내산','한우','토종','손','왕','특']
UNIT=r'\d+\s*(?:g|kg|인분|인|개|줄|그릇|마리|접시|공기|ml|mL|cc)'
def norm(n): return re.sub(r'\s','',re.sub(UNIT,'',re.sub(r'\([^)]*\)','',n)))
def resolve(k):
    for c in [k]+[k[len(p):] for p in PREFIX if k.startswith(p) and len(k)>len(p)+1]:
        if c in D: return D[c],'official'
        if c in ALIAS and ALIAS[c] in D: return D[ALIAS[c]],'official'
        if c in OWN: return OWN[c],'own'
    return None,None
s=open('/home/claude/hoolzzeok_site/index.html',encoding='utf-8').read()
i=s.index('const GOOD = '); j=s.index(';\n',i); G=json.loads(s[i+13:j])
i=s.index('const COURSES = '); j=s.index(';\n',i); C=json.loads(s[i+16:j])
c=Counter()
for pid,rows in G.items():
    for r in rows:
        if r[1] in ('s',): continue
        for m in r[3]: c[m[0]]+=1
for pid,cs in C.items():
    for co in cs:
        for st in co['stops']:
            if st.get('menu'): c[st['menu']]+=1
out={}; kind=Counter(); occ=Counter()
for name,n in c.items():
    k=norm(name); v,src=resolve(k)
    if v: out[k]=v; kind[src]+=1; occ[src]+=n
    else: occ['none']+=n
tot=sum(c.values())
print(f"메뉴 종류 {len(c)}, 번역 연결 {len(out)}종(공식 {kind['official']}, 자체 {kind['own']})")
print(f"화면에 나오는 횟수 기준: 공식 {occ['official']/tot*100:.0f}% + 자체 {occ['own']/tot*100:.0f}% = {(occ['official']+occ['own'])/tot*100:.0f}% / 미번역 {occ['none']/tot*100:.0f}%")
js='/* 메뉴 외국어 표기: 한식진흥원 「한식메뉴 외국어표기 길라잡이 800선」(2023-06-01) + 부산광역시 메뉴 외국어 표기사전 API. 한식 외 흔한 메뉴 일부만 훌쩍 자체 표기. [영,일,중] */\nconst MENU_TR = '+json.dumps(out,ensure_ascii=False,separators=(',',':'))+';\n'
open('menu_tr.js','w',encoding='utf-8').write(js); print('JS',len(js.encode())//1024,'KB')
