const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
for(const m of ['senior','junior']){const c=await b.newContext({viewport:{width:390,height:844},locale:'ko-KR',deviceScaleFactor:1});await c.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));const p=await c.newPage();
await p.goto('file:///home/claude/www.hoolzzeok.com/index.html');await p.waitForTimeout(1000);
await p.click('#ui-'+m).catch(()=>{});await p.waitForTimeout(600);
await p.screenshot({path:`shots/home_${m}.png`,fullPage:false});
await p.screenshot({path:`shots/homefull_${m}.png`,fullPage:true});await c.close();}
await b.close()})();
