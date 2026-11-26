const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const c=await b.newContext({viewport:{width:884,height:1104},locale:'ko-KR'});const p=await c.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await c.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));
await p.goto('file:///home/claude/www.hoolzzeok.com/index.html');await p.waitForTimeout(900);await p.click('#ui-junior');await p.waitForTimeout(300);await p.click('#calc-go');await p.waitForTimeout(1800);
const cdp=await c.newCDPSession(p);
for (const tryit of [
 ()=>cdp.send('Emulation.setDeviceMetricsOverride',{width:884,height:1104,deviceScaleFactor:1,mobile:true,displayFeature:{orientation:'vertical',offset:432,maskLength:20}}),
]){try{await tryit();console.log('ok')}catch(e){console.log('err',e.message.slice(0,150))}}
await p.waitForTimeout(600);
console.log(await p.evaluate(()=>{const pl=document.querySelector('.planner'),s=getComputedStyle(pl);const r=[...pl.children].filter(e=>e.offsetParent).map(e=>{const q=e.getBoundingClientRect();return (e.id||e.className).toString().slice(0,15)+':'+Math.round(q.left)+'-'+Math.round(q.right)});return {seg:matchMedia('(horizontal-viewport-segments: 2)').matches,cols:s.gridTemplateColumns,gap:s.columnGap,r,sw:document.documentElement.scrollWidth,bar:getComputedStyle(document.querySelector('.bar')).left}}));
await p.screenshot({path:'shots/f2_seg.jpg',type:'jpeg',quality:45});console.log('errs',errs);await b.close()})();
