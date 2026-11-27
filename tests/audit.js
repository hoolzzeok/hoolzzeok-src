const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
const c=await b.newContext({viewport:{width:390,height:844},locale:'ko-KR',deviceScaleFactor:1});await c.route(/fonts\.|unpkg|jsdelivr|supabase/,r=>r.fulfill({body:''}));
const p=await c.newPage();
await p.goto('file:///home/claude/www.hoolzzeok.com/index.html?from=seoul&to=yeosu&nights=1&people=2');await p.waitForTimeout(1300);
await p.click('#ui-junior').catch(()=>{});if(await p.isVisible('#calc-go'))await p.click('#calc-go');await p.waitForTimeout(1500);
// 모든 details 펼치기
await p.evaluate(()=>document.querySelectorAll('#junior details, #dest-info details').forEach(d=>d.open=true));await p.waitForTimeout(500);
const H=await p.evaluate(()=>document.documentElement.scrollHeight);console.log('height',H);
for(let y=0,i=0;y<H && i<12;y+=1600,i++){await p.screenshot({path:`shots/au_${i}.png`,clip:{x:0,y,width:390,height:Math.min(1600,H-y)},fullPage:true});}
console.log(await p.evaluate(()=>[...document.querySelectorAll('#junior details>summary, #dest-info details>summary')].map(s=>s.innerText.replace(/\s+/g,' ').slice(0,40)).join(' | ')));
await b.close()})();
