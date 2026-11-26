#!/usr/bin/env python3
"""훌쩍 버스 요금 실측 — 국토교통부(TAGO) 고속버스정보·시외버스정보. 표준 라이브러리만.
사용: TAGO_KEY=<일반 인증키> python3 tago_fetch.py [YYYYMMDD]
- places.json(사이트 164곳)마다 터미널을 이름으로 고르고, 큰 도시 5곳(서울·부산·대구·광주·대전)에서
  나머지 모든 곳까지 '가장 싼 등급' 편도 요금을 찾는다. 고속버스 먼저, 없으면 시외버스.
- 결과: fares.json {"출발id-도착id": [요금, "exp|sub", 출발터미널, 도착터미널]} (이어 받기 가능)
- 근거: 오픈API활용가이드_국토교통부(TAGO)_고속버스정보 v1.1 / 시외버스정보 v1.1
  GetStrtpntAlocFndExpbusInfo, GetStrtpntAlocFndSuberbsBusInfo (응답 charge = 운임, 원)
- 인증키는 파일에 저장하지 않는다.
"""
import json, os, re, sys, time, urllib.parse, urllib.request

KEY = os.environ.get("TAGO_KEY", "").strip()
DATE = sys.argv[1] if len(sys.argv) > 1 else "20261118"
HUBS = ["seoul", "busan", "daegu", "gwangju", "daejeon"]
# 큰 도시는 터미널을 직접 지정(이름이 여러 개라)
FIX_EXP = {"seoul": ["서울경부", "센트럴시티(서울)", "동서울"], "busan": ["부산", "부산사상"], "daegu": ["동대구", "서대구"],
           "gwangju": ["광주(유·스퀘어)"], "daejeon": ["대전복합", "대전청사(샘머리)"]}
FIX_SUB = {"seoul": ["동서울", "서울남부"], "busan": ["부산동부", "부산서부(사상)"], "daegu": ["대구동부", "서대구"],
           "gwangju": ["광주(유·스퀘어)"], "daejeon": ["대전복합"]}
SLEEP = 0.12
calls = 0

def call(svc, op, **p):
    global calls
    u = f"https://apis.data.go.kr/1613000/{svc}/{op}?serviceKey={KEY}&_type=json&" + urllib.parse.urlencode(p)
    for a in range(3):
        try:
            calls += 1
            with urllib.request.urlopen(u, timeout=30) as r:
                d = json.loads(r.read().decode())
            h = d["response"]["header"]
            if h.get("resultCode") != "00":
                raise RuntimeError(h)
            it = d["response"]["body"].get("items") or {}
            it = it.get("item", []) if isinstance(it, dict) else []
            return it if isinstance(it, list) else [it]
        except RuntimeError as e:
            if "LIMITED" in str(e) or "22" in str(e):
                print("한도 초과로 멈춤", e); save(); sys.exit(2)
            raise
        except Exception as e:
            err = e; time.sleep(1 + a)
    raise err

def pick_terms(terms, ko, fix):
    if fix:
        out = []
        for n in fix:
            out += [t["terminalId"] for t in terms if t["terminalNm"] == n]   # 같은 이름 ID가 여럿(노선별)일 수 있어 모두
        return out
    k = re.sub(r"\(.*\)", "", ko).strip()
    pref = [k, k + "종합", k + "시외", k + "고속", k + "복합", k + "터미널", k + "공용", k + "시외버스터미널"]
    out = []
    for n in pref:
        out += [t["terminalId"] for t in terms if t["terminalNm"] == n and t["terminalId"] not in out]
    if not out:
        out = [t["terminalId"] for t in terms if t["terminalNm"].startswith(k)]
    return out[:6]

places = json.load(open("places.json", encoding="utf-8"))
EX = json.load(open("ExpBusInfo_terminals.json", encoding="utf-8"))
SB = json.load(open("SuburbsBusInfo_terminals.json", encoding="utf-8"))
TERM = {}
for p in places:
    TERM[p["id"]] = {"exp": pick_terms(EX, p["ko"], FIX_EXP.get(p["id"])), "sub": pick_terms(SB, p["ko"], FIX_SUB.get(p["id"]))}
json.dump(TERM, open("terminal_map.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)

fares = json.load(open("fares.json", encoding="utf-8")) if os.path.exists("fares.json") else {}
def save():
    json.dump(fares, open("fares.json", "w", encoding="utf-8"), ensure_ascii=False)

def cheapest(svc, op, deps, arrs):
    best = None
    for a in deps:
        for b in arrs:
            try:
                it = call(svc, op, depTerminalId=a, arrTerminalId=b, depPlandTime=DATE, numOfRows=200, pageNo=1)
            except Exception as e:
                print("ERR", svc, a, b, e); continue
            time.sleep(SLEEP)
            ch = [int(i["charge"]) for i in it if str(i.get("charge", "")).isdigit() and int(i["charge"]) > 0]
            if ch and (best is None or min(ch) < best[0]):
                best = (min(ch), a, b)
        if best:      # 첫 출발 터미널에서 찾으면 그만(호출 절약)
            break
    return best

if not KEY:
    sys.exit("TAGO_KEY 환경변수가 없어요")
for h in HUBS:
    for p in places:
        d = p["id"]
        if d == h or fares.get(f"{h}-{d}"):
            continue
        t = TERM[d]
        r = cheapest("ExpBusInfo", "GetStrtpntAlocFndExpbusInfo", TERM[h]["exp"], t["exp"]) if t["exp"] else None
        kind = "exp"
        if not r and t["sub"]:
            r = cheapest("SuburbsBusInfo", "GetStrtpntAlocFndSuberbsBusInfo", TERM[h]["sub"], t["sub"]); kind = "sub"
        fares[f"{h}-{d}"] = [r[0], kind, r[1], r[2]] if r else None
        save()
    print(h, "끝, 누적 호출", calls)
print("완료", sum(1 for v in fares.values() if v), "/", len(fares), "호출", calls)
