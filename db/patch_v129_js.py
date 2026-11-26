# v129 여행 후기 JS: 한 화면 후기 쓰기 + 새 후기 보기
p = '/home/claude/hoolzzeok_site/index.html'
s = open(p, encoding='utf-8').read()
def R(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (a[:80], c)
    s = s.replace(a, b)
def span(start, end):
    """start 문자열부터 end 문자열 바로 앞까지를 돌려줌 (둘 다 정확히 한 번)"""
    assert s.count(start) == 1, ('start', start[:60], s.count(start))
    i = s.index(start); j = s.index(end, i)
    return s[i:j]

# 1) 상수·상태
R('''  const cmF = {mood: null, say: [], tags: []};''',
'''  const cmF = {mood: null, star: 0, kw: [], say: [], tags: [], pick: null};
  /* v129 후기 쓰기: 별점(1~5)은 cost.star 에, 키워드는 tags 에 'k:키' 로 저장 (DB 칸 그대로). mood 는 별점에서 자동 */
  const RW_STAR = ["", "별로였어요", "아쉬웠어요", "괜찮았어요", "좋았어요", "최고였어요"];
  const RW_KW = {
    good: [["food","🍜","밥이 맛있어요"],["value","💰","가성비 좋아요"],["view","🌊","경치가 좋아요"],["stay","🛏️","숙소가 좋아요"],["quiet","🌿","한적해요"],["easy","🚌","다니기 편해요"],["photo","📸","사진 찍기 좋아요"],["kids","🧒","아이와 좋아요"],["parents","👵","부모님과 좋아요"],["solo","🎒","혼자도 좋아요"],["again","🔁","또 가고 싶어요"]],
    bad: [["pricey","💸","생각보다 비싸요"],["crowd","🚶","사람이 많아요"],["move","🚧","이동이 불편해요"],["nofood","🍽️","먹을 곳이 적어요"],["staybad","🛌","숙소가 아쉬워요"],["needcar","🚗","차 없으면 힘들어요"],["weather","🌧️","날씨 운이 없었어요"]]
  };
  const RW_KW_ALL = [...RW_KW.good.map(x => [...x, "good"]), ...RW_KW.bad.map(x => [...x, "bad"])];
  const rwKw = k => RW_KW_ALL.find(x => x[0] === k);
  const rwMood = n => n >= 4 ? "good" : n === 3 ? "ok" : n ? "bad" : null;
  const RW_STAR_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2.6l2.9 6 6.6.8-4.9 4.6 1.3 6.5L12 17.3 6.1 20.5l1.3-6.5L2.5 9.4l6.6-.8z"/></svg>';
  const cmMan = v => v >= 10000 ? (Math.round(v / 1000) / 10) + "만 원" : T.ko.won(v);''')

# 2) cmRoute: 경로 글 + 쓴 돈 고르기(덜/비슷/더) + 금액 칸
old = span('  function cmRoute(){', '  function cmSave(){')
s = s.replace(old, '''  function cmRoute(){
    const o = byId($("cm-origin").value), d = byId($("cm-dest").value), L = T.ko;
    $("cm-route-txt").textContent = o && d ? `${L.name(o)} → ${L.name(d)} · ${L.nights(+$("cm-nights").value)} · ${Math.max(1, +$("cm-people").value || 1)}명 · ${L.mode[$("cm-mode").value] || ""}` : "어디 다녀오셨는지 골라 주세요";
    const est = cmEst();
    $("cm-est-txt").innerHTML = est ? `훌쩍 예상은 한 사람 <b>${cmMan(est)}</b>이었어요. 실제로는요?` : "예상 금액이 없는 길이에요. 쓴 돈을 바로 적어 주세요.";
    cmRcPaint();
    const opts = est ? [["less", "덜 썼어요", "예상보다 적게"], ["same", "비슷해요", "거의 같게"], ["more", "더 썼어요", "예상보다 많이"]] : [];
    $("cm-quick").hidden = !est;
    $("cm-quick").innerHTML = opts.map(([k, t, sub]) => `<button type="button" data-k="${k}" aria-pressed="${cmF.pick === k}">${t}<small>${sub}</small></button>`).join("");
    $("cm-quick").querySelectorAll("button").forEach(b => b.addEventListener("click", () => {
      const f = {less: .85, same: 1, more: 1.15}[b.dataset.k], cur = cmEst();
      cmF.pick = b.dataset.k; cmPress($("cm-quick"), x => x === b);
      if (cur) $("cm-total").value = cmFmt(Math.round(cur * f / 10000) * 10000 || 10000);
      $("rw-amt").hidden = false; cmSave(); }));
    $("rw-amt").hidden = !!est && !cmNum($("cm-total").value) && !cmF.pick;
  }
''')

# 3) 임시 저장·채우기
old = span('  function cmSave(){', '  function cmFillForm(keepDraft){')
s = s.replace(old, '''  function cmSave(){
    try { localStorage.setItem("hz-cm-draft", JSON.stringify({star: cmF.star, kw: cmF.kw, pick: cmF.pick, tags: cmF.tags, total: $("cm-total").value, text: $("cm-text").value, parts: Object.fromEntries(CM_COSTS.map(([k]) => [k, (($("cm-c-" + k) || {}).value) || ""])),
      o: $("cm-origin").value, d: $("cm-dest").value, n: $("cm-nights").value, m: $("cm-mode").value, p: $("cm-people").value})); } catch(e) {}
  }
''')
old = span('  function cmFillForm(keepDraft){', '  function cmFormBind(){')
s = s.replace(old, '''  function cmFillForm(keepDraft){
    $("cm-origin").value = state.origin; $("cm-dest").value = state.dest; $("cm-nights").value = String(state.nights);
    $("cm-mode").value = state.mode; $("cm-people").value = String(state.people || 2);
    cmF.mood = null; cmF.star = 0; cmF.kw = []; cmF.say = []; cmF.tags = []; cmF.pick = null; $("cm-total").value = ""; $("cm-text").value = "";
    CM_COSTS.forEach(([k]) => { const el = $("cm-c-" + k); if (el) el.value = ""; });
    let dr = null; if (keepDraft) { try { dr = JSON.parse(localStorage.getItem("hz-cm-draft") || "null"); } catch(e) {} }
    if (dr) {
      if (byId(dr.o)) $("cm-origin").value = dr.o;
      if (byId(dr.d)) $("cm-dest").value = dr.d;
      if (dr.n != null) $("cm-nights").value = String(dr.n);
      if (dr.m) $("cm-mode").value = dr.m;
      if (dr.p) $("cm-people").value = String(dr.p);
      cmF.star = Math.max(0, Math.min(5, +dr.star || 0)); cmF.mood = rwMood(cmF.star);
      cmF.kw = (dr.kw || []).filter(k => rwKw(k)); cmF.tags = (dr.tags || []).filter(x => CM_TAGS.includes(x));
      cmF.pick = ["less", "same", "more"].includes(dr.pick) ? dr.pick : null;
      $("cm-total").value = dr.total || ""; $("cm-text").value = dr.text || "";
      cmDraftParts = dr.parts || null;
    }
    rwStars();
    const kwBox = (box, list, cls) => { box.className = "rw-kw" + (cls ? " " + cls : "");
      box.innerHTML = list.map(([k, ic, t]) => `<button type="button" data-k="${k}" aria-pressed="${cmF.kw.includes(k)}"><span aria-hidden="true">${ic}</span> ${t}</button>`).join("");
      box.querySelectorAll("button").forEach(b => b.addEventListener("click", () => { const k = b.dataset.k, on = !cmF.kw.includes(k);
        if (on && cmF.kw.length >= 5) { $("cm-msg").textContent = "5개까지 고를 수 있어요."; return; }
        cmF.kw = on ? [...cmF.kw, k] : cmF.kw.filter(x => x !== k); b.setAttribute("aria-pressed", String(on)); $("cm-msg").textContent = ""; cmSave(); })); };
    /* 별점이 3 이하면 아쉬웠던 점을 먼저 (에어비앤비처럼 점수에 맞춰 묻기) */
    const lowFirst = cmF.star && cmF.star <= 3;
    $("rw-kw-h").firstChild.textContent = lowFirst ? "아쉬웠던 점 " : "좋았던 점 ";
    $("rw-kw-h2").textContent = lowFirst ? "좋았던 점도 있었다면" : "아쉬웠던 점도 있었다면";
    kwBox($("cm-say"), lowFirst ? RW_KW.bad : RW_KW.good, lowFirst ? "bad" : "");
    kwBox($("cm-say2"), lowFirst ? RW_KW.good : RW_KW.bad, lowFirst ? "" : "bad");
    $("cm-tagpick").innerHTML = CM_TAGS.map(t => `<button type="button" data-t="${t}" aria-pressed="${cmF.tags.includes(t)}">#${t}</button>`).join("");
    $("cm-tagpick").querySelectorAll("button").forEach(b => b.addEventListener("click", () => { const t = b.dataset.t, on = !cmF.tags.includes(t);
      if (on && cmF.tags.length >= 4) { $("cm-msg").textContent = "취미 태그는 4개까지예요."; return; }
      cmF.tags = on ? [...cmF.tags, t] : cmF.tags.filter(x => x !== t); b.setAttribute("aria-pressed", String(on)); cmSave(); }));
    cmPaintRoute(); cmRoute(); rwFoot();
  }
  function rwStars(){
    const box = $("cm-stars"); if (!box) return;
    box.innerHTML = [1, 2, 3, 4, 5].map(n => `<button type="button" role="radio" data-n="${n}" aria-checked="${cmF.star === n}" aria-label="별 ${n}개, ${RW_STAR[n]}" class="${n <= cmF.star ? "on" : ""}" tabindex="${(cmF.star || 1) === n ? 0 : -1}">${RW_STAR_SVG}</button>`).join("");
    $("cm-star-t").textContent = cmF.star ? RW_STAR[cmF.star] : "별을 눌러 주세요";
    $("cm-star-t").classList.toggle("empty", !cmF.star);
    $("rw-more").hidden = !cmF.star;
  }
  function rwSetStar(n){
    const first = !cmF.star, wasLow = cmF.star && cmF.star <= 3;
    cmF.star = n; cmF.mood = rwMood(n);
    const nowLow = n <= 3;
    if (first || wasLow !== nowLow) { cmSave(); cmFillForm(true); }
    else rwStars();
    cmSave(); rwFoot();
    const b = $("cm-stars").querySelector(`[data-n="${n}"]`); if (b) b.focus({preventScroll: true});
    if (first) setTimeout(() => { const m = $("rw-more"); if (m && !m.hidden) m.scrollIntoView({behavior: reduce ? "auto" : "smooth", block: "start"}); }, 220);
  }
''')

# 4) 폼 연결
old = span('  function cmFormBind(){', '  function cmChips(){')
s = s.replace(old, '''  function cmFormBind(){
    cmAC("cm-origin"); cmAC("cm-dest");
    $("cm-nights-c").addEventListener("click", e => { const b = e.target.closest("button[data-n]"); if (b) cmSetRoute("cm-nights", b.dataset.n); });
    $("cm-mode-c").addEventListener("click", e => { const b = e.target.closest("button[data-m]"); if (b) cmSetRoute("cm-mode", b.dataset.m); });
    $("cm-p-minus").addEventListener("click", () => cmSetRoute("cm-people", Math.max(1, (+$("cm-people").value || 1) - 1)));
    $("cm-p-plus").addEventListener("click", () => cmSetRoute("cm-people", Math.min(20, (+$("cm-people").value || 1) + 1)));
    $("cm-total").addEventListener("input", () => { const n = cmNum($("cm-total").value); $("cm-total").value = cmFmt(n); cmSave(); });
    $("cm-text").addEventListener("input", cmSave);
    $("rw-amt").querySelectorAll("[data-d]").forEach(b => b.addEventListener("click", () => {
      const n = Math.max(0, cmNum($("cm-total").value) + +b.dataset.d); $("cm-total").value = cmFmt(n); cmSave(); }));
    const routeToggle = open => { $("cm-route-box").hidden = !open; $("cm-route-edit").setAttribute("aria-expanded", String(open)); $("cm-route-edit").textContent = open ? "접기" : "바꾸기"; };
    $("cm-route-edit").addEventListener("click", () => routeToggle($("cm-route-box").hidden));
    $("cm-route-done").addEventListener("click", () => { routeToggle(false); $("cm-stars").scrollIntoView({behavior: reduce ? "auto" : "smooth", block: "center"}); });
    $("cm-stars").addEventListener("click", e => { const b = e.target.closest("button[data-n]"); if (b) rwSetStar(+b.dataset.n); });
    $("cm-stars").addEventListener("keydown", e => {
      const d = {ArrowRight: 1, ArrowUp: 1, ArrowLeft: -1, ArrowDown: -1}[e.key]; if (!d) return;
      e.preventDefault(); rwSetStar(Math.max(1, Math.min(5, (cmF.star || 0) + d))); });
  }
''')

# 5) 지역 칩(후기 있는 곳만, 개수) + 고른 태그
old = span('  function cmChips(){', '  const cmSum = c =>')
s = s.replace(old, '''  function cmChips(){
    const cnt = {}; cm.reviews.forEach(r => { cnt[r.region] = (cnt[r.region] || 0) + 1; });
    const regs = CM_REGIONS.filter(([k]) => k === "all" || cnt[k] || cm.region === k);
    $("cm-regions").hidden = regs.length < 3;
    $("cm-regions").innerHTML = regs.map(([k, n]) => `<button type="button" data-r="${k}" aria-pressed="${cm.region === k}">${n} <small>${k === "all" ? cm.reviews.length : cnt[k] || 0}</small></button>`).join("");
    $("cm-regions").querySelectorAll("button").forEach(b => b.addEventListener("click", () => { cm.region = b.dataset.r; cmRender(); }));
    $("cm-tags").hidden = !cm.tag;
    $("cm-tags").innerHTML = cm.tag ? `<button type="button" aria-label="#${esc(cm.tag)} 거르기 풀기">#${esc(cm.tag)} ✕</button>` : "";
    const tb = $("cm-tags").querySelector("button"); if (tb) tb.addEventListener("click", () => { cm.tag = null; cmRender(); });
  }
''')

# 6) 카드
old = span('  function cmCard(r, mode){', '  function cmBind(box){')
s = s.replace(old, '''  const cmEstCache = {};
  function cmEstOf(r){
    const key = [r.origin, r.dest, r.nights, r.mode].join("|");
    if (key in cmEstCache) return cmEstCache[key];
    const o = byId(r.origin) || byId("seoul"), d = byId(r.dest); let est = null;
    try { if (d && o.id !== d.id && modeAvailable(o, d, r.mode)) est = calcBudget(o, d, r.nights, r.mode, "standard", false, null).total; } catch(e) {}
    return (cmEstCache[key] = est);
  }
  function cmDiff(r){
    const sum = cmSum(r.cost || {}), n = r.cost && +r.cost.total > 0 ? 6 : (r.cost && CM_COSTS.filter(([k]) => +r.cost[k] > 0).length) || 0, est = cmEstOf(r);
    return {sum, est, pct: est && sum && n >= 4 ? Math.round((sum - est) / est * 100) : null};
  }
  const cmStarOf = r => { const n = Math.round(+(r.cost && r.cost.star) || 0); return n >= 1 && n <= 5 ? n : 0; };
  function cmCard(r, mode){
    const o = byId(r.origin) || byId("seoul"), d = byId(r.dest), L = T.ko;
    if (!d) return "";
    const {sum, est, pct} = cmDiff(r), star = cmStarOf(r), open = cm.open[r.id];
    const kws = (r.tags || []).filter(t => /^k:/.test(t)).map(t => rwKw(t.slice(2))).filter(Boolean);
    const hob = (r.tags || []).filter(t => !/^k:/.test(t));
    const when = (r.at || "").slice(0, 10).split("-").map(Number);
    const meta = [`${L.name(o)}에서`, `${+r.people || 1}명`, L.mode[r.mode] || "", when[1] ? `${when[1]}월 ${when[2]}일 작성` : ""].filter(Boolean).join(" · ");
    const max = Math.max(sum || 0, est || 0) || 1;
    const money = sum ? `<div class="rl-money">
        <div class="rl-money-row"><small>1인 실제로 쓴 돈</small><b class="num">${cmMan(sum)}</b></div>
        ${est ? `<div class="rl-bar" aria-hidden="true"><i style="width:${Math.round(sum / max * 100)}%"></i><u style="left:calc(${Math.round(est / max * 100)}% - 1px)"></u></div>
        <div class="rl-money-row"><small>훌쩍 예상 (세로 줄)</small><span class="est num">${cmMan(est)}</span></div>` : ""}
        ${pct != null ? `<p class="rl-diff ${Math.abs(pct) < 5 ? "" : pct < 0 ? "less" : "more"}">${Math.abs(pct) < 5 ? "예상과 거의 같았어요" : `예상보다 ${Math.abs(pct)}% ${pct < 0 ? "덜 들었어요" : "더 들었어요"}`}</p>` : est ? `<p class="rl-diff">항목 일부만 적었어요</p>` : ""}
      </div>` : "";
    const btns = mode === "pending"
      ? `<button type="button" class="go" data-act="approve" data-id="${esc(r.id)}" data-uid="${esc(r.uid)}">승인</button><button type="button" class="sub warn" data-act="reject" data-id="${esc(r.id)}" data-uid="${esc(r.uid)}">반려</button>`
      : `<button type="button" class="go" data-act="calc" data-id="${esc(r.id)}">이 여행 경비 계산하기</button>${(r.text || "").length > 140 ? `<button type="button" class="sub" data-act="more" data-id="${esc(r.id)}">${open ? "접기" : "더 보기"}</button>` : ""}<span class="sp"></span>${cm.uid && !cm.admin ? (cm.myReports.includes(r.id) ? `<button type="button" class="sub" disabled>신고함</button>` : `<button type="button" class="sub" data-act="report" data-id="${esc(r.id)}">신고</button>`) : ""}${cm.admin ? `<button type="button" class="sub warn" data-act="hide" data-id="${esc(r.id)}">숨기기${cm.reports[r.id] ? ` (신고 ${cm.reports[r.id]})` : ""}</button>` : ""}`;
    return `<li class="cm-card rl-card">${reviewPaid(r) ? `<p class="cm-paid">${REVIEW_PAID.txt}</p>` : ""}
      <div class="rl-top"><span class="rl-av" aria-hidden="true">${esc(L.name(d).slice(0, 1))}</span><div class="rl-tt"><h3>${esc(L.name(d))} ${L.nights(r.nights)}</h3><span class="rl-meta">${esc(meta)}</span></div>
        ${star ? `<span class="rl-star" aria-label="별점 ${star}점"><i aria-hidden="true">★</i> ${star}</span>` : r.mood ? `<span class="rl-mood">${esc(cmMoodTxt(r.mood))}</span>` : ""}</div>
      ${kws.length || hob.length ? `<div class="rl-kws">${kws.map(([, ic, t, , g]) => `<span class="rl-kw${g === "bad" ? " bad" : ""}">${ic} ${t}</span>`).join("")}${hob.map(t => `<button type="button" class="rl-tag" data-act="tag" data-id="${esc(r.id)}" data-tag="${esc(t)}">#${esc(t)}</button>`).join("")}</div>` : ""}
      ${r.text ? `<p class="cm-text${open ? "" : " short"}">${esc(r.text)}</p>` : ""}
      ${money}
      <div class="rl-acts">${btns}</div></li>`;
  }
''')
R('''    box.querySelectorAll("[data-act]").forEach(b => b.addEventListener("click", () => cmAct(b.dataset.act, b.dataset.id, b.dataset.uid, b)));''',
'''    box.querySelectorAll("[data-act]").forEach(b => b.addEventListener("click", () => { if (b.dataset.act === "tag") { cm.tag = b.dataset.tag; cmRender(); $("rp").scrollTo({top: 0, behavior: reduce ? "auto" : "smooth"}); return; } cmAct(b.dataset.act, b.dataset.id, b.dataset.uid, b); }));''')

# 7) 목록 + 요약
old = span('  function cmRender(){', '  function cmCalc(r){')
s = s.replace(old, '''  function cmRender(){
    if (!$("rp")) return;
    try { rvSync(); } catch(e) {}
    cmChips();
    const list = cm.reviews.filter(r => (cm.region === "all" || r.region === cm.region) && (!cm.tag || (r.tags || []).includes(cm.tag)));
    const canWrite = !(cm.canWrite === false || (!cm.sb && !cm.uid) || cm.db === false);
    /* 요약: 평균 별점, 실제 경비와 예상의 평균 차이 (훌쩍만의 숫자) */
    { const stars = cm.reviews.map(cmStarOf).filter(Boolean), diffs = cm.reviews.map(r => cmDiff(r).pct).filter(x => x != null);
      const avg = stars.length ? (stars.reduce((a, b) => a + b, 0) / stars.length).toFixed(1) : null;
      const md = diffs.length ? Math.round(diffs.reduce((a, b) => a + b, 0) / diffs.length) : null;
      const cta = canWrite ? `<button type="button" class="rl-sum-cta" data-rv-open>✏️ 내 여행 후기 쓰기<small>30초</small></button>` : "";
      $("rl-sum").innerHTML = !cm.loaded ? "" : cm.reviews.length
        ? `<div class="rl-sum-top">${avg ? `<span class="rl-sum-star"><i aria-hidden="true">★</i> ${avg}</span>` : ""}<span class="rl-sum-n">후기 ${cm.reviews.length}개</span></div>
           ${md != null ? `<p class="rl-sum-diff">실제로 쓴 돈은 훌쩍 예상과 평균 <b>${Math.abs(md) < 5 ? "거의 같았어요" : `${Math.abs(md)}% ${md < 0 ? "덜 들었어요" : "더 들었어요"}`}</b> <small>(경비를 적은 후기 ${diffs.length}개)</small></p>` : ""}${cta}`
        : `<p class="rl-sum-empty"><b>아직 후기가 없어요.</b><br>다녀온 여행의 실제 경비를 남기면 다음 사람이 경비를 더 정확히 짤 수 있어요.</p>${cta}`;
      $("rl-sum").querySelectorAll("[data-rv-open]").forEach(b => b.addEventListener("click", () => rvOpen())); }
    if (!cm.loaded) $("cm-list").innerHTML = "";
    else if (!list.length) $("cm-list").innerHTML = cm.reviews.length ? `<li class="rl-empty"><b>이 조건의 후기가 아직 없어요</b><span>다른 지역을 골라 보세요.</span></li>` : "";
    else $("cm-list").innerHTML = list.map(r => cmCard(r)).join("");
    cmBind($("cm-list"));
    $("cm-write").hidden = !canWrite || !cm.loaded;
    const mineWaiting = cm.mine.length;
    $("cm-status").textContent = !cm.loaded ? (cm.db === false ? "" : "후기를 불러오는 중이에요…") : (cm.region !== "all" || cm.tag ? `후기 ${list.length}개` : "") + (mineWaiting ? `${cm.region !== "all" || cm.tag ? ", " : ""}내 후기 ${mineWaiting}개 확인 중` : "");
    $("cm-admin").hidden = !cm.admin || !cm.pending.length;
    if (cm.admin && cm.pending.length) { $("cm-admin").innerHTML = `<h3>승인 대기 ${cm.pending.length}건</h3><ol class="cm-list">${cm.pending.map(r => cmCard(r, "pending")).join("")}</ol>`; cmBind($("cm-admin")); }
  }
''')

# 8) 보내기
old = span('  async function cmSubmit(ev){', '  /* ===== v99: 반값여행 안내 페이지')
s = s.replace(old, '''  async function cmSubmit(ev){
    ev.preventDefault();
    const msg = $("cm-msg"), send = $("cm-send"), L = T.ko;
    if ((!cm.db && !cm.sb) || !cm.uid) { msg.textContent = "지금은 후기를 보낼 수 없어요."; return; }
    const dest = byId($("cm-dest").value), origin = byId($("cm-origin").value);
    if (!cmF.star) { msg.textContent = "별점을 먼저 눌러 주세요."; $("cm-stars").scrollIntoView({block: "center"}); return; }
    if (!dest || !origin) { msg.textContent = "다녀온 곳을 골라 주세요. 위 '바꾸기'를 눌러요."; return; }
    if (origin.id === dest.id) { msg.textContent = "출발과 도착이 같아요. 위 '바꾸기'로 고쳐 주세요."; return; }
    if (!$("cm-agree").checked) { msg.textContent = "아래 확인 칸에 체크해 주세요."; $("cm-agree-row").scrollIntoView({block: "center"}); return; }
    const cost = {}; CM_COSTS.forEach(([k]) => { const v = cmNum(($("cm-c-" + k) || {}).value); if (v > 0) cost[k] = Math.min(v, 5000000); });
    const parts = CM_COSTS.reduce((s2, [k]) => s2 + (cost[k] || 0), 0), typed = cmNum($("cm-total").value);
    const total = Math.min(parts || typed, 5000000); if (total > 0) cost.total = total;
    cost.star = cmF.star;
    const nights = +$("cm-nights").value, people = Math.max(1, Math.min(20, Math.round(+$("cm-people").value || 1)));
    const free = $("cm-text").value.trim().slice(0, 1500);
    /* 글을 안 써도 되게: 비어 있으면 고른 키워드나 별점 말로 채움 (DB는 본문 1자 이상) */
    const body = free || (cmF.kw.length ? cmF.kw.map(k => rwKw(k)[2]).join(". ") + "." : RW_STAR[cmF.star] + ".");
    const title = `${L.name(dest)} ${L.nights(nights)}, ${people}명` + (total ? `, 1인 ${cmMan(total)}` : "");
    const item = {id: Date.now().toString(36) + Math.random().toString(36).slice(2, 6), uid: cm.uid, at: new Date().toISOString(),
      title: title.slice(0, 60), origin: origin.id, dest: dest.id, region: regionOfPlace(dest), nights, mode: $("cm-mode").value,
      people, tags: [...cmF.kw.slice(0, 5).map(k => "k:" + k), ...cmF.tags.slice(0, 4)].slice(0, 9), mood: rwMood(cmF.star), cost, text: body.slice(0, 2000)};
    send.disabled = true; msg.textContent = "올리는 중…";
    try {
      if (await BE().submit(item) === "full") { msg.textContent = "확인 중인 후기가 5개 있어요. 공개된 뒤에 더 올려 주세요."; return; }
      try { localStorage.removeItem("hz-cm-draft"); } catch(e) {}
      cmFillForm(false);
      msg.textContent = "보냈어요. 확인 후 공개돼요. 고마워요!";
    } catch(e) {
      msg.textContent = e && e.code === "invalid_argument" ? "이 화면에서는 후기를 쓸 권한이 없어요." : "올리지 못했어요. 잠시 뒤에 다시 시도해 주세요.";
      if (e && e.code === "invalid_argument") { cm.canWrite = false; $("cm-write").hidden = true; }
    } finally { send.disabled = false; }
  }
''')

# 9) 후기 쓰기 화면 여닫기·아래 줄(로그인/동의/버튼)
old = span('  function rvOpen(step){', '  function rvClose(fromPop){')
s = s.replace(old, '''  function rvOpen(){
    let has = false; try { has = !!localStorage.getItem("hz-cm-draft"); } catch(e) {}
    if (!has) {
      cmFillForm(false);
      const lp = rv.lastPlan;
      if (lp) { $("cm-origin").value = lp.o; $("cm-dest").value = lp.d; $("cm-nights").value = String(lp.n); $("cm-mode").value = lp.m || "transit"; $("cm-people").value = String(lp.p || 2); cmPaintRoute(); cmRoute(); }
    } else cmFillForm(true);
    if (rv.lastPlan) { try { localStorage.setItem("hz-rv-asked", rv.lastPlan.key); } catch(e) {} }
    $("cm-route-box").hidden = true; $("cm-route-edit").textContent = "바꾸기"; $("cm-route-edit").setAttribute("aria-expanded", "false");
    $("rv").hidden = false; lockSync();
    if (!(history.state && history.state.rv)) { try { history.pushState({rv: 1, rp: $("rp").hidden ? 0 : 1}, ""); } catch(e) {} }
    rvView("form"); rvSync();
  }
''')
old = span('  const rvConsented = () =>', '  /* v113: 계산 결과에서 바로')
s = s.replace(old, '''  const rvConsented = () => { try { return !!cm.uid && localStorage.getItem("hz-rv-ok-" + cm.uid) === "1"; } catch(e) { return false; } };
  /* 아래 고정 줄: 로그인 안 했으면 '카카오로 로그인하고 올리기', 했으면 '후기 올리기'. 동의는 처음 한 번 */
  function rwFoot(){
    if (!$("rw-foot")) return;
    const needLogin = !cm.uid, agreed = rvConsented(), box = $("rv-login");
    box.hidden = !needLogin;
    if (needLogin) {
      box.innerHTML = cm.sb ? `<div class="sso-list">` + ssoOrder(cm.providers).map(pv => ssoBtn(pv, "data-login")).join("") + `</div><p class="rv-sm">로그인하면 바로 올라가요. 쓴 내용은 그대로 남아 있어요.</p>`
        : `<p class="rv-sm">이 화면에서는 후기를 올릴 수 없어요.</p>`;
      box.querySelectorAll("[data-login]").forEach(b => b.addEventListener("click", () => {
        if (!cmF.star) { $("cm-msg").textContent = "별점을 먼저 눌러 주세요."; $("cm-stars").scrollIntoView({block: "center"}); return; }
        if (!$("cm-agree").checked) { $("cm-msg").textContent = "위 확인 칸에 체크해 주세요."; return; }
        cmSave(); try { localStorage.setItem("hz-signup-ok", "1"); sessionStorage.setItem("hz-rv-auto", "1"); } catch(e) {}
        cmLogin(b.dataset.login, "5"); }));
    }
    $("cm-agree-row").hidden = agreed; $("rv-agreed").hidden = true;
    if (agreed) $("cm-agree").checked = true;
    $("cm-send").hidden = needLogin;
    $("cm-send").setAttribute("aria-disabled", String(!cmF.star));
    $("cm-send").textContent = cmF.star ? "후기 올리기" : "별점을 먼저 눌러 주세요";
  }
  function rvView(v){
    $("cm-form").hidden = v !== "form"; $("rw-done").hidden = v !== "done";
    $("cm-msg").textContent = "";
    $("rv").scrollTop = 0;
    if (v === "form") rwFoot();
    const h = v === "done" ? $("rw-done-h") : $("rw-star-h"); if (h) { h.tabIndex = -1; h.focus({preventScroll: true}); }
  }
''')
R('''    rvOpen();
  }
  $("went-btn").addEventListener("click", rvWentGo);''', '''    rvOpen();
  }
  $("went-btn").addEventListener("click", rvWentGo);''')
old = span('  function rvBind(){', '  async function cmInit(){')
s = s.replace(old, '''  function rvBind(){
    const arm = e => { if (e.target.closest && e.target.closest("#junior, #senior")) { rvRemember.armed = true; document.removeEventListener("pointerdown", arm, true); document.removeEventListener("keydown", arm, true); } };
    document.addEventListener("pointerdown", arm, true); document.addEventListener("keydown", arm, true);
    document.querySelectorAll("[data-rv-open]").forEach(b => b.addEventListener("click", () => rvOpen()));
    $("rv-close").addEventListener("click", () => rvClose());
    $("rv-done").addEventListener("click", () => rvClose());
    $("rv-done-list").addEventListener("click", () => { rvClose(); if ($("rp").hidden) setTimeout(() => rpOpen(), 50); });
    $("rv").addEventListener("keydown", e => { if (e.key === "Escape") rvClose(); });
    window.addEventListener("popstate", () => { if (!$("rv").hidden && !(history.state && history.state.rv)) rvClose(true); });
    $("cm-agree").addEventListener("change", () => { $("cm-msg").textContent = ""; });
    $("cm-form").addEventListener("submit", async ev => {
      ev.preventDefault();
      if (!cm.uid) { rwFoot(); return; }
      await cmSubmit({preventDefault(){}});
      const m = $("cm-msg").textContent;
      if (/^보냈어요/.test(m)) { try { localStorage.setItem("hz-rv-ok-" + cm.uid, "1"); } catch(e) {} rvView("done"); }
    });
  }
''')

# 10) 로그인하고 돌아오면: 쓰던 후기를 열고, '로그인하고 올리기'였으면 바로 올림
R('''        if (rvBack) { rvOpen(+rvBack || 5); if (!cm.uid) $("cm-msg").textContent = "로그인하지 못했어요. 다시 시도해 주세요."; }''',
'''        if (rvBack) { rvOpen(); let auto = false; try { auto = sessionStorage.getItem("hz-rv-auto") === "1"; sessionStorage.removeItem("hz-rv-auto"); } catch(e) {}
          if (!cm.uid) $("cm-msg").textContent = "로그인하지 못했어요. 다시 시도해 주세요.";
          else if (auto && cmF.star) { $("cm-agree").checked = true; $("cm-form").requestSubmit ? $("cm-form").requestSubmit() : $("cm-send").click(); } }''')

# 11) 남은 옛 이름 정리
R('''    if (!$("rp").hidden) { cmRender(); $("rp-t-list").focus({preventScroll: true}); }''',
  '''    if (!$("rp").hidden) { cmRender(); $("rp-title").focus({preventScroll: true}); }''')
open(p, 'w', encoding='utf-8').write(s)
print('js ok')
