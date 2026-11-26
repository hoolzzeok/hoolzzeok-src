const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const c=await b.newContext({viewport:{width:390,height:844},locale:'ko-KR',colorScheme:'dark',hasTouch:true,isMobile:true});const p=await c.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await c.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));
await p.goto('file:///home/claude/hoolzzeok_site/index.html');await p.waitForTimeout(1000);
await p.click('#ui-junior');await p.waitForTimeout(600);
const vis=()=>p.evaluate(()=>[...document.querySelectorAll('input,button')].filter(e=>e.offsetParent&&e.getBoundingClientRect().top<900).slice(0,25).map(e=>(e.id||e.className)+':'+(e.value||e.textContent||'').trim().slice(0,20)));
console.log(await vis());
await p.screenshot({path:'shots/muju1.jpg',type:'jpeg',quality:60});
console.log('errs',errs);await b.close()})();
