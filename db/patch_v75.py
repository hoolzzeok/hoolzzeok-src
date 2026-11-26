import sys
P = '/home/claude/hoolzzeok_site/index.html'; s = open(P, encoding='utf-8').read()
def rep(o, n, c=1):
    global s
    k = s.count(o)
    if k != c: sys.exit(f'못 찾음({k}) {o[:90]}')
    s = s.replace(o, n)
DB = '/home/claude/hoolzzeok_db/'
data = open(DB + 'hub/hub.js').read() + open(DB + 'pet/pet.js').read() + open(DB + 'lodging/trest.js').read() + open(DB + 'lodging/lodging.js').read()
rep('const TILE_IC = {', data + '''/* v75 여행객 흐름 공통(주니어 칸·시니어 줄) */
function crowdParts(pid, lg, m){ const cr = CROWD[pid]; if (!cr) return null; const L = T[lg];
  const [nb, yoy, idx, wr, nc] = cr, mi = idx[m], md = d8 => `${+d8.slice(4, 6)}.${+d8.slice(6)}`;
  const lv = mi == null ? "" : mi >= 112 ? L.crowdLv.busy : mi <= 90 ? L.crowdLv.calm : L.crowdLv.mid;
  const mx = Math.max(...idx.filter(x => x != null));
  const bars = idx.every(x => x != null) ? `<ol class="cr-bars" aria-hidden="true">${idx.map((v, i) => `<li${i === m ? ' class="on"' : ""}><i style="height:${Math.max(3, Math.round(v / mx * 52))}px"></i><small>${i + 1}</small></li>`).join("")}</ol>` : "";
  const lines = [L.crowdRecent(L.crowdN(nb), md(CROWD_META.from), md(CROWD_META.to)), yoy != null ? L.crowdYoy(yoy, md(CROWD_META.yoyFrom), md(CROWD_META.to)) : "",
    mi != null ? L.crowdMonth(m + 1, mi - 100) : "", wr != null ? L.crowdWeekend((wr / 100).toFixed(1)) : "", nc != null ? L.crowdForeign(L.crowdN(nc)) : ""].filter(Boolean);
  if (lg !== "ko" && nc != null) lines.unshift(lines.pop());
  return {sub: [lv, L.crowdDay(L.crowdN(nb))].filter(Boolean).join(" · "), html: `<ul class="plain">${lines.map(x => `<li>${x}</li>`).join("")}</ul>${bars}<small class="muted">${L.crowdNote}</small>`}; }
/* v75 요즘 많이 찾는 곳 · 반려견 · 관광식당 · 숙소 공급 */
const kmap = (n, x, y) => `https://map.kakao.com/link/map/${encodeURIComponent(n)},${y},${x}`;
function hubParts(pid, lg){ const h = HUB[pid]; if (!h) return null; const L = T[lg];
  return {sub: h[0].slice(0, 3).map(x => x[0]).join(" · "), html: `<ol class="hub-list">${h[0].map(([n, c, x, y]) => `<li><a href="${kmap(n, x, y)}" target="_blank" rel="noopener noreferrer"><b lang="ko">${menuEsc(n)}</b><small>${L.hubCat[c] || ""}</small></a></li>`).join("")}</ol>${h[1].length ? `<p class="hub-stay"><b>${L.hubStays}</b> <span lang="ko">${h[1].map(menuEsc).join(" · ")}</span></p>` : ""}<small class="muted">${L.hubNote}</small>`}; }
function petParts(pid, lg){ const p = PET[pid]; if (!p) return null; const L = T[lg], [sg, st, ea, n, shop] = p, row = (h, a) => a.length ? `<li><b>${h}</b> <span lang="ko">${a.map(menuEsc).join(" · ")}</span></li>` : "";
  return {sub: L.petSub(n >= 1000 ? "1,000+" : n), html: `<ul class="plain pet-list">${row(L.petSights, sg)}${row(L.petStays, st)}${row(L.petEats, ea)}${shop ? `<li>${L.petShop(shop >= 1000 ? "1,000+" : shop)}</li>` : ""}</ul><small class="muted">${L.petNote}</small>`}; }
function trestParts(pid, lg){ const t = TREST[pid]; if (!t) return null; const L = T[lg], [n, list] = t;
  return {sub: L.trestSub(n), html: `<ul class="good-list">${list.map(([nm, en, tel, ad]) => `<li><b><span lang="ko">${menuEsc(nm)}</span>${en ? ` <small>${menuEsc(en)}</small>` : ""}</b><a href="https://map.kakao.com/link/search/${encodeURIComponent(nm + " " + ad.split(" ").slice(0, 2).join(" "))}" target="_blank" rel="noopener noreferrer">${L.goodMap} ↗</a><small lang="ko">${menuEsc(ad)}${tel ? " · ☎ " + menuEsc(tel) : ""}</small></li>`).join("")}</ul>${n > list.length ? `<p class="muted">${L.trestMore(n - list.length)}</p>` : ""}<small class="muted">${L.trestNote}</small>`}; }
function supplyHtml(pid, lg){ const v = STAY_SUPPLY[pid]; if (!v) return ""; const L = T[lg], tot = v.reduce((a, b) => a + b, 0);
  return `<p class="supply">${L.stSupply(v)}${tot < 15 ? `<br><b class="few">${L.stFew}</b>` : ""}</p><small class="muted">${L.stSupplyNote}</small>`; }
const TILE_IC = {''')
i = s.index('const GOOD_STAY = '); j = s.index(';\n', i) + 2
s = s[:j] + '/* v75 숙박업 인허가로 확인: 폐업은 빼고, 영업 중이면 전화번호 */\nfor (const k in GOOD_STAY) GOOD_STAY[k] = GOOD_STAY[k].filter(g => { const v = GSV[k + "|" + g[0]]; if (v && v[1]) g.tel = v[1]; return !(v && v[0] === "c"); });\n' + s[j:]
assert s.index('const GSV = ') < s.index('for (const k in GOOD_STAY) GOOD_STAY[k]'), 'GSV 순서'
rep('''<div class="fold-body"><p class="muted">${L.stayNone}</p></div></details>`;''', '''<div class="fold-body"><p class="muted">${L.stayNone}</p>${supplyHtml(calcId(p), lang)}</div></details>`;''')
rep('''<small class="muted">${L.stayNote}</small></div></details>`;''', '''<small class="muted">${L.stayNote}</small>${supplyHtml(calcId(p), lang)}</div></details>`;''')
i = s.index('    { const cr = CROWD[p.id], m = wxMonth();'); j = s.index('"t-crowd")); } }', i) + len('"t-crowd")); } }')
s = s[:i] + '    { const c = crowdParts(p.id, lang, wxMonth()); if (c) tiles.push(tile(L.hCrowd, c.sub, c.html, "t-crowd")); }' + s[j:]
rep('    if (info && info.musts.length) tiles.push(tile(L.hMusts,', '    { const h = hubParts(p.id, lang); if (h) tiles.push(tile(L.hHub, h.sub, h.html, "t-hub")); }\n    if (info && info.musts.length) tiles.push(tile(L.hMusts,')
rep('    tiles.push(goodHtml(p), stayHtml(p));', '    tiles.push(goodHtml(p), stayHtml(p));\n    { const t = trestParts(p.id, lang); if (t) tiles.push(tile(L.hTrest, t.sub, t.html, "t-trest")); }')
rep('    const nb = nearby(p);', '    { const pt = petParts(p.id, lang); if (pt) tiles.push(tile(L.hPet, pt.sub, pt.html, "t-pet")); }\n    const nb = nearby(p);')
rep('const k = ["now", "c-tile", "special", "good-stay", "good", "t-spots", "t-musts", "t-wx", "t-crowd",', 'const k = ["now", "c-tile", "special", "good-stay", "good", "t-spots", "t-hub", "t-musts", "t-wx", "t-crowd", "t-trest", "t-pet",')
rep('''  "t-near": ''', '''  "t-hub": '<rect class="y" x="13" y="8" width="10" height="23" rx="1.5"/><rect class="l" x="3.5" y="15.5" width="9.5" height="15.5" rx="1.5"/><rect class="p" x="23" y="20" width="9.5" height="11" rx="1.5"/><path d="M2 31h32M18 12.5v5"/>',
  "t-pet": '<ellipse class="p" cx="18" cy="24.5" rx="7.5" ry="6.5"/><ellipse class="y" cx="8" cy="15.5" rx="3.2" ry="4"/><ellipse class="y" cx="14" cy="8.5" rx="3.2" ry="4"/><ellipse class="y" cx="22" cy="8.5" rx="3.2" ry="4"/><ellipse class="y" cx="28" cy="15.5" rx="3.2" ry="4"/>',
  "t-trest": '<circle class="s" cx="18" cy="19" r="10"/><circle cx="18" cy="19" r="5.5"/><path d="M4 7v7.5a2.5 2.5 0 0 0 2.5 2.5V31M4 7v5.5M7 7v5.5M32 7c-2.6 0-3.6 3.2-3.6 7.5H32V31"/>',
  "t-near": ''')
