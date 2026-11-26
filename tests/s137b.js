const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
for(const [lg,loc,q] of [['ja','ja-JP','5.history+food.standard.jeonju.icn.20261207'],['zh','zh-CN','4.nature.standard..cju.20261207']]){
 const c=await b.newContext({viewport:{width:390,height:900},locale:loc,deviceScaleFactor:1.5});const p=await c.newPage();
 await c.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));
 await p.goto('file:///home/claude/hoolzzeok_site/index.html?lang='+lg+'&qt='+encodeURIComponent(q));await p.waitForTimeout(1200);
 const d=p.locator('#qt .qt-day').nth(lg==='ja'?3:1);await d.screenshot({path:'shots/v137_'+lg+'_day.jpg',quality:75,type:'jpeg'});await c.close();}
await b.close()})();
