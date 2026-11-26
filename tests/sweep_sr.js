const {chromium}=require('playwright');
const FILE='file:///home/claude/hoolzzeok_site/index.html';const LOC={ko:'ko-KR',en:'en-US',ja:'ja-JP',zh:'zh-CN'};
const BADS='NaN|undefined|\\[object|Infinity|\\$\\{|null원|\\bnull\\b';
const scan=(BADS)=>{const BAD=new RegExp(BADS);const out=[];const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;
 while(n=w.nextNode()){const t=n.nodeValue;if(!BAD.test(t))continue;const el=n.parentElement;if(!el||el.closest('script,style,[hidden]'))continue;if(!el.checkVisibility())continue;const h=el.closest('[id]');out.push((h?'#'+h.id:'')+': '+t.trim().slice(0,90));}
 if(document.documentElement.scrollWidth>innerWidth+1)out.push('OVERFLOW '+document.documentElement.scrollWidth);return out;};
(async()=>{const b=await chromium.launch();const issues={};let runs=0,results=0;
for(const L of ['ko','en','ja','zh']){const c=await b.newContext({viewport:{width:390,height:844},locale:LOC[L]});const p=await c.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await c.route(/fonts\.|cdn\.jsdelivr|unpkg/,r=>r.fulfill({body:''}));
 for(let seed=0;seed<(L==='ko'?40:15);seed++){runs++;
  await p.goto(FILE);await p.waitForTimeout(400);await p.click('#ui-senior');await p.waitForTimeout(150);
  const path=[];
  for(let step=0;step<14;step++){ if(await p.$('#sr-body .sr-big'))break;
   const bs=await p.$$('#sr-body .sr-btn');if(!bs.length)break;
   const k=(seed*7+step*3)%bs.length;path.push(k);await bs[k].click();await p.waitForTimeout(120);
   const r=await p.evaluate(scan,BADS);for(const x of r)(issues[L+' '+x]=issues[L+' '+x]||[]).push('s'+seed+':'+path.join('.'));}
  if(await p.$('#sr-body .sr-big')){results++;await p.evaluate(()=>document.querySelectorAll('#sr-body details').forEach(d=>d.open=true));
   // 일정 '맘에 안 들어요' 대안도 한번
   const nope=await p.$('.sr-plan .tl-nope');if(nope){await nope.click().catch(()=>{});await p.waitForTimeout(80);}
   const r=await p.evaluate(scan,BADS);for(const x of r)(issues[L+' '+x]=issues[L+' '+x]||[]).push('s'+seed+':'+path.join('.'));}
 }
 for(const e of errs)(issues[L+' PAGEERROR '+e]=issues[L+' PAGEERROR '+e]||[]).push('');await c.close();}
console.log('runs',runs,'reached result',results);for(const k in issues)console.log(k,'×',issues[k].length,issues[k].slice(0,3).join(' '));
await b.close()})();