rep('''      if (meals.length) { const mm = meals[0][3].find(isMealMenu); srFold("🍚",''', '''      { const h = hubParts(d.id, lang); if (h) srFold("📍", L.hHub, esc(h.sub), h.html); }
      { const c = crowdParts(d.id, lang, srMonthNum() - 1); if (c) srFold("👥", L.hCrowd, esc(c.sub), c.html); }
      if (meals.length) { const mm = meals[0][3].find(isMealMenu); srFold("🍚",''')
rep('''      { const it = shopItems(d); srFold("🎒",''', '''      { const t = trestParts(d.id, lang); if (t && lang !== "ko") srFold("🍽", L.hTrest, esc(t.sub), t.html); }
      { const pt = petParts(d.id, lang); if (pt) srFold("🐾", L.hPet, esc(pt.sub), pt.html); }
      { const it = shopItems(d); srFold("🎒",''')
rep('''    { const cr = CROWD[d.id]; if (cr) {''', '''    { const h = HUB[d.id]; if (h) out.push(`${L.hHub}: ${h[0].map(x => x[0]).join(", ")}${h[1].length ? ` (${L.hubStays}: ${h[1].join(", ")})` : ""}`);
      const v = STAY_SUPPLY[calcId(d)]; if (v) out.push(L.stSupply(v));
      const pt = PET[d.id]; if (pt) out.push(`${L.hPet}: ${L.petSub(pt[3])} — ${[...pt[0], ...pt[1], ...pt[2]].join(", ")}`);
      const tr = TREST[d.id]; if (tr) out.push(`${L.hTrest}: ${tr[1].map(x => x[0]).join(", ")}`); }
    { const cr = CROWD[d.id]; if (cr) {''')
