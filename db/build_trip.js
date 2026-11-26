/* v135 외국인 검색용 "한국 N일 일정과 경비" 페이지 (영어·일본어·번체)
   사용: NODE_PATH=$(npm root -g) node build_trip.js [사이트 폴더]   (build_seo.js 뒤에 돌리기: 사이트맵에 덧붙임)
   내용은 사이트의 "3번 탭" 결과 화면(?qt=)을 그대로 읽어 옴. 손으로 쓴 일정·숫자 없음. */
const {chromium} = require('playwright');
const fs = require('fs'), path = require('path');
const OUT = process.argv[2] || '/home/claude/www.hoolzzeok.com';
const SRC = '/home/claude/hoolzzeok_site/index.html';
const SITE = 'https://www.hoolzzeok.com';

// 3일은 서울만(공항 이동 2일), 4·5·7일은 서울 + 부산 / 서울 + 경주
const PLANS = [
  {slug: '3-days-seoul', days: 3, style: 'food', city: ''},
  {slug: '4-days-seoul-busan', days: 4, style: 'food', city: 'busan'},
  {slug: '5-days-seoul-busan', days: 5, style: 'food', city: 'busan'},
  {slug: '7-days-seoul-busan', days: 7, style: 'food', city: 'busan'},
  {slug: '4-days-seoul-gyeongju', days: 4, style: 'culture', city: 'gyeongju'},
  {slug: '5-days-seoul-gyeongju', days: 5, style: 'culture', city: 'gyeongju'},
  {slug: '7-days-seoul-gyeongju', days: 7, style: 'culture', city: 'gyeongju'},
  // v136: 제주 (외국인 방문율 4위, 9.7%)
  {slug: '4-days-jeju', days: 4, style: 'nature', city: '', air: 'cju'},
  {slug: '5-days-jeju', days: 5, style: 'nature', city: '', air: 'cju'},
  {slug: '5-days-seoul-jeju', days: 5, style: 'nature', city: 'jeju'},
  {slug: '7-days-seoul-jeju', days: 7, style: 'nature', city: 'jeju'},
  {slug: '5-days-busan-jeju', days: 5, style: 'nature', city: 'jeju', air: 'pus'},
];
const LANGS = {
  en: {q: 'en', html: 'en', loc: 'en-US', og: 'en_US', brand: 'Hoolzzeok',
    h1: t => `${t}: day-by-day plan and cost`,
    title: (t, c) => `${t} itinerary and cost (about ${c} per person) | Hoolzzeok`,
    desc: (t, c, p) => `${t} for first-time visitors: ${/^land/.test(p) ? '' : 'arrive at Incheon, '}${p}. About ${c} per person with two people sharing a room. Day-by-day stops, meals, train and booking order.`,
    path: {busan: 'then take the KTX to Busan', gyeongju: 'then take the KTX to Gyeongju', jeju: 'then fly to Jeju', cju: 'land at Jeju Airport', pus: 'land in Busan and fly to Jeju', '': 'stay in Seoul'},
    intro: 'A ready-made plan for people who don\'t want to plan. No sign-up, no Korean phone number needed.',
    cost: 'Cost per person', costNote: 'Two people sharing a room. Flights, entrance fees and shopping are not included. Prices are estimates.',
    level: 'Budget', total: 'Total', b: {budget: 'Budget', standard: 'Standard', comfort: 'Comfort'},
    bNote: {budget: 'Guesthouses, simple meals', standard: 'Mid-range hotels', comfort: 'Nicer hotels and meals'},
    days: 'Day by day (standard budget)', cta: 'Change days, interests or budget (3 taps)',
    more: 'Other plans', all: 'All Korea itineraries', hubT: 'Korea itineraries with costs | Hoolzzeok', hubH: 'Korea itineraries with costs',
    hubP: 'Ready-made plans for Seoul, Busan, Gyeongju and Jeju. Costs are per person, two people sharing a room.',
    q1: (t, c) => `How much does ${t.replace(/^(\d+) days in/, 'a $1-day trip to')} cost?`,
    a1: (c, b, k, d) => `About ${c} per person on a standard budget (two people sharing a room), from ${b} on a budget to ${k} for comfort. Flights and entrance fees are not included. Estimate as of ${d}.`,
    foot: 'Hoolzzeok: Korea trip cost calculator. Prices are estimates and may differ. No commission from links on this page.',
    upd: d => `Updated ${d}. Exchange rate: Seoul Money Brokerage base rate.`},
  ja: {q: 'ja', html: 'ja', loc: 'ja-JP', og: 'ja_JP', brand: 'フルチョク',
    h1: t => `${t}：日ごとの予定と費用`,
    title: (t, c) => `${t}のモデルコースと費用（1人約${c}）| フルチョク`,
    desc: (t, c, p) => `初めての韓国旅行向け${t}。${/空港|釜山に/.test(p) ? '' : '仁川に着いて'}${p}。2人1室で1人約${c}。日ごとの観光地・食事・列車・予約の順番まで。`,
    path: {busan: 'ソウルからKTXで釜山へ', gyeongju: 'ソウルからKTXで慶州へ', jeju: 'ソウルから飛行機で済州へ', cju: '済州空港に到着', pus: '釜山に着いて済州へ', '': 'ソウルに滞在'},
    intro: '計画が面倒な人のための、そのまま使えるプランです。会員登録なし、韓国の電話番号も不要です。',
    cost: '1人あたりの費用', costNote: '2人1室の場合。航空券・入場料・買い物は含みません。金額は目安です。',
    level: '予算', total: '合計', b: {budget: '節約', standard: 'ふつう', comfort: 'ゆったり'},
    bNote: {budget: 'ゲストハウス・シンプルな食事', standard: '中級ホテル', comfort: '良いホテルと食事'},
    days: '日ごとの予定（ふつう）', cta: '日数・好み・予算を変える（3タップ）',
    more: 'ほかのプラン', all: '韓国モデルコース一覧', hubT: '韓国旅行モデルコースと費用 | フルチョク', hubH: '韓国旅行モデルコースと費用',
    hubP: 'ソウル・釜山・慶州・済州のモデルコース。費用は2人1室の1人あたりです。',
    q1: t => `${t}の費用はいくら？`,
    a1: (c, b, k, d) => `ふつうの予算で1人約${c}（2人1室）。節約なら${b}、ゆったりなら${k}。航空券・入場料は含みません。${d}時点の見積もりです。`,
    foot: 'フルチョク：韓国旅行の費用計算。金額は見積もりで、実際と異なる場合があります。このページのリンクから手数料は受け取っていません。',
    upd: d => `${d}更新。為替：ソウル外国為替仲介の基準レート。`},
  'zh-tw': {q: 'zh-tw', html: 'zh-Hant-TW', loc: 'zh-TW', og: 'zh_TW', brand: 'Hoolzzeok',
    h1: t => `${t}：每日行程與費用`,
    title: (t, c) => `${t}行程與費用（每人約${c}）| Hoolzzeok`,
    desc: (t, c, p) => `第一次去韓國的${t}：${/直接|到釜山/.test(p) ? '' : '抵達仁川，'}${p}。兩人一間房每人約${c}。每天的景點、餐廳、火車和預訂順序。`,
    path: {busan: '再搭KTX到釜山', gyeongju: '再搭KTX到慶州', jeju: '再飛到濟州', cju: '直接飛到濟州', pus: '到釜山再飛濟州', '': '住在首爾'},
    intro: '給懶得排行程的人，直接照著走就好。不用註冊，也不需要韓國手機號碼。',
    cost: '每人費用', costNote: '兩人一間房。不含機票、門票和購物。金額為估算。',
    level: '預算', total: '合計', b: {budget: '經濟', standard: '標準', comfort: '舒適'},
    bNote: {budget: '青旅、簡單餐食', standard: '中檔酒店', comfort: '更好的酒店和餐食'},
    days: '每日行程（標準預算）', cta: '改天數、喜好或預算（點3下）',
    more: '其他行程', all: '全部韓國行程', hubT: '韓國自由行行程與費用 | Hoolzzeok', hubH: '韓國自由行行程與費用',
    hubP: '首爾、釜山、慶州、濟州的現成行程。費用為兩人一間房的每人金額。',
    q1: t => `${t}要花多少錢？`,
    a1: (c, b, k, d) => `標準預算每人約${c}（兩人一間房）；經濟約${b}，舒適約${k}。不含機票和門票。${d}的估算。`,
    foot: 'Hoolzzeok：韓國旅行費用計算。金額為估算，可能與實際不同。本頁連結不收取佣金。',
    upd: d => `${d}更新。匯率：首爾外匯經紀公司基準匯率（新台幣為約略換算）。`},
};
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const url = (lg, slug) => `${SITE}/${lg}/korea-itinerary/${slug ? slug + '/' : ''}`;
const HREFL = {en: 'en', ja: 'ja', 'zh-tw': 'zh-Hant'};

