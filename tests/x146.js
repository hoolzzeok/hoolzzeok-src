const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
for(const [L,q] of [['ko','영월'],['ko','부산'],['en','Seoul'],['ja','Gyeongju'],['zh-tw','Busan']]){
const c=await b.newContext({viewport:{width:390,height:844},hasTouch:true,isMobile:true});const p=await c.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await c.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));
await p.goto('file:///home/claude/www.hoolzzeok.com/index.html?lang='+L);await p.waitForTimeout(900);await p.click('#ui-junior').catch(()=>{});await p.waitForTimeout(300);
await p.fill('#dest','');await p.type('#dest',q,{delay:20});await p.waitForTimeout(200);await p.tap('#dest-list li:visible >> nth=0');await p.waitForTimeout(500);
const t=await p.$('#dest-info details.t-extra');
if(!t){console.log(L,q,'no extra tile','errs',errs);await c.close();continue}
await t.evaluate(e=>e.open=true);await p.waitForTimeout(200);
console.log(L,q,'|',(await t.innerText()).replace(/\n+/g,' / ').slice(0,420),'| errs',errs.length);

await c.close()}
await b.close()})();
