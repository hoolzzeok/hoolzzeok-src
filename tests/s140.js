const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const errs=[];
for(const [lg,loc,q] of [['en','en-US','5.history.standard.jeonju.icn.20261202'],['ja','ja-JP','5.food.standard.busan.icn.20261202'],['zt','zh-TW','4.history.standard.gyeongju.pus.20261202']]){
 const c=await b.newContext({viewport:{width:390,height:900},locale:loc,deviceScaleFactor:1.5});const p=await c.newPage();p.on('pageerror',e=>errs.push(lg+':'+e.message));
 await c.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));
 await p.goto('file:///home/claude/hoolzzeok_site/index.html?lang='+(lg==='zt'?'zh-tw':lg)+'&qt='+encodeURIComponent(q));await p.waitForTimeout(1200);
 console.log('==',lg,q,'\n'+await p.evaluate(()=>[...document.querySelectorAll('#qt .qt-ktx')].map(x=>x.innerText).join('\n')));
 const n=await p.locator('#qt .qt-day').count(); const i=await p.evaluate(()=>[...document.querySelectorAll('#qt .qt-day')].findIndex(s=>s.querySelector('.qt-ktx')));
 await p.locator('#qt .qt-day').nth(i).screenshot({path:`shots/v140_${lg}.jpg`,quality:75,type:'jpeg'});
 await c.close();}
console.log('errs',errs);await b.close()})();
