import sys, re
P = '/home/claude/hoolzzeok_site/index.html'; s = open(P, encoding='utf-8').read()
def rep(o, n, c=1):
    global s
    k = s.count(o)
    if k != c: sys.exit(f'못 찾음({k}) {o[:80]}')
    s = s.replace(o, n)
js = open('/home/claude/hoolzzeok_db/datalab/crowd.js', encoding='utf-8').read()
if 'const CROWD = ' in s:
    s = re.sub(r'/\* 여행객 흐름:.*?\nconst CROWD_META = .*?;\nconst CROWD = .*?;\n', lambda m: js, s, flags=re.S)
else:
    rep('const TILE_IC = {', js + 'const TILE_IC = {')
    # 아이콘: 사람 셋
    rep('''  "t-near": ''', '''  "t-crowd": '<circle class="p" cx="9" cy="13" r="3.6"/><circle class="y" cx="27" cy="13" r="3.6"/><circle class="s" cx="18" cy="10.5" r="4.4"/><path class="s" d="M10 31v-4.5a8 8 0 0 1 16 0V31z"/><path d="M3 29v-3a6 6 0 0 1 6-6M33 29v-3a6 6 0 0 0-6-6"/>',
  "t-near": ''')
    rep('const k = ["now", "c-tile", "special", "good-stay", "good", "t-spots", "t-musts", "t-wx",', 'const k = ["now", "c-tile", "special", "good-stay", "good", "t-spots", "t-musts", "t-wx", "t-crowd",')
    # 칸
    rep('''      else tiles.push(tile(L.hWx(m + 1), L.wxNoNear, `<p>${L.wxNoNearBody(CLIMATE.nat.t[m].toFixed(1))}</p>`, "t-wx")); }''',
        '''      else tiles.push(tile(L.hWx(m + 1), L.wxNoNear, `<p>${L.wxNoNearBody(CLIMATE.nat.t[m].toFixed(1))}</p>`, "t-wx")); }
    { const cr = CROWD[p.id], m = wxMonth();
      if (cr) { const [nb, yoy, idx, wr, nc] = cr, mi = idx[m], md = d8 => `${+d8.slice(4, 6)}.${+d8.slice(6)}`;
        const lv = mi == null ? "" : mi >= 112 ? L.crowdLv.busy : mi <= 90 ? L.crowdLv.calm : L.crowdLv.mid;
        const mx = Math.max(...idx.filter(x => x != null));
        const bars = idx.every(x => x != null) ? `<ol class="cr-bars" aria-hidden="true">${idx.map((v, i) => `<li${i === m ? ' class="on"' : ""}><i style="height:${Math.round(v / mx * 100)}%"></i><small>${L.wxMon(i + 1)}</small></li>`).join("")}</ol>` : "";
        const lines = [L.crowdRecent(L.crowdN(nb), md(CROWD_META.from), md(CROWD_META.to)),
          yoy != null ? L.crowdYoy(yoy, md(CROWD_META.yoyFrom), md(CROWD_META.to)) : "",
          mi != null ? L.crowdMonth(m + 1, mi - 100) : "",
          wr != null ? L.crowdWeekend((wr / 100).toFixed(1)) : "",
          nc != null ? L.crowdForeign(L.crowdN(nc)) : ""].filter(Boolean);
        if (lang !== "ko" && nc != null) lines.unshift(lines.pop());
        tiles.push(tile(L.hCrowd, [lv, L.crowdDay(L.crowdN(nb))].filter(Boolean).join(" · "), `<ul class="plain">${lines.map(x => `<li>${x}</li>`).join("")}</ul>${bars}<small class="muted">${L.crowdNote}</small>`, "t-crowd")); } }''')
    # AI 질문에 쓰는 사실
    rep('''    const sea = inSeason(d.id); if (sea.length) out.push(`${L.hSeason}: ${sea.map(s => lang==="ko"?s[0]:s[1]).join(", ")}`);''',
        '''    const sea = inSeason(d.id); if (sea.length) out.push(`${L.hSeason}: ${sea.map(s => lang==="ko"?s[0]:s[1]).join(", ")}`);
    { const cr = CROWD[d.id]; if (cr) { const mm = srMonthNum(), mi = cr[2][mm - 1]; out.push(`${L.hCrowd}: ${L.crowdDay(L.crowdN(cr[0]))}${cr[1] != null ? ", " + L.crowdYoy(cr[1], "10.1", "") : ""}${mi != null ? ", " + L.crowdMonth(mm, mi - 100) : ""}${cr[3] != null ? ", " + L.crowdWeekend((cr[3] / 100).toFixed(1)) : ""} (${L.crowdSrc})`); } }''')
    # 문구
    K = {
     'ko': '''hCrowd:"여행객 흐름", crowdLv:{busy:"이맘때 붐벼요", calm:"이맘때 한적해요", mid:"이맘때 평소 수준"}, crowdN:n=>n >= 10000 ? (n / 10000).toFixed(1).replace(/\\.0$/, "") + "만" : n.toLocaleString("ko-KR"), crowdDay:n=>`하루 약 ${n} 명`,
  crowdRecent:(n,a,b)=>`최근 3주(${a}~${b}) 다른 지역에서 온 방문자: 하루 평균 약 ${n} 명`, crowdYoy:(p,a,b)=>Math.abs(p) <= 2 ? `작년 같은 기간${b ? `(${a}~${b})` : ""}과 비슷해요` : `작년 같은 기간${b ? `(${a}~${b})` : ""}보다 ${Math.abs(p)}% ${p > 0 ? "많아요" : "적어요"}`,
  crowdMonth:(m,p)=>Math.abs(p) <= 3 ? `${m}월은 1년 평균과 비슷해요(최근 1년 자료)` : `${m}월은 1년 평균보다 ${Math.abs(p)}% ${p > 0 ? "많아요" : "적어요"}(최근 1년 자료)`, crowdWeekend:r=>`주말엔 평일(월~목)의 ${r}배예요`, crowdForeign:n=>`외국인 방문자: 하루 평균 약 ${n} 명`,
  crowdSrc:"한국관광공사 데이터랩", crowdNote:"한국관광공사 데이터랩 「지역별 방문자수」(KT·SK텔레콤 통신 자료). 방문자는 그 지역 생활권 밖에서 온 사람이라 관광객과 똑같지는 않아요. 큰 도시는 출장·업무 방문도 섞여 있어요.", ''',
     'en': '''hCrowd:"Visitor flow", crowdLv:{busy:"Busy this time of year", calm:"Quiet this time of year", mid:"Usual crowds this time of year"}, crowdN:n=>n.toLocaleString("en-US"), crowdDay:n=>`about ${n} a day`,
  crowdRecent:(n,a,b)=>`Visitors from outside the area, last 3 weeks (${a}–${b}): about ${n} a day`, crowdYoy:(p,a,b)=>Math.abs(p) <= 2 ? `About the same as last year${b ? ` (${a}–${b})` : ""}` : `${Math.abs(p)}% ${p > 0 ? "more" : "fewer"} than the same days last year${b ? ` (${a}–${b})` : ""}`,
  crowdMonth:(m,p)=>Math.abs(p) <= 3 ? `${["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][m - 1]} is close to the yearly average (last 12 months of data)` : `${["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][m - 1]} is ${Math.abs(p)}% ${p > 0 ? "above" : "below"} the yearly average (last 12 months of data)`, crowdWeekend:r=>`Weekends get ${r}× the weekday (Mon–Thu) crowds`, crowdForeign:n=>`Foreign visitors: about ${n} a day`,
  crowdSrc:"Korea Tourism Organization DataLab", crowdNote:"Korea Tourism Organization DataLab, visitors by region (KT and SK Telecom mobile data). Visitors are people from outside the local living area, so not only tourists; big cities include business trips.", ''',
     'ja': '''hCrowd:"旅行者の流れ", crowdLv:{busy:"この時期は混みます", calm:"この時期は空いています", mid:"この時期は平年並み"}, crowdN:n=>n >= 10000 ? (n / 10000).toFixed(1).replace(/\\.0$/, "") + "万" : n.toLocaleString("ja-JP"), crowdDay:n=>`1日 約${n}人`,
  crowdRecent:(n,a,b)=>`直近3週間（${a}〜${b}）域外からの訪問者：1日平均 約${n}人`, crowdYoy:(p,a,b)=>Math.abs(p) <= 2 ? `昨年同期${b ? `（${a}〜${b}）` : ""}並み` : `昨年同期${b ? `（${a}〜${b}）` : ""}より${Math.abs(p)}%${p > 0 ? "多い" : "少ない"}`,
  crowdMonth:(m,p)=>Math.abs(p) <= 3 ? `${m}月は年平均並み（直近1年のデータ）` : `${m}月は年平均より${Math.abs(p)}%${p > 0 ? "多い" : "少ない"}（直近1年のデータ）`, crowdWeekend:r=>`週末は平日（月〜木）の${r}倍`, crowdForeign:n=>`外国人訪問者：1日平均 約${n}人`,
  crowdSrc:"韓国観光公社データラボ", crowdNote:"韓国観光公社データラボ「地域別訪問者数」（KT・SKテレコムの通信データ）。訪問者は生活圏の外から来た人で、観光客だけではありません。大都市は出張なども含みます。", ''',
     'zh': '''hCrowd:"游客流量", crowdLv:{busy:"这个时期人多", calm:"这个时期人少", mid:"这个时期人流正常"}, crowdN:n=>n >= 10000 ? (n / 10000).toFixed(1).replace(/\\.0$/, "") + "万" : n.toLocaleString("zh-CN"), crowdDay:n=>`日均约${n}人`,
  crowdRecent:(n,a,b)=>`最近3周（${a}～${b}）外地访客：日均约${n}人`, crowdYoy:(p,a,b)=>Math.abs(p) <= 2 ? `与去年同期${b ? `（${a}～${b}）` : ""}持平` : `比去年同期${b ? `（${a}～${b}）` : ""}${p > 0 ? "多" : "少"}${Math.abs(p)}%`,
  crowdMonth:(m,p)=>Math.abs(p) <= 3 ? `${m}月与全年平均持平（最近一年数据）` : `${m}月比全年平均${p > 0 ? "多" : "少"}${Math.abs(p)}%（最近一年数据）`, crowdWeekend:r=>`周末人流是平日（周一至周四）的${r}倍`, crowdForeign:n=>`外国访客：日均约${n}人`,
  crowdSrc:"韩国观光公社数据实验室", crowdNote:"韩国观光公社数据实验室“地区访客数”（KT、SK电讯通信数据）。访客指来自当地生活圈以外的人，不全是游客；大城市也包括出差等。", '''}
    for lg, key in [('ko', 'wxNat:(m,t,p)=>`${m}월 전국 평균'), ('en', 'wxNat:(m,t,p)=>`National average'), ('ja', 'wxNat:(m,t,p)=>`${m}月の全国平均'), ('zh', 'wxNat:(m,t,p)=>`${m}月全国平均')]:
        rep(key, K[lg] + key)
    rep('.t-ic svg{', '''.cr-bars{list-style:none;margin:6px 0 4px;padding:0;display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:3px;align-items:end;height:72px}
.cr-bars li{display:grid;grid-template-rows:1fr auto;height:100%;align-items:end;text-align:center}
.cr-bars i{display:block;width:100%;min-height:3px;border-radius:4px 4px 0 0;background:var(--line)}
.cr-bars li.on i{background:var(--accent)}
.cr-bars small{font-size:10px;color:var(--muted);line-height:1.6}
.cr-bars li.on small{color:var(--accent);font-weight:700}
.t-ic svg{''')
open(P, 'w', encoding='utf-8').write(s); print('ok')
