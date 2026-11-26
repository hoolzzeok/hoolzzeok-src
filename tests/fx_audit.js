// 외국어 화면 점검: 보이는 글자 중 한글(lang=ko 표시가 없는 것), 가로 넘침, 오류
const {chromium}=require('playwright');const fs=require('fs');
const FILE='file:///home/claude/hoolzzeok_site/index.html';
const LOC={en:'en-US',ja:'ja-JP',zh:'zh-CN'};
const scan=()=>{const out=[];const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;
 while(n=w.nextNode()){const t=n.nodeValue;if(!/[가-힣]/.test(t))continue;const el=n.parentElement;if(!el)continue;
  if(el.closest('[lang="ko"],script,style,noscript,[hidden],option'))continue;
  if(!el.checkVisibility||!el.checkVisibility({checkOpacity:true,checkVisibilityCSS:true}))continue;
  const r=el.getBoundingClientRect();if(!r.width&&!r.height)continue;
  const host=el.closest('[id]');out.push((host?'#'+host.id:'')+' <'+el.tagName.toLowerCase()+(el.className&&typeof el.className==='string'?'.'+el.className.split(' ')[0]:'')+'> '+t.trim().slice(0,70));}
 return [...new Set(out)];};
(async()=>{const b=await chromium.launch();const report={};
for(const L of ['en','ja','zh']){
 const c=await b.newContext({viewport:{width:390,height:844},locale:LOC[L]});const p=await c.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await c.route(/fonts\.|cdn\.jsdelivr|unpkg/,r=>r.fulfill({body:''}));
 const R=report[L]={};const step=async(name,fn)=>{try{await fn();await p.waitForTimeout(400);R[name]={leaks:await p.evaluate(scan),ow:await p.evaluate(()=>document.documentElement.scrollWidth)};await p.screenshot({path:`fx/${L}_${name}.png`});}catch(e){R[name]={err:String(e).slice(0,160)}}};
 await step('home',async()=>{await p.goto(FILE);await p.waitForTimeout(900);await p.click('#ui-junior').catch(()=>{});});
 await step('result',async()=>{await p.goto(FILE+'?from=seoul&to=busan&nights=2&people=2');await p.waitForTimeout(900);});
 await step('result_full',async()=>{await p.evaluate(()=>{document.querySelectorAll('details').forEach(d=>d.open=true)});});
 await step('easy_start',async()=>{await p.goto(FILE);await p.waitForTimeout(800);await p.click('#ui-senior');});
 // 쉽게: 각 단계 첫 버튼/적당한 버튼
 await step('easy_result',async()=>{for(let i=0;i<10;i++){const bs=await p.$$('#sr-body .sr-btn');if(!bs.length||await p.$('.sr-big'))break;await bs[Math.min(1,bs.length-1)].click();await p.waitForTimeout(200);}});
 await step('easy_full',async()=>{await p.evaluate(()=>{document.querySelectorAll('#sr-body details').forEach(d=>d.open=true)});});
 R.errs=errs;await c.close();}
fs.writeFileSync('fx/report.json',JSON.stringify(report,null,1));
for(const L in report){console.log('=====',L,'errs',report[L].errs.length);for(const k in report[L]){if(k==='errs')continue;const v=report[L][k];console.log('--',k,v.err?'ERR '+v.err:`overflow ${v.ow} leaks ${v.leaks.length}`);(v.leaks||[]).slice(0,25).forEach(x=>console.log('   ',x));}}
await b.close()})();
