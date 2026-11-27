const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
const c=await b.newContext({viewport:{width:390,height:844},locale:'ko-KR',deviceScaleFactor:1});await c.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));const p=await c.newPage();
await p.goto('file:///home/claude/www.hoolzzeok.com/index.html?from=seoul&to=busan&nights=1&people=2');await p.waitForTimeout(1300);
await p.click('#ui-junior').catch(()=>{});if(await p.isVisible('#calc-go'))await p.click('#calc-go');await p.waitForTimeout(1200);
const y0=await p.evaluate(()=>document.querySelector('#dest-info').getBoundingClientRect().top+scrollY);
const H=await p.evaluate(()=>document.querySelector('#dest-info').getBoundingClientRect().height);console.log('H',H);
await p.screenshot({path:'shots/jr_tiles.png',clip:{x:0,y:y0,width:390,height:Math.min(H,2400)},fullPage:true});
await b.close()})();
