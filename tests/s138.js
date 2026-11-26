const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const errs=[];
for(const [lg,loc,q,idx] of [['en','en-US','5.history+food.standard..icn.20261222',[1,3]],['zt','zh-TW','4.food.standard..icn.20261128',[1]],['ja','ja-JP','5.nature.standard.jeonju.icn.20261201',[1]]]){
 const c=await b.newContext({viewport:{width:390,height:900},locale:loc,deviceScaleFactor:1.5});const p=await c.newPage();p.on('pageerror',e=>errs.push(lg+':'+e.message));
 await c.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));
 await p.goto('file:///home/claude/hoolzzeok_site/index.html?lang='+(lg==='zt'?'zh-tw':lg)+'&qt='+encodeURIComponent(q));await p.waitForTimeout(1200);
 const t=await p.evaluate(()=>[...document.querySelectorAll('#qt .qt-day')].map(s=>s.innerText.split('\n').slice(0,6).join(' | ')).join('\n'));console.log('==',lg,q,'\n'+t);
 console.log('HS:',await p.evaluate(()=>(document.querySelector('#qt .qt-hs')||{}).textContent));
 for(const i of idx) await p.locator('#qt .qt-day').nth(i).screenshot({path:`shots/v138_${lg}_${i}.jpg`,quality:75,type:'jpeg'});
 await c.close();}
console.log('errs',errs);await b.close()})();
