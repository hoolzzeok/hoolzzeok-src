const {chromium}=require('playwright');
const FILE='file:///home/claude/hoolzzeok_site/index.html';const LOC={ko:'ko-KR',en:'en-US',ja:'ja-JP',zh:'zh-CN'};
const BADS='NaN|undefined|\\[object|Infinity|\\$\\{|null원|\\bnull\\b';
const scan=(BADS)=>{const BAD=new RegExp(BADS);const out=[];const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;
 while(n=w.nextNode()){const t=n.nodeValue;if(!BAD.test(t))continue;const el=n.parentElement;if(!el||el.closest('script,style,[hidden]'))continue;if(!el.checkVisibility())continue;const h=el.closest('[id]');out.push((h?'#'+h.id:'')+': '+t.trim().slice(0,90));}
 if(document.documentElement.scrollWidth>innerWidth+1)out.push('OVERFLOW '+document.documentElement.scrollWidth);return out;};
(async()=>{const b=await chromium.launch();const issues={};const add=(L,tag,r)=>{for(const x of r)(issues[L+' '+x]=issues[L+' '+x]||[]).push(tag);};
for(const L of ['ko','en','ja','zh']){const c=await b.newContext({viewport:{width:390,height:844},locale:LOC[L]});const p=await c.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message+' @'+p.__tag));
 p.on('dialog',d=>d.dismiss());
 await c.route(/fonts\.|cdn\.jsdelivr|unpkg/,r=>r.fulfill({body:''}));
 for(const dest of ['busan','jeju','gyeongju','namhae','ulleung','gangneung']){
  await p.goto(`${FILE}?from=seoul&to=${dest}&nights=2&people=2`);await p.waitForTimeout(500);
  // 바로가기 타일 하나씩
  const nq=await p.$$eval('#qk .qk-b',a=>a.length);
  for(let i=0;i<nq;i++){p.__tag=dest+' qk'+i;await p.goto(`${FILE}?from=seoul&to=${dest}&nights=2&people=2`);await p.waitForTimeout(350);
   const ok=await p.$$eval('#qk .qk-b',(a,i)=>{const b=a[i];if(!b||b.hidden)return false;b.click();return true;},i);if(!ok)continue;await p.waitForTimeout(500);
   await p.evaluate(()=>document.querySelectorAll('details').forEach(d=>d.open=true));add(L,p.__tag,await p.evaluate(scan,BADS));}
  // 루트 짜기
  p.__tag=dest+' route';await p.goto(`${FILE}?from=seoul&to=${dest}&nights=2&people=2`);await p.waitForTimeout(350);
  const ro=await p.$('#rt-open');if(ro&&await ro.isVisible()){await ro.click();await p.waitForTimeout(300);
   const fill=await p.$('#rt [data-rt="fill"], #rt .rt-fill');if(fill)await fill.click().catch(()=>{});await p.waitForTimeout(200);
   add(L,p.__tag,await p.evaluate(scan,BADS));}
 }
 for(const e of errs)(issues[L+' PAGEERROR '+e]=issues[L+' PAGEERROR '+e]||[]).push('');await c.close();}
for(const k in issues)console.log(k,'×',issues[k].length,issues[k].slice(0,3).join(' '));console.log('done');
await b.close()})();
