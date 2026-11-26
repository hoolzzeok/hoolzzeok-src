const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
for (const w of [393,700]){const c=await b.newContext({viewport:{width:w,height:900},locale:'ko-KR'});const p=await c.newPage();
await c.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));
await p.goto('file:///home/claude/www.hoolzzeok.com/index.html');await p.waitForTimeout(900);await p.click('#ui-junior');await p.waitForTimeout(400);
const f=()=>[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.right>innerWidth+1&&getComputedStyle(e).visibility!=='hidden'}).slice(0,6).map(e=>{const r=e.getBoundingClientRect();let a=e,ov=null;while(a=a.parentElement){const s=getComputedStyle(a);if(/auto|scroll|hidden|clip/.test(s.overflowX)){ov=(a.id||a.className).toString().slice(0,30);break}}return {t:e.tagName,id:e.id,c:(e.className.baseVal??e.className).slice(0,40),l:Math.round(r.left),r:Math.round(r.right),txt:(e.textContent||'').trim().slice(0,20),clip:ov}});
console.log(w,'직접',JSON.stringify(await p.evaluate(f)));
await p.click('#calc-go');await p.waitForTimeout(1800);
console.log(w,'결과',JSON.stringify(await p.evaluate(f)));await c.close()}
await b.close()})();
