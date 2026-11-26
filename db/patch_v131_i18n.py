# v131 후기·가입 화면 외국어(영·일·중)로 열기
import re
p = '/home/claude/hoolzzeok_site/index.html'
s = open(p, encoding='utf-8').read()
def R(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (a[:90], c)
    s = s.replace(a, b)
def span(start, end):
    assert s.count(start) == 1, ('start', start[:60], s.count(start))
    i = s.index(start); j = s.index(end, i)
    return s[i:j]
def rep_span(start, end, new):
    global s
    old = span(start, end); s = s.replace(old, new)

# 0) 사전 넣기 (cmMan 바로 뒤)
tx = open('/home/claude/hoolzzeok_db/rw_i18n.js', encoding='utf-8').read()
R('const T = {', tx.replace("  const RT = () => RW_TX[lang] || RW_TX.en;", "  function RT(){ return RW_TX[lang] || RW_TX.en; }").replace("  const rwWon = v =>", "  function rwWon(v){ return lang === \"ko\" ? cmMan(v) : \"₩\" + Math.round(v).toLocaleString(\"en-US\"); }\n  const rwWonOld = v =>") + "\nconst T = {")

# 1) 외국어 화면에서 숨기던 것 풀기
R('''html:not([lang="ko"]) .rv-open{display:none!important}''', '''/* v131: 외국어 화면에도 후기·가입 열림 */''')

# 2) 고정 글자 → rwApply 로 채움
R('<span class="hp-k">훌쩍</span><button type="button" class="rv-x" id="rp-close">닫기</button>', '<span class="hp-k" data-rw="brand">훌쩍</span><button type="button" class="rv-x" id="rp-close" data-rw="close">닫기</button>')
R('<h2 class="hp-h" id="rp-title">여행 후기</h2>\n    <p class="rv-sm">실제로 다녀온 사람이 쓴 돈과 한마디예요.</p>', '<h2 class="hp-h" id="rp-title" data-rw="listTitle">여행 후기</h2>\n    <p class="rv-sm" data-rw="listSub">실제로 다녀온 사람이 쓴 돈과 한마디예요.</p>')
R('<details class="rl-rule"><summary>후기 운영 기준</summary>', '<details class="rl-rule"><summary data-rw="ruleT">후기 운영 기준</summary>')
i = s.index('<details class="rl-rule">'); j = s.index('</details>', i)
s = s[:i] + '<details class="rl-rule"><summary data-rw="ruleT">후기 운영 기준</summary>\n      <ul id="rl-rules"></ul>\n    ' + s[j:]
R('<button type="button" class="rl-fab-b" data-rv-open><span aria-hidden="true">✏️</span> 내 여행 후기 쓰기 <small>30초</small></button>', '<button type="button" class="rl-fab-b" data-rv-open><span aria-hidden="true">✏️</span> <span data-rw="writeCta">내 여행 후기 쓰기</span> <small data-rw="sec30">30초</small></button>')
R('<button type="button" class="rv-x" id="rv-close">닫기</button><b class="rw-hd">후기 쓰기</b><span class="rw-time">30초면 끝나요</span>', '<button type="button" class="rv-x" id="rv-close" data-rw="close">닫기</button><b class="rw-hd" data-rw="wHd">후기 쓰기</b><span class="rw-time" data-rw="wTime">30초면 끝나요</span>')
R('<div class="rw-trip-t"><small>다녀온 여행</small>', '<div class="rw-trip-t"><small data-rw="trip">다녀온 여행</small>')
R('<span class="cm-l">출발</span><input id="cm-origin-q"', '<span class="cm-l" data-rw="lFrom">출발</span><input id="cm-origin-q"')
R('<span class="cm-l">도착</span><input id="cm-dest-q"', '<span class="cm-l" data-rw="lTo">도착</span><input id="cm-dest-q"')
R('<div class="cm-q2"><span class="cm-l">일정</span><div class="chips cm-wrap" id="cm-nights-c"', '<div class="cm-q2"><span class="cm-l" data-rw="lNights">일정</span><div class="chips cm-wrap" id="cm-nights-c"')
R('<div class="cm-q2"><span class="cm-l">이동</span><div class="chips cm-wrap" id="cm-mode-c"', '<div class="cm-q2"><span class="cm-l" data-rw="lMode">이동</span><div class="chips cm-wrap" id="cm-mode-c"')
R('<div class="cm-q2"><span class="cm-l">인원</span><div class="cm-step">', '<div class="cm-q2"><span class="cm-l" data-rw="lPeople">인원</span><div class="cm-step">')
R('<button type="button" class="rw-routedone" id="cm-route-done">이 여행으로 할게요</button>', '<button type="button" class="rw-routedone" id="cm-route-done" data-rw="routeDone">이 여행으로 할게요</button>')
R('<h3 id="rw-star-h">여행은 어땠어요?</h3>', '<h3 id="rw-star-h" data-rw="starQ">여행은 어땠어요?</h3>')
R('<h3>한 사람이 쓴 돈은요? <small>대충이어도 돼요</small></h3>', '<h3><span data-rw="moneyQ">한 사람이 쓴 돈은요?</span> <small data-rw="moneySub">대충이어도 돼요</small></h3>')
R('<label><span class="sr">한 사람이 쓴 돈 (원)</span><input id="cm-total" type="text" inputmode="numeric" autocomplete="off" placeholder="0"><i>원</i></label>', '<label><span class="sr" data-rw="amtL">한 사람이 쓴 돈 (원)</span><input id="cm-total" type="text" inputmode="numeric" autocomplete="off" placeholder="0"><i data-rw="amtUnit">원</i></label>')
R('<button type="button" data-d="-10000" aria-label="1만 원 줄이기">−1만</button>', '<button type="button" data-d="-10000" id="rw-minus">−1만</button>')
R('<button type="button" data-d="10000" aria-label="1만 원 늘리기">+1만</button>', '<button type="button" data-d="10000" id="rw-plus">+1만</button>')
R('<summary>항목별로 적기 <small>교통·숙박·식비 따로, 선택</small></summary>', '<summary><span data-rw="partsT">항목별로 적기</span> <small data-rw="partsS">교통·숙박·식비 따로, 선택</small></summary>')
R('<h3 id="rw-kw-h">좋았던 점 <small>여러 개 골라도 돼요</small></h3>', '<h3 id="rw-kw-h"><span id="rw-kw-ht">좋았던 점</span> <small data-rw="multi">여러 개 골라도 돼요</small></h3>')
R('<h3>한마디 <small>안 써도 돼요</small></h3>', '<h3><span data-rw="textQ">한마디</span> <small data-rw="textSub">안 써도 돼요</small></h3>')
R('<summary>취미 태그 <small>캠핑·낚시·등산 등, 선택</small></summary>', '<summary><span data-rw="tagsQ">취미 태그</span> <small data-rw="tagsS">캠핑·낚시·등산 등, 선택</small></summary>')
R('<p class="rw-paid" id="rv-paid-note">', '<p class="rw-paid" id="rv-paid-note" data-rw="paidNote">')
R('<p class="rv-sm" id="rv-agreed" hidden>처음 쓸 때 동의하셨어요.</p>', '<p class="rv-sm" id="rv-agreed" hidden data-rw="agreed">처음 쓸 때 동의하셨어요.</p>')
R('<h3 id="rw-done-h">올렸어요. 고마워요!</h3>\n      <p class="rv-sm">확인한 뒤 공개돼요. 다음 사람이 경비를 짤 때 큰 도움이 돼요.</p>\n      <div class="rv-acts"><button type="button" class="rv-main" id="rv-done-list">다른 사람 후기 보기</button><button type="button" class="rv-sub" id="rv-done">닫기</button></div>',
  '<h3 id="rw-done-h" data-rw="doneT">올렸어요. 고마워요!</h3>\n      <p class="rv-sm" data-rw="doneS">확인한 뒤 공개돼요. 다음 사람이 경비를 짤 때 큰 도움이 돼요.</p>\n      <div class="rv-acts"><button type="button" class="rv-main" id="rv-done-list" data-rw="doneList">다른 사람 후기 보기</button><button type="button" class="rv-sub" id="rv-done" data-rw="close">닫기</button></div>')
R('<small class="cm-fine">글의 저작권은 작성자에게 있고, 훌쩍은 서비스 안에서만 보여 줘요. 권리 침해 신고가 들어오면 확인할 때까지 숨길 수 있어요. 얼굴·이름·카드번호는 쓰지 마세요.</small>', '<small class="cm-fine" data-rw="fine">글의 저작권은 작성자에게 있고, 훌쩍은 서비스 안에서만 보여 줘요. 권리 침해 신고가 들어오면 확인할 때까지 숨길 수 있어요. 얼굴·이름·카드번호는 쓰지 마세요.</small>')
R('<span class="hp-k">훌쩍</span><button type="button" class="rv-x" id="ac-close">닫기</button>', '<span class="hp-k" data-rw="brand">훌쩍</span><button type="button" class="rv-x" id="ac-close" data-rw="close">닫기</button>')
R('<button type="button" class="went" id="went-btn" hidden><b>다녀오셨어요? 실제로 쓴 돈 남기기</b><small>경비가 미리 채워져 있어요. 다음 사람 계산이 정확해져요.</small></button>', '<button type="button" class="went" id="went-btn" hidden><b data-rw="wentT">다녀오셨어요? 실제로 쓴 돈 남기기</b><small data-rw="wentS">경비가 미리 채워져 있어요. 다음 사람 계산이 정확해져요.</small></button>')
R('<p class="sr-switch" id="sr-rv-row" hidden><button type="button" id="sr-rv">여행 후기 보기·쓰기</button></p>', '<p class="sr-switch" id="sr-rv-row" hidden><button type="button" id="sr-rv" data-rw="srRv">여행 후기 보기·쓰기</button></p>')
R('''      if (lang === "ko" && !EMBED) h += `<button type="button" class="went sr-went" data-went hidden><b>다녀오셨어요? 실제로 쓴 돈 남기기</b><small>경비가 미리 채워져 있어요. 다음 사람 계산이 정확해져요.</small></button>`;''',
  '''      if (!EMBED) h += `<button type="button" class="went sr-went" data-went hidden><b>${RT().wentT}</b><small>${RT().wentS}</small></button>`;''')

# rwApply: 언어에 맞춰 글자 채우기
R('''  function RT(){ return RW_TX[lang] || RW_TX.en; }''', '''  function RT(){ return RW_TX[lang] || RW_TX.en; }
  function rwApply(){
    const X = RT();
    document.querySelectorAll("[data-rw]").forEach(el => { const v = X[el.dataset.rw]; if (typeof v === "string") el.textContent = v; });
    ["rp", "rv", "ac"].forEach(id => { const el = $(id); if (el) el.lang = lang === "zh" ? "zh-CN" : lang; });
    if ($("rl-rules")) $("rl-rules").innerHTML = X.rules.map(([b, t]) => `<li><b>${b}</b> ${t}</li>`).join("");
    if ($("cm-text")) $("cm-text").placeholder = X.textPh;
    ["cm-origin-q", "cm-dest-q"].forEach(id => { if ($(id)) $(id).placeholder = X.acPh; });
    if ($("cm-p-minus")) { $("cm-p-minus").setAttribute("aria-label", X.pMinus); $("cm-p-plus").setAttribute("aria-label", X.pPlus); }
    if ($("rw-minus")) { $("rw-minus").textContent = X.minus; $("rw-minus").setAttribute("aria-label", X.minusA); $("rw-plus").textContent = X.plus; $("rw-plus").setAttribute("aria-label", X.plusA); }
    if ($("cm-agree-txt")) $("cm-agree-txt").innerHTML = X.agree(X.privacy);
    if ($("cm-route-edit")) $("cm-route-edit").textContent = $("cm-route-box").hidden ? X.change : X.changeClose;
    /* 공개 전 지인 베타 안내는 한국어 지인용. 외국어 화면에는 보상 안내를 그 말로 */
  }''')

# 3) 경로 그리기·자동완성: 지금 언어로
R('''    const L = T.ko, o = byId($("cm-origin").value), d = byId($("cm-dest").value);
    if (document.activeElement !== $("cm-origin-q"))''', '''    const L = T[lang], o = byId($("cm-origin").value), d = byId($("cm-dest").value);
    if (document.activeElement !== $("cm-origin-q"))''')
R('''    $("cm-p-txt").textContent = `${Math.max(1, +$("cm-people").value || 1)}명`;''', '''    $("cm-p-txt").textContent = RT().people(Math.max(1, +$("cm-people").value || 1));''')
R('''      list.innerHTML = (r.head ? `<li class="ac-head" role="presentation">${T.ko.acPopular}</li>` : "") + (items.length ? items.map((p, i) => `<li role="option" id="${key}-opt-${i}" data-id="${p.id}" aria-selected="${i === active}" class="${i === active ? "on" : ""}"><b>${T.ko.name(p)}</b><span>${T.ko.prov(p)}</span></li>`).join("") : `<li class="ac-none" role="presentation">${T.ko.acNone}</li>`);''',
  '''      list.innerHTML = (r.head ? `<li class="ac-head" role="presentation">${T[lang].acPopular}</li>` : "") + (items.length ? items.map((p, i) => `<li role="option" id="${key}-opt-${i}" data-id="${p.id}" aria-selected="${i === active}" class="${i === active ? "on" : ""}"><b>${T[lang].name(p)}</b><span>${T[lang].prov(p)}</span></li>`).join("") : `<li class="ac-none" role="presentation">${T[lang].acNone}</li>`);''')
R('''      const q = inp.value.replace(/\\s+/g, ""), exact = AC_PLACES().find(p => p.ko === q);''', '''      const q = inp.value.replace(/\\s+/g, ""), exact = AC_PLACES().find(p => p.ko === q || String(T[lang].name(p)).replace(/\\s+/g, "") === q);''')

# 4) 항목별 영수증
R('''    $("cm-rc-total").textContent = sum ? T.ko.won(sum) : "0원";''', '''    $("cm-rc-total").textContent = rwWon(sum || 0);''')
R('''    box.innerHTML = `<button type="button" class="cm-rc-fill" id="cm-rc-fill">예상값으로 모두 채우기</button><small class="cm-rc-tip">채운 뒤 다른 것만 고치세요.</small>` + CM_COSTS.map(([k, n]) => `<div class="cm-rc-row"><span class="cm-rc-k"><b>${n}</b><small>${est[k] ? `훌쩍 예상 ${T.ko.won(est[k])}` : k === "souv" ? "산 만큼" : "예상 없음"}</small></span><label class="cm-rc-v"><input id="cm-c-${k}" type="text" inputmode="numeric" autocomplete="off" aria-label="${n} (원)" placeholder="${est[k] ? cmFmt(est[k]) : "0"}" value="${keep[k] || ""}"><i>원</i></label></div>`).join("")
      + `<div class="cm-rc-sum"><span>합계 (한 사람)</span><b id="cm-rc-total">0원</b></div>`;''',
  '''    const X = RT();
    box.innerHTML = `<button type="button" class="cm-rc-fill" id="cm-rc-fill">${X.rcFill}</button><small class="cm-rc-tip">${X.rcTip}</small>` + CM_COSTS.map(([k]) => { const n = X.costs[k]; return `<div class="cm-rc-row"><span class="cm-rc-k"><b>${n}</b><small>${est[k] ? X.rcEst(rwWon(est[k])) : k === "souv" ? X.rcSouv : X.rcNone}</small></span><label class="cm-rc-v"><input id="cm-c-${k}" type="text" inputmode="numeric" autocomplete="off" aria-label="${n} (${X.amtUnit})" placeholder="${est[k] ? cmFmt(est[k]) : "0"}" value="${keep[k] || ""}"><i>${X.amtUnit}</i></label></div>`; }).join("")
      + `<div class="cm-rc-sum"><span>${X.rcSum}</span><b id="cm-rc-total">${rwWon(0)}</b></div>`;''')

# 5) cmRoute
R('''    const o = byId($("cm-origin").value), d = byId($("cm-dest").value), L = T.ko;
    $("cm-route-txt").textContent = o && d ? `${L.name(o)} → ${L.name(d)} · ${L.nights(+$("cm-nights").value)} · ${Math.max(1, +$("cm-people").value || 1)}명 · ${L.mode[$("cm-mode").value] || ""}` : "어디 다녀오셨는지 골라 주세요";
    const est = cmEst();
    $("cm-est-txt").innerHTML = est ? `훌쩍 예상은 한 사람 <b>${cmMan(est)}</b>이었어요. 실제로는요?` : "예상 금액이 없는 길이에요. 쓴 돈을 바로 적어 주세요.";
    cmRcPaint();
    const opts = est ? [["less", "덜 썼어요", "예상보다 적게"], ["same", "비슷해요", "거의 같게"], ["more", "더 썼어요", "예상보다 많이"]] : [];''',
  '''    const o = byId($("cm-origin").value), d = byId($("cm-dest").value), L = T[lang], X = RT();
    $("cm-route-txt").textContent = o && d ? `${L.name(o)} → ${L.name(d)} · ${L.nights(+$("cm-nights").value)} · ${X.people(Math.max(1, +$("cm-people").value || 1))} · ${L.mode[$("cm-mode").value] || ""}` : X.pickTrip;
    const est = cmEst();
    $("cm-est-txt").innerHTML = est ? X.estTxt(rwWon(est)) : X.noEst;
    cmRcPaint();
    const opts = est ? ["less", "same", "more"].map(k => [k, ...X.seg[k]]) : [];''')

# 6) cmFillForm 키워드·태그 글
R('''      box.innerHTML = list.map(([k, ic, t]) => `<button type="button" data-k="${k}" aria-pressed="${cmF.kw.includes(k)}"><span aria-hidden="true">${ic}</span> ${t}</button>`).join("");
      box.querySelectorAll("button").forEach(b => b.addEventListener("click", () => { const k = b.dataset.k, on = !cmF.kw.includes(k);
        if (on && cmF.kw.length >= 5) { $("cm-msg").textContent = "5개까지 고를 수 있어요."; return; }''',
  '''      box.innerHTML = list.map(([k, ic]) => `<button type="button" data-k="${k}" aria-pressed="${cmF.kw.includes(k)}"><span aria-hidden="true">${ic}</span> ${RT().kw[k]}</button>`).join("");
      box.querySelectorAll("button").forEach(b => b.addEventListener("click", () => { const k = b.dataset.k, on = !cmF.kw.includes(k);
        if (on && cmF.kw.length >= 5) { $("cm-msg").textContent = RT().kwMax; return; }''')
R('''    $("rw-kw-h").firstChild.textContent = lowFirst ? "아쉬웠던 점 " : "좋았던 점 ";
    $("rw-kw-h2").textContent = lowFirst ? "좋았던 점도 있었다면" : "아쉬웠던 점도 있었다면";''',
  '''    $("rw-kw-ht").textContent = lowFirst ? RT().bad : RT().good;
    $("rw-kw-h2").textContent = lowFirst ? RT().goodAlso : RT().badAlso;''')
R('''    $("cm-tagpick").innerHTML = CM_TAGS.map(t => `<button type="button" data-t="${t}" aria-pressed="${cmF.tags.includes(t)}">#${t}</button>`).join("");
    $("cm-tagpick").querySelectorAll("button").forEach(b => b.addEventListener("click", () => { const t = b.dataset.t, on = !cmF.tags.includes(t);
      if (on && cmF.tags.length >= 4) { $("cm-msg").textContent = "취미 태그는 4개까지예요."; return; }''',
  '''    $("cm-tagpick").innerHTML = CM_TAGS.map(t => `<button type="button" data-t="${t}" aria-pressed="${cmF.tags.includes(t)}">#${RT().tags[t] || t}</button>`).join("");
    $("cm-tagpick").querySelectorAll("button").forEach(b => b.addEventListener("click", () => { const t = b.dataset.t, on = !cmF.tags.includes(t);
      if (on && cmF.tags.length >= 3) { $("cm-msg").textContent = RT().tagMax(3); return; }''')
R('''    box.innerHTML = [1, 2, 3, 4, 5].map(n => `<button type="button" role="radio" data-n="${n}" aria-checked="${cmF.star === n}" aria-label="별 ${n}개, ${RW_STAR[n]}" class="${n <= cmF.star ? "on" : ""}" tabindex="${(cmF.star || 1) === n ? 0 : -1}">${RW_STAR_SVG}</button>`).join("");
    $("cm-star-t").textContent = cmF.star ? RW_STAR[cmF.star] : "별을 눌러 주세요";''',
  '''    const X = RT();
    box.innerHTML = [1, 2, 3, 4, 5].map(n => `<button type="button" role="radio" data-n="${n}" aria-checked="${cmF.star === n}" aria-label="${X.starBtn(n, X.stars[n])}" class="${n <= cmF.star ? "on" : ""}" tabindex="${(cmF.star || 1) === n ? 0 : -1}">${RW_STAR_SVG}</button>`).join("");
    $("cm-star-t").textContent = cmF.star ? X.stars[cmF.star] : X.starHint;''')
R('''    const routeToggle = open => { $("cm-route-box").hidden = !open; $("cm-route-edit").setAttribute("aria-expanded", String(open)); $("cm-route-edit").textContent = open ? "접기" : "바꾸기"; };''',
  '''    const routeToggle = open => { $("cm-route-box").hidden = !open; $("cm-route-edit").setAttribute("aria-expanded", String(open)); $("cm-route-edit").textContent = open ? RT().changeClose : RT().change; };''')

# 7) 지역 칩
R('''    $("cm-regions").innerHTML = regs.map(([k, n]) => `<button type="button" data-r="${k}" aria-pressed="${cm.region === k}">${n} <small>${k === "all" ? cm.reviews.length : cnt[k] || 0}</small></button>`).join("");''',
  '''    $("cm-regions").innerHTML = regs.map(([k]) => `<button type="button" data-r="${k}" aria-pressed="${cm.region === k}">${RT().regions[k]} <small>${k === "all" ? cm.reviews.length : cnt[k] || 0}</small></button>`).join("");''')
R('''    $("cm-tags").innerHTML = cm.tag ? `<button type="button" aria-label="#${esc(cm.tag)} 거르기 풀기">#${esc(cm.tag)} ✕</button>` : "";''',
  '''    $("cm-tags").innerHTML = cm.tag ? `<button type="button" aria-label="${esc(RT().tagOff(RT().tags[cm.tag] || cm.tag))}">#${esc(RT().tags[cm.tag] || cm.tag)} ✕</button>` : "";''')

# 8) 카드
rep_span('  function cmCard(r, mode){', '  function cmBind(box){', '''  function cmCard(r, mode){
    const o = byId(r.origin) || byId("seoul"), d = byId(r.dest), L = T[lang], X = RT();
    if (!d) return "";
    const {sum, est, pct} = cmDiff(r), star = cmStarOf(r), open = cm.open[r.id];
    const kws = (r.tags || []).filter(t => /^k:/.test(t)).map(t => rwKw(t.slice(2))).filter(Boolean);
    const hob = (r.tags || []).filter(t => !/^[kl]:/.test(t));
    const rl = ((r.tags || []).find(t => /^l:/.test(t)) || "l:ko").slice(2);
    const when = (r.at || "").slice(0, 10).split("-").map(Number);
    const meta = [X.from(L.name(o)), X.people(+r.people || 1), L.mode[r.mode] || "", when[1] ? X.written(when[1], when[2]) : ""].filter(Boolean).join(" · ");
    const max = Math.max(sum || 0, est || 0) || 1;
    const money = sum ? `<div class="rl-money">
        <div class="rl-money-row"><small>${X.spent}</small><b class="num">${rwWon(sum)}</b></div>
        ${est ? `<div class="rl-bar" aria-hidden="true"><i style="width:${Math.round(sum / max * 100)}%"></i><u style="left:calc(${Math.round(est / max * 100)}% - 1px)"></u></div>
        <div class="rl-money-row"><small>${X.est} <span aria-hidden="true">┃</span></small><span class="est num">${rwWon(est)}</span></div>` : ""}
        ${pct != null ? `<p class="rl-diff ${Math.abs(pct) < 5 ? "" : pct < 0 ? "less" : "more"}">${Math.abs(pct) < 5 ? X.dSame : pct < 0 ? X.dLess(Math.abs(pct)) : X.dMore(Math.abs(pct))}</p>` : est ? `<p class="rl-diff">${X.partial}</p>` : ""}
      </div>` : "";
    const tl = lang === "zh" ? "zh-CN" : lang;
    const tr = r.text && rl !== lang ? `<a class="rl-tr" href="https://translate.google.com/?sl=auto&tl=${tl}&op=translate&text=${encodeURIComponent(String(r.text).slice(0, 1500))}" target="_blank" rel="noopener">${X.translate}</a>` : "";
    const btns = mode === "pending"
      ? `<button type="button" class="go" data-act="approve" data-id="${esc(r.id)}" data-uid="${esc(r.uid)}">${X.approve}</button><button type="button" class="sub warn" data-act="reject" data-id="${esc(r.id)}" data-uid="${esc(r.uid)}">${X.reject}</button>`
      : `<button type="button" class="go" data-act="calc" data-id="${esc(r.id)}">${X.calc}</button>${(r.text || "").length > 140 ? `<button type="button" class="sub" data-act="more" data-id="${esc(r.id)}">${open ? X.fold : X.more}</button>` : ""}<span class="sp"></span>${cm.uid && !cm.admin ? (cm.myReports.includes(r.id) ? `<button type="button" class="sub" disabled>${X.reported}</button>` : `<button type="button" class="sub" data-act="report" data-id="${esc(r.id)}">${X.report}</button>`) : ""}${cm.admin ? `<button type="button" class="sub warn" data-act="hide" data-id="${esc(r.id)}">${X.hide}${cm.reports[r.id] ? X.rep(cm.reports[r.id]) : ""}</button>` : ""}`;
    /* 보상 표시: 한국어 문장이 맨 위(법), 외국어 화면은 바로 아래에 그 말로 */
    const paid = reviewPaid(r) ? `<p class="cm-paid">${REVIEW_PAID.txt}${lang !== "ko" && X.paidTr ? `<span class="cm-paid-tr" lang="${tl}">${X.paidTr}</span>` : ""}</p>` : "";
    return `<li class="cm-card rl-card">${paid}
      <div class="rl-top"><span class="rl-av" aria-hidden="true">${esc(String(L.name(d)).slice(0, 1))}</span><div class="rl-tt"><h3>${esc(L.name(d))} ${L.nights(r.nights)}</h3><span class="rl-meta">${esc(meta)}</span></div>
        ${star ? `<span class="rl-star" aria-label="${X.starAria(star)}"><i aria-hidden="true">★</i> ${star}</span>` : r.mood ? `<span class="rl-mood">${esc(X.moods[r.mood] || "")}</span>` : ""}</div>
      ${kws.length || hob.length ? `<div class="rl-kws">${kws.map(([k, ic, , g]) => `<span class="rl-kw${g === "bad" ? " bad" : ""}">${ic} ${X.kw[k]}</span>`).join("")}${hob.map(t => `<button type="button" class="rl-tag" data-act="tag" data-id="${esc(r.id)}" data-tag="${esc(t)}">#${esc(X.tags[t] || t)}</button>`).join("")}</div>` : ""}
      ${r.text ? `${rl !== lang ? `<span class="rl-lang">${X.langTag[rl] || ""}</span>` : ""}<p class="cm-text${open ? "" : " short"}" lang="${rl === "zh" ? "zh-CN" : rl}">${esc(r.text)}</p>${tr}` : ""}
      ${money}
      <div class="rl-acts">${btns}</div></li>`;
  }
''')

# 9) 목록 요약·상태
R('''      const cta = canWrite ? `<button type="button" class="rl-sum-cta" data-rv-open>✏️ 내 여행 후기 쓰기<small>30초</small></button>` : "";
      $("rl-sum").innerHTML = !cm.loaded ? "" : cm.reviews.length
        ? `<div class="rl-sum-top">${avg ? `<span class="rl-sum-star"><i aria-hidden="true">★</i> ${avg}</span>` : ""}<span class="rl-sum-n">후기 ${cm.reviews.length}개</span></div>
           ${md != null ? `<p class="rl-sum-diff">${Math.abs(md) < 5 ? `실제로 쓴 돈은 훌쩍 예상과 <b>거의 같았어요</b>` : `실제로 쓴 돈은 훌쩍 예상보다 <b>평균 ${Math.abs(md)}% ${md < 0 ? "덜" : "더"}</b> 들었어요`} <small>(경비를 적은 후기 ${diffs.length}개)</small></p>` : ""}${cta}`
        : `<p class="rl-sum-empty"><b>아직 후기가 없어요.</b><br>다녀온 여행의 실제 경비를 남기면 다음 사람이 경비를 더 정확히 짤 수 있어요.</p>${cta}`;''',
  '''      const X = RT(), cta = canWrite ? `<button type="button" class="rl-sum-cta" data-rv-open>✏️ ${X.writeCta}<small>${X.sec30}</small></button>` : "";
      $("rl-sum").innerHTML = !cm.loaded ? "" : cm.reviews.length
        ? `<div class="rl-sum-top">${avg ? `<span class="rl-sum-star"><i aria-hidden="true">★</i> ${avg}</span>` : ""}<span class="rl-sum-n">${X.sumN(cm.reviews.length)}</span></div>
           ${md != null ? `<p class="rl-sum-diff">${Math.abs(md) < 5 ? X.sumSame : X.sumDiff(Math.abs(md), md < 0)} <small>${X.sumBase(diffs.length)}</small></p>` : ""}${cta}`
        : `<p class="rl-sum-empty"><b>${X.sumEmptyT}</b><br>${X.sumEmpty}</p>${cta}`;''')
R('''    else if (!list.length) $("cm-list").innerHTML = cm.reviews.length ? `<li class="rl-empty"><b>이 조건의 후기가 아직 없어요</b><span>다른 지역을 골라 보세요.</span></li>` : "";''',
  '''    else if (!list.length) $("cm-list").innerHTML = cm.reviews.length ? `<li class="rl-empty"><b>${RT().emptyFT}</b><span>${RT().emptyF}</span></li>` : "";''')
R('''    $("cm-status").textContent = !cm.loaded ? (cm.db === false ? "" : "후기를 불러오는 중이에요…") : (cm.region !== "all" || cm.tag ? `후기 ${list.length}개` : "") + (mineWaiting ? `${cm.region !== "all" || cm.tag ? ", " : ""}내 후기 ${mineWaiting}개 확인 중` : "");''',
  '''    $("cm-status").textContent = !cm.loaded ? (cm.db === false ? "" : RT().loading) : (cm.region !== "all" || cm.tag ? RT().countN(list.length) : "") + (mineWaiting ? `${cm.region !== "all" || cm.tag ? ", " : ""}${RT().mineN(mineWaiting)}` : "");''')
R('''    if (cm.admin && cm.pending.length) { $("cm-admin").innerHTML = `<h3>승인 대기 ${cm.pending.length}건</h3>''', '''    if (cm.admin && cm.pending.length) { $("cm-admin").innerHTML = `<h3>${RT().pendingN(cm.pending.length)}</h3>''')
R('''      if (act === "report") { await BE().report(id); btn.textContent = "신고됨"; }''', '''      if (act === "report") { await BE().report(id); btn.textContent = RT().reportedNow; }''')
R('''    } catch(e) { btn.disabled = false; btn.textContent = "다시 시도"; }''', '''    } catch(e) { btn.disabled = false; btn.textContent = RT().retry; }''')

# 10) 보내기 메시지 + 언어 표시 태그
R('''    const msg = $("cm-msg"), send = $("cm-send"), L = T.ko;
    if ((!cm.db && !cm.sb) || !cm.uid) { msg.textContent = "지금은 후기를 보낼 수 없어요."; return; }''', '''    const msg = $("cm-msg"), send = $("cm-send"), L = T.ko, X = RT();
    if ((!cm.db && !cm.sb) || !cm.uid) { msg.textContent = X.mCant; return; }''')
R('''    if (!cmF.star) { msg.textContent = "별점을 먼저 눌러 주세요."; $("cm-stars").scrollIntoView({block: "center"}); return; }
    if (!dest || !origin) { msg.textContent = "다녀온 곳을 골라 주세요. 위 '바꾸기'를 눌러요."; return; }
    if (origin.id === dest.id) { msg.textContent = "출발과 도착이 같아요. 위 '바꾸기'로 고쳐 주세요."; return; }
    if (!$("cm-agree").checked) { msg.textContent = "아래 확인 칸에 체크해 주세요."; $("cm-agree-row").scrollIntoView({block: "center"}); return; }''',
  '''    if (!cmF.star) { msg.textContent = X.mNeedStar; $("cm-stars").scrollIntoView({block: "center"}); return; }
    if (!dest || !origin) { msg.textContent = X.mNeedPlace; return; }
    if (origin.id === dest.id) { msg.textContent = X.mSame; return; }
    if (!$("cm-agree").checked) { msg.textContent = X.mAgree; $("cm-agree-row").scrollIntoView({block: "center"}); return; }''')
R('''    const body = free || (cmF.kw.length ? cmF.kw.map(k => rwKw(k)[2]).join(". ") + "." : RW_STAR[cmF.star] + ".");''',
  '''    const body = free || (cmF.kw.length ? cmF.kw.map(k => X.kw[k]).join(lang === "ja" || lang === "zh" ? "。" : ". ") + (lang === "ja" || lang === "zh" ? "。" : ".") : X.stars[cmF.star] + (lang === "ja" || lang === "zh" ? "。" : "."));''')
R('''      people, tags: [...cmF.kw.slice(0, 5).map(k => "k:" + k), ...cmF.tags.slice(0, 4)].slice(0, 9), mood: rwMood(cmF.star), cost, text: body.slice(0, 2000)};
    send.disabled = true; msg.textContent = "올리는 중…";
    try {
      if (await BE().submit(item) === "full") { msg.textContent = "확인 중인 후기가 5개 있어요. 공개된 뒤에 더 올려 주세요."; return; }
      try { localStorage.removeItem("hz-cm-draft"); } catch(e) {}
      cmFillForm(false);
      msg.textContent = "보냈어요. 확인 후 공개돼요. 고마워요!";
    } catch(e) {
      msg.textContent = e && e.code === "invalid_argument" ? "이 화면에서는 후기를 쓸 권한이 없어요." : "올리지 못했어요. 잠시 뒤에 다시 시도해 주세요.";''',
  '''      people, tags: [...cmF.kw.slice(0, 5).map(k => "k:" + k), ...cmF.tags.slice(0, 3), "l:" + lang].slice(0, 9), mood: rwMood(cmF.star), cost, text: body.slice(0, 2000)};
    send.disabled = true; msg.textContent = X.mSending;
    try {
      if (await BE().submit(item) === "full") { msg.textContent = X.mFull; return; }
      try { localStorage.removeItem("hz-cm-draft"); } catch(e) {}
      cmFillForm(false);
      msg.textContent = X.mSent; msg.dataset.ok = "1";
    } catch(e) {
      msg.textContent = e && e.code === "invalid_argument" ? X.mNoPerm : X.mFail;''')
R('''      if (/^보냈어요/.test(m)) { try { localStorage.setItem("hz-rv-ok-" + cm.uid, "1"); } catch(e) {} rvView("done"); }''',
  '''      if ($("cm-msg").dataset.ok === "1") { delete $("cm-msg").dataset.ok; try { localStorage.setItem("hz-rv-ok-" + cm.uid, "1"); } catch(e) {} rvView("done"); }''')
R('''    send.disabled = true; msg.textContent = X.mSending;''', '''    send.disabled = true; msg.textContent = X.mSending; delete msg.dataset.ok;''')

# 11) 아래 줄
R('''      box.innerHTML = cm.sb ? `<div class="sso-list">` + ssoOrder(cm.providers).map(pv => ssoBtn(pv, "data-login")).join("") + `</div><p class="rv-sm">로그인하면 바로 올라가요. 쓴 내용은 그대로 남아 있어요.</p>`
        : `<p class="rv-sm">이 화면에서는 후기를 올릴 수 없어요.</p>`;
      box.querySelectorAll("[data-login]").forEach(b => b.addEventListener("click", () => {
        if (!cmF.star) { $("cm-msg").textContent = "별점을 먼저 눌러 주세요."; $("cm-stars").scrollIntoView({block: "center"}); return; }
        if (!$("cm-agree").checked) { $("cm-msg").textContent = "위 확인 칸에 체크해 주세요."; return; }''',
  '''      box.innerHTML = cm.sb ? `<div class="sso-list">` + ssoOrder(cm.providers).map(pv => ssoBtn(pv, "data-login")).join("") + `</div><p class="rv-sm">${RT().loginNote}</p>`
        : `<p class="rv-sm">${RT().cantSend}</p>`;
      box.querySelectorAll("[data-login]").forEach(b => b.addEventListener("click", () => {
        if (!cmF.star) { $("cm-msg").textContent = RT().mNeedStar; $("cm-stars").scrollIntoView({block: "center"}); return; }
        if (!$("cm-agree").checked) { $("cm-msg").textContent = RT().mAgreeUp; return; }''')
R('''    $("cm-send").textContent = cmF.star ? "후기 올리기" : "별점을 먼저 눌러 주세요";''', '''    $("cm-send").textContent = cmF.star ? RT().send : RT().sendNeedStar;
    /* 지인 베타 보상 안내는 한국어 화면에만(외국인 보상은 따로 정함) */
    $("rv-paid-note").hidden = lang !== "ko";''')
R('''  function rvView(v){''', '''  function rvView(v){
    rwApply();''')

# 12) 로그인 버튼: 외국어 화면은 구글 먼저, 문구는 각 회사 규정의 외국어 문구
R('''  const ssoOrder = a => ["kakao", "google"].filter(p => (a || ["google"]).includes(p));
  const ssoBtn = (pv, attr) => `<button type="button" class="sso sso-${pv}" ${attr}="${pv}"><span class="sso-ic">${SSO_ICON[pv]}</span><span class="sso-tx">${pv === "kakao" ? "카카오 로그인" : "Google 계정으로 로그인"}</span></button>`;''',
  '''  const ssoOrder = a => (lang === "ko" ? ["kakao", "google"] : ["google", "kakao"]).filter(p => (a || ["google"]).includes(p));
  /* 문구: 카카오 디자인 가이드의 '카카오 로그인 / Login with Kakao'(국문·영문만 있음 → 일·중도 영문), 구글은 'Sign in with Google' 각 언어 번역 */
  const ssoBtn = (pv, attr) => `<button type="button" class="sso sso-${pv}" ${attr}="${pv}"><span class="sso-ic">${SSO_ICON[pv]}</span><span class="sso-tx">${pv === "kakao" ? RT().kakao : RT().google}</span></button>`;''')

# 13) 가입·내 정보 화면
rep_span('''    if (!cm.uid) {
      box.innerHTML = `<div class="ac-hero">''', '''    $("cm-write").hidden = false; rvSync();''', '''    const X = RT(); rwApply();
    if (!cm.uid) {
      box.innerHTML = `<div class="ac-hero"><span class="ac-mascot" aria-hidden="true">${mascot}</span>
          <h2 class="ac-h" id="ac-title">${X.acTitle}</h2>
          <p class="ac-lede">${X.acLede}</p></div>
        <ul class="ac-perks">${X.perks.map(([ic, b, sm]) => `<li><span aria-hidden="true">${ic}</span><div><b>${b}</b><small>${sm}</small></div></li>`).join("")}</ul>
        <label class="ac-agree" id="ac-agree-row"><input type="checkbox" id="ac-agree"><span class="ac-box" aria-hidden="true"></span><span class="ac-agree-t">${X.acAgree(X.privacy)}</span></label>
        <div class="sso-list">${ssoOrder(cm.providers).map(pv => ssoBtn(pv, "data-p")).join("")}</div>
        <p class="hint ac-msg" id="ac-msg" aria-live="polite"></p>
        <ul class="ac-trust">${X.trust.map(t => `<li>${t}</li>`).join("")}</ul>
        <p class="rv-sm sso-note">${X.acNote}</p>`;
      $("ac-agree").addEventListener("change", () => { $("ac-agree-row").classList.remove("need"); $("ac-msg").textContent = ""; });
      box.querySelectorAll("button[data-p]").forEach(b => b.addEventListener("click", () => {
        if (!$("ac-agree").checked) { const r = $("ac-agree-row"); r.classList.remove("need"); void r.offsetWidth; r.classList.add("need"); $("ac-msg").textContent = X.acNeed; r.scrollIntoView({block: "center", behavior: reduce ? "auto" : "smooth"}); return; }
        try { localStorage.setItem("hz-signup-ok", "1"); } catch(e) {}
        cmLogin(b.dataset.p, "ac"); }));
    } else {
      const pub = cm.reviews.length;
      box.innerHTML = `<div class="ac-hero ac-hero-in"><span class="ac-mascot" aria-hidden="true">${mascot}</span>
          <h2 class="ac-h" id="ac-title">${X.meT}</h2>
          <p class="ac-lede">${cm.email ? esc(mask(cm.email)) : X.meIn}${cm.admin ? ` <span class="ac-badge">${X.admin}</span>` : ""}</p></div>
        <div class="ac-stats"><div><b>${cm.mine.length}</b><small>${X.stMine}</small></div><div><b>${pub}</b><small>${X.stAll}</small></div></div>
        <div class="rv-acts"><button type="button" class="rv-main" id="ac-write">${X.meWrite}</button><button type="button" class="rv-sub" id="ac-reviews">${X.meView}</button></div>
        <div class="ac-low"><button type="button" class="ac-lk" id="cm-out">${X.logout}</button><span aria-hidden="true">·</span><button type="button" class="ac-lk warn" id="cm-quit">${X.quit}</button></div>
        <p class="hint" id="cm-quit-msg" aria-live="polite"></p><p class="hint" id="ac-msg" aria-live="polite"></p>`;
      $("ac-write").addEventListener("click", () => { acClose(); setTimeout(() => rvOpen(), 50); });
      $("ac-reviews").addEventListener("click", () => { acClose(); setTimeout(rpOpen, 50); });
      $("cm-out").addEventListener("click", async () => { await cm.sb.auth.signOut(); acClose(); });
      let armed = false;
      $("cm-quit").addEventListener("click", async () => {
        if (!armed) { armed = true; $("cm-quit").textContent = X.quitSure; return; }
        $("cm-quit").disabled = true;
        const {error} = await cm.sb.rpc("delete_my_account");
        if (error) { $("cm-quit-msg").textContent = X.quitFail; $("cm-quit").disabled = false; return; }
        await cm.sb.auth.signOut(); acOpen(X.quitDone);
      });
    }
''')
R('''    $("cm-agree-txt").innerHTML = `직접 다녀온 사실만 골랐고, 만 14세 이상이며 <a href="/privacy/" target="_blank" rel="noopener">개인정보 처리방침</a>에 동의해요.`;''', '''    $("cm-agree-txt").innerHTML = RT().agree(RT().privacy);''')
R('''        if (acBack) acOpen(cm.uid ? "가입했어요. 이제 여행 후기를 남길 수 있어요." : "로그인하지 못했어요. 다시 시도해 주세요.");''', '''        if (acBack) acOpen(cm.uid ? RT().joined : RT().mLoginFail);''')
R('''          if (!cm.uid) $("cm-msg").textContent = "로그인하지 못했어요. 다시 시도해 주세요.";''', '''          if (!cm.uid) $("cm-msg").textContent = RT().mLoginFail;''')

# 14) 머리줄·진입점: 언어 제한 풀기
R('''    { const wb = $("went-btn"); if (wb) wb.hidden = !ok || lang !== "ko" || EMBED; }''', '''    { const wb = $("went-btn"); if (wb) wb.hidden = !ok || EMBED; }''')
R('''    document.querySelectorAll("[data-went]").forEach(b => { b.hidden = !ok || lang !== "ko"; });''', '''    document.querySelectorAll("[data-went]").forEach(b => { b.hidden = !ok; });''')
R('''    { const r = $("sr-rv-row"); if (r) r.hidden = !ok || lang !== "ko" || EMBED; }''', '''    { const r = $("sr-rv-row"); if (r) r.hidden = !ok || EMBED; }
    try { rwApply(); } catch(e) {}''')
R('''    if ($("rp-top")) $("rp-top").hidden = !cm.sb;
    if ($("ac-open")) { $("ac-open").hidden = !cm.sb; $("ac-open").innerHTML = cm.uid ? "내 정보" : `<span class="ac-l">가입하기</span><span class="ac-s">가입</span>`; $("ac-open").setAttribute("aria-label", cm.uid ? "내 정보" : "가입하기"); }''',
  '''    { const X = RT();
      if ($("rp-top")) { $("rp-top").hidden = !cm.sb; $("rp-top").innerHTML = `<span class="ac-l">${X.topRv[0]}</span><span class="ac-s">${X.topRv[1]}</span>`; $("rp-top").setAttribute("aria-label", X.topRv[0]); }
      if ($("ac-open")) { $("ac-open").hidden = !cm.sb; $("ac-open").innerHTML = cm.uid ? X.topMe : `<span class="ac-l">${X.topJoin[0]}</span><span class="ac-s">${X.topJoin[1]}</span>`; $("ac-open").setAttribute("aria-label", cm.uid ? X.topMe : X.topJoin[0]); } }''')
R('''function rvOk(){ try { return lang === "ko" && !!(cm.sb || (cm.db && cm.uid && cm.canWrite !== false)); } catch(e) { return false; } }''', '''function rvOk(){ try { return !!(cm.sb || (cm.db && cm.uid && cm.canWrite !== false)); } catch(e) { return false; } }''')
R('''qb.setAttribute("aria-label", rv.lastPlan ? `여행 후기: ${T.ko.name(byId(rv.lastPlan.d))} 다녀오셨어요?` : "여행 후기"); }''', '''qb.setAttribute("aria-label", RT().listTitle); }''')
R('''      ...(lang === "ko" ? [["½", Q.half, () => hpOpen()], ["", "여행 후기", () => rpOpen(), "rv"]] : [["🗣️", Q.phrase, () => { const k = $("kit"); if (k) { k.querySelectorAll("details.kfold").forEach(d => d.open = true); k.scrollIntoView({behavior: reduce ? "auto" : "smooth"}); } }]])''',
  '''      ...(lang === "ko" ? [["½", Q.half, () => hpOpen()], ["", "여행 후기", () => rpOpen(), "rv"]] : [["🗣️", Q.phrase, () => { const k = $("kit"); if (k) { k.querySelectorAll("details.kfold").forEach(d => d.open = true); k.scrollIntoView({behavior: reduce ? "auto" : "smooth"}); } }], ["", RT().listTitle, () => rpOpen(), "rv"]])''')
R('''  function rpOpen(){
    if (ui === "senior") setUi("junior", true);''', '''  function rpOpen(){
    if (ui === "senior") setUi("junior", true);
    rwApply();''')

# 15) 스타일 추가
R('''.rl-rule{margin:4px 0 0;font-size:13px;color:var(--muted)}''', '''.rl-rule{margin:4px 0 0;font-size:13px;color:var(--muted)}
.cm-paid-tr{display:block;font-weight:500;margin-top:3px}
.rl-lang{justify-self:start;font-size:12px;font-weight:700;color:var(--muted);background:var(--surface-2);border-radius:999px;padding:2px 9px}
.rl-tr{justify-self:start;font-size:13px;font-weight:700;color:var(--accent);min-height:32px;display:inline-flex;align-items:center}''')

open(p, 'w', encoding='utf-8').write(s)
print('i18n ok')
