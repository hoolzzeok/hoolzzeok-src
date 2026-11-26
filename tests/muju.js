const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const c=await b.newContext({viewport:{width:390,height:844},locale:'ko-KR',colorScheme:'dark',hasTouch:true,isMobile:true});const p=await c.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await c.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));
await p.goto('file:///home/claude/hoolzzeok_site/index.html');await p.waitForTimeout(1000);
// 직접 모드
const modes=await p.$$eval('button',bs=>bs.filter(b=>/직접|쉽게/.test(b.textContent)&&b.offsetParent).map(b=>b.id+':'+b.textContent.trim()));console.log('mode btns',modes);
const st=()=>p.evaluate(()=>({stage:document.getElementById('junior').dataset.stage,o:document.getElementById('origin').value,d:document.getElementById('dest').value,oVis:!!document.getElementById('origin').offsetParent,dVis:!!document.getElementById('dest').offsetParent,sum:(document.querySelector('#planner h3, .sum-line, .cond')||{}).textContent}));
console.log('init',await st());
await p.screenshot({path:'shots/muju0.jpg',type:'jpeg',quality:60});
await b.close()})();
