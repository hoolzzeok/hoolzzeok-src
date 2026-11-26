"""군 지역 78곳 hub 장소 → KorService2 공식 상세 (db/pull/hub78_detail.json)."""
import json, math, re, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _api import call, items, header
BASE = "https://apis.data.go.kr/B551011"
HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "hub78_detail.json")
SKIP_TYPES = {"32", "39"}  # 숙박·음식점은 hub 대상 아님
HOURS = {"12": ("usetime", "restdate"), "14": ("usetimeculture", "restdateculture"),
         "28": ("usetimeleports", "restdateleports"), "38": ("opentime", "restdateshopping"),
         "15": ("playtime", None), "25": ("taketime", None)}
LANGS = {"en": "EngService2", "ja": "JpnService2", "zh_cn": "ChsService2", "zh_tw": "ChtService2"}

def norm(s):
    s = re.sub(r"\[[^\]]*\]|\([^)]*\)|<[^>]*>", "", s or "")
    return re.sub(r"[\s·・\-_,.]", "", s)
def km(a, b, c, d):
    r = math.radians
    x = math.sin(r(c - a) / 2) ** 2 + math.cos(r(a)) * math.cos(r(c)) * math.sin(r(d - b) / 2) ** 2
    return 12742 * math.asin(math.sqrt(x))
def clean(t):
    t = re.sub(r"<br\s*/?>", " ", t or "", flags=re.I)
    t = re.sub(r"<[^>]+>", "", t)
    return re.sub(r"\s+", " ", t).strip()
def first_sentence(t):
    t = clean(t)
    m = re.search(r"^.+?(?:다\.|요\.|\.)(?=\s|$)", t)
    return (m.group(0) if m else t)[:300]

SUFFIX = ("국민관광지", "관광단지", "관광지", "유원지")
def keywords(name):
    """검색어 후보: 원래 이름 → '/'로 나눈 부분 → 흔한 접미어 뗀 이름 (2글자 이상만)."""
    ks = [name] + [x.strip() for x in name.split("/") if x.strip()]
    for k in list(ks):
        for suf in SUFFIX:
            if k.endswith(suf) and len(k) - len(suf) >= 2: ks.append(k[: -len(suf)])
    return list(dict.fromkeys(ks))

def match(h):
    names = [norm(x) for x in [h["name"]] + h["name"].split("/") if norm(x)]
    found, res = {}, {}
    for kw in keywords(h["name"]):
        res = call(f"{BASE}/KorService2", "searchKeyword2", keyword=kw, numOfRows=50, pageNo=1, arrange="A")
        for it in items(res): found.setdefault(it["contentid"], it)
        if found: break
    cands = []
    for it in found.values():
        if it.get("contenttypeid") in SKIP_TYPES: continue
        t = norm(it.get("title"))
        hit = [n for n in names if len(t) >= 2 and (n in t or t in n)]
        if not hit: continue
        n = min(hit, key=lambda n: abs(len(t) - len(n)))
        try: d = km(h["lat"], h["lon"], float(it["mapy"]), float(it["mapx"]))
        except Exception: continue
        if d > 2: continue
        cands.append((abs(len(t) - len(n)), d, it))
    if not cands: return None, "no_match" if "response" in res else header(res)
    cands.sort(key=lambda c: (c[0], c[1]))
    if len(cands) > 1 and cands[0][0] == cands[1][0] and cands[0][2]["contentid"] != cands[1][2]["contentid"]:
        return None, "ambiguous"
    return cands[0], None

def detail(cid, ctype):
    k = f"{BASE}/KorService2"
    c = items(call(k, "detailCommon2", contentId=cid))
    c = c[0] if c else {}
    i = items(call(k, "detailIntro2", contentId=cid, contentTypeId=ctype))
    i = i[0] if i else {}
    im = items(call(k, "detailImage2", contentId=cid, imageYN="Y", numOfRows=10, pageNo=1))
    hk, rk = HOURS.get(ctype, (None, None))
    photo = {"url": c.get("firstimage") or "", "cpyrhtDivCd": c.get("cpyrhtDivCd") or ""}
    if not photo["url"] and im:
        photo = {"url": im[0].get("originimgurl") or "", "cpyrhtDivCd": im[0].get("cpyrhtDivCd") or ""}
    names = {}
    for lg, svc in LANGS.items():
        r = items(call(f"{BASE}/{svc}", "detailCommon2", contentId=cid))
        names[lg] = (r[0].get("title") or "") if r else ""
    return {
        "overview_first": first_sentence(c.get("overview")),
        "hours": clean(i.get(hk)) if hk else "",
        "restdate": clean(i.get(rk)) if rk else "",
        "photo": photo,
        "images": [{"url": x.get("originimgurl"), "cpyrhtDivCd": x.get("cpyrhtDivCd")} for x in im],
        "names": names,
    }

def main():
    targets = json.load(open(os.path.join(HERE, "targets_78.json"), encoding="utf-8"))
    done = {}
    if os.path.exists(OUT):
        for r in json.load(open(OUT, encoding="utf-8"))["places"]:
            done[(r["region"], r["hub_name"])] = r
    out = []
    for reg in targets:
        for h in reg["hub"]:
            key = (reg["id"], h["name"])
            if key in done and done[key].get("status") in ("ok", "ambiguous", "no_match"):
                out.append(done[key]); continue
            rec = {"region": reg["id"], "region_ko": reg["ko"], "hub_name": h["name"], "kind": h.get("kind")}
            m, why = match(h)
            if not m:
                rec["status"] = why if why in ("no_match", "ambiguous") else "error"
                if rec["status"] == "error": rec["error"] = str(why)[:200]
            else:
                _, d, it = m
                rec.update({"status": "ok", "contentid": it["contentid"], "contenttypeid": it.get("contenttypeid"),
                            "title": it.get("title"), "addr": " ".join(x for x in (it.get("addr1"), it.get("addr2")) if x),
                            "lat": float(it["mapy"]), "lon": float(it["mapx"]), "dist_km": round(d, 3)})
                rec.update(detail(it["contentid"], it.get("contenttypeid")))
            out.append(rec)
            print(rec["status"], reg["ko"], h["name"], rec.get("title", ""), flush=True)
            json.dump({"source": "KorService2 (한국관광공사)", "places": out}, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump({"source": "KorService2 (한국관광공사)", "places": out}, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

if __name__ == "__main__":
    main()
