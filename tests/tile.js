const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
for (const w of [390,430]){const c=await b.newContext({viewport:{width:w,height:844},locale:'ko-KR',deviceScaleFactor:2,isMobile:true,hasTouch:true});await c.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));const p=await c.newPage();
await p.goto('file:///home/claude/www.hoolzzeok.com/index.html?from=seoul&to=goheung&nights=1&people=2');await p.waitForTimeout(1300);
await p.click('#ui-junior').catch(()=>{});if(await p.isVisible('#calc-go'))await p.click('#calc-go');await p.waitForTimeout(1200);
const info=await p.evaluate(()=>{const t=document.querySelector('#dest-info .tiles>details');t.scrollIntoView({block:'center'});const r=t.getBoundingClientRect();const out=[];let e=t.parentElement;while(e&&e!==document.body){const s=getComputedStyle(e);const q=e.getBoundingClientRect();if(s.overflow!=='visible'||s.overflowX!=='visible'||s.overflowY!=='visible'||s.clipPath!=='none'||s.contain!=='none')out.push({el:(e.id||e.className).toString().slice(0,40),ov:s.overflow,clip:s.clipPath.slice(0,40),top:Math.round(q.top),pt:s.paddingTop});e=e.parentElement;}
 return {tileTop:Math.round(r.top),ancestors:out, tf:getComputedStyle(t).transform, mt:getComputedStyle(t).marginTop}});
console.log(w,JSON.stringify(info));
const t=await p.$('#dest-info .tiles');const bb=await t.boundingBox();await p.screenshot({path:`shots/tile_${w}.png`,clip:{x:0,y:bb.y-40,width:w,height:300}});
await c.close();}
await b.close()})();
