  /* ===== v133 '3번 누르면 한국 여행' (외국어 화면). 며칠 → 좋아하는 것 → 예산 → 인천공항 도착부터 서울 + 지방 1곳 일정·경비 =====
     일정은 이미 검증해 넣은 테마 코스(COURSES: 서울 3, 부산 3, 경주 2)를 날짜에 배치. 경비는 calcBudget(인천→서울, 서울→지방), 2명이 방 1개 기준 1인.
     안내 배지는 종류별로 이미 확인한 내용만(T-money 현금 충전, 카카오T·우버 해외 카드, 시장 현금, 한복 고궁 무료, KTX 코레일+ 2개월 전). 가게별 배지는 후기 쌓인 뒤 */
  const QT_STYLE = {
    culture: {ic: "🏯", city: "gyeongju", seoul: ["history", "market", "easy"], cityC: ["history", "night"]},
    food: {ic: "🍜", city: "busan", seoul: ["market", "history", "easy"], cityC: ["oldtown", "sea", "easy"]},
    sea: {ic: "🌊", city: "busan", seoul: ["history", "market", "easy"], cityC: ["sea", "oldtown", "easy"]},
    easy: {ic: "🌿", city: "busan", seoul: ["easy", "history", "market"], cityC: ["easy", "sea", "oldtown"]}
  };
  const QT_CITY_C = {busan: ["sea", "oldtown", "easy"], gyeongju: ["history", "night"]};
  const QT_TX = {
    en: {
      cta: "Plan my Korea trip in 3 taps", ctaSub: "No sign-up · No Korean phone number · Costs in your currency",
      h1: "Plan Korea in 3 taps", lede: "Tell us how many days and what you love. We plan Seoul plus one more city, with costs in your currency. No sign-up, no Korean phone number.",
      close: "Close", back: "Back", step: (i) => `${i} of 3`,
      q1: "How many days in Korea?", q1s: "Counting your arrival and departure days", days: n => `${n} days`,
      q2: "What do you love?", styles: {culture: ["K-culture & history", "Palaces, hanok, Silla relics"], food: ["Food & markets", "Street food and local markets"], sea: ["Sea & city views", "Busan beaches and lookouts"], easy: ["Easy pace", "Fewer stops, more rest"]},
      q3: "Your budget?", budgets: {budget: ["Budget", "Guesthouses, simple meals"], standard: ["Standard", "Mid-range hotels"], comfort: ["Comfort", "Nicer hotels and meals"]},
      title: (n, c) => `${n} days in Seoul + ${c}`, perP: "per person, 2 people sharing a room", total: "Estimated total",
      parts: {stay: "Stay", food: "Food", move: "Transport (airport, between cities, local)"}, notIncl: "Entrance fees and shopping are not included. Prices are estimates.",
      swap: "Second city", order: "Book in this order",
      book: [["📶", "Mobile data (eSIM)", "Many Korean apps need data. Buy before you fly."], ["🚄", "Train between cities", "KTX and SRT are booked in the Korail+ app (English menu). Seats open 2 months before, at 7 a.m. Klook also sells Korean train tickets."], ["🏨", "Places to stay", "Book Seoul and your second city."], ["💳", "On arrival", "Get a T-money card at a convenience store for subways and buses. It's charged with cash."]],
      links: {esim: "Find an eSIM", train: "Korail+ / Klook", stay: "Search stays", map: "Open map"}, noFee: "These are regular links. Hoolzzeok earns no commission from them.",
      day: i => `Day ${i}`, arrive: "Arrive at Incheon Airport", arriveT: "Take the Airport Railroad (AREX) or an airport bus into Seoul and check in. Get cash and a T-money card at the airport or a convenience store. Rest tonight.",
      moveEve: c => `Evening: go to ${c}`, moveEveT: "KTX is fastest. Express buses are cheaper. Sleep there tonight.",
      leave: "Fly home", leaveSeoul: "Take AREX from Seoul Station to Incheon Airport. Check your airline's check-in deadline.",
      leaveCity: c => `From ${c}, take the KTX back to Seoul, then AREX to Incheon Airport. Leave plenty of time, or check flights from the nearest airport.`,
      tips: {tmoney: "🚇 Subway & bus: T-money card (charge with cash)", taxi: "🚕 Taxi: Kakao T or Uber take foreign cards. Show the Korean name to the driver", cash: "💵 Small eateries and market stalls may be cash only", hanbok: "👘 Wear hanbok and palace entry is free", ktx: "🚄 KTX tickets: Korail+ app or Klook"},
      share: "Share this plan", copied: "Link copied", calc: "Change details in the calculator", again: "Start over", seoul: "Seoul"
    },
    ja: {
      cta: "3回タップで韓国旅行プラン", ctaSub: "会員登録なし・韓国の電話番号なし・費用はあなたの通貨で",
      h1: "3回タップで韓国旅行", lede: "日数と好きなことを選ぶだけ。ソウル＋もう1都市の旅程と費用を、あなたの通貨で。登録も韓国の電話番号もいりません。",
      close: "閉じる", back: "戻る", step: (i) => `${i} / 3`,
      q1: "韓国に何日いますか？", q1s: "到着日と出発日を含めて", days: n => `${n}日`,
      q2: "好きなことは？", styles: {culture: ["Kカルチャーと歴史", "古宮・韓屋・新羅の遺跡"], food: ["グルメと市場", "屋台と地元の市場"], sea: ["海と街の景色", "釜山の海と展望"], easy: ["のんびり", "少なめの移動でゆっくり"]},
      q3: "予算は？", budgets: {budget: ["節約", "ゲストハウス・シンプルな食事"], standard: ["ふつう", "中級ホテル"], comfort: ["ゆったり", "良いホテルと食事"]},
      title: (n, c) => `${n}日間 ソウル＋${c}`, perP: "1人あたり（2人で1部屋）", total: "費用の目安",
      parts: {stay: "宿泊", food: "食事", move: "交通（空港・都市間・現地）"}, notIncl: "入場料と買い物は含みません。金額は目安です。",
      swap: "2つ目の都市", order: "この順番で予約",
      book: [["📶", "モバイルデータ（eSIM）", "韓国のアプリはデータ通信が必要です。出発前に。"], ["🚄", "都市間の列車", "KTXとSRTはアプリ「코레일+（Korail+）」で予約（日本語メニューあり）。乗車日の2か月前の午前7時から。Klookでも買えます。"], ["🏨", "宿", "ソウルと2つ目の都市を予約。"], ["💳", "到着したら", "地下鉄・バス用にコンビニでT-moneyカード。チャージは現金です。"]],
      links: {esim: "eSIMを探す", train: "Korail+ / Klook", stay: "宿を探す", map: "地図を開く"}, noFee: "通常のリンクです。フルチョクは手数料を受け取りません。",
      day: i => `${i}日目`, arrive: "仁川空港に到着", arriveT: "空港鉄道（AREX）か空港バスでソウルへ行き、チェックイン。空港かコンビニで現金とT-moneyカードを用意。今夜は休みましょう。",
      moveEve: c => `夜：${c}へ移動`, moveEveT: "KTXが最速、高速バスは安め。今夜はそちらに泊まります。",
      leave: "帰国", leaveSeoul: "ソウル駅からAREXで仁川空港へ。航空会社のチェックイン締切を確認してください。",
      leaveCity: c => `${c}からKTXでソウルへ戻り、AREXで仁川空港へ。時間に余裕を持つか、近くの空港の便を確認してください。`,
      tips: {tmoney: "🚇 地下鉄・バス：T-moneyカード（チャージは現金）", taxi: "🚕 タクシー：Kakao TとUberは海外カードOK。運転手に韓国語の名前を見せる", cash: "💵 小さな食堂や屋台は現金のみのことも", hanbok: "👘 韓服を着ると古宮は無料", ktx: "🚄 KTX：Korail+アプリかKlook"},
      share: "このプランを共有", copied: "リンクをコピーしました", calc: "計算機で細かく変える", again: "最初から", seoul: "ソウル"
    },
    zh: {
      cta: "点3下，排好韩国行程", ctaSub: "无需注册·无需韩国手机号·费用按你的货币",
      h1: "点3下，韩国行程搞定", lede: "选天数和喜好，就给你首尔＋另一个城市的行程和费用，按你的货币显示。不用注册，也不用韩国手机号。",
      close: "关闭", back: "返回", step: (i) => `${i} / 3`,
      q1: "在韩国待几天？", q1s: "包括到达和离开的那天", days: n => `${n}天`,
      q2: "你喜欢什么？", styles: {culture: ["韩流与历史", "古宫、韩屋、新罗遗迹"], food: ["美食与市场", "小吃和本地市场"], sea: ["海景与城市景观", "釜山海滩和观景点"], easy: ["慢节奏", "少走动，多休息"]},
      q3: "预算？", budgets: {budget: ["经济", "青旅、简单餐食"], standard: ["标准", "中档酒店"], comfort: ["舒适", "更好的酒店和餐食"]},
      title: (n, c) => `${n}天 首尔＋${c}`, perP: "每人（2人住1间）", total: "预计总费用",
      parts: {stay: "住宿", food: "餐饮", move: "交通（机场、城际、当地）"}, notIncl: "不含门票和购物。金额为估算。",
      swap: "第二个城市", order: "按这个顺序预订",
      book: [["📶", "手机流量（eSIM）", "韩国的应用大多需要流量，出发前买好。"], ["🚄", "城际火车", "KTX和SRT在“코레일+（Korail+）”应用预订（有中文菜单）。乘车日前2个月上午7点开售。Klook也有卖。"], ["🏨", "住宿", "预订首尔和第二个城市的住处。"], ["💳", "到了以后", "在便利店买T-money交通卡坐地铁和公交，只能用现金充值。"]],
      links: {esim: "找eSIM", train: "Korail+ / Klook", stay: "找住宿", map: "打开地图"}, noFee: "这些是普通链接，Hoolzzeok不收佣金。",
      day: i => `第${i}天`, arrive: "到达仁川机场", arriveT: "坐机场铁路（AREX）或机场巴士进首尔，办理入住。在机场或便利店准备现金和T-money卡。今晚好好休息。",
      moveEve: c => `晚上：前往${c}`, moveEveT: "KTX最快，高速巴士更便宜。今晚住那里。",
      leave: "回国", leaveSeoul: "从首尔站坐AREX到仁川机场。请确认航空公司的值机截止时间。",
      leaveCity: c => `从${c}坐KTX回首尔，再坐AREX到仁川机场。留足时间，或看看附近机场的航班。`,
      tips: {tmoney: "🚇 地铁和公交：T-money卡（现金充值）", taxi: "🚕 出租车：Kakao T和Uber可用境外卡。把韩文名字给司机看", cash: "💵 小饭馆和市场摊位可能只收现金", hanbok: "👘 穿韩服参观古宫免费", ktx: "🚄 KTX：Korail+应用或Klook"},
      share: "分享这个行程", copied: "已复制链接", calc: "在计算器里细调", again: "重新开始", seoul: "首尔"
    }
  };
  const QTX = () => QT_TX[lang] || QT_TX.en;
  const qt = {step: 1, days: null, style: null, budget: null, city: null};
  function courseOne(pid, id){
    const keep = courseSel[pid]; courseSel[pid] = id;
    let h = courseHtml(pid, false); courseSel[pid] = keep;
    return h.replace(/<p class="c-sub">[\s\S]*?<\/p>/, "").replace(/<div class="c-chips">[\s\S]*?<\/div>/, "").replace('data-course-box="', 'data-qt-course="');
  }
  /* 날짜 배치: 첫날 도착, 마지막 날 출국. 가운데 날(F일)을 서울·지방 코스로 나눔 */
  function qtPlan(days, style, cityId){
    const S = QT_STYLE[style], city = cityId || S.city, cc = city === S.city ? S.cityC : QT_CITY_C[city];
    const F = days - 2, C = F < 2 ? 0 : Math.min(cc.length, Math.ceil(F / 2)), Sd = F - C;
    const seoulC = Array.from({length: Sd}, (_, i) => S.seoul[i % S.seoul.length]);
    return {city, C, Sd, nightsSeoul: C ? Sd : days - 1, nightsCity: C ? days - 1 - Sd : 0, seoulC, cityC: cc.slice(0, C)};
  }
  function qtCost(p, budget){
    const keep = PARTY; PARTY = 2;
    try {
      const a = calcBudget(byId("incheon"), byId("seoul"), p.nightsSeoul, "transit", budget, false, null);
      const b = p.C ? calcBudget(byId("seoul"), byId(p.city), p.nightsCity, "transit", budget, false, null) : null;
      const f = b ? p.nightsCity / (p.nightsCity + 1) : 0;   // 하루 겹치는 식비·현지교통 빼기
      const stay = a.lodging + (b ? b.lodging : 0), food = a.food + (b ? Math.round(b.food * f) : 0);
      const move = a.transport + a.local + (b ? b.transport + Math.round(b.local * f) : 0);
      return {stay, food, move, total: stay + food + move};
    } finally { PARTY = keep; }
  }
  function qtRender(){
    const X = QTX(), L = T[lang], box = $("qt-body");
    $("qt-back").hidden = qt.step === 1 || qt.step === 4;
    $("qt-prog").style.width = `${Math.min(100, (qt.step - 1) / 3 * 100)}%`;
    $("qt-step").textContent = qt.step <= 3 ? X.step(qt.step) : "";
    const btns = (items, key) => `<div class="qt-opts">${items.map(([v, t, s, ic]) => `<button type="button" class="qt-opt" data-k="${key}" data-v="${v}" aria-pressed="${qt[key] === v}">${ic ? `<span class="qt-ic" aria-hidden="true">${ic}</span>` : ""}<b>${t}</b>${s ? `<small>${s}</small>` : ""}</button>`).join("")}</div>`;
    if (qt.step === 1) box.innerHTML = `<h2 class="qt-h" id="qt-title">${X.q1}</h2><p class="qt-sub">${X.q1s}</p>` + btns([3, 4, 5, 6, 7].map(n => [n, X.days(n), "", ""]), "days");
    else if (qt.step === 2) box.innerHTML = `<h2 class="qt-h" id="qt-title">${X.q2}</h2>` + btns(Object.keys(QT_STYLE).map(k => [k, X.styles[k][0], X.styles[k][1], QT_STYLE[k].ic]), "style");
    else if (qt.step === 3) box.innerHTML = `<h2 class="qt-h" id="qt-title">${X.q3}</h2>` + btns(["budget", "standard", "comfort"].map(k => [k, X.budgets[k][0], X.budgets[k][1], ""]), "budget");
    else box.innerHTML = qtResult();
    box.querySelectorAll(".qt-opt").forEach(b => b.addEventListener("click", () => {
      const k = b.dataset.k; qt[k] = k === "days" ? +b.dataset.v : b.dataset.v; if (k === "style") qt.city = null;
      qtGo(qt.step + 1); }));
    box.querySelectorAll("[data-qt-city]").forEach(b => b.addEventListener("click", () => { qt.city = b.dataset.qtCity; qtRender(); qtUrl(); }));
    const sh = $("qt-share"); if (sh) sh.addEventListener("click", qtShare);
    const ag = $("qt-again"); if (ag) ag.addEventListener("click", () => { qt.days = qt.style = qt.budget = qt.city = null; qtGo(1); });
    const cl = $("qt-calc"); if (cl) cl.addEventListener("click", () => { const p = qtPlan(qt.days, qt.style, qt.city); qtClose();
      state.origin = "seoul"; state.dest = p.C ? p.city : "seoul" === p.city ? "busan" : p.city; state.nights = Math.min(6, p.nightsCity || 1); state.style = qt.budget; state.mode = "transit"; state.picks = []; render(); setTimeout(() => toResult && toResult(), 60); });
    const h = $("qt-title") || box.querySelector("h2"); if (h) { h.tabIndex = -1; h.focus({preventScroll: true}); }
  }
  function qtResult(){
    const X = QTX(), L = T[lang], p = qtPlan(qt.days, qt.style, qt.city), c = qtCost(p, qt.budget), cityNm = L.name(byId(p.city));
    const tips = keys => `<ul class="qt-tips">${keys.map(k => `<li>${X.tips[k]}</li>`).join("")}</ul>`;
    const dayCard = (i, h, body, cls) => `<section class="qt-day${cls ? " " + cls : ""}"><h3><span class="qt-dn">${X.day(i)}</span> ${h}</h3>${body}</section>`;
    let d = 1, html = "";
    html += dayCard(d++, X.arrive, `<p>${X.arriveT}</p>${tips(["tmoney", "taxi"])}`, "qt-move");
    p.seoulC.forEach((cid, i) => {
      const last = i === p.seoulC.length - 1 && p.C;
      const c0 = COURSES.seoul.find(x => x.id === cid);
      html += dayCard(d++, `${X.seoul} · ${esc((c0.t[lang] || c0.t.en))}`, courseOne("seoul", cid) + tips(cid === "history" ? ["hanbok", "cash"] : ["cash"]) + (last ? `<p class="qt-eve"><b>${X.moveEve(cityNm)}</b> ${X.moveEveT}</p>${tips(["ktx"])}` : ""));
    });
    p.cityC.forEach(cid => { const c0 = COURSES[p.city].find(x => x.id === cid);
      html += dayCard(d++, `${esc(cityNm)} · ${esc((c0.t[lang] || c0.t.en))}`, courseOne(p.city, cid) + tips(["cash", "taxi"])); });
    html += dayCard(d++, X.leave, `<p>${p.C ? X.leaveCity(cityNm) : X.leaveSeoul}</p>`, "qt-move");
    const aff = AFF.klook || {};
    const link = (u, t) => `<a class="qt-lk" href="${esc(u)}" target="_blank" rel="noopener noreferrer">${t}</a>`;
    const bookLinks = [link(aff.esim || "https://www.klook.com/en-US/", X.links.esim), p.C ? link("https://www.korail.com/global/eng/main", X.links.train) : "", link("https://www.agoda.com/", X.links.stay), ""];
    const swap = Object.keys(QT_CITY_C).map(k => `<button type="button" class="qt-chip" data-qt-city="${k}" aria-pressed="${k === p.city}">${esc(L.name(byId(k)))}</button>`).join("");
    return `<div class="qt-res">
      <h2 class="qt-h" id="qt-title">${esc(X.title(qt.days, p.C ? cityNm : X.seoul))}</h2>
      <div class="qt-sum"><small>${X.total} · ${X.perP}</small><b class="num">${L.won(c.total)}</b>
        <ul class="qt-parts"><li><span>${X.parts.stay}</span><b class="num">${L.won(c.stay)}</b></li><li><span>${X.parts.food}</span><b class="num">${L.won(c.food)}</b></li><li><span>${X.parts.move}</span><b class="num">${L.won(c.move)}</b></li></ul>
        <small class="qt-note">${X.notIncl}</small></div>
      ${qt.days >= 4 ? `<div class="qt-swap"><span>${X.swap}</span>${swap}</div>` : ""}
      <section class="qt-book"><h3>${X.order}</h3><ol>${X.book.map(([ic, t, s], i) => (i === 1 && !p.C) ? "" : `<li><span class="qt-bi" aria-hidden="true">${ic}</span><div><b>${t}</b><small>${s}</small>${bookLinks[i] || ""}</div></li>`).join("")}</ol><small class="qt-note">${X.noFee}</small></section>
      ${html}
      <div class="qt-acts"><button type="button" class="rv-main" id="qt-share">${X.share}</button><button type="button" class="rv-sub" id="qt-calc">${X.calc}</button><button type="button" class="qt-again" id="qt-again">${X.again}</button></div>
    </div>`;
  }
  function qtUrl(){
    try { const u = new URL(location.href); if (qt.step === 4) u.searchParams.set("qt", [qt.days, qt.style, qt.budget, qt.city || ""].join(".")); else u.searchParams.delete("qt"); history.replaceState(history.state, "", u.toString()); } catch(e) {}
  }
  async function qtShare(){
    const u = new URL(location.href); u.hash = ""; ["code", "join", "sbtest"].forEach(k => u.searchParams.delete(k));
    const p = qtPlan(qt.days, qt.style, qt.city), txt = `${QTX().title(qt.days, p.C ? T[lang].name(byId(p.city)) : QTX().seoul)} — Hoolzzeok`;
    try { if (navigator.share) { await navigator.share({title: txt, url: u.toString()}); return; } } catch(e) { if (e && e.name === "AbortError") return; }
    try { await navigator.clipboard.writeText(u.toString()); toast(QTX().copied); } catch(e) { toast(u.toString()); }
  }
  function qtGo(n){ qt.step = Math.max(1, Math.min(4, n)); qtRender(); qtUrl(); $("qt").scrollTop = 0; }
  function qtOpen(start){
    $("qt").hidden = false; $("qt").lang = lang === "zh" ? "zh-CN" : lang; lockSync();
    if (!(history.state && history.state.qt)) { try { history.pushState({qt: 1}, ""); } catch(e) {} }
    $("qt-close").textContent = QTX().close; $("qt-back").textContent = QTX().back;
    qtGo(start || 1);
  }
  function qtClose(fromPop){
    if ($("qt").hidden) return;
    $("qt").hidden = true; lockSync(); qt.step = 1; qtUrl();
    if (!fromPop && history.state && history.state.qt) { try { history.back(); } catch(e) {} }
  }
  $("qt-close").addEventListener("click", () => qtClose());
  $("qt-back").addEventListener("click", () => qtGo(qt.step - 1));
  $("qt").addEventListener("keydown", e => { if (e.key === "Escape") qtClose(); });
  window.addEventListener("popstate", () => { if (!$("qt").hidden && !(history.state && history.state.qt)) qtClose(true); });
  $("qt-go").addEventListener("click", () => qtOpen(1));
  /* 공유 링크 ?qt=5.food.standard.busan → 결과 바로 열기 */
  try { const v = new URLSearchParams(location.search).get("qt"); if (v && lang !== "ko") { const [dd, st, bg, ct] = v.split(".");
    if (+dd >= 3 && +dd <= 7 && QT_STYLE[st] && ["budget", "standard", "comfort"].includes(bg)) { qt.days = +dd; qt.style = st; qt.budget = bg; qt.city = QT_CITY_C[ct] ? ct : null; setTimeout(() => qtOpen(4), 0); } } } catch(e) {}
  function qtHero(){
    const on = lang !== "ko" && !EMBED, X = QTX();
    $("qt-go").hidden = !on;
    if (on) { $("qt-go").innerHTML = `<b>${X.cta}</b><small>${X.ctaSub}</small>`;
      const h1 = document.querySelector("#top h1"), ld = document.querySelector("#top .lede"); if (h1) h1.textContent = X.h1; if (ld) ld.textContent = X.lede; }
  }
