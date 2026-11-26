#!/usr/bin/env python3
"""방문자수 → 사이트용 CROWD 상수.
입력: raw/locgo.json, raw/metco.json ({code:{yyyymmdd:[현지인,외지인,외국인]}}), placemap.json, names_old*.json, codes.json
값(장소별): [최근4주 외지인 하루평균, 작년대비 %(10/1~최근일 같은 기간), 달별 지수 12개(1년 평균=100), 주말/평일 x100, 최근3주 외국인 하루평균]
- 2026-07 전남·광주 통합으로 전남 시군 코드가 46xxx → 12xxx로 바뀜: 이름으로 이어 붙임
- 광역(서울·부산·대구·인천·대전·울산·세종)은 광역 자료(metco)를 씀. 광주는 통합 뒤 광주만의 광역 값이 없어 뺌
"""
import json, datetime as dt, statistics as st, os
D = os.path.dirname(os.path.abspath(__file__))
L = json.load(open(f"{D}/raw/locgo.json")); M = json.load(open(f"{D}/raw/metco.json"))
P = json.load(open(f"{D}/placemap.json"))["map"]
new = json.load(open(f"{D}/codes.json"))["locgo"]
old = {r["signguCode"]: r["signguNm"] for r in json.load(open(f"{D}/names_old.json"))["response"]["body"]["items"]["item"]}
# 전남 옛 코드 → 새 코드
o2n = {}
for oc, nm in old.items():
    if oc.startswith("46"):
        m = [nc for nc, nn in new.items() if nc.startswith("12") and nn == nm]
        if len(m) == 1: o2n[oc] = m[0]
for oc, nc in o2n.items():
    for d, v in L.get(oc, {}).items(): L.setdefault(nc, {}).setdefault(d, v)
days = sorted({d for c in L.values() for d in c})
last = days[-1]; ld = dt.date(int(last[:4]), int(last[4:6]), int(last[6:]))
ymd = lambda d: d.strftime("%Y%m%d")
rng = lambda a, b: [ymd(a + dt.timedelta(days=i)) for i in range((b - a).days + 1)]
recent = rng(ld - dt.timedelta(days=20), ld)   # 최근 3주(2026 추석 9.24~26 뒤)
this_oct = rng(dt.date(ld.year, 10, 1), ld); last_oct = [str(int(d[:4]) - 1) + d[4:] for d in this_oct]
wk8 = rng(ld - dt.timedelta(days=55), ld)
def avg(series, ds, k):
    v = [series[d][k] for d in ds if d in series and series[d][k] is not None]
    return st.mean(v) if len(v) >= max(3, len(ds) * 0.7) else None
def months(series):
    out = {}
    for m in range(1, 13):
        for y in ([ld.year, ld.year - 1] if m <= ld.month else [ld.year - 1]):
            ds = [d for d in series if d[:6] == f"{y}{m:02d}" and series[d][1] is not None]
            if len(ds) >= 20: out[m] = st.mean(series[d][1] for d in ds); break
    return out
crowd = {}; skipped = []
for pid, (kind, code) in P.items():
    s = (M if kind == "m" else L).get(code)
    if not s: skipped.append(pid); continue
    r_b = avg(s, recent, 1); r_c = avg(s, recent, 2)
    a, b = avg(s, this_oct, 1), avg(s, last_oct, 1)
    yoy = None   # 작년 10월은 추석 긴 연휴(10.3~10.12)라 같은 날짜 비교가 왜곡돼서 쓰지 않음
    mo = months(s); idx = [round(mo[m] / st.mean(mo.values()) * 100) if m in mo and len(mo) == 12 else None for m in range(1, 13)]
    we = [s[d][1] for d in wk8 if d in s and dt.date(int(d[:4]), int(d[4:6]), int(d[6:])).weekday() >= 5]
    wd = [s[d][1] for d in wk8 if d in s and dt.date(int(d[:4]), int(d[4:6]), int(d[6:])).weekday() <= 3]
    wr = round(st.mean(we) / st.mean(wd) * 100) if we and wd else None
    if r_b is None: skipped.append(pid); continue
    crowd[pid] = [round(r_b), yoy, idx, wr, round(r_c) if r_c is not None else None]
meta = {"from": recent[0], "to": recent[-1], "yoyFrom": this_oct[0], "monthsFrom": f"{ld.year - 1}-{ld.month + 1:02d}" if ld.month < 12 else f"{ld.year}-01"}
print("장소", len(crowd), "빠짐", skipped, meta)
for pid in ["seoul", "busan", "jeju", "seogwipo", "gyeongju", "gangneung", "goheung", "yeosu", "jeonju"]:
    if pid in crowd: print(pid, crowd[pid])
js = ("/* 여행객 흐름: 한국관광공사 「빅데이터 지역별 방문자수」(KT·SK텔레콤 통신 자료, 데이터랩). 외지인 = 그 지역 생활권 밖에서 온 방문자(관광객과 같지 않음).\n"
      "   [최근4주 외지인 하루평균, 작년 같은 기간 대비 %, 달별 지수(1년 평균=100) 1~12월, 주말/평일×100, 최근3주 외국인 하루평균] */\n"
      f"const CROWD_META = {json.dumps(meta)};\nconst CROWD = {json.dumps(crowd, separators=(',', ':'))};\n")
open(f"{D}/crowd.js", "w").write(js); print("JS", len(js) // 1024, "KB")
