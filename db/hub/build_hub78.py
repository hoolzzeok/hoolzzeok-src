#!/usr/bin/env python3
"""군 지역 78곳(명소 자료가 없던 곳) → 관광공사 공식 상세로 대표 관광지 채우기.

입력: db/pull/targets_78.json (관광공사 중심관광지, 많이 찾는 순), db/pull/hub78_detail.json (KorService2 공식 상세)
출력: site/index.html 의 `const HUB78 = …;` 한 줄 (없으면 TOUR 줄 바로 뒤에 넣음) + site/img/*.webp (공공누리 1유형만)

고르는 기준
- 공식 상세와 연결된 곳(status ok)만. 연결 안 된 곳은 지어내지 않음.
- 골프장·체력단련장·체육공원·경기장·영화관·축제·공사 중·휴관은 뺌. 행사·여행코스·숙박·음식점 유형(15·25·32·39)도 뺌.
- 같은 contentid는 하나만. 많이 찾는 순서대로 최대 4곳.
- 사진은 공공누리 1유형(출처표시, 변경 허용)만 480px WebP로 줄여 저장. 3유형·표기 없음은 넣지 않음.
"""
import hashlib, html, io, json, os, re, sys, urllib.request
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PULL = os.path.join(ROOT, "db", "pull")
SITE = os.path.join(ROOT, "site", "index.html")
IMG = os.path.join(ROOT, "site", "img")

BAD = re.compile(r"골프|컨트리클럽|CC$|체력단련|체육공원|경기장|야구장|체육관|시네마|CGV|메가박스|영화관|아레나|축제|페스티벌|박람회|엑스포|공사중|공사 중|휴관|폐관|개관예정")
BAD_TYPE = {"15", "25", "32", "39"}
MAXN = 4

def clean(t, n=60):
    t = html.unescape(re.sub(r"<[^>]+>", " ", t or ""))
    t = t.split("※")[0]
    t = re.sub(r"\s+", " ", t).strip(" /,·")
    return t if len(t) <= n else t[: n - 1].rstrip() + "…"

TIME = re.compile(r"\d{1,2}:\d{2}\s*[~\-]\s*\d{1,2}:\d{2}")
def hours_short(t):
    """운영시간이 길거나 계절별로 나뉘면 첫 시간대만 + '계절마다 달라요'"""
    raw = html.unescape(re.sub(r"<[^>]+>", " ", t or "")).split("※")[0]
    raw = re.sub(r"\s*-\s+", " / ", raw); raw = re.sub(r"\s+", " ", raw).strip(" /,·")
    raw = raw.replace("상이함", "달라요")
    if len(raw) <= 34 and "[" not in raw: return raw
    m = TIME.search(raw)
    return (m.group(0).replace(" ", "") + " 등(계절·요일마다 달라요)") if m else clean(raw, 34)

def webp(url):
    if not url: return ""
    url = url.replace("http://", "https://", 1)
    name = hashlib.sha1(url.encode()).hexdigest()[:10] + ".webp"
    p = os.path.join(IMG, name)
    if not os.path.exists(p):
        try:
            with urllib.request.urlopen(url, timeout=25) as r: raw = r.read()
            im = Image.open(io.BytesIO(raw)).convert("RGB")
            w = min(480, im.width); h = round(im.height * w / im.width)
            im.resize((w, h), Image.LANCZOS).save(p, "WEBP", quality=68, method=6)
        except Exception as e:
            print("img fail", url, e); return ""
    return "img/" + name

def main():
    targets = json.load(open(os.path.join(PULL, "targets_78.json"), encoding="utf-8"))
    det = json.load(open(os.path.join(PULL, "hub78_detail.json"), encoding="utf-8"))["places"]
    by = {}
    for d in det:
        by.setdefault((d["region"], d["hub_name"]), d)
    out, nspots, nimg, nh = {}, 0, 0, 0
    for t in targets:
        pid, picked, seen = t["id"], [], set()
        for h in t["hub"]:
            d = by.get((pid, h["name"]))
            if not d or d.get("status") != "ok": continue
            if BAD.search(h["name"]) or BAD.search(d.get("title") or "") or str(d.get("contenttypeid")) in BAD_TYPE: continue
            if d["contentid"] in seen: continue
            seen.add(d["contentid"]); picked.append((h, d))
            if len(picked) >= MAXN: break
        if not picked: continue
        spots, tour, hrs = [], {}, {}
        for h, d in picked:
            key = h["name"].replace("/", " ").strip()
            ph = d.get("photo") or {}
            img = webp(ph.get("url")) if ph.get("cpyrhtDivCd") == "Type1" else ""
            nimg += bool(img)
            spots.append([key, key])
            tour[key] = [d["contentid"], clean(d.get("title"), 40), clean(d.get("overview_first"), 110), img, "1" if img else "",
                         round(d["lon"], 5), round(d["lat"], 5)]
            hh, rr = hours_short(d.get("hours")), clean(d.get("restdate"), 44).replace("상이함", "달라요")
            if hh or rr: hrs[key] = [hh, rr]; nh += 1
        names = [s[0] for s in spots]
        out[pid] = {"d": {"ko": "많이 찾는 곳: " + " · ".join(names[:3]), "en": "Most-visited sights, picked from Korea Tourism Organization data."},
                    "s": spots, "t": tour, "h": hrs}
        nspots += len(spots)
    line = "const HUB78 = " + json.dumps(out, ensure_ascii=False, separators=(",", ":")) + ";"
    s = open(SITE, encoding="utf-8").read()
    if re.search(r"^const HUB78 = .*$", s, re.M):
        s = re.sub(r"^const HUB78 = .*$", lambda m: line, s, count=1, flags=re.M)
    else:
        m = re.search(r"^const TOUR = .*$", s, re.M)
        s = s[: m.end()] + "\n" + line + s[m.end():]
    open(SITE, "w", encoding="utf-8").write(s)
    print(f"지역 {len(out)}/78, 관광지 {nspots}, 사진 {nimg}, 운영시간·휴무 {nh}")

if __name__ == "__main__":
    main()
