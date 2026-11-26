const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const c=await b.newContext({viewport:{width:390,height:844},locale:'ko-KR',hasTouch:true,isMobile:true});const p=await c.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await c.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));
await p.goto('file:///home/claude/hoolzzeok_site/index.html?from=yangsan&to=busan&nights=0&people=1');await p.waitForTimeout(1200);
console.log('url 들어옴',await p.evaluate(()=>location.search),await p.inputValue('#dest').catch(()=>'?'));
const vis=await p.isVisible('#dest');console.log('dest visible',vis);if(!vis){await p.tap('#ts-edit');await p.waitForTimeout(500)}
await p.fill('#dest','');await p.type('#dest','덕유',{delay:20});await p.evaluate(()=>document.activeElement.blur());await p.waitForTimeout(400);
console.log('덕유 →',await p.inputValue('#dest'),'| toast:',await p.$eval('#toast',e=>e.hidden?'(없음)':e.textContent));
await p.fill('#dest','');await p.type('#dest','무주군',{delay:20});await p.evaluate(()=>document.activeElement.blur());await p.waitForTimeout(300);
console.log('무주군 →',await p.inputValue('#dest'),'| url',await p.evaluate(()=>location.search));
await p.reload();await p.waitForTimeout(1200);console.log('새로고침 뒤 dest',await p.inputValue('#dest'));
for(const L of ['en','ja','zh']){await p.evaluate(l=>{localStorage.setItem('hz-lang',l)},L);}
console.log('errs',errs);await b.close()})();
