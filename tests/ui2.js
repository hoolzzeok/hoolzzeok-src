const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
for(const [w,h,n] of [[390,844,'m'],[1280,900,'d']]){const c=await b.newContext({viewport:{width:w,height:h},locale:'ko-KR',hasTouch:w<500,isMobile:w<500,deviceScaleFactor:1});const p=await c.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await c.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));
await p.goto('file:///home/claude/www.hoolzzeok.com/index.html');await p.waitForTimeout(1000);
await p.click('#ui-junior');await p.waitForTimeout(500);await p.screenshot({path:`shots/ui2_${n}1.jpg`,type:'jpeg',quality:55,fullPage:true});
await p.click('#calc-go');await p.waitForTimeout(2500);await p.screenshot({path:`shots/ui2_${n}2.jpg`,type:'jpeg',quality:50,fullPage:false});
await p.click('#ts-edit');await p.waitForTimeout(600);console.log(n,'edit back stage',await p.$eval('#junior',e=>e.dataset.stage),'calc visible',await p.isVisible('#calc-go'),'errs',errs);
await c.close()}
await b.close()})();
