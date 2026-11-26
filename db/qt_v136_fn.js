  const QTX = () => QT_TX[lang] || QT_TX.en;
  Object.entries(QT_TX2).forEach(([k, v]) => Object.assign(QT_TX[k], v));
  const qt = {step: 1, days: null, themes: [], budget: null, city: null, air: "icn", start: ""};
  const qtZ = s => (zhT && typeof ZT === "function") ? ZT(String(s)) : String(s);   // 번체 화면: 공유 글·엑셀도 번체로
  function courseOne(pid, id){
    const keep = courseSel[pid]; courseSel[pid] = id;
    let h = courseHtml(pid, false); courseSel[pid] = keep;
    return h.replace(/<p class="c-sub">[\s\S]*?<\/p>/, "").replace(/<div class="c-chips">[\s\S]*?<\/div>/, "").replace('data-course-box="', 'data-qt-course="');
  }
  const qtCourse = (pid, id) => (COURSES[pid] || []).find(c => c.id === id);
  /* 테마 점수로 코스 줄 세우기: 첫 테마 3점, 둘째 2점. 같으면 원래 순서 */
  function qtRank(pid, themes){
    const list = (COURSES[pid] || []).filter(c => !(pid === "gyeongju" && c.id === "night"));   // 경주 두 코스는 명소 4곳이 겹쳐 하루만
    const sc = c => themes.reduce((a, t, i) => a + ((c.tags || []).includes(t) ? (i === 0 ? 3 : 2) : 0), 0);
    return list.map((c, i) => ({id: c.id, i, s: sc(c)})).sort((a, b) => b.s - a.s || a.i - b.i).map(x => x.id);
  }
  function qtPlan(q){
    const A = QT_AIR[q.air] || QT_AIR.icn, base = A.base, themes = q.themes.length ? q.themes : ["food"];
    let city = A.second.length ? (A.second.includes(q.city) ? q.city : A.second.includes(QT_PICK[themes[0]]) ? QT_PICK[themes[0]] : A.second[0]) : null;
    const F = q.days - 2, cc = city ? qtRank(city, themes) : [];
    const C = city && F >= 2 ? Math.min(cc.length, Math.floor(F / 2)) : 0;
    if (!C) city = null;
    const Bd = F - C, bc = qtRank(base, themes);
    /* 서울에 3일 이상이면 수원 당일치기를 후보에 (테마가 맞을 때 세 번째 날 무렵) */
    if (base === "seoul" && Bd >= 3 && COURSES.suwon && themes.some(t => (COURSES.suwon[0].tags || []).includes(t))) bc.splice(Math.min(2, bc.length), 0, "suwon:" + COURSES.suwon[0].id);
    const baseC = Array.from({length: Bd}, (_, i) => i < bc.length ? bc[i] : "free");
    return {base, city, C, Bd, baseC, cityC: cc.slice(0, C), nightsBase: C ? Bd : q.days - 1, nightsCity: C ? q.days - 1 - Bd : 0, themes};
  }
  /* 날짜별 목록. 출발일이 있으면 각 도시 안에서 휴무 요일을 피하도록 순서를 바꿈 */
  const qtDate = (start, i) => { if (!start) return null; const d = new Date(start + "T12:00:00"); if (isNaN(d)) return null; d.setDate(d.getDate() + i); return d; };
  function qtClosedOn(c, d){
    if (!c || !d) return [];
    const dow = d.getDay(), nth = Math.ceil(d.getDate() / 7);
    return c.stops.filter(x => x.k === "spot" && ((x.off || []).includes(dow) || (x.offNth || []).some(([n, w]) => w === dow && n === nth)));   // offNth: [몇째 주, 요일] 예) 성산일출봉 매월 첫째 월요일
  }
  function qtDays(p, q){
    const seg = (pid, ids, from) => {
      const pool = ids.slice(), out = [];
      const open = (x, d) => x !== "free" && !qtClosedOn(qtCourse(...(x.includes(":") ? x.split(":") : [pid, x])), d).length;
      ids.forEach((_, k) => {
        const d = qtDate(q.start, from + k);
        let j = d ? pool.findIndex(x => open(x, d)) : 0;   // 그날 문 연 코스 중 앞선 것, 없으면 자유일, 그것도 없으면 원래 순서
        if (j < 0) j = pool.indexOf("free");
        if (j < 0) j = 0;
        out.push(pool.splice(j, 1)[0]);
      });
      return out.map(x => x === "free" ? {k: "free", pid} : x.includes(":") ? {k: "course", pid: x.split(":")[0], id: x.split(":")[1], trip: true} : {k: "course", pid, id: x});
    };
    const days = [{k: "arrive"}, ...seg(p.base, p.baseC, 1)];
    if (p.city) { days[days.length - 1].move = p.city; days.push(...seg(p.city, p.cityC, 1 + p.Bd)); }
    days.push({k: "leave"});
    return days.map((d, i) => ({...d, n: i + 1, date: qtDate(q.start, i)}));
  }
  function qtCost(p, budget){
    const keep = PARTY; PARTY = 2;
    try {
      const from = {seoul: "incheon", busan: "gimhae"}[p.base];
      const a = from ? calcBudget(byId(from), byId(p.base), p.nightsBase, "transit", budget, false, null)
        : (r => ({...r, transport: 0}))(calcBudget(byId("seoul"), byId(p.base), p.nightsBase, "flight", budget, false, null));   // 제주 도착: 머무는 비용만
      const mode = p.city === "jeju" ? "flight" : "transit";
      const b = p.city ? calcBudget(byId(p.base), byId(p.city), p.nightsCity, mode, budget, false, null) : null;
      const f = b ? p.nightsCity / (p.nightsCity + 1) : 0;   // 하루 겹치는 식비·현지교통 빼기
      const trips = p.baseC.filter(x => x.includes(":")).reduce((s, x) => { try { return s + calcBudget(byId(p.base), byId(x.split(":")[0]), 1, "transit", budget, false, null).transport; } catch(e) { return s; } }, 0);
      const stay = a.lodging + (b ? b.lodging : 0), food = a.food + (b ? Math.round(b.food * f) : 0);
      const move = a.transport + a.local + (b ? b.transport + Math.round(b.local * f) : 0) + trips;
      return {stay, food, move, total: stay + food + move};
    } finally { PARTY = keep; }
  }
  const qtName = pid => T[lang].name(byId(pid));
  const qtFmtDate = d => { try { return d.toLocaleDateString(lang === "zh" ? (zhT ? "zh-TW" : "zh-CN") : lang, {weekday: "short", month: "short", day: "numeric"}); } catch(e) { return ""; } };
  function qtMove(p){ const X = QTX(), k = p.city === "jeju" ? "jeju" : (p.base === "busan" && p.city === "gyeongju") ? "gyeongju" : "_"; const [h, t] = X.moveTo[k]; return [h.replace("{c}", qtName(p.city)), t]; }
  function qtLeave(p){
    const X = QTX().leaveX, a = qt.air;
    if (a === "cju") return X.cju;
    if (a === "pus") return !p.city ? X.pus : p.city === "jeju" ? X.pusFromJeju : X.pusFrom(qtName(p.city));
    return !p.city ? X.icn : p.city === "jeju" ? X.icnFromJeju : X.icnFrom(qtName(p.city));
  }
  /* 하루 요약: 시간 + 이름만 한 줄씩. 자세한 시간표(이동·가격·사진)는 접어 둠 */
  function qtBrief(pid, cid){
    const c0 = qtCourse(pid, cid), L = T[lang], mu = ((INFO[pid] || {}).musts || [])[0];
    const items = c0.stops.map(x => x.k === "spot" ? `<li><b class="num">${x.at}</b> ${esc(lang === "ko" ? x.ko : x.en)}</li>`
      : x.name ? `<li class="meal"><b class="num">${x.at}</b> ${esc(L.srSlot[x.slot])} · ${esc(romKo(x.name))} <small>${esc(menuTxt(x.menu, lang))} ${L.won(x.price)}</small></li>`
      : `<li class="meal"><b class="num">${x.at}</b> ${esc(L.srSlot[x.slot])} · ${esc(EAT_NEAR[lang] || EAT_NEAR.en)}${mu ? ` <small>${esc(lang === "ko" ? mu[0] : mu[1])}</small>` : ""}</li>`).join("");
    return `<ol class="qt-brief">${items}</ol><details class="qt-more"><summary>${QTX().more}</summary>${courseOne(pid, cid)}</details>`;
  }
  function qtResult(){
    const X = QTX(), L = T[lang], p = qtPlan(qt), c = qtCost(p, qt.budget), days = qtDays(p, qt);
    const tips = keys => `<ul class="qt-tips">${keys.map(k => `<li>${X.tips[k]}</li>`).join("")}</ul>`;
    const dl = d => d.date ? ` <small class="qt-date">${esc(qtFmtDate(d.date))}</small>` : "";
    const dayCard = (d, h, body, cls) => `<section class="qt-day${cls ? " " + cls : ""}"><h3><span class="qt-dn">${X.day(d.n)}</span> ${h}${dl(d)}</h3>${body}</section>`;
    const rainHtml = pid => { const r = (QT_RAIN[pid] || [])[0]; return r ? `<p class="qt-rain">☔ ${X.rain} <a href="https://map.kakao.com/link/search/${encodeURIComponent(r[0])}" target="_blank" rel="noopener noreferrer">${esc(lang === "ko" ? r[0] : r[1])}</a></p>` : ""; };
    let html = "";
    days.forEach(d => {
      if (d.k === "arrive") { const [h, t] = X.arriveAt[qt.air] || X.arriveAt.icn; html += dayCard(d, h, `<p>${t}</p>${tips(qt.air === "cju" ? ["taxi", "cash"] : ["tmoney", "taxi"])}`, "qt-move"); return; }
      if (d.k === "leave") { html += dayCard(d, X.leaveX.home, `<p>${qtLeave(p)}</p>`, "qt-move"); return; }
      const mv = d.move ? (([h, t]) => `<p class="qt-eve"><b>${esc(h)}</b> ${esc(t)}</p>${tips(d.move === "jeju" ? [] : ["ktx"])}`)(qtMove(p)) : "";
      if (d.k === "free") { html += dayCard(d, `${esc(qtName(d.pid))} · ${X.freeT}`, `<p>${X.freeD}</p>` + mv, "qt-move"); return; }
      const c0 = qtCourse(d.pid, d.id), shut = qtClosedOn(c0, d.date);
      const go = c0.go ? `<p class="qt-go-to">🧭 ${X.go} ${esc(c0.go[lang] || c0.go.en)}</p>` : "";
      const warn = shut.length ? `<p class="qt-warn" role="note">⚠ ${esc(X.closed(shut.map(x => lang === "ko" ? x.ko : x.en).join(", ")))}</p>` : "";
      const head = `${esc(qtName(d.pid))}${d.trip ? ` <small class="qt-trip">${X.dayTrip}</small>` : ""} · ${esc(c0.t[lang] || c0.t.en)}`;
      const tk = d.pid === "seoul" && d.id === "history" ? ["hanbok", "cash"] : d.pid === "jeju" ? ["taxi", "cash"] : ["cash"];
      html += dayCard(d, head, warn + go + qtBrief(d.pid, d.id) + tips(tk) + rainHtml(d.pid) + mv);
    });
    const aff = AFF.klook || {};
    const link = (u, t) => `<a class="qt-lk" href="${esc(u)}" target="_blank" rel="noopener noreferrer">${t}</a>`;
    const needTrain = p.city && p.city !== "jeju";
    const bookLinks = [link(aff.esim || "https://www.klook.com/en-US/", X.links.esim), needTrain ? link("https://www.korail.com/", X.links.train) : "", link("https://www.agoda.com/", X.links.stay), ""];
    const A = QT_AIR[qt.air] || QT_AIR.icn;
    const airChips = Object.keys(QT_AIR).map(k => `<button type="button" class="qt-chip" data-qt-air="${k}" aria-pressed="${k === qt.air}">${esc(X.airs[k])}</button>`).join("");
    const cityChips = A.second.map(k => `<button type="button" class="qt-chip" data-qt-city="${k}" aria-pressed="${k === p.city}">${esc(qtName(k))}</button>`).join("");
    return `<div class="qt-res">
      <h2 class="qt-h" id="qt-title">${esc(X.titleX(qt.days, qtName(p.base), p.city ? qtName(p.city) : ""))}</h2>
      <div class="qt-sum"><small>${X.total} · ${X.perP}</small><b class="num">${L.won(c.total)}</b>
        <ul class="qt-parts"><li><span>${X.parts.stay}</span><b class="num">${L.won(c.stay)}</b></li><li><span>${X.parts.food}</span><b class="num">${L.won(c.food)}</b></li><li><span>${X.parts.move}</span><b class="num">${L.won(c.move)}</b></li></ul>
        <small class="qt-note">${X.notIncl}</small></div>
      <div class="qt-swap"><span>${X.air}</span>${airChips}</div>
      ${qt.days >= 4 && A.second.length ? `<div class="qt-swap"><span>${X.swap}</span>${cityChips}</div>` : ""}
      <div class="qt-start"><label for="qt-start-in">${X.start}</label><div><input type="date" id="qt-start-in" value="${esc(qt.start)}">${qt.start ? `<button type="button" class="qt-chip" id="qt-start-x">${X.clear}</button>` : ""}</div><small>${X.startNote}</small></div>
      <section class="qt-send"><h3>${X.share2}</h3><div class="qt-send-row" id="qt-send-row"></div>
        <button type="button" class="qt-xl" id="qt-xl"><b>📊 ${X.excel}</b><small>${X.excelSub}</small></button></section>
      <section class="qt-book"><h3>${X.order}</h3><ol>${X.book.map(([ic, t, s], i) => (i === 1 && !needTrain) ? "" : `<li><span class="qt-bi" aria-hidden="true">${ic}</span><div><b>${t}</b><small>${s}</small>${bookLinks[i] || ""}</div></li>`).join("")}</ol><small class="qt-note">${X.noFee}</small></section>
      ${html}
      <div class="qt-acts"><button type="button" class="rv-sub" id="qt-calc">${X.calc}</button><button type="button" class="qt-again" id="qt-again">${X.again}</button></div>
    </div>`;
  }
  /* 공유 버튼: 언어별로 많이 쓰는 앱 먼저(일본어·번체 LINE, 영어 WhatsApp, 간체는 복사해서 위챗) */
  function qtSendRow(){
    const X = QTX(), row = $("qt-send-row"); if (!row) return;
    const order = lang === "ja" || (lang === "zh" && zhT) ? ["line", "wa", "copy", "more"] : lang === "zh" ? ["copy", "more", "line", "wa"] : ["wa", "line", "copy", "more"];
    const lab = {line: X.line, wa: X.wa, copy: X.copyT, more: X.moreApps}, ic = {line: "💬", wa: "🟢", copy: "📋", more: "↗"};
    row.innerHTML = order.filter(k => k !== "more" || navigator.share).map(k => `<button type="button" class="qt-send-b" data-send="${k}"><span aria-hidden="true">${ic[k]}</span> ${lab[k]}</button>`).join("");
    row.querySelectorAll("[data-send]").forEach(b => b.addEventListener("click", () => qtSend(b.dataset.send)));
  }
  function qtLink(){
    const u = new URL("https://www.hoolzzeok.com/");
    u.searchParams.set("qt", qtKey()); u.searchParams.set("lang", lang === "zh" && zhT ? "zh-tw" : lang);
    return u.toString();
  }
  function qtShort(){
    const X = QTX(), L = T[lang], p = qtPlan(qt), c = qtCost(p, qt.budget), days = qtDays(p, qt);
    const t = X.titleX(qt.days, qtName(p.base), p.city ? qtName(p.city) : "");
    const line = d => {
      const dd = d.date ? ` (${qtFmtDate(d.date)})` : "";
      if (d.k === "arrive") return `D${d.n}${dd} ${(X.arriveAt[qt.air] || X.arriveAt.icn)[0]}`;
      if (d.k === "leave") return `D${d.n}${dd} ${X.leaveX.home}`;
      const mv = d.move ? ` → ${qtName(d.move)}` : "";
      if (d.k === "free") return `D${d.n}${dd} ${qtName(d.pid)} · ${X.freeT}${mv}`;
      const c0 = qtCourse(d.pid, d.id); return `D${d.n}${dd} ${qtName(d.pid)} · ${c0.t[lang] || c0.t.en}${mv}`;
    };
    return qtZ([X.shortHead(t, L.won(c.total)), ...days.map(line), `${X.shortLink} ${qtLink()}`].join("\n"));
  }
  async function qtSend(k){
    const X = QTX(), txt = qtShort();
    if (k === "line") { window.open(`https://line.me/R/share?text=${encodeURIComponent(txt)}`, "_blank", "noopener"); return; }
    if (k === "wa") { window.open(`https://wa.me/?text=${encodeURIComponent(txt)}`, "_blank", "noopener"); return; }
    if (k === "more") { try { await navigator.share({text: txt}); return; } catch(e) { if (e && e.name === "AbortError") return; } }
    try { await navigator.clipboard.writeText(txt); toast(X.copiedT); } catch(e) { toast(txt.slice(0, 200)); }
  }
  /* 엑셀(자세한 판): 누를 때만 SheetJS(Apache-2.0)를 불러와 휴대폰 안에서 만듦. 서버로 보내는 것 없음 */
  let xlsxP = null;
  const loadXlsx = () => xlsxP || (xlsxP = new Promise((ok, no) => { if (window.XLSX) return ok(window.XLSX); const s = document.createElement("script");
    s.src = "https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"; s.onload = () => window.XLSX ? ok(window.XLSX) : no(new Error("xlsx")); s.onerror = () => { xlsxP = null; no(new Error("xlsx")); }; document.head.appendChild(s); }));
  const qtRate = () => lang === "ja" ? FX.jpy100 / 100 : lang === "zh" ? (zhT ? FX_TWD : FX.cny) : FX.usd;
  const qtCur = () => lang === "ja" ? "JPY" : lang === "zh" ? (zhT ? "TWD" : "CNY") : "USD";
  const qtGoTo = ko => { const c = String(ko).slice(-1).charCodeAt(0), j = c >= 0xAC00 && c <= 0xD7A3 ? (c - 0xAC00) % 28 : 0; return `${ko}${j === 0 || j === 8 ? "로" : "으로"} 가 주세요.`; };
  async function qtExcel(){
    const X = QTX(), Y = X.xl, L = T[lang], btn = $("qt-xl");
    if (btn) { btn.disabled = true; btn.querySelector("small").textContent = X.excelBusy; }
    try {
      const XL = await loadXlsx(), p = qtPlan(qt), c = qtCost(p, qt.budget), days = qtDays(p, qt);
      const title = X.titleX(qt.days, qtName(p.base), p.city ? qtName(p.city) : "");
      const rows = [[title], [Y.note], [], Y.cols], ko = [Y.kcols], seen = new Set();
      const hNum = h => (String(h || "").match(/\d{1,2}:\d{2}\s*~\s*\d{1,2}:\d{2}/) || [""])[0];
      days.forEach(d => {
        const dt = d.date ? qtFmtDate(d.date) : "";
        if (d.k === "arrive") { const [h, t] = X.arriveAt[qt.air] || X.arriveAt.icn; rows.push([d.n, dt, "", h, "", "", t, "", ""]); return; }
        if (d.k === "leave") { rows.push([d.n, dt, "", X.leaveX.home, "", "", qtLeave(p), "", ""]); return; }
        if (d.k === "free") rows.push([d.n, dt, "", `${qtName(d.pid)} · ${X.freeT}`, "", "", X.freeD, "", ""]);
        else {
          const c0 = qtCourse(d.pid, d.id);
          rows.push([d.n, dt, "", `${qtName(d.pid)} · ${c0.t[lang] || c0.t.en}`, "", "", c0.go ? `${X.go} ${c0.go[lang] || c0.go.en}` : "", "", qtClosedOn(c0, d.date).length ? X.closed(qtClosedOn(c0, d.date).map(x => x.en).join(", ")) : ""]);
          c0.stops.forEach(x => {
            const g = x.leg, how = !g ? "" : g.m === "walk" ? Y.walk(g.min) : g.m === "taxi" ? Y.taxi(g.min, g.fare) : Y.near;
            if (x.k === "spot") {
              rows.push(["", "", x.at, lang === "ko" ? x.ko : x.en, x.ko, x.addr || "", how, g && g.fare ? g.fare : "", lang === "ko" ? x.h : (hNum(x.h) || "")]);
              if (!seen.has(x.ko)) { seen.add(x.ko); ko.push([lang === "ko" ? x.ko : x.en, x.ko, qtGoTo(x.ko)]); }
            } else if (x.name) rows.push(["", "", x.at, `${L.srSlot[x.slot]} · ${romKo(x.name)} (${menuTxt(x.menu, lang)})`, x.name, x.addr || "", how, x.price || "", x.tel || ""]);
            else rows.push(["", "", x.at, `${L.srSlot[x.slot]} · ${EAT_NEAR[lang] || EAT_NEAR.en}`, x.area || "", "", how, "", ""]);
          });
          const r = (QT_RAIN[d.pid] || [])[0]; if (r) rows.push(["", "", "", `☔ ${X.rain} ${lang === "ko" ? r[0] : r[1]}`, r[0], "", "", "", ""]);
        }
        if (d.move) { const [h, t] = qtMove(p); rows.push(["", "", "", h, "", "", t, "", ""]); }
      });
      const wb = XL.utils.book_new();
      const s1 = XL.utils.aoa_to_sheet(rows.map(r => r.map(v => typeof v === "string" ? qtZ(v) : v)));
      s1["!cols"] = [5, 12, 7, 34, 22, 30, 34, 10, 26].map(w => ({wch: w}));
      XL.utils.book_append_sheet(wb, s1, qtZ(Y.plan));
      /* 예산: 금액·환율·인원을 바꾸면 수식으로 다시 계산 */
      const b = [[qtZ(title)], [qtZ(Y.rate) + ` (${qtCur()})`, +qtRate().toFixed(2)], [qtZ(Y.people), 2], [], Y.bcols.map(qtZ),
        [qtZ(X.parts.stay), c.stay], [qtZ(X.parts.food), c.food], [qtZ(X.parts.move), c.move], [qtZ(Y.extra), 0]];
      const s2 = XL.utils.aoa_to_sheet(b);
      for (let i = 6; i <= 9; i++) s2[`C${i}`] = {t: "n", f: `ROUND(B${i}/$B$2,1)`};
      XL.utils.sheet_add_aoa(s2, [[qtZ(Y.total)], [qtZ(Y.group)]], {origin: "A10"});
      s2.B10 = {t: "n", f: "SUM(B6:B9)"}; s2.C10 = {t: "n", f: "ROUND(B10/$B$2,1)"}; s2.B11 = {t: "n", f: "B10*$B$3"}; s2.C11 = {t: "n", f: "ROUND(B11/$B$2,1)"};
      s2["!ref"] = "A1:C11"; s2["!cols"] = [{wch: 34}, {wch: 16}, {wch: 22}];
      XL.utils.book_append_sheet(wb, s2, qtZ(Y.budget));
      const bk = [[X.order, "", Y.done], ...X.book.filter((_, i) => i !== 1 || (p.city && p.city !== "jeju")).map(([ic, t, s]) => [`${ic} ${t}`, s, "☐"])];
      const s3 = XL.utils.aoa_to_sheet(bk.map(r => r.map(qtZ))); s3["!cols"] = [{wch: 28}, {wch: 70}, {wch: 6}];
      XL.utils.book_append_sheet(wb, s3, qtZ(Y.book));
      const s4 = XL.utils.aoa_to_sheet(ko.map((r, i) => i ? [qtZ(r[0]), r[1], r[2]] : r.map(qtZ))); s4["!cols"] = [{wch: 34}, {wch: 22}, {wch: 30}];
      XL.utils.book_append_sheet(wb, s4, qtZ(Y.korean));
      XL.writeFile(wb, `hoolzzeok-korea-${qt.days}days.xlsx`);
      if (btn) btn.querySelector("small").textContent = X.excelSub;
    } catch(e) { toast(X.excelFail); if (btn) btn.querySelector("small").textContent = X.excelSub; }
    finally { if (btn) btn.disabled = false; }
  }
  function qtRender(){
    const X = QTX(), L = T[lang], box = $("qt-body");
    $("qt-back").hidden = qt.step === 1 || qt.step === 4;
    $("qt-prog").style.width = `${Math.min(100, (qt.step - 1) / 3 * 100)}%`;
    $("qt-step").textContent = qt.step <= 3 ? X.step(qt.step) : "";
    const btns = (items, key, multi) => `<div class="qt-opts">${items.map(([v, t, s, ic]) => `<button type="button" class="qt-opt" data-k="${key}" data-v="${v}" aria-pressed="${multi ? qt.themes.includes(v) : qt[key] === v}">${ic ? `<span class="qt-ic" aria-hidden="true">${ic}</span>` : ""}<b>${t}</b>${s ? `<small>${s}</small>` : ""}${multi && qt.themes.includes(v) ? `<span class="qt-pick num">${qt.themes.indexOf(v) + 1}</span>` : ""}</button>`).join("")}</div>`;
    if (qt.step === 1) box.innerHTML = `<h2 class="qt-h" id="qt-title">${X.q1}</h2><p class="qt-sub">${X.q1s}</p>` + btns([3, 4, 5, 6, 7].map(n => [n, X.days(n), "", ""]), "days");
    else if (qt.step === 2) box.innerHTML = `<h2 class="qt-h" id="qt-title">${X.q2}</h2><p class="qt-sub">${X.q2s}</p>` + btns(Object.keys(QT_THEMES).map(k => [k, X.themes[k][0], X.themes[k][1], QT_THEMES[k]]), "themes", true)
      + `<button type="button" class="rv-main qt-next" id="qt-next"${qt.themes.length ? "" : " disabled"}>${X.next}</button><small class="qt-src">${X.src}</small>`;
    else if (qt.step === 3) box.innerHTML = `<h2 class="qt-h" id="qt-title">${X.q3}</h2>` + btns(["budget", "standard", "comfort"].map(k => [k, X.budgets[k][0], X.budgets[k][1], ""]), "budget");
    else box.innerHTML = qtResult();
    box.querySelectorAll(".qt-opt").forEach(b => b.addEventListener("click", () => {
      const k = b.dataset.k, v = b.dataset.v;
      if (k === "themes") {   // 2개까지. 두 번째를 고르면 바로 다음으로
        const i = qt.themes.indexOf(v); if (i >= 0) qt.themes.splice(i, 1); else { if (qt.themes.length >= 2) qt.themes.shift(); qt.themes.push(v); }
        qt.city = null; if (qt.themes.length === 2) return qtGo(3); return qtRender();
      }
      qt[k] = k === "days" ? +v : v; qtGo(qt.step + 1); }));
    const nx = $("qt-next"); if (nx) nx.addEventListener("click", () => qt.themes.length && qtGo(3));
    box.querySelectorAll("[data-qt-city]").forEach(b => b.addEventListener("click", () => { qt.city = b.dataset.qtCity; qtRender(); qtUrl(); }));
    box.querySelectorAll("[data-qt-air]").forEach(b => b.addEventListener("click", () => { qt.air = b.dataset.qtAir; qt.city = null; qtRender(); qtUrl(); }));
    const si = $("qt-start-in"); if (si) si.addEventListener("change", () => { qt.start = /^\d{4}-\d{2}-\d{2}$/.test(si.value) ? si.value : ""; qtRender(); qtUrl(); });
    const sx = $("qt-start-x"); if (sx) sx.addEventListener("click", () => { qt.start = ""; qtRender(); qtUrl(); });
    qtSendRow();
    const xl = $("qt-xl"); if (xl) xl.addEventListener("click", qtExcel);
    const ag = $("qt-again"); if (ag) ag.addEventListener("click", () => { qt.days = qt.budget = qt.city = null; qt.themes = []; qt.start = ""; qtGo(1); });
    const cl = $("qt-calc"); if (cl) cl.addEventListener("click", () => { const p = qtPlan(qt); qtClose();
      const from = {seoul: "incheon", busan: "gimhae", jeju: "seoul"}[p.base];
      if (p.city) { state.origin = p.base; state.dest = p.city; state.nights = Math.min(6, p.nightsCity); } else { state.origin = from; state.dest = p.base; state.nights = Math.min(6, p.nightsBase); }
      state.picked = state.dest; state.half = false; state.style = qt.budget; state.mode = p.city === "jeju" || (!p.city && p.base === "jeju") ? "flight" : "transit"; state.picks = []; render(); setTimeout(() => toResult(), 60); });
    const h = $("qt-title") || box.querySelector("h2"); if (h) { h.tabIndex = -1; h.focus({preventScroll: true}); }
  }
  const qtKey = () => [qt.days, qt.themes.join("+"), qt.budget, qt.city || "", qt.air !== "icn" ? qt.air : "", qt.start ? qt.start.replace(/-/g, "") : ""].join(".").replace(/\.+$/, "");
  function qtUrl(){
    try { const u = new URL(location.href); if (qt.step === 4) u.searchParams.set("qt", qtKey()); else u.searchParams.delete("qt"); history.replaceState(history.state, "", u.toString()); } catch(e) {}
  }
