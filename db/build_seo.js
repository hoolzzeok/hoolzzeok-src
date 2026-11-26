/* 훌쩍 검색용 경비 페이지 생성 (시험판)
   사용: NODE_PATH=$(npm root -g) node build_seo.js [사이트 폴더]   (build_www.py 실행 뒤에 돌리기)
   값은 사이트 계산기(index.html의 calcBudget)에서 그대로 가져옴. 손으로 쓴 숫자 없음. */
const {chromium} = require('playwright');
const fs = require('fs'), path = require('path');
const OUT = process.argv[2] || '/home/claude/www.hoolzzeok.com';
const SRC = '/home/claude/hoolzzeok_site/index.html';
const SITE = 'https://www.hoolzzeok.com';
const ORIGINS = ['seoul', 'busan', 'daegu', 'gwangju', 'daejeon'];
const DESTS = ['jeju', 'busan', 'gangneung', 'gyeongju', 'yeosu', 'sokcho', 'jeonju', 'seoul', 'chuncheon', 'andong', 'mokpo', 'pohang'];
const PER_ORIGIN = 10;
const MODES = ['transit', 'car', 'flight', 'ferry'];
const MODE_KO = {transit: '버스·기차', car: '내 차', flight: '비행기', ferry: '배'};
const MODE_NOTE = {transit: '가장 싼 고속·시외버스 요금 기준', car: '기름값과 통행료를 두 명이 나눠 낸다고 본 값(혼자 타면 더 듭니다)', flight: '공항까지 버스비와 가장 싼 평일 요금', ferry: '항구까지 버스비와 뱃삯'};
const STYLE_KO = {budget: '아껴서', standard: '보통', comfort: '넉넉하게'};
const STYLE_NOTE = {budget: '게스트하우스 도미토리, 점심 칼국수, 저녁 백반', standard: '모텔·여관 2인 1실, 점심 비빔밥, 저녁 삼겹살', comfort: '호텔 또는 펜션 2인 1실, 점심 삼계탕, 저녁 삼겹살과 냉면'};
const LODGE_KO = {dorm: '게스트하우스 도미토리', motel: '모텔·여관 (2인 1실을 반으로 나눔)', hotel: '호텔 (2인 1실을 반으로 나눔)', pension: '펜션 (2인 1실을 반으로 나눔)'};

