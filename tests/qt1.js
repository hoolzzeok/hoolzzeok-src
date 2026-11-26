const {chromium}=require('playwright');
const FILE='file:///home/claude/hoolzzeok_site/index.html';
(async()=>{const b=await chromium.launch();
for(const [L,loc] of [['en','en-US'],['ja','ja-JP'],['zh','zh-CN'],['ko','ko-KR']]){
 const c=await b.newContext({viewport:{width:390,height:844},locale:loc});const p=await c.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await c.route(/fonts\.|cdn\.jsdelivr|unpkg/,r=>r.fulfill({body:''}));
 await p.goto(FILE);await p.waitForTimeout(800);
 const vis=await p.$eval('#qt-go',e=>!e.hidden);console.log('==',L,'cta visible',vis, vis?await p.$eval('#qt-go',e=>e.innerText.replace(/\n/g,' | ')):'', '| h1', await p.$eval('#top h1',e=>e.textContent));
 if(!vis){console.log(' errs',errs);await c.close();continue;}
 await p.screenshot({path:`qt/${L}_home.png`});
 await p.click('#qt-go');await p.waitForTimeout(200);await p.screenshot({path:`qt/${L}_q1.png`});
 await p.click('.qt-opt[data-v="5"]');await p.waitForTimeout(150);await p.screenshot({path:`qt/${L}_q2.png`});
 await p.click('.qt-opt[data-v="food"]');await p.waitForTimeout(150);await p.click('#qt-next');await p.waitForTimeout(150);
 await p.click('.qt-opt[data-v="standard"]');await p.waitForTimeout(300);
 await p.screenshot({path:`qt/${L}_res.png`});
 console.log(' title',await p.$eval('#qt-title',e=>e.textContent),'| total',await p.$eval('.qt-sum>b',e=>e.textContent),'| days',await p.$$eval('.qt-day h3',a=>a.map(x=>x.innerText.replace(/\n/g,' ')).join(' / ')));
 console.log(' url',p.url().split('?')[1]);
 const leaks=await p.evaluate(()=>{const out=[];const w=document.createTreeWalker(document.getElementById('qt'),NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){if(/NaN|undefined|null/.test(n.nodeValue))out.push(n.nodeValue.slice(0,60));}return out;});console.log(' bad',leaks);
 await p.click('.qt-chip[data-qt-city="gyeongju"]');await p.waitForTimeout(200);console.log(' swap',await p.$eval('#qt-title',e=>e.textContent),await p.$eval('.qt-sum>b',e=>e.textContent));
 for(const d of [3,4,7]){await p.goto(FILE+`?qt=${d}.culture.budget`);await p.waitForTimeout(700);console.log(' qt',d,await p.$eval('#qt-title',e=>e.textContent).catch(()=>'NO'),await p.$$eval('.qt-day',a=>a.length).catch(()=>0),await p.$eval('.qt-sum>b',e=>e.textContent).catch(()=>''));}
 await p.screenshot({path:`qt/${L}_res7.png`,fullPage:true});
 await p.click('#qt-calc');await p.waitForTimeout(800);console.log(' calc ->',await p.$eval('#bar-route',e=>e.textContent).catch(()=>'?'));
 console.log(' overflow',await p.evaluate(()=>document.documentElement.scrollWidth),' errs',errs);await c.close();}
await b.close()})();
