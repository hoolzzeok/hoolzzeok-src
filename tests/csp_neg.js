// v142: 실제 _headers(CSP 등)를 붙여서 사이트를 열고, 막힌 것(위반)을 모두 기록
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const OUT='/home/claude/www.hoolzzeok.com';
const rules=[];{let cur=null;for(const l of fs.readFileSync(OUT+'/_headers','utf8').split('\n')){if(!l.trim())continue;if(!/^\s/.test(l)){cur={pat:l.trim(),ops:[]};rules.push(cur)}else{const t=l.trim();if(t.startsWith('!'))cur.ops.push(['del',t.slice(1).trim().toLowerCase()]);else{const i=t.indexOf(':');cur.ops.push(['set',t.slice(0,i).trim().toLowerCase(),t.slice(i+1).trim()])}}}}
const match=(pat,p)=>new RegExp('^'+pat.replace(/[.+?^${}()|[\]\\]/g,'\\$&').replace(/\*/g,'.*')+'$').test(p);
const headersFor=p=>{const h={};for(const r of rules)if(match(r.pat,p))for(const o of r.ops){if(o[0]==='del')delete h[o[1]];else h[o[1]]=h[o[1]]?h[o[1]]+', '+o[2]:o[2]}return h};
const type=f=>({'.html':'text/html; charset=utf-8','.js':'application/javascript','.svg':'image/svg+xml','.webp':'image/webp','.xml':'application/xml','.txt':'text/plain'}[path.extname(f)]||'application/octet-stream');
(async()=>{const b=await chromium.launch();const ctx=await b.newContext({viewport:{width:390,height:844}});
await ctx.route('https://www.hoolzzeok.com/**',r=>{const u=new URL(r.request().url());let f=OUT+decodeURIComponent(u.pathname);if(f.endsWith('/'))f+='index.html';if(!fs.existsSync(f))return r.fulfill({status:404,body:'nf'});return r.fulfill({status:200,body:fs.readFileSync(f),headers:{'content-type':type(f),...headersFor(u.pathname)}})});
await ctx.route(/supabase\.co|fonts\.|cloudflareinsights/,r=>r.fulfill({status:200,body:'{}',headers:{'content-type':'application/json','access-control-allow-origin':'*'}}));
const viol=[];const run=async(url,fn)=>{const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error'&&/Content Security Policy|Refused/.test(m.text()))viol.push(url+' :: '+m.text().slice(0,200))});
 await p.addInitScript(()=>document.addEventListener('securitypolicyviolation',e=>console.error('Refused CSP '+e.violatedDirective+' '+e.blockedURI+' '+(e.sourceFile||'')+':'+e.lineNumber)));
 await p.goto(url);await p.waitForTimeout(1200);if(fn)await fn(p);console.log(url,'errs',errs.slice(0,3));await p.close()};
await run('https://www.hoolzzeok.com/',async p=>{await p.evaluate(()=>{const s=document.createElement('script');s.textContent='window.__x=1';document.head.appendChild(s);const t=document.createElement('script');t.src='https://evil.example/x.js';document.head.appendChild(t)});await p.waitForTimeout(500);console.log(' injected ran?',await p.evaluate(()=>window.__x))});
await run('https://www.hoolzzeok.com/?sbtest=1',async p=>{await p.waitForTimeout(1500);console.log(' supabase loaded:',await p.evaluate(()=>!!window.supabase&&typeof window.supabase.createClient))});
await run('https://www.hoolzzeok.com/?lang=en&qt='+encodeURIComponent('5.history+food.standard.busan.icn.20261210'),async p=>{
  const [dl]=await Promise.all([p.waitForEvent('download',{timeout:20000}).catch(e=>null),p.click('.qt-xl').catch(e=>console.log('no xl btn',e.message.slice(0,80)))]);
  console.log(' excel:',dl?dl.suggestedFilename():'NO DOWNLOAD',await p.evaluate(()=>!!window.XLSX))});
await run('https://www.hoolzzeok.com/?lang=en',async p=>{for(const sel of ['#qt-go','.qt-opt[data-v="5"]','.qt-opt[data-v="food"]','#qt-next','.qt-opt[data-v="standard"]','.qt-chip[data-qt-city="gyeongju"]','#qt-calc']){await p.click(sel).catch(e=>console.log(' miss',sel));await p.waitForTimeout(250)}
  console.log(' qt days:',await p.$$eval('#qt .qt-day',a=>a.length));await p.click('.qt-send').catch(()=>{});await p.waitForTimeout(300);
  await p.keyboard.press('Escape');await p.click('#ac-open').catch(()=>{});await p.waitForTimeout(300);await p.keyboard.press('Escape');
  await p.click('#rp-top').catch(()=>{});await p.waitForTimeout(300);await p.click('#rl-sum [data-rv-open]').catch(()=>{});await p.waitForTimeout(300);await p.click('#cm-stars [data-n="4"]').catch(()=>{});await p.waitForTimeout(300)});
await run('https://www.hoolzzeok.com/?lang=zh-tw');
await run('https://www.hoolzzeok.com/?lang=ja',async p=>{await p.click('#rp-top').catch(()=>{});await p.waitForTimeout(500)});
for(const u of ['/gyeongbi/','/en/korea-itinerary/','/en/korea-itinerary/5-days-seoul-jeju/','/zh-tw/korea-itinerary/4-days-jeju/','/privacy/','/terms/','/notice/privacy-2026-12-01/','/embed/'])await run('https://www.hoolzzeok.com'+u);
// 퍼가기: 다른 사이트 안에서 열리는지
await ctx.route('https://example.org/**',r=>r.fulfill({status:200,contentType:'text/html',body:'<iframe id=f src="https://www.hoolzzeok.com/embed/" width=380 height=600></iframe>'}));
{const p=await ctx.newPage();await p.goto('https://example.org/');await p.waitForTimeout(1500);const f=p.frames().find(x=>x.url().includes('/embed/'));console.log('embed in other site:',f?(await f.evaluate(()=>document.body.innerText.length)):'BLOCKED');
 const p2=await ctx.newPage();await ctx.route('https://evil.example/**',r=>r.fulfill({status:200,contentType:'text/html',body:'<iframe src="https://www.hoolzzeok.com/" width=380 height=600></iframe>'}));await p2.goto('https://evil.example/');await p2.waitForTimeout(1200);const g=p2.frames().find(x=>x.url().startsWith('https://www.hoolzzeok.com/'));let t='?';try{t=g?await g.evaluate(()=>document.body.innerText.length):'none'}catch(e){t='blocked'};console.log('main page in other site (should be blocked):',t)}
console.log('VIOLATIONS',viol.length);viol.slice(0,20).forEach(v=>console.log(' ',v));
console.log('headers /:',JSON.stringify(Object.keys(headersFor('/'))),'embed CSP frame:',headersFor('/embed/')['content-security-policy'].match(/frame-ancestors [^;]*/)[0],'| xfo',headersFor('/embed/')['x-frame-options']);
await b.close()})();
