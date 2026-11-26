const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
for(const [lg,loc,q] of [['ja','ja-JP','5.history+nature.standard.jeonju.icn.20261207'],['zh','zh-CN','4.nature.standard..cju.20261207'],['zt','zh-TW','5.food.standard.gangneung.icn.20261207']]){
 const c=await b.newContext({viewport:{width:390,height:1400},locale:loc,deviceScaleFactor:1.5});const p=await c.newPage();
 await c.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));
 await p.goto('file:///home/claude/hoolzzeok_site/index.html?lang='+lg+'&qt='+encodeURIComponent(q));await p.waitForTimeout(1200);
 const t=await p.evaluate(()=>document.getElementById('qt').innerText);require("fs").writeFileSync("/tmp/qt_"+lg+".txt",t);
 await p.locator('#qt').screenshot({path:'shots/v137_'+lg+'.jpg',quality:70,type:'jpeg'});await c.close();}
await b.close()})();