K = {'ko': '''hHub:"요즘 많이 찾는 곳", hubCat:{c:"문화",n:"자연",h:"역사",l:"레저",x:"체험",s:"시장",o:"기타"}, hubStays:"많이 찾는 숙소", hubNote:"한국관광공사 「기초지자체 중심 관광지」(2026-10) 순위예요. 방문·검색이 많은 순서이고, 훌쩍이 고른 게 아니에요. 이름을 누르면 지도가 열려요.",
  hPet:"반려견과 함께", petSub:n=>`동반 가능한 곳 ${n}곳`, petSights:"관광·체험", petStays:"숙소", petEats:"식당·카페", petShop:n=>`반려동물 동반 쇼핑 ${n}곳`, petNote:"한국관광공사 「반려동물 동반여행」(2026-11) 자료예요. 크기·실내 출입 같은 조건은 곳마다 달라서 가기 전에 전화로 확인하세요.",
  hTrest:"관광식당", trestSub:n=>`문체부 지정 ${n}곳`, trestMore:n=>`외 ${n}곳`, trestNote:"문화체육관광부가 외국인 관광객을 위해 지정한 식당이에요(인허가 자료, 2026-11). 외국어 메뉴·서비스는 가게마다 달라요.",
  stSupply:v=>`이 지역 영업 중인 숙소(인허가 기준): 호텔 ${v[0]} · 여관·모텔 ${v[1]}${v[2] ? ` · 여인숙 ${v[2]}` : ""}${v[3] ? ` · 생활숙박 ${v[3]}` : ""}${v[4] ? ` · 콘도 ${v[4]}` : ""}`, stFew:"숙소가 적은 편이에요. 주말·축제 때는 미리 잡으세요.", stSupplyNote:"펜션·민박·게스트하우스는 따로 신고라 이 수에 빠져 있어요(행정안전부 인허가, 2026-11-16).", ''',
 'en': '''hHub:"Popular right now", hubCat:{c:"Culture",n:"Nature",h:"History",l:"Leisure",x:"Hands-on",s:"Market",o:"Other"}, hubStays:"Popular stays", hubNote:"Ranking from the Korea Tourism Organization's local hub-attraction data (Oct 2026), by visits and searches. Tap a name to open the map.",
  hPet:"With your dog", petSub:n=>`${n} pet-friendly places`, petSights:"Sights", petStays:"Stays", petEats:"Food & cafés", petShop:n=>`${n} pet-friendly shops`, petNote:"Korea Tourism Organization pet travel data (Nov 2026). Size limits and indoor rules differ by place, so call ahead.",
  hTrest:"Tourist restaurants", trestSub:n=>`${n} government-designated`, trestMore:n=>`+${n} more`, trestNote:"Restaurants designated by the Ministry of Culture, Sports and Tourism for international visitors (licensing data, Nov 2026). Foreign-language menus vary by restaurant.",
  stSupply:v=>`Licensed lodging in the area: ${v[0]} hotels · ${v[1]} motels/inns${v[2] ? ` · ${v[2]} yeoinsuk` : ""}${v[3] ? ` · ${v[3]} serviced residences` : ""}${v[4] ? ` · ${v[4]} condos` : ""}`, stFew:"Few places to stay. Book ahead for weekends and festivals.", stSupplyNote:"Pensions, minbak and guesthouses are registered separately and not counted (Ministry of the Interior licensing data, 2026-11-16).", ''',
 'ja': '''hHub:"最近よく訪れる場所", hubCat:{c:"文化",n:"自然",h:"歴史",l:"レジャー",x:"体験",s:"市場",o:"その他"}, hubStays:"人気の宿", hubNote:"韓国観光公社「基礎自治体の中心観光地」（2026年10月）の順位です。名前を押すと地図が開きます。",
  hPet:"ペットと一緒に", petSub:n=>`同伴可 ${n}か所`, petSights:"観光・体験", petStays:"宿", petEats:"食事・カフェ", petShop:n=>`同伴可の店 ${n}か所`, petNote:"韓国観光公社「ペット同伴旅行」（2026年11月）のデータです。大きさや室内同伴などの条件は場所ごとに違うので、事前に電話で確認してください。",
  hTrest:"観光食堂", trestSub:n=>`文化体育観光部指定 ${n}か所`, trestMore:n=>`ほか${n}か所`, trestNote:"文化体育観光部が外国人観光客向けに指定した食堂です（許認可データ、2026年11月）。外国語メニューは店によって異なります。",
  stSupply:v=>`この地域で営業中の宿（許認可）：ホテル ${v[0]}・旅館/モーテル ${v[1]}${v[2] ? `・旅人宿 ${v[2]}` : ""}${v[3] ? `・レジデンス ${v[3]}` : ""}${v[4] ? `・コンド ${v[4]}` : ""}`, stFew:"宿が少なめです。週末や祭りの時期は早めに予約してください。", stSupplyNote:"ペンション・民泊・ゲストハウスは別の届出のため含まれていません（行政安全部許認可、2026-11-16）。", ''',
 'zh': '''hHub:"近期热门地点", hubCat:{c:"文化",n:"自然",h:"历史",l:"休闲",x:"体验",s:"市场",o:"其他"}, hubStays:"热门住宿", hubNote:"来自韩国观光公社“基层地区中心景点”（2026年10月）排名。点名称可打开地图。",
  hPet:"携宠物出行", petSub:n=>`可携宠 ${n}处`, petSights:"景点·体验", petStays:"住宿", petEats:"餐饮", petShop:n=>`可携宠商店 ${n}处`, petNote:"来自韩国观光公社“携宠物旅行”数据（2026年11月）。体型、室内是否可进等条件各处不同，请提前电话确认。",
  hTrest:"观光餐厅", trestSub:n=>`文体部指定 ${n}家`, trestMore:n=>`另有${n}家`, trestNote:"韩国文化体育观光部为外国游客指定的餐厅（许可数据，2026年11月）。外语菜单因店而异。",
  stSupply:v=>`本地区营业中的住宿（许可数据）：酒店 ${v[0]} · 旅馆/汽车旅馆 ${v[1]}${v[2] ? ` · 旅人宿 ${v[2]}` : ""}${v[3] ? ` · 公寓式酒店 ${v[3]}` : ""}${v[4] ? ` · 度假公寓 ${v[4]}` : ""}`, stFew:"住宿较少，周末和节庆期间请提前预订。", stSupplyNote:"民宿、家庭旅馆、青旅另行登记，未计入（行政安全部许可数据，2026-11-16）。", '''}
