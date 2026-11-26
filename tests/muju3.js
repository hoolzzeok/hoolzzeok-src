const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const c=await b.newContext({viewport:{width:390,height:844},locale:'ko-KR',colorScheme:'dark',hasTouch:true,isMobile:true});const p=await c.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await c.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));
await p.goto('file:///home/claude/hoolzzeok_site/index.html');await p.waitForTimeout(1000);
await p.click('#ui-junior');await p.waitForTimeout(500);
const list=id=>p.$$eval('#'+id+'-list li',a=>a.filter(x=>x.offsetParent).map(x=>x.textContent.trim().slice(0,14)));
for(const q of ['무','무주','무주군','양산','양']){await p.fill('#dest','');await p.type('#dest',q,{delay:30});await p.waitForTimeout(250);console.log('dest q',q,'→',JSON.stringify(await list('dest')));}
// a) 무주 입력 후 Enter
await p.fill('#dest','');await p.type('#dest','무주',{delay:30});await p.keyboard.press('Enter');await p.waitForTimeout(400);
console.log('after Enter dest=',await p.inputValue('#dest'), 'stage', await p.evaluate(()=>document.getElementById('junior').dataset.stage));
await p.screenshot({path:'shots/muju2.jpg',type:'jpeg',quality:60});
console.log('errs',errs);await b.close()})();
