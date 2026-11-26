const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const c=await b.newContext({viewport:{width:390,height:844},locale:'ko-KR',colorScheme:'dark',hasTouch:true,isMobile:true});const p=await c.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await c.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));
await p.goto('file:///home/claude/www.hoolzzeok.com/index.html');await p.waitForTimeout(1000);await p.click('#ui-junior');await p.waitForTimeout(400);
const pick=async(id,q)=>{await p.fill('#'+id,'');await p.type('#'+id,q,{delay:30});await p.waitForTimeout(250);await p.tap('#'+id+'-list li:visible >> nth=0');await p.waitForTimeout(300)};
await pick('origin','양산');await pick('dest','무주');
// car kinds
await p.$eval('#mode-car',e=>e.scrollIntoView({block:'center'}));await p.tap('#mode-car');await p.waitForTimeout(400);
const val=async()=>p.$eval('#calc-go',e=>e.textContent.replace(/\s+/g,' ').trim());
for(const k of ['avg','light','suv','hev','ev']){await p.tap(`#ev-seg [data-ev="${k}"]`);await p.waitForTimeout(300);console.log(k,'|',await val(),'|',(await p.$eval('#mode-hint',e=>e.textContent)).slice(0,90))}
await p.tap('#ev-seg [data-ev="my"]');await p.waitForTimeout(300);console.log('my box',await p.isVisible('#car-my'));await p.fill('#car-my','20');await p.waitForTimeout(300);console.log('my 20 |',await val(),'|',(await p.$eval('#mode-hint',e=>e.textContent)).slice(0,60));
await p.$eval('#ev-seg',e=>e.scrollIntoView({block:'center'}));await p.screenshot({path:'shots/carseg.jpg',type:'jpeg',quality:60});
await p.reload();await p.waitForTimeout(1000);console.log('reload kind kept:',await p.evaluate(()=>localStorage.getItem('hz-car')));
console.log('errs',errs);await b.close()})();
