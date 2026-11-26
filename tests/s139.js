const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const errs=[];
for(const [lg,loc,q,idx] of [['en','en-US','5.history+food.standard.busan.icn.20261126',[0,1,3]],['ja','ja-JP','4.nature.standard..cju.20261127',[1]],['zt','zh-TW','5.food.standard.gangneung.icn.20261129',[3]]]){
 const c=await b.newContext({viewport:{width:390,height:900},locale:loc,deviceScaleFactor:1.5});const p=await c.newPage();p.on('pageerror',e=>errs.push(lg+':'+e.message));
 await c.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));
 await p.goto('file:///home/claude/hoolzzeok_site/index.html?lang='+(lg==='zt'?'zh-tw':lg)+'&qt='+encodeURIComponent(q));await p.waitForTimeout(1200);
 console.log('==',lg,q,'\n'+await p.evaluate(()=>[...document.querySelectorAll('#qt .qt-day')].map(s=>s.querySelector('h3').innerText+' || '+[...s.querySelectorAll('.qt-wx,.qt-hol,.qt-crowd')].map(x=>x.innerText).join(' | ')).join('\n')));
 for(const i of idx) await p.locator('#qt .qt-day').nth(i).screenshot({path:`shots/v139_${lg}_${i}.jpg`,quality:75,type:'jpeg'});
 await c.close();}
console.log('errs',errs);await b.close()})();
