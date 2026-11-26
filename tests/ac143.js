const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
for(const [L,q,bad,url] of [['en','Muju-gun','zzzz',''],['ja','무주군','xyzq',''],['zh','무주군','xyzq',''],['zh','무주군','xyzq','tw']]){
const c=await b.newContext({viewport:{width:390,height:844},locale:L==='zh'?(url?'zh-TW':'zh-CN'):L,hasTouch:true,isMobile:true});const p=await c.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await c.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));
await p.goto('file:///home/claude/www.hoolzzeok.com/index.html?lang='+(url?'zh-tw':L));await p.waitForTimeout(1200);
if(!await p.isVisible('#dest')){await p.click('#ui-junior').catch(()=>{});await p.waitForTimeout(400)}
if(!await p.isVisible('#dest')){console.log(L,'dest not visible');await c.close();continue}
await p.fill('#dest','');await p.type('#dest',q,{delay:20});await p.evaluate(()=>document.activeElement.blur());await p.waitForTimeout(300);const v1=await p.inputValue('#dest');
await p.fill('#dest','');await p.type('#dest',bad,{delay:20});await p.evaluate(()=>document.activeElement.blur());await p.waitForTimeout(400);
console.log(L+(url?'-TW':''),'|',q,'→',v1,'| toast:',await p.$eval('#toast',e=>e.textContent),'| errs',errs.length);await c.close()}
await b.close()})();
