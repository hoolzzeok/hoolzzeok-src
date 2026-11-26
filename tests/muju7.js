const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const c=await b.newContext({viewport:{width:390,height:844},locale:'ko-KR',hasTouch:true,isMobile:true});const p=await c.newPage();
await c.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));
await p.goto('file:///home/claude/hoolzzeok_site/index.html');await p.waitForTimeout(1000);await p.click('#ui-junior');await p.waitForTimeout(400);
for(const q of ['무주군','무주 ','전북 무주','무주구천동','덕유산','무주리조트','양산시','부산광역시']){
 await p.fill('#dest','');await p.type('#dest',q,{delay:20});await p.waitForTimeout(250);
 const L=await p.$$eval('#dest-list li',a=>a.filter(x=>x.offsetParent).map(x=>x.textContent.trim().slice(0,8)));
 await p.tap('#people-row, h1, body').catch(()=>{});await p.evaluate(()=>document.activeElement.blur());await p.waitForTimeout(300);
 console.log(JSON.stringify(q),'list',L,'→ 남은 값',await p.inputValue('#dest'),'| strip',await p.$eval('#ts-t',e=>e.textContent));}
await b.close()})();
