const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const errs=[];
for (const [lg,w] of [['ko',390],['en',390],['ko',884]]){
const c=await b.newContext({viewport:{width:w,height:900},locale:'ko-KR',deviceScaleFactor:2});await c.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));const p=await c.newPage();p.on('pageerror',e=>errs.push(e.message));
await p.goto(`file:///home/claude/www.hoolzzeok.com/index.html?lang=${lg}`);await p.waitForTimeout(1200);
if(lg==='ko'){await p.click('#ui-junior').catch(()=>{});await p.waitForTimeout(300);}
const sat=await p.$$eval('#sat-seg button:not([hidden])',a=>a.map(x=>x.innerText.replace(/\n/g,' / ')));
console.log(lg,w,'sat:',sat.join(' | '));
console.log('  qk:',await p.$$eval('#qk .qk-g',a=>a.map(g=>g.innerText.replace(/\n+/g,' · ')).join(' || ')));
console.log('  picks open:',await p.$eval('#picks-fold',e=>e.open));
const el=await p.$('#sat-field');await el.scrollIntoViewIfNeeded();
const box=await p.evaluate(()=>{const a=document.getElementById('sat-field').getBoundingClientRect(), r=document.getElementById('recs').getBoundingClientRect();return {y:a.top+scrollY, h:r.bottom-a.top}});
await p.screenshot({path:`shots/qk148_${lg}_${w}.png`,clip:{x:0,y:box.y-10,width:w,height:Math.min(1100,box.h+20)},fullPage:true});
await c.close();}
console.log('errs',errs);await b.close()})();
