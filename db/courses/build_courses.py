#!/usr/bin/env python3
"""테마 코스 → 사이트용 JS 상수 COURSES.
입력: course_def.json(순서·머무는 시간·운영시간 메모), spots.json(관광공사 좌표·소개·사진),
      eat_cand.json + eat_coords.json(착한가격 밥집 + 인허가 좌표), ../seed/goodprice_menus.csv
계산: 이동 — 직선거리 1.2km 이하 도보(직선×1.3, 시속 4km), 넘으면 택시(직선×1.35, 시속 20km + 대기 5분)
      택시비 — 지역 기본요금표(TAXI) 기준 추정. 시간은 5분 단위로 올림
검사: 도착 시각이 입장 마감(close) 뒤이거나 개장(open) 전이면 warn
"""
import csv, json, math, os, re, io, base64, urllib.request
I18N = {k: v for k, v in json.load(open("names_i18n_ok.json", encoding="utf-8")).items() if k != "_note"}   # 관광공사 일문·중문 이름(검수본)
from PIL import Image

D = os.path.dirname(os.path.abspath(__file__))
cdef = json.load(open(f"{D}/course_def.json", encoding="utf-8"))
spots = json.load(open(f"{D}/spots.json", encoding="utf-8"))
eats = {r["id"]: r for r in json.load(open(f"{D}/eat_cand.json", encoding="utf-8"))}
coords = json.load(open(f"{D}/eat_coords.json", encoding="utf-8")) if os.path.exists(f"{D}/eat_coords.json") else {}
menus = {}
for r in csv.DictReader(open(f"{D}/../seed/goodprice_menus.csv", encoding="utf-8-sig")):
    menus.setdefault(r["eatery_id"], []).append((r["menu"], int(r["price"] or 0), r["is_meal"] == "1"))
TAXI = {"seoul": (4800, 1.6, 131), "busan": (4800, 1.6, 131), "gyeongju": (4500, 1.7, 131),   # seed/taxi_fares.csv 시·도 기본요금
        "suwon": (4800, 1.6, 131), "jeju": (4500, 2.0, 131), "jeonju": (4000, 2.0, 132), "gangneung": (4000, 2.0, 132)}
NOT_MEAL = re.compile(r"커피|음료|빵|떡|아이스|주스|라떼|아메리카노|사리|추가|공기밥|\d\s*g\b|\((?:소|중|대)\)|[중대]자\b")   # v136: 여럿이 나눠 먹는 크기 메뉴 제외

def km(a, b):
    R, t = 6371, math.radians
    h = math.sin(t(b[0] - a[0]) / 2) ** 2 + math.cos(t(a[0])) * math.cos(t(b[0])) * math.sin(t(b[1] - a[1]) / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))
up5 = lambda m: int(math.ceil(m / 5.0) * 5)
def leg(a, b, pid):
    d = km(a, b)
    if d <= 1.2:
        return {"m": "walk", "min": max(5, up5(d * 1.3 / 4.0 * 60)), "km": round(d * 1.3, 1)}
    road = d * 1.35; base, bkm, per = TAXI[pid]
    fare = base + max(0, road - bkm) * 1000 / per * 100
    return {"m": "taxi", "min": up5(road / (20 if road < 5 else 35) * 60 + 5), "km": round(road, 1), "fare": int(round(fare, -2))}   # 시내 시속 20km, 5km 넘는 구간 35km
hm = lambda s: int(s[:2]) * 60 + int(s[3:5])
fmt = lambda m: f"{m // 60:02d}:{m % 60:02d}"

def first_sentence(t, n=120):
    m = re.match(r"(.+?[다요]\.)(\s|$)", t or "")
    s = m.group(1) if m else (t or "")
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"

CACHE = f"{D}/img"; os.makedirs(CACHE, exist_ok=True)
def thumb(url, cid):
    if not url: return ""
    p = f"{CACHE}/{cid}.jpg"
    if not os.path.exists(p):
        try:
            with urllib.request.urlopen(url.replace("http://", "https://", 1), timeout=20) as r: raw = r.read()
            im = Image.open(io.BytesIO(raw)).convert("RGB"); w = 220; im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
            im.save(p, "JPEG", quality=62, optimize=True, progressive=True)
        except Exception as e:
            print("img fail", cid, e); return ""
    return "data:image/jpeg;base64," + base64.b64encode(open(p, "rb").read()).decode()

def meal_menu(eid):
    ms = [m for m in menus.get(eid, []) if m[1] >= 5000 and not NOT_MEAL.search(m[0])]
    ms.sort(key=lambda m: m[1]); return ms[0] if ms else None

def pick_meal(pid, anchor, slot, used, anchor_addr, area=""):
    cands = []
    for eid, r in eats.items():
        if r["place_id"] != pid or eid in used: continue
        mm = meal_menu(eid)
        if not mm: continue
        c = coords.get(eid)
        if c and "lat" in c:
            d = km(anchor, (c["lat"], c["lon"]))
            if r["has_grill"] == "1" and slot == "dinner": d -= 0.3      # 저녁은 고깃집을 조금 우선
            if slot == "lunch" and r["has_grill"] == "1": d += 0.3
            cands.append((d, eid, mm, (c["lat"], c["lon"]), c.get("tel", "")))
    cands.sort()
    if cands and cands[0][0] <= 1.5:
        d, eid, mm, pos, tel = cands[0]; return eid, mm, pos, tel
    # 좌표가 없거나 멀면: 코스에 적어 둔 근처 동 이름(area)과 주소가 맞는 집(고깃집은 저녁에 우선)
    if area:
        pool = [(eid, r) for eid, r in eats.items() if r["place_id"] == pid and eid not in used and meal_menu(eid) and re.search(area, r["address"] + " " + (r["neighborhood"] or ""))]
        pool.sort(key=lambda x: (0 if (x[1]["has_grill"] == "1") == (slot == "dinner") else 1, meal_menu(x[0])[1]))
        if pool:
            eid = pool[0][0]; c = coords.get(eid); pos = (c["lat"], c["lon"]) if c and "lat" in c else None
            return eid, meal_menu(eid), pos, (c or {}).get("tel", "")
    return None

