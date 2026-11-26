#!/usr/bin/env python3
"""백년가게(중기부 지정) 음식점·빵집 → 여행지별 목록 CENTURY = {id: [[이름, 종류(f 음식점 | b 빵·떡), 주소, 메뉴(있으면)], ...]}
자료: 소상공인시장진흥공단 「전국 백년가게 지정리스트 현황 정보_20260820」(1,511곳, 업종 없음)
     + 「전국 백년가게 현황_20220713」(1,262곳, 주요사업 있음). 둘 다 공공데이터포털, 이용허락 제한 없음.
분류: 2022 목록과 이름이 같으면 '주요사업'으로, 아니면 가게 이름에 확실한 음식 낱말이 있을 때만(애매하면 뺌)."""
import csv, json, re, os, collections
D = os.path.dirname(os.path.abspath(__file__))
a = list(csv.DictReader(open(f'{D}/raw/l22.csv', encoding='utf-8')))
b = list(csv.DictReader(open(f'{D}/raw/l26.csv', encoding='utf-8')))
P = json.load(open(f'{D}/places.json'))
nz = lambda s: re.sub(r'[\s()（）\[\]·,.&]|주식회사|\(주\)|㈜|유한회사|본점', '', s)
NON = re.compile(r'식육|정육|축산|식품|상회|상사|유통|참기름|기름집|제유|젓갈|건어물|곡물|쌀상회|수산$|미용|헤어|이용원|바버|안경|사진|스튜디오|현상소|문구|서점|서적|문고|플라워|꽃집|꽃배달|꽃예술|꽃피는|꽃화훼|화원|생화|화훼|원예|정비|카센타|자동차|목욕탕|사우나|양복|의상|한복|보석|주단|원단|침구|솜틀|장갑|벨트|타올|조명|화방|학원|태권도|건설|건축|개발|가스$|가스상사|염전|농원|농자재|자전거|오토바이|체육사|스포츠|시계|전자|보청기|국악기|공방|도자|요$|앵글|주방|에어|인삼|홍삼|선식|반찬|김치$|방앗간$|떡방앗간|음악감상실|기공사')
BAK = re.compile(r'제과|과자|베이커리|제빵|빵|떡집|떡$|찹쌀떡|꿀빵|케익|케이크|화월당')
FOOD = re.compile(r'식당|국밥|해장국|순대|냉면|면옥|막국수|밀면|국수|국시|칼국수|만두|갈비|곱창|족발|보쌈|닭갈비|닭한마리|닭발|통닭|치킨|삼계탕|백숙|추어탕|설렁탕|곰탕|육개장|감자국|감자탕|매운탕|해물탕|짬뽕|짬순|반점|중식|중화|중국|탕수육|횟집|회식당|물회|복집|복국|복어|아구|장어|꼼장어|게장|낙지|초밥|일식|한정식|정식|돌솥|쌀밥|청국장|두부|김밥|분식|떡볶이|불고기|불갈비|주물럭|삼겹살|흑돼지|한우|숯불|바베큐|오리|경양식|레스토랑|피자|가든|회관|할매집|뚝배기|샤브|찌개|전골|콩탕|황태|산채|헛제사밥|기사식당|실비집|맛집|보말|한식|양식|비빔밥|육회|국$|탕$|면$|회$|빈대떡|전$|구이|생선|게$|꽃게|대게|조개|굴|해장|돈가스|카레|커피|다방|찻집|전통차')
NOT_REST = re.compile(r'식품|상회|수산$|젓갈')
# 2022 '주요사업' 판정용: 가게(판매·가공)·음식 아닌 업종
STORE22 = re.compile(r'도소매|도매|소매|판매|가공|제조|냉동수산물|수산물|젓갈|건어물|정육|식육$|식육판매|식육전문|고기판매|^육류$|^생고기$|기름|곡물|^쌀$|양곡|잡화|슈퍼|수퍼|식료|농산물|인삼|홍삼|건강식품|한약|과일|벌꿀|대중탕|목욕|숙박|여관|^닭$|^흑염소$|^홍어$|^소고기, 돼지고기$|^명란젓$|^양돈$|^떡류 제조|^굴비$|^생선$')
REST22 = re.compile(r'식당|전문점|요리|국밥|구이|정식|한식|힌식|음식|백반|탕|찜|죽|밥|버거|골뱅이|차돌|몸국|돔베|돈가스|돈까스|호프|볶음|약선|곱장|막창|쌈|짜장|묵|빙수|닭강정|카페|茶|회$|회,|회덮밥|삼치|쫄면|파전|철판|생맥주|옻닭|꿩|우동|메밀|이탈리안|와인|화로|면$|국$')
BAK22 = re.compile(r'떡(?!갈비)|빵|제과|제빵|과자|베이커리|타르트|몽블랑|카스테라|완당')
def kind_of(text, by_name):
    t = text.strip()
    if not t: return None
    if not by_name:
        if NON.search(t) and not re.search(r'식당|요리|한식|감자탕', t) or STORE22.search(t) and not re.search(r'식당|전문점|탕,|감자탕', t):
            return None
        if FOOD.search(t) or REST22.search(t):
            return 'b' if BAK22.search(t) and not re.search(r'만두|우동|국수|면', t) else 'f'
        if BAK22.search(t): return 'b'
        return None
    if NON.search(t) and not (FOOD.search(t) and not NOT_REST.search(t) and re.search(r'식당|횟집|회관|가든', t)):
        return None
    if FOOD.search(t): return 'f'
    if BAK.search(t): return 'b'
    return None