(async () => {
  const b = await chromium.launch();
  const data = {};
  for (const lg of Object.keys(LANGS)) {
    const L = LANGS[lg];
    const ctx = await b.newContext({locale: L.loc, viewport: {width: 390, height: 844}});
    const p = await ctx.newPage();
    await p.route(/fonts\.|cdn\.jsdelivr|unpkg|supabase/, r => r.fulfill({body: ''}));
    data[lg] = [];
    for (const pl of PLANS) {
      const one = {};
      for (const bud of ['budget', 'standard', 'comfort']) {
        const q = `${pl.days}.${pl.style}.${bud}.${pl.city || ''}${pl.air ? '.' + pl.air : ''}`;
        await p.goto(`file://${SRC}?qt=${q}&lang=${L.q}`); await p.waitForTimeout(700);
        const r = await p.evaluate(() => {
          const T = s => (document.querySelector(s) || {}).textContent?.trim() || '';
          const days = [...document.querySelectorAll('#qt-body .qt-day')].map(sec => {
            const c = sec.cloneNode(true); c.querySelectorAll('details, button').forEach(x => x.remove());
            return {move: sec.classList.contains('qt-move'), h: c.querySelector('h3').textContent.replace(/\s+/g, ' ').trim(),
              dn: (c.querySelector('.qt-dn') || {}).textContent || '', rest: (() => { const h = c.querySelector('h3').cloneNode(true); const d = h.querySelector('.qt-dn'); if (d) d.remove(); return h.textContent.replace(/\s+/g, ' ').trim(); })(),
              brief: [...c.querySelectorAll('.qt-brief li')].map(li => ({t: (li.querySelector('b') || {}).textContent || '', x: li.textContent.replace((li.querySelector('b') || {}).textContent || '', '').replace(/\s+/g, ' ').trim(), meal: li.classList.contains('meal')})),
              ps: [...c.querySelectorAll(':scope > p')].map(x => { const bb = x.querySelector('b'); const bt = bb ? bb.textContent.trim() : ''; return {b: bt, r: x.textContent.replace(bt, '').replace(/\s+/g, ' ').trim()}; }),
              tips: [...c.querySelectorAll('.qt-tips li')].map(x => x.textContent.trim())};
          });
          const book = [...document.querySelectorAll('#qt-body .qt-book li')].map(li => ({b: (li.querySelector('b') || {}).textContent || '', s: (li.querySelector('small') || {}).textContent || '', a: li.querySelector('a') ? {h: li.querySelector('a').href, t: li.querySelector('a').textContent} : null}));
          return {title: T('#qt-title'), total: T('.qt-sum > b'), parts: [...document.querySelectorAll('.qt-parts li')].map(li => [li.querySelector('span').textContent, li.querySelector('b').textContent]),
            sumNote: T('.qt-sum .qt-note'), bookH: T('.qt-book h3'), book, bookNote: T('.qt-book .qt-note'), days};
        });
        one[bud] = r;
      }
      data[lg].push({...pl, ...one.standard, totals: {budget: one.budget.total, standard: one.standard.total, comfort: one.comfort.total}, partsB: one.budget.parts, partsC: one.comfort.parts});
    }
    await ctx.close();
  }
  const fxDate = await (async () => { const p = await b.newPage(); await p.goto('file://' + SRC); await p.waitForTimeout(500); const d = await p.evaluate(() => FX.date); await p.close(); return d; })();
  await b.close();

  const today = new Date(Date.now() + 9 * 3600 * 1000).toISOString().slice(0, 10);
  const css = `:root{--ink:#12302E;--bg:#F8FAF9;--teal:#0B7A75;--line:#CFDCDA;--body:#46555A;--soft:#E6F2F1}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.7 -apple-system,"Segoe UI","Hiragino Sans","PingFang TC","Noto Sans",system-ui,sans-serif}
header{border-bottom:2px solid var(--line);padding:14px max(16px,env(safe-area-inset-left))}header a{color:var(--teal);font-weight:800;text-decoration:none;font-size:20px}
main{max-width:760px;margin:0 auto;padding:28px max(16px,env(safe-area-inset-left)) 64px}
h1{font-size:28px;line-height:1.35;margin:0 0 12px;text-wrap:balance}h2{font-size:21px;margin:36px 0 10px}h3{font-size:18px;margin:22px 0 6px}p{margin:0 0 12px;color:var(--body)}
.wrap{overflow-x:auto;margin:8px 0 14px}table{border-collapse:collapse;width:100%;font-size:16px}th,td{border-bottom:1px solid var(--line);padding:9px 8px;text-align:left}td.n,th.n{text-align:right;font-variant-numeric:tabular-nums}th{color:var(--teal)}
.big{font-size:34px;font-weight:800;color:var(--ink);margin:4px 0}.cta{display:inline-block;background:var(--teal);color:#fff;padding:13px 22px;border-radius:10px;text-decoration:none;font-weight:700;margin:10px 0}
.day{border-left:3px solid var(--line);padding:2px 0 2px 14px;margin:18px 0}.day ol{list-style:none;margin:6px 0 8px;padding:0}.day li{margin:3px 0}.day b.t{display:inline-block;min-width:52px;color:var(--teal)}.meal{color:var(--body)}.dn{display:inline-block;background:var(--soft);color:var(--teal);border-radius:6px;padding:0 8px;margin-right:4px;font-size:15px}
ul{margin:0 0 12px;padding-left:22px;color:var(--body)}li{margin-bottom:6px}.links a,main a{color:var(--teal)}small,.note{font-size:14px;color:#5b6b6e}
.tips{list-style:none;padding:0;font-size:15px}.book li{margin-bottom:10px}
footer{border-top:2px solid var(--line);padding:18px max(16px,env(safe-area-inset-left));font-size:14px;color:#5b6b6e}`;
  const alts = slug => Object.keys(LANGS).map(l => `<link rel="alternate" hreflang="${HREFL[l]}" href="${url(l, slug)}">`).join('') + `<link rel="alternate" hreflang="x-default" href="${url('en', slug)}">`;
  const shell = (L, title, desc, u, slug, body, ld) => `<!doctype html>
<html lang="${L.html}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>${esc(title)}</title><meta name="description" content="${esc(desc)}"><link rel="canonical" href="${u}">${alts(slug)}
<meta property="og:type" content="article"><meta property="og:site_name" content="${L.brand}"><meta property="og:title" content="${esc(title)}"><meta property="og:description" content="${esc(desc)}"><meta property="og:url" content="${u}"><meta property="og:locale" content="${L.og}">
<meta name="theme-color" content="#0B7A75"><link rel="icon" href="/favicon.svg" type="image/svg+xml">${ld ? `<script type="application/ld+json">${JSON.stringify(ld).replace(/</g, '\\u003c')}</script>` : ''}<style>${css}</style></head>
<body><header><a href="/?lang=${L.q}">${L.brand}</a></header><main>${body}</main><footer>${esc(L.foot)}</footer></body></html>`;

  const urls = [];
  for (const [lg, L] of Object.entries(LANGS)) {
    const dir0 = path.join(OUT, lg, 'korea-itinerary');
    fs.rmSync(dir0, {recursive: true, force: true}); fs.mkdirSync(dir0, {recursive: true});
    for (const x of data[lg]) {
      const u = url(lg, x.slug), t = x.title, c = x.totals.standard;
      const title = L.title(t, c), desc = L.desc(t, c, L.path[x.air === 'cju' ? 'cju' : x.air === 'pus' ? 'pus' : x.city]);
      const costRows = ['budget', 'standard', 'comfort'].map(k => `<tr><td>${esc(L.b[k])}</td><td>${esc(L.bNote[k])}</td><td class="n"><b>${esc(x.totals[k])}</b></td></tr>`).join('');
      const parts = x.parts.map(([a, v]) => `<li>${esc(a)}: ${esc(v)}</li>`).join('');
      const book = `<h2>${esc(x.bookH)}</h2><ol class="book">${x.book.map(k => `<li><b>${esc(k.b)}</b><br><small>${esc(k.s)}</small>${k.a ? ` <a href="${esc(k.a.h)}" rel="noopener" target="_blank">${esc(k.a.t)}</a>` : ''}</li>`).join('')}</ol><p class="note">${esc(x.bookNote)}</p>`;
      const days = x.days.map(d => `<section class="day"><h3>${d.dn ? `<span class="dn">${esc(d.dn)}</span> ` : ''}${esc(d.dn ? d.rest : d.h)}</h3>${d.brief.length ? `<ol>${d.brief.map(s => `<li${s.meal ? ' class="meal"' : ''}><b class="t">${esc(s.t)}</b> ${esc(s.x)}</li>`).join('')}</ol>` : ''}${d.ps.map(s => `<p>${s.b ? `<b>${esc(s.b)}</b><br>` : ''}${esc(s.r)}</p>`).join('')}${d.tips.length ? `<ul class="tips">${d.tips.map(s => `<li>${esc(s)}</li>`).join('')}</ul>` : ''}</section>`).join('');
      const qt = `/?qt=${x.days}.${x.style}.standard.${x.city || ''}${x.air ? '.' + x.air : ''}&amp;lang=${L.q}`;
      const others = data[lg].filter(y => y.slug !== x.slug).map(y => `<a href="/${lg}/korea-itinerary/${y.slug}/">${esc(y.title)}</a>`).join(' · ');
      const faq = [[L.q1(t), L.a1(c, x.totals.budget, x.totals.comfort, fxDate)]];
      const ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'FAQPage', mainEntity: faq.map(([q, a]) => ({'@type': 'Question', name: q, acceptedAnswer: {'@type': 'Answer', text: a}}))},
        {'@type': 'WebPage', name: L.h1(t), url: u, dateModified: today, inLanguage: L.html, isPartOf: {'@type': 'WebSite', name: L.brand, url: SITE + '/'}}]};
      const body = `<h1>${esc(L.h1(t))}</h1>
<p>${esc(L.intro)}</p>
<h2>${esc(L.cost)}</h2>
<p class="big">${esc(c)}</p><ul>${parts}</ul>
<div class="wrap"><table><thead><tr><th>${esc(L.level)}</th><th></th><th class="n">${esc(L.total)}</th></tr></thead><tbody>${costRows}</tbody></table></div>
<p class="note">${esc(L.costNote)}</p>
<p><a class="cta" href="${qt}">${esc(L.cta)}</a></p>
${book}
<h2>${esc(L.days)}</h2>${days}
<h2>${esc(faq[0][0])}</h2><p>${esc(faq[0][1])}</p>
<p><a class="cta" href="${qt}">${esc(L.cta)}</a></p>
<h2>${esc(L.more)}</h2><p class="links">${others}</p><p class="links"><a href="/${lg}/korea-itinerary/">${esc(L.all)}</a></p>
<p class="note">${esc(L.upd(today))}</p>`;
      fs.mkdirSync(path.join(dir0, x.slug), {recursive: true});
      fs.writeFileSync(path.join(dir0, x.slug, 'index.html'), shell(L, title, desc, u, x.slug, body, ld));
      urls.push(u);
    }
    const hub = `<h1>${esc(L.hubH)}</h1><p>${esc(L.hubP)}</p><ul class="links">${data[lg].map(y => `<li><a href="/${lg}/korea-itinerary/${y.slug}/">${esc(y.title)}</a>: ${esc(y.totals.standard)}</li>`).join('')}</ul><p><a class="cta" href="/?lang=${L.q}">${esc(L.cta)}</a></p>`;
    fs.writeFileSync(path.join(dir0, 'index.html'), shell(L, L.hubT, L.hubP, url(lg, ''), '', hub, null));
    urls.push(url(lg, ''));
  }
  // 사이트맵에 덧붙임
  const sm = path.join(OUT, 'sitemap.xml'); let s = fs.readFileSync(sm, 'utf8');
  s = s.replace(/<url><loc>[^<]*\/korea-itinerary\/[^<]*<\/loc>[^\n]*\n/g, '');
  s = s.replace('</urlset>', urls.map(u => `<url><loc>${u}</loc><lastmod>${today}</lastmod></url>`).join('\n') + '\n</urlset>');
  fs.writeFileSync(sm, s);
  console.log('trip pages', urls.length);
})();