const won = n => n.toLocaleString('ko-KR') + '원';
function man(n) { // 147000 -> 14만 7천 원
  const m = Math.floor(n / 10000), c = Math.round((n % 10000) / 1000);
  if (c === 10) return (m + 1) + '만 원';
  return (m ? m + '만' : '') + (c ? (m ? ' ' : '') + c + '천' : '') + ' 원';
}
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://' + SRC); await p.waitForTimeout(1500);
  const data = await p.evaluate(({ORIGINS, DESTS, PER_ORIGIN, MODES}) => {
    const by = id => PLACES.find(x => x.id === id);
    const out = [];
    const month = (TRAVEL_MONTH ?? KST_MONTH) + 1;
    for (const oid of ORIGINS) {
      let n = 0;
      for (const did of DESTS) {
        if (n >= PER_ORIGIN) break;
        const o = by(oid), d = by(did); if (!o || !d || oid === did) continue;
        const modes = MODES.filter(m => modeAvailable(o, d, m));
        if (!modes.length) continue;
        const rows = {};
        for (const m of modes) {
          rows[m] = {};
          for (const s of STYLES) { const r = calcBudget(o, d, 1, m, s, false, null); rows[m][s] = {transport: r.transport, lodging: r.lodging, food: r.food, local: r.local, total: r.total, est: r.est, via: r.via, busIsReal: r.busIsReal, km: r.km, lodgeKind: r.lodge.kind, lunch: r.foodInfo.lunch, dinner: r.foodInfo.dinner, coffee: r.foodInfo.coffee, rides: r.localInfo}; }
        }
        out.push({o: oid, oko: o.ko, d: did, dko: d.ko, prov: d.prov, modes, rows, half: HALF.has(did), month});
        n++;
      }
    }
    return out;
  }, {ORIGINS, DESTS, PER_ORIGIN, MODES});
  await b.close();

  const today = new Date(Date.now() + 9 * 3600 * 1000);
  const dateKo = `${today.getUTCFullYear()}년 ${today.getUTCMonth() + 1}월 ${today.getUTCDate()}일`;
  const dateIso = today.toISOString().slice(0, 10);

  const css = `:root{--ink:#12302E;--bg:#F8FAF9;--teal:#0B7A75;--line:#CFDCDA;--body:#46555A;--fur:#F3EDDC}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.7 -apple-system,"Apple SD Gothic Neo","Noto Sans KR",system-ui,sans-serif}
header{border-bottom:2px solid var(--line);padding:14px max(16px,env(safe-area-inset-left))}header a{color:var(--teal);font-weight:800;text-decoration:none;font-size:20px}
main{max-width:760px;margin:0 auto;padding:28px max(16px,env(safe-area-inset-left)) 64px}
h1{font-size:28px;line-height:1.35;margin:0 0 12px}h2{font-size:21px;margin:36px 0 10px}p{margin:0 0 12px;color:var(--body)}
.wrap{overflow-x:auto;margin:8px 0 14px}table{border-collapse:collapse;width:100%;min-width:520px;font-size:16px}th,td{border-bottom:1px solid var(--line);padding:9px 8px;text-align:right}th:first-child,td:first-child{text-align:left}th{color:var(--teal);font-weight:700}tr.sum td{font-weight:800;color:var(--ink)}
.cta{display:inline-block;background:var(--teal);color:#fff;padding:13px 22px;border-radius:10px;text-decoration:none;font-weight:700;margin:6px 0 4px}
ul{margin:0 0 12px;padding-left:22px;color:var(--body)}li{margin-bottom:6px}.links a{color:var(--teal)}small,.note{font-size:14px;color:#5b6b6e}
footer{border-top:2px solid var(--line);padding:18px max(16px,env(safe-area-inset-left));font-size:14px;color:#5b6b6e}`;

  const shell = (title, desc, url, body, ld) => `<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>${esc(title)}</title><meta name="description" content="${esc(desc)}"><link rel="canonical" href="${url}">
<meta property="og:type" content="website"><meta property="og:site_name" content="훌쩍"><meta property="og:title" content="${esc(title)}"><meta property="og:description" content="${esc(desc)}"><meta property="og:url" content="${url}"><meta property="og:locale" content="ko_KR">
<meta name="theme-color" content="#0B7A75"><link rel="icon" href="/favicon.svg" type="image/svg+xml">${ld ? `<script type="application/ld+json">${JSON.stringify(ld).replace(/</g, "\\u003c")}</script>` : ""}<style>${css}</style></head>
<body><header><a href="/">훌쩍</a></header><main>${body}</main><footer>훌쩍, 얼마 들까? 여행 경비 계산기. 이 페이지에는 광고와 제휴 링크가 없습니다. 금액은 예상치이고 실제와 다를 수 있습니다.</footer></body></html>`;

  const pageUrl = x => `${SITE}/gyeongbi/${x.o}-${x.d}/`;
  fs.rmSync(path.join(OUT, 'gyeongbi'), {recursive: true, force: true});

  for (const x of data) {
    const prim = x.modes.includes('transit') ? 'transit' : x.modes.includes('flight') ? 'flight' : x.modes.slice().sort((a, b) => x.rows[a].standard.total - x.rows[b].standard.total)[0];
    const std = x.rows[prim].standard;
    const title = `${x.oko}에서 ${x.dko} 1박 2일 경비, 1인 약 ${man(std.total)} | 훌쩍`;
    const cheapestTxt = x.modes.length > 1 ? `${MODE_KO[prim]} 기준 금액이고, 다른 이동 방법도 아래 표에 비교했습니다.` : `이동 방법은 ${MODE_KO[prim]} 하나입니다.`;
    const desc = `${x.oko}에서 ${x.dko}까지 1박 2일, 1인 기준 교통 ${man(std.transport)}, 숙박 ${man(std.lodging)}, 식비 ${man(std.food)}, 현지 교통 ${man(std.local)}. 합계 약 ${man(std.total)}. ${cheapestTxt}`;

    const modeRows = x.modes.map(m => { const r = x.rows[m].standard; return `<tr><td>${MODE_KO[m]}</td><td>${won(r.transport)}</td><td>${won(r.lodging)}</td><td>${won(r.food)}</td><td>${won(r.local)}</td><td><b>${won(r.total)}</b></td></tr>`; }).join('');
    const styleRows = ['budget', 'standard', 'comfort'].map(s => { const r = x.rows[prim][s]; return `<tr><td>${STYLE_KO[s]}</td><td>${esc(STYLE_NOTE[s])}</td><td><b>${won(r.total)}</b></td></tr>`; }).join('');
    const sameOrigin = data.filter(y => y.o === x.o && y.d !== x.d).map(y => `<a href="/gyeongbi/${y.o}-${y.d}/">${y.oko}에서 ${y.dko}</a>`).join(' · ');
    const sameDest = data.filter(y => y.d === x.d && y.o !== x.o).map(y => `<a href="/gyeongbi/${y.o}-${y.d}/">${y.oko}에서 ${y.dko}</a>`).join(' · ');

    const busNote = x.modes.includes('transit') ? (x.rows.transit.standard.busIsReal ? '버스 요금은 실제 요금표 값입니다.' : '이 구간의 버스 요금은 거리로 추정한 값이라 실제와 20% 안팎 차이가 날 수 있습니다.') : '';
    const flightNote = x.modes.includes('flight') ? (x.rows.flight.standard.est ? '항공 요금은 같은 노선 자료가 없어 비슷한 노선 값으로 추정했습니다.' : '항공 요금은 가장 싼 평일 요금입니다.') : '';
    const lk = std.lodgeKind;
    /* v113: 자주 묻는 질문 — AI·검색이 그대로 인용할 수 있게 숫자·기준·기준일을 한 문장에 */
    const cheap = x.modes.map(m => ({m, v: x.rows[m].budget.total})).sort((a, b) => a.v - b.v)[0];
    const faq = [
      [`${x.oko}에서 ${x.dko} 1박 2일 여행 경비는 1인 얼마인가요?`, `${MODE_KO[prim]}로 가는 보통 여행 기준 1인 약 ${man(std.total)}입니다(왕복 교통 ${won(std.transport)}, 숙박 ${won(std.lodging)}, 식비 ${won(std.food)}, 현지 교통 ${won(std.local)}). ${dateKo} 기준 훌쩍 계산값이며 입장료·체험·기념품은 빠져 있습니다.`],
      [`${x.oko}에서 ${x.dko}까지 가장 싸게 가면 얼마인가요?`, `${MODE_KO[cheap.m]}로 가고 게스트하우스 도미토리에 묵으며 아껴 쓰면 1인 약 ${man(cheap.v)}입니다(${dateKo} 기준 예상치).`],
      [`${x.dko} 숙박비는 1인 얼마로 잡나요?`, `보통 여행은 ${LODGE_KO[std.lodgeKind] || '모텔·여관'} 기준 1박 1인 ${won(std.lodging)}입니다. ${x.month ? x.month + '월 ' : ''}지역 평균값이라 연휴·큰 행사 주간에는 더 비쌀 수 있습니다.`]
    ];
    const faqHtml = `<h2>자주 묻는 질문</h2>${faq.map(([q, a]) => `<h3 style="font-size:17px;margin:18px 0 6px">${esc(q)}</h3><p>${esc(a)}</p>`).join('')}`;
    const ld = {"@context": "https://schema.org", "@graph": [
      {"@type": "FAQPage", "mainEntity": faq.map(([q, a]) => ({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}))},
      {"@type": "WebPage", "name": `${x.oko}에서 ${x.dko} 1박 2일 경비`, "url": pageUrl(x), "dateModified": dateIso, "inLanguage": "ko", "isPartOf": {"@type": "WebSite", "name": "훌쩍", "url": SITE + "/"}}
    ]};
    const stdLodge = x.rows[prim].standard;
    const body = `
<h1>${x.oko}에서 ${x.dko} 1박 2일 경비, 1인 약 ${man(std.total)}</h1>
<p>${x.oko}에서 ${x.dko}까지 1박 2일 여행을 혼자 쓸 돈으로 계산했습니다. 교통, 숙박, 식비, 현지 교통을 더한 보통 여행 기준이고, ${cheapestTxt} 도로 거리는 약 ${std.km}km입니다.</p>
<h2>교통 방법별 합계 (보통 여행)</h2>
<div class="wrap"><table><thead><tr><th>방법</th><th>왕복 교통</th><th>숙박 1박</th><th>식비</th><th>현지 교통</th><th>합계</th></tr></thead><tbody>${modeRows}</tbody></table></div>
<ul>${x.modes.map(m => `<li>${MODE_KO[m]}: ${MODE_NOTE[m]}</li>`).join('')}</ul>
<h2>쓰는 정도에 따라 얼마나 달라지나</h2>
<p>${MODE_KO[prim]}로 갈 때 기준입니다. 교통비는 같고 숙소와 식사만 달라집니다.</p>
<div class="wrap"><table><thead><tr><th>선택</th><th>숙소와 식사</th><th>합계</th></tr></thead><tbody>${styleRows}</tbody></table></div>
<h2>보통 여행의 계산 내역</h2>
<ul>
<li>숙박 1박 ${won(stdLodge.lodging)}: ${LODGE_KO[lk]}. ${x.month ? x.month + '월 요금 기준입니다.' : ''}</li>
<li>식비 ${won(stdLodge.food)}: 점심 2번(${won(stdLodge.lunch)}씩), 저녁 1번(${won(stdLodge.dinner)}), 커피 2잔(${won(stdLodge.coffee)}씩). 아침은 뺐습니다.</li>
<li>현지 교통 ${won(stdLodge.local)}: ${prim === 'car' ? '도착한 뒤 차로 돌아다니는 기름값' : `하루 버스 ${stdLodge.rides.bus}번, 택시 ${stdLodge.rides.taxi}번을 2일 치로 계산`}.</li>
<li>입장료, 체험, 기념품은 넣지 않았습니다. 앱에서 고르면 더해집니다.</li>
</ul>
<p class="note">${[busNote, flightNote].filter(Boolean).join(' ')} 식비는 한국소비자원 참가격 시·도별 외식비 기준입니다. ${dateKo} 기준으로 계산했습니다.</p>
${x.half ? `<p>${x.dko}은 인구감소지역 반값여행(지역사랑 휴가지원) 대상일 수 있는 지역입니다. 신청 기간과 환급 조건이 있으니 앱에서 확인하세요.</p>` : ''}
${faqHtml}
<p><a class="cta" href="/?from=${x.o}&amp;to=${x.d}&amp;nights=1">이 구간을 계산기에서 열기</a></p>
<h2>다른 구간 보기</h2>
<p class="links">${sameOrigin}</p>
${sameDest ? `<p class="links">${sameDest}</p>` : ''}
<p class="links"><a href="/gyeongbi/">전체 목록</a></p>`;
    const dir = path.join(OUT, 'gyeongbi', `${x.o}-${x.d}`);
    fs.mkdirSync(dir, {recursive: true});
    fs.writeFileSync(path.join(dir, 'index.html'), shell(title, desc, pageUrl(x), body, ld));
  }

  /* 목록 페이지 */
  const byO = {}; data.forEach(x => (byO[x.oko] = byO[x.oko] || []).push(x));
  const hub = Object.entries(byO).map(([k, arr]) => `<h2>${k}에서 출발</h2><ul class="links">${arr.map(x => `<li><a href="/gyeongbi/${x.o}-${x.d}/">${x.oko}에서 ${x.dko} 1박 2일</a>, 1인 약 ${man(Math.min(...x.modes.map(m => x.rows[m].standard.total)))}</li>`).join('')}</ul>`).join('');
  fs.writeFileSync(path.join(OUT, 'gyeongbi', 'index.html'), shell('국내 여행 1박 2일 경비 모아보기 | 훌쩍', '출발지와 도착지별 1박 2일 1인 여행 경비. 교통, 숙박, 식비, 현지 교통을 더해 계산했습니다.', SITE + '/gyeongbi/',
    `<h1>국내 여행 1박 2일 경비</h1><p>출발지와 도착지를 고르면 1인 기준 보통 여행 경비가 나옵니다. 아래는 많이 찾는 구간입니다. 다른 구간은 <a href="/" style="color:var(--teal)">계산기</a>에서 직접 넣어 보세요.</p>${hub}`));

  /* 사이트맵 */
  const urls = [SITE + '/', SITE + '/gyeongbi/', ...data.map(pageUrl)];
  fs.writeFileSync(path.join(OUT, 'sitemap.xml'), `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls.map(u => `<url><loc>${u}</loc><lastmod>${dateIso}</lastmod></url>`).join('\n')}\n</urlset>\n`);
  console.log('pages', data.length, 'urls', urls.length);
})();
