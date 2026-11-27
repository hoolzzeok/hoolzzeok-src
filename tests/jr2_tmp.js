const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
const c=await b.newContext({viewport:{width:390,height:844},locale:'ko-KR',deviceScaleFactor:1,colorScheme:'dark'});await c.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));const p=await c.newPage();
await p.goto('file:///home/claude/www.hoolzzeok.com/index.html?from=seoul&to=gangneung&nights=1&people=2');await p.waitForTimeout(1300);
await p.click('#ui-junior').catch(()=>{});if(await p.isVisible('#calc-go'))await p.click('#calc-go');await p.waitForTimeout(1200);
const y0=await p.evaluate(()=>document.querySelector('#dest-info .tiles').getBoundingClientRect().top+scrollY-20);
await p.screenshot({path:'shots/jr_dark.png',clip:{x:0,y:y0,width:390,height:600},fullPage:true});
await b.close()})();
