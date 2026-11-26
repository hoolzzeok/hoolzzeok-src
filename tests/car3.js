const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
for(const L of ['en','ja','zh','zh-tw']){const c=await b.newContext({viewport:{width:360,height:780},hasTouch:true,isMobile:true});const p=await c.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await c.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));
await p.goto('file:///home/claude/www.hoolzzeok.com/index.html?lang='+L);await p.waitForTimeout(1000);await p.click('#ui-junior').catch(()=>{});await p.waitForTimeout(300);
await p.$eval('#mode-car',e=>e.scrollIntoView({block:'center'}));await p.tap('#mode-car');await p.waitForTimeout(300);await p.tap('#ev-seg [data-ev="light"]');await p.waitForTimeout(300);
const ov=await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth);
console.log(L,'| chips',await p.$$eval('#ev-seg button',a=>a.map(x=>x.textContent).join('/')),'| hint',(await p.$eval('#mode-hint',e=>e.textContent)).slice(0,70),'| overflow',ov,'| errs',errs.length);
await p.fill('#dest','');await p.type('#dest','Muju',{delay:20});await p.tap('#dest-list li:visible >> nth=0').catch(()=>{});await p.waitForTimeout(300);
await p.tap('.qk-b[data-qk="2"]').catch(e=>console.log('qk?',e.message.slice(0,40)));await p.waitForTimeout(300);console.log('  note:',await p.$eval('#qk-note p',e=>e.textContent).catch(()=>'none'));
if(L==='en'){await p.$eval('#ev-seg',e=>e.scrollIntoView({block:'center'}));await p.screenshot({path:'shots/car_en.jpg',type:'jpeg',quality:60})}
await c.close()}
await b.close()})();
