const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const c=await b.newContext({viewport:{width:393,height:852},locale:'ko-KR',hasTouch:true,isMobile:true});const p=await c.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await c.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));
await p.goto('file:///home/claude/www.hoolzzeok.com/index.html');await p.waitForTimeout(900);await p.click('#ui-junior');await p.waitForTimeout(300);
await p.click('#calc-go');await p.waitForTimeout(2000);
const st=async l=>console.log(l,await p.evaluate(()=>({w:innerWidth,sw:document.documentElement.scrollWidth>innerWidth,cols:getComputedStyle(document.querySelector('.planner')).gridTemplateColumns,stage:document.getElementById('junior').dataset.stage,dig:getComputedStyle(document.getElementById('dig-open')).display})));
await st('접힘 393');
for(const [w,h] of [[884,1104],[984,1092],[1092,984],[393,852],[1180,820],[700,840]]){await p.setViewportSize({width:w,height:h});await p.waitForTimeout(400);await st('→'+w+'x'+h)}
await p.setViewportSize({width:884,height:1104});await p.waitForTimeout(300);await p.screenshot({path:'shots/f2_884.jpg',type:'jpeg',quality:45});
// 접은 자세 흉내: 세로 접힘선 가운데
const cdp=await c.newCDPSession(p);
try{await cdp.send('Emulation.setDisplayFeaturesOverride',{displayFeatures:[{orientation:'vertical',offset:442,maskLength:20}]});await p.waitForTimeout(500);
 console.log('segments', await p.evaluate(()=>matchMedia('(horizontal-viewport-segments: 2)').matches), await p.evaluate(()=>getComputedStyle(document.querySelector('.planner')).gridTemplateColumns+' gap '+getComputedStyle(document.querySelector('.planner')).columnGap));
 await p.screenshot({path:'shots/f2_seg.jpg',type:'jpeg',quality:45});}catch(e){console.log('cdp',e.message.slice(0,120))}
console.log('errs',errs);await b.close()})();
