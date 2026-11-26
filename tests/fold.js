const {chromium}=require('playwright');
const VW=[[320,640,'tiny'],[360,780,'s'],[393,852,'phone'],[430,932,'max'],[540,720,'flip-l'],[600,960,'fold-cover-l?'],[700,840,'duo-open'],[768,1024,'tablet'],[884,1104,'fold-open'],[984,1092,'fold7-open'],[1092,984,'fold7-land'],[1180,820,'tri-land'],[1366,1024,'tri-big'],[1440,900,'desk']];
(async()=>{const b=await chromium.launch();const out=[];
for(const [w,h,n] of VW){const c=await b.newContext({viewport:{width:w,height:h},locale:'ko-KR',hasTouch:w<1100,isMobile:w<1100});const p=await c.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await c.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));
await p.goto('file:///home/claude/www.hoolzzeok.com/index.html');await p.waitForTimeout(900);
const ov=async()=>p.evaluate(()=>{const W=document.documentElement.clientWidth;const bad=[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.right>W+1&&getComputedStyle(e).position!=='fixed'}).slice(0,3).map(e=>(e.id||e.className||e.tagName).toString().slice(0,30));return {sw:document.documentElement.scrollWidth>W,bad}});
const o0=await ov();await p.screenshot({path:`shots/f_${w}_0.jpg`,type:'jpeg',quality:45});
await p.click('#ui-junior');await p.waitForTimeout(400);const o1=await ov();await p.screenshot({path:`shots/f_${w}_1.jpg`,type:'jpeg',quality:45});
await p.click('#calc-go');await p.waitForTimeout(2200);const o2=await ov();await p.screenshot({path:`shots/f_${w}_2.jpg`,type:'jpeg',quality:45,fullPage:true});
const h2=await p.evaluate(()=>document.documentElement.scrollHeight);
out.push(`${n} ${w}x${h}: 쉽게 ${JSON.stringify(o0)} 직접 ${JSON.stringify(o1)} 결과 ${JSON.stringify(o2)} 결과높이 ${h2} errs ${errs.length}`);await c.close()}
console.log(out.join('\n'));await b.close()})();
