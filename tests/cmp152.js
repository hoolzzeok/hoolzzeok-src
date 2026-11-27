const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const errs=[];
const c=await b.newContext({viewport:{width:390,height:844},locale:'ko-KR',deviceScaleFactor:2});await c.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));
const p=await c.newPage();p.on('pageerror',e=>errs.push(e.message));
await p.goto('file:///home/claude/www.hoolzzeok.com/index.html?from=seoul&to=yeosu&nights=1&people=2');await p.waitForTimeout(1200);
await p.click('#ui-junior').catch(()=>{});await p.waitForTimeout(300);if(await p.isVisible('#calc-go'))await p.click('#calc-go');await p.waitForTimeout(1500);
const rd=async()=>p.$eval('#cmp-box',e=>e.innerText.replace(/\s+/g,' ').slice(0,400));
console.log('직접:',await rd());
const chips=await p.$$('#cmp-box .cmp-chip');if(chips[1]){await chips[1].click();await p.waitForTimeout(400);console.log('칩2:',(await rd()).slice(0,200));}
await p.fill('#cmp-box .cmp-in','강릉');await p.dispatchEvent('#cmp-box .cmp-in','change');await p.waitForTimeout(400);console.log('입력 강릉:',(await rd()).slice(0,220));
const y=await p.evaluate(()=>{const e=document.querySelector('#cmp-box');e.scrollIntoView();return e.getBoundingClientRect().top+scrollY});
await p.screenshot({path:'shots/cmp152.png',clip:{x:0,y:y-10,width:390,height:620},fullPage:true});
await p.click('#cmp-box .cmp-go');await p.waitForTimeout(800);console.log('바꾼 뒤 도착:',await p.$eval('#t-route',e=>e.textContent));
for(const lg of ['en','ja']){const q=await c.newPage();q.on('pageerror',e=>errs.push(e.message));await q.goto(`file:///home/claude/www.hoolzzeok.com/index.html?lang=${lg}&from=seoul&to=busan&nights=1&people=2`);await q.waitForTimeout(1200);await q.click('#ui-junior').catch(()=>{});if(await q.isVisible('#calc-go'))await q.click('#calc-go');await q.waitForTimeout(1200);console.log(lg,(await q.$eval('#cmp-box',e=>e.innerText.replace(/\s+/g,' '))).slice(0,160));}
console.log('errs',errs);await b.close()})();
