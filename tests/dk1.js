const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
for(const L of ['ko','en','ja','zh-tw']){const c=await b.newContext({viewport:{width:390,height:844},colorScheme:'dark',hasTouch:true,isMobile:true});const p=await c.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await c.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));
await p.goto('file:///home/claude/www.hoolzzeok.com/index.html?lang='+L);await p.waitForTimeout(1000);await p.click('#ui-junior').catch(()=>{});await p.waitForTimeout(300);
const pick=async(id,q)=>{await p.fill('#'+id,'');await p.type('#'+id,q,{delay:30});await p.waitForTimeout(250);await p.tap('#'+id+'-list li:visible >> nth=0');await p.waitForTimeout(300)};
await pick('origin',L==='ko'?'양산':'Yangsan');await pick('dest',L==='ko'?'무주':'Muju');
await p.tap('.qk-b[data-qk="2"]');await p.waitForTimeout(800);
console.log(L,'| rt open',await p.isVisible('#rt'),'| dest',await p.inputValue('#dest'),'| title',await p.$eval('#rt-title',e=>e.textContent).catch(()=>'-'));
console.log('  note:',await p.$eval('.rt-auto',e=>e.textContent).catch(()=>'none'));
console.log('  items:',await p.$$eval('#rt-list li',a=>a.map(x=>x.textContent.replace(/\s+/g,' ').trim().slice(0,30)).join(' | ')));
if(L==='ko')await p.screenshot({path:'shots/dk_ko.jpg',type:'jpeg',quality:60});
await p.tap('#rt-close');await p.waitForTimeout(300);console.log('  닫음 rt',await p.isVisible('#rt'),'dest',await p.inputValue('#dest'));
// course city still works
await pick('dest',L==='ko'?'부산':'Busan');await p.tap('.qk-b[data-qk="2"]');await p.waitForTimeout(900);console.log('  부산 테마코스 tile open',await p.$eval('#dest-info details.c-tile',e=>e.open).catch(()=>'?'),'rt',await p.isVisible('#rt'));
console.log('  errs',errs);await c.close()}
await b.close()})();