for lg, a in [('ko', 'accT:"무장애 정보"'), ('en', 'accT:"Accessibility"'), ('ja', 'accT:"バリアフリー情報"'), ('zh', 'accT:"无障碍信息"')]: rep(a, K[lg] + a)
rep('.acc{display:flex;', '''.hub-list{list-style:none;counter-reset:hub;margin:0;padding:0;display:grid;gap:6px}
.hub-list li{counter-increment:hub}
.hub-list a{display:grid;grid-template-columns:28px minmax(0,1fr) auto;gap:8px;align-items:center;padding:8px 10px;border-radius:12px;background:var(--surface-2);color:var(--ink);text-decoration:none}
.hub-list a::before{content:counter(hub);font-weight:800;color:var(--accent);text-align:center}
.hub-list small{color:var(--muted);font-size:12px}
.hub-stay{margin:8px 0 4px;font-size:13px;color:var(--muted)}.hub-stay b{color:var(--ink)}
.pet-list li{margin-bottom:4px}.pet-list b{margin-right:4px}
.supply{margin:10px 0 2px;font-size:13px;line-height:1.5}.supply .few{color:var(--deal)}
.senior .hub-list a{font-size:17px;padding:12px}.senior .supply{font-size:16px}
.acc{display:flex;''')
open(P, 'w', encoding='utf-8').write(s); print('ok')
