const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const errs=[];
const c=await b.newContext({viewport:{width:390,height:844},locale:'ko-KR',deviceScaleFactor:2,isMobile:true,hasTouch:true});await c.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));const p=await c.newPage();p.on('pageerror',e=>errs.push(e.message));
// 아이폰 상단 여백 흉내: 머리줄을 50px 아래로
await p.addInitScript(()=>{document.addEventListener('DOMContentLoaded',()=>{const st=document.createElement('style');st.textContent='header.top{top:50px !important}';document.head.appendChild(st);});});
await p.goto('file:///home/claude/www.hoolzzeok.com/index.html?from=seoul&to=goheung&nights=1&people=2');await p.waitForTimeout(1300);
await p.click('#ui-junior').catch(()=>{});if(await p.isVisible('#calc-go'))await p.click('#calc-go');await p.waitForTimeout(1200);
for(const i of [1,0,3]){
 await p.evaluate(i=>{const t=document.querySelectorAll('#dest-info .tiles>details')[i];const y=t.getBoundingClientRect().top+scrollY-95;scrollTo(0,y);},i);await p.waitForTimeout(300);
 await p.tap(`#dest-info .tiles>details:nth-of-type(${i+1})>summary`);await p.waitForTimeout(900);
 const r=await p.evaluate(i=>{const t=document.querySelectorAll('#dest-info .tiles>details')[i];return {tile:Math.round(t.getBoundingClientRect().top),hdr:Math.round(document.querySelector('header.top').getBoundingClientRect().bottom),open:t.open}},i);
 console.log('tile',i,JSON.stringify(r), r.tile>=r.hdr?'OK':'잘림');}
console.log('errs',errs);await b.close()})();
