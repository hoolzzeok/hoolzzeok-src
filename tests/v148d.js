const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const errs=[];
for (const [lg,q] of [['en','yeongwol'],['ja','damyang'],['zh','muju'],['en','gapyeong']]){
const c=await b.newContext({viewport:{width:390,height:844},locale:'en-US'});await c.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));const p=await c.newPage();p.on('pageerror',e=>errs.push(e.message));
await p.goto(`file:///home/claude/www.hoolzzeok.com/index.html?lang=${lg}&to=${q}`);await p.waitForTimeout(1500);
const sp=await p.$$eval('#dest-info .spot-list li b, #dest-info .spot-list li strong',a=>a.map(x=>x.textContent.trim()).slice(0,5));
console.log(lg,q,sp.join(' | '));await c.close();}
console.log('errs',errs);await b.close()})();