out = {}; report = []
for pid, courses in cdef["courses"].items():
    for c in courses:
        t = hm(c["start"]); prev = None; prev_addr = ""; used = set(); rows = []; walk_km = 0; taxi = 0; off = set(); off_nth = []
        for st in c["stops"]:
            kind, key, stay = st[:3]; area = st[3] if len(st) > 3 else ""
            if kind == "spot":
                s = spots[f"{pid}|{key}"]; pos = (s["lat"], s["lon"]); f = cdef["facts"].get(key, {})
                lg = leg(prev, pos, pid) if prev else None
                if lg: t += lg["min"]; walk_km += lg["km"] if lg["m"] == "walk" else 0; taxi += lg.get("fare", 0)
                warn = ""
                if f.get("open") and t < hm(f["open"]): warn = f"opens {f['open']}"
                if f.get("close") and t > hm(f["close"]): warn = f"last entry {f['close']}"
                off |= set(f.get("off", [])); off_nth += [x for x in f.get("offNth", []) if x not in off_nth]
                rows.append({"k": "spot", "ko": key, "en": cdef["names"][key][0], **{lg: v for lg, v in zip(("ja", "zh", "zt"), I18N.get(key, ["", "", ""])) if v}, "at": fmt(t), "stay": stay, "leg": lg, "h": f.get("h", ""), "off": f.get("off", []), **({"offNth": f["offNth"]} if f.get("offNth") else {}),
                             "img": thumb(s["img"], s["cid"]) if s.get("cpy") == "Type1" else "", "addr": s.get("addr", ""), "intro": (lambda t: t if key.replace(" ", "")[:3] in t.replace(" ", "") else "")(first_sentence(s.get("overview", ""))), "warn": warn})
                if warn: report.append(f"{pid}/{c['id']} {key} {fmt(t)} {warn}")
                t += stay; prev = pos; prev_addr = s.get("addr", "")
            else:
                nxt_anchor = area.startswith(">"); area = area.lstrip(">")
                if nxt_anchor:
                    nk = next(x[1] for x in c["stops"][c["stops"].index(st) + 1:] if x[0] == "spot"); ns = spots[f"{pid}|{nk}"]
                    anchor_pos = (ns["lat"], ns["lon"])
                else:
                    anchor_pos = prev
                m = pick_meal(pid, anchor_pos, key, used, prev_addr, area)
                if not m:
                    report.append(f"{pid}/{c['id']} {key} 밥집 없음 → 주변 식당 찾기")
                    rows.append({"k": "meal", "slot": key, "name": "", "area": area.split("|")[0].replace("\\d", ""), "at": fmt(t), "stay": stay, "leg": None}); t += stay; continue
                eid, mm, pos, tel = m; used.add(eid); r = eats[eid]
                if not pos and nxt_anchor: pos = anchor_pos            # 좌표 없는 밥집은 다음 명소 근처로 어림
                lg = leg(prev, pos, pid) if (prev and pos) else {"m": "near", "min": 10}   # 좌표 없는 밥집: 근처로 보고 10분 어림
                if lg.get("min"): t += lg["min"]; walk_km += lg["km"] if lg["m"] == "walk" else 0; taxi += lg.get("fare", 0)
                rows.append({"k": "meal", "slot": key, "name": r["name"], "menu": mm[0], "price": mm[1], "addr": r["address"], "tel": tel, "grill": r["has_grill"] == "1",
                             "at": fmt(t), "stay": stay, "leg": lg})
                t += stay
                if pos: prev = pos
        o = {"id": c["id"], "emoji": c["emoji"], "t": c["t"], "d": c["d"], "walk": c["walk"], "stops": rows,
             "end": fmt(t), "walkKm": round(walk_km, 1), "taxi": int(round(taxi, -2)), "off": sorted(off)}
        if off_nth: o["offNth"] = off_nth
        if c.get("tags"): o["tags"] = c["tags"]
        if c.get("go"): o["go"] = c["go"]
        out.setdefault(pid, []).append(o)
        report.append(f"{pid}/{c['id']}: {c['start']}~{fmt(t)}, 걷기 {walk_km:.1f}km, 택시 약 {taxi:,.0f}원, 쉬는 요일 {sorted(off)}")
js = ("/* 테마 코스(2026-11-17): 명소 순서는 훌쩍요원(AI)이 관광공사 공식 정보 안에서 고르고, 이동 시간·택시비·밥집은 좌표로 계산.\n"
      "   운영시간은 관광공사 TourAPI(11월 기준), 밥집은 착한가격업소 + 지방행정 인허가 좌표 */\n"
      f"const COURSES = {json.dumps(out, ensure_ascii=False, separators=(',', ':'))};\n")
open(f"{D}/courses.js", "w", encoding="utf-8").write(js)
print("\n".join(report)); print(f"JS {len(js.encode())/1024:.0f}KB")
