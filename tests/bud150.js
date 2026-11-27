const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const errs=[];
for (const lg of ['ko','en','ja','zh']){const c=await b.newContext({viewport:{width:390,height:844},locale:'ko-KR'});await c.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));const p=await c.newPage();p.on('pageerror',e=>errs.push(e.message));
await p.goto(`file:///home/claude/www.hoolzzeok.com/index.html?lang=${lg}`);await p.waitForTimeout(1200);await p.click('#ui-junior').catch(()=>{});await p.waitForTimeout(300);
const t=await p.$eval('#qk [data-qk="0"]',e=>e.innerText.replace(/\n/g,' / '));await p.click('#qk [data-qk="0"]');await p.waitForTimeout(600);
console.log(lg,t,'| map open',await p.$eval('#map',e=>!e.hidden),'|',await p.$eval('#budget-label',e=>e.innerText));await c.close();}
console.log('errs',errs);await b.close()})();
