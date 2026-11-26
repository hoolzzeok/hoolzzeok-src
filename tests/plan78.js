const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const c=await b.newContext({viewport:{width:390,height:844},hasTouch:true,isMobile:true,locale:'ko-KR'});const p=await c.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await c.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));
await p.goto('file:///home/claude/www.hoolzzeok.com/index.html');await p.waitForTimeout(1000);await p.click('#ui-junior');await p.waitForTimeout(300);
for(const q of ['영월','하동','단양','담양','청송','인제','신안','가평']){
 await p.fill('#dest','');await p.type('#dest',q,{delay:20});await p.waitForTimeout(200);await p.tap('#dest-list li:visible >> nth=0');await p.waitForTimeout(300);
 await p.tap('.qk-b[data-qk="2"]');await p.waitForTimeout(500);
 const d1=await p.$$eval('#rt-list li.rt-blk.k-u b',a=>a.map(x=>x.textContent));
 let d2=[];if(await p.$('.rt-days [data-day="1"]')){await p.tap('.rt-days [data-day="1"]');await p.waitForTimeout(200);d2=await p.$$eval('#rt-list li.rt-blk.k-u b',a=>a.map(x=>x.textContent));}
 console.log(q,'| 1일째',d1.join('→')||'-','| 2일째',d2.join('→')||'-');
 await p.tap('#rt-close');await p.waitForTimeout(200);}
console.log('errs',errs);await b.close()})();
