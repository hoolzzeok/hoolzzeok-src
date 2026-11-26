const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const c=await b.newContext({viewport:{width:390,height:844},locale:'ko-KR',hasTouch:true,isMobile:true});const p=await c.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await c.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));
await p.goto('file:///home/claude/www.hoolzzeok.com/index.html');await p.waitForTimeout(1000);await p.click('#ui-junior');await p.waitForTimeout(300);
for(const q of ['영월','담양']){await p.fill('#dest','');await p.type('#dest',q,{delay:20});await p.waitForTimeout(200);await p.tap('#dest-list li:visible >> nth=0');await p.waitForTimeout(500);
 const sp=await p.$$eval('#dest-info .spot-list li',a=>a.map(x=>x.innerText.replace(/\s+/g,' ').slice(0,120)));console.log(q,sp.length);sp.forEach(x=>console.log('  ',x));
 console.log('  imgs',await p.$$eval('#dest-info .spot-list img',a=>a.map(x=>x.getAttribute('src'))));}
await p.tap('.qk-b[data-qk="2"]');await p.waitForTimeout(600);console.log('rt',await p.$$eval('#rt-list li',a=>a.map(x=>x.textContent.replace(/\s+/g,' ').trim().slice(0,30)).join(' | ')));
await p.tap('#rt-close');await p.$eval('#dest-info',e=>e.scrollIntoView());await p.screenshot({path:'shots/h78.jpg',type:'jpeg',quality:60,fullPage:false});
console.log('errs',errs);await b.close()})();
