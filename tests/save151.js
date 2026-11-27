const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const errs=[];
const c=await b.newContext({viewport:{width:390,height:844},locale:'ko-KR',deviceScaleFactor:2});await c.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));const p=await c.newPage();p.on('pageerror',e=>errs.push(e.message));
await p.goto('file:///home/claude/www.hoolzzeok.com/index.html?from=seoul&to=jeju&nights=1&people=2');await p.waitForTimeout(1200);
// 쉽게(senior) 결과까지
const btns=async()=>p.$$eval('#sr-body .sr-btn',a=>a.map(x=>x.innerText.replace(/\n/g,'/')));
const pick=async(re)=>{const L=await btns();const i=L.findIndex(t=>re.test(t));if(i<0){console.log('NO',re,L.slice(0,10));return false;}await (await p.$$('#sr-body .sr-btn'))[i].click();await p.waitForTimeout(250);return true;};
if(await p.$('#ui-senior')){await p.click('#ui-senior').catch(()=>{});await p.waitForTimeout(400);}
await pick(/^서울/);await pick(/^부산/);await pick(/정했/);
for(let k=0;k<9;k++){const L0=await btns();if(L0.some(t=>/^1박/.test(t))){await pick(/^1박/);continue;}if(L0.some(t=>/^둘|^2명|두 명/.test(t))){await pick(/^둘|^2명|두 명/);continue;}const L=await btns();if(!L.length)break;await (await p.$$('#sr-body .sr-btn'))[0].click();await p.waitForTimeout(250);}
const sv=await p.$$eval('#sr-body .save li',a=>a.map(x=>x.innerText.replace(/\s+/g,' ')));console.log('쉽게 save:',sv);
const det=await p.$('#sr-body details.sc');if(det){await det.evaluate(e=>e.open=true);}
await p.waitForTimeout(300);
const y=await p.evaluate(()=>{const e=document.querySelector('#sr-body .sr-big');return e?e.getBoundingClientRect().top+scrollY:0});
await p.screenshot({path:'shots/save151_a.png',clip:{x:0,y:Math.max(0,y-10),width:390,height:1500},fullPage:true});
const y2=await p.evaluate(()=>{const e=document.querySelector('.sr-links');return e?e.getBoundingClientRect().top+scrollY:0});
await p.screenshot({path:'shots/save151_b.png',clip:{x:0,y:Math.max(0,y2-30),width:390,height:220},fullPage:true});
// 적용 눌러보기
if(sv.length){await p.click('#sr-body .save-go');await p.waitForTimeout(600);console.log('적용 후:',await p.$$eval('#sr-body .save li',a=>a.map(x=>x.innerText.replace(/\s+/g,' '))), await p.$eval('#sr-body .sr-big',e=>e.innerText.replace(/\s+/g,' ')));}
// 직접 화면
const p2=await c.newPage();p2.on('pageerror',e=>errs.push(e.message));await p2.goto('file:///home/claude/www.hoolzzeok.com/index.html?from=seoul&to=yeosu&nights=1&people=2');await p2.waitForTimeout(1200);
await p2.click('#ui-junior').catch(()=>{});await p2.waitForTimeout(300);if(await p2.isVisible('#calc-go'))await p2.click('#calc-go');await p2.waitForTimeout(1200);
console.log('직접 save:',await p2.$$eval('#save-box .save li',a=>a.map(x=>x.innerText.replace(/\s+/g,' '))));
console.log('errs',errs);await b.close()})();
