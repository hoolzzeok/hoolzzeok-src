const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const bad=[];
for(const lg of ['ko','en','ja','zh','zh-tw'])for(const w of [320,360,375,390,412,430,480]){
 const c=await b.newContext({viewport:{width:w,height:800},locale:'en-US'});await c.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));const p=await c.newPage();
 await p.goto(`file:///home/claude/www.hoolzzeok.com/index.html?lang=${lg}`);await p.waitForTimeout(700);
 // 로그인 버튼들 보이게(실제 사이트처럼)
 await p.evaluate(()=>{['rp-top','ac-open'].forEach(id=>{const e=document.getElementById(id);if(e)e.hidden=false;});const a=document.getElementById('ac-open');if(a&&!a.textContent.trim())a.textContent='マイページ';});
 await p.waitForTimeout(100);
 const r=await p.evaluate(()=>{const m=document.querySelector('.logo-mark').getBoundingClientRect(),tr=document.querySelector('.top-right').getBoundingClientRect();const kids=[...document.querySelectorAll('.top-right>*')].filter(e=>!e.hidden).map(e=>Math.round(e.getBoundingClientRect().right));return {mR:Math.round(m.right),mL:Math.round(m.left),trL:Math.round(tr.left),trR:Math.round(tr.right),maxR:Math.max(...kids),vw:innerWidth,sw:document.documentElement.scrollWidth}});
 const ok=r.trL>=r.mR+2 && r.maxR<=r.vw && r.mL>=0 && r.sw<=r.vw;
 if(!ok)bad.push(lg+' '+w+' '+JSON.stringify(r));
 if(w===390&&(lg==='ja'||lg==='en'))await p.screenshot({path:`shots/hdr_${lg}.png`,clip:{x:0,y:0,width:w,height:70}});
 await c.close();}
console.log(bad.length?bad.join('\n'):'all ok');await b.close()})();
