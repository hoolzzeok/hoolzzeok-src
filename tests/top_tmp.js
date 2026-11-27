const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const c=await b.newContext({viewport:{width:390,height:844},locale:'ko-KR',deviceScaleFactor:2});await c.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));const p=await c.newPage();
await p.goto('file:///home/claude/www.hoolzzeok.com/index.html');await p.waitForTimeout(900);await p.click('#ui-senior').catch(()=>{});await p.waitForTimeout(500);
await p.screenshot({path:'shots/top_sr.png'});
const btn=await p.$$('#sr-body .sr-btn');await btn[0].click();await p.waitForTimeout(400);await p.screenshot({path:'shots/top_sr2.png'});
await b.close()})();
