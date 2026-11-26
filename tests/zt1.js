const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const c=await b.newContext({viewport:{width:390,height:844},locale:'zh-TW'});const p=await c.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await c.route(/fonts\.|cdn\.jsdelivr|unpkg/,r=>r.fulfill({body:''}));
await p.goto('file:///home/claude/hoolzzeok_site/index.html');await p.waitForTimeout(1200);
const simp=/[们这个说为国时会对过还发经从机车门问间见长东开关头买卖让请认识说话钱银饭汤鸡鱼面]/;
const chk=async tag=>{const t=await p.evaluate(()=>document.body.innerText);const m=t.match(new RegExp(simp.source,'g'))||[];console.log(tag,'len',t.length,'simplified left',m.length,m.slice(0,15).join(''),'| sel',await p.$eval('#lang-sel',e=>e.value),'| html lang',await p.evaluate(()=>document.documentElement.lang));};
await chk('home');console.log((await p.evaluate(()=>document.body.innerText)).slice(0,300).replace(/\n/g,' / '));
await p.click('#qt-go');await p.waitForTimeout(300);await p.screenshot({path:'qt/zt_q1.png'});
await p.goto('file:///home/claude/hoolzzeok_site/index.html?qt=5.food.standard');await p.waitForTimeout(1000);await chk('qt result');
console.log(await p.$eval('#qt-title',e=>e.textContent),await p.$eval('.qt-sum>b',e=>e.textContent));await p.screenshot({path:'qt/zt_res.png'});
console.log(await p.$eval('.qt-book',e=>e.innerText.slice(0,300)).catch(()=>'-'));
// 언어 바꾸기: 간체로
await p.goto('file:///home/claude/hoolzzeok_site/index.html');await p.waitForTimeout(800);
await p.selectOption('#lang-sel','zh');await p.waitForLoadState();await p.waitForTimeout(1200);await chk('to simplified');
await p.selectOption('#lang-sel','zh-tw');await p.waitForLoadState();await p.waitForTimeout(1200);await chk('back to TW');
await p.selectOption('#lang-sel','en');await p.waitForLoadState();await p.waitForTimeout(1200);await chk('to en');
console.log('errs',errs);await b.close()})();