SIDO = {'서울특별시':'서울','부산광역시':'부산','대구광역시':'대구','인천광역시':'인천','광주광역시':'광주','대전광역시':'대전','울산광역시':'울산','세종특별자치시':'세종',
        '경기도':'경기','강원도':'강원','강원특별자치도':'강원','충청북도':'충북','충청남도':'충남','전라북도':'전북','전북특별자치도':'전북','전라남도':'전남','경상북도':'경북','경상남도':'경남','제주특별자치도':'제주','제주도':'제주'}
METRO = {'서울','부산','대구','인천','광주','대전','울산','세종'}
def dest_of(addr):
    tk = addr.split()
    if not tk: return None
    sd = SIDO.get(tk[0], tk[0])
    if sd in METRO and tk[0] in (sd, *[k for k,v in SIDO.items() if v == sd]):
        hit = [p for p in P if p[2] == sd and p[1] == sd]
        return hit[0][0] if hit else None
    if sd == '제주':
        sg = tk[1] if len(tk) > 1 else ''
        hit = [p for p in P if p[2] == '제주' and sg.startswith(p[1])] or [p for p in P if p[2] == '제주']
        return hit[0][0] if hit else None
    if len(tk) < 2: return None
    sg = re.sub(r'(시|군)$', '', tk[1])
    hit = [p for p in P if p[2] == sd and p[1] == sg]
    return hit[0][0] if hit else None
m22 = {nz(r['업체명']): r for r in a}
out = collections.defaultdict(list); stat = collections.Counter(); seen = set()
for r in b:
    name = r['업체명'].strip(); addr = r['업체주소'].strip(); key = nz(name)
    if key in seen: continue
    seen.add(key)
    old = m22.get(key)
    if old:
        k = kind_of(old['주요사업'], False); menu = old['주요사업'].strip(); src = '22'
    else:
        k = kind_of(name, True); menu = ''; src = 'nm'
    stat[(src, k)] += 1
    if not k: continue
    did = dest_of(addr)
    if not did: stat['no_dest'] += 1; continue
    disp = re.sub(r'^(주식회사|\(주\)|㈜)\s*|\s*(주식회사|유한회사)$', '', name).strip()
    short = re.sub(r'^\S+\s+', '', addr) if addr.split()[0] in SIDO or addr.split()[0] in SIDO.values() else addr
    out[did].append([disp, k, short, menu])
for v in out.values(): v.sort(key=lambda x: (x[1] != 'f', x[0]))
tot = sum(len(v) for v in out.values())
print(dict(stat)); print('dest', len(out), 'shops', tot)
for k in sorted(out, key=lambda k: -len(out[k]))[:15]: print(k, len(out[k]), ', '.join(x[0] for x in out[k][:6]))
js = '/* 백년가게(중소벤처기업부 지정) 음식점·빵집. 소상공인시장진흥공단 지정리스트 2026-08-20 + 현황 2022-07-13(주요사업), 공공데이터포털(이용허락 제한 없음). [이름, f 음식점|b 빵·떡, 주소, 주요사업] */\nconst CENTURY = ' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';'
open(f'{D}/century.js', 'w').write(js); print('bytes', len(js.encode()))
