const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const errs=[];
const run=async(loc,url,fn)=>{const c=await b.newContext({viewport:{width:390,height:844},locale:loc,acceptDownloads:true});const p=await c.newPage();p.on('pageerror',e=>errs.push(url+' '+e.message));
 await c.route(/fonts\.|unpkg|supabase/,r=>r.fulfill({body:''}));await c.route(/xlsx\.full\.min\.js/,r=>r.fulfill({path:'/tmp/xl/node_modules/xlsx/dist/xlsx.full.min.js',contentType:'application/javascript'}));
 await p.goto('file:///home/claude/hoolzzeok_site/index.html'+url);await p.waitForTimeout(900);const r=await fn(p);await c.close();return r;};
const sum=async p=>({t:await p.$eval('#qt-title',e=>e.textContent).catch(()=>'-'),c:await p.$eval('.qt-sum>b',e=>e.textContent).catch(()=>'-'),d:await p.$$eval('.qt-day h3',a=>a.map(x=>x.innerText.replace(/\n/g,' ')).join(' / ')),ow:await p.evaluate(()=>document.getElementById('qt').scrollWidth)});
for (const u of ['?qt=6.history.standard..icn.20261130','?qt=5.nature.standard..cju.20261207','?qt=5.food.standard.busan','?qt=3.culture.budget','?qt=7.nature.standard','?qt=6.history+food.comfort','?qt=5.kpop+shop.standard','?qt=4.rest.budget..cju','?qt=5.nature.standard.jeju.pus','?qt=6.food.standard.jeonju','?qt=7.rest+nature.standard.gangneung','?qt=5.history.standard.gyeongju.icn.20261201','?qt=6.history.standard..icn.20261201'])
  console.log(u, JSON.stringify(await run('en-US',u,sum)));
// 탭 흐름
console.log(await run('ja-JP','',async p=>{await p.click('#qt-go');await p.click('[data-v="5"]');await p.click('[data-v="nature"]');await p.click('[data-v="food"]');await p.click('[data-v="standard"]');await p.waitForTimeout(300);return JSON.stringify(await sum(p))+' | '+await p.$$eval('[data-send]',a=>a.map(x=>x.innerText).join(','));}));
console.log(await run('zh-TW','?qt=5.nature.standard.jeju',async p=>{const t=await p.evaluate(()=>1);await p.click('[data-send="copy"]').catch(()=>{});return JSON.stringify(await sum(p));}));
// 엑셀
console.log(await run('en-US','?qt=5.food+history.standard.busan.icn.20261202',async p=>{const [dl]=await Promise.all([p.waitForEvent('download',{timeout:20000}),p.click('#qt-xl')]);const f='/tmp/qt.xlsx';await dl.saveAs(f);return 'xlsx '+dl.suggestedFilename();}));
console.log('errs',errs);await b.close()})();
