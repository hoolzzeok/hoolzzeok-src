const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const errs=[];
const c=await b.newContext({viewport:{width:390,height:844},locale:'ko-KR'});await c.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));const p=await c.newPage();p.on('pageerror',e=>errs.push(e.message));
await p.goto('file:///home/claude/www.hoolzzeok.com/index.html');await p.waitForTimeout(1200);
const btns=async()=>p.$$eval('#sr-body .sr-btn',a=>a.map(x=>x.innerText.replace(/\n/g,'/')));
const pick=async(re)=>{const L=await btns();const i=L.findIndex(t=>re.test(t));if(i<0)return false;await (await p.$$('#sr-body .sr-btn'))[i].click();await p.waitForTimeout(250);return true;};
if(await p.$('#ui-senior')){await p.click('#ui-senior').catch(()=>{});await p.waitForTimeout(400);}
await pick(/^서울/);await pick(/^부산/);await pick(/추천/);
for(let k=0;k<9;k++){const L0=await btns();if(!L0.length)break;if(L0.some(t=>/^1박/.test(t))){await pick(/^1박/);continue;}if(L0.some(t=>/^둘|^2명|두 명/.test(t))){await pick(/^둘|^2명|두 명/);continue;}await (await p.$$('#sr-body .sr-btn'))[0].click();await p.waitForTimeout(250);}
const y0=await p.evaluate(()=>document.querySelector('#sr-body').getBoundingClientRect().top+scrollY);
const H=await p.evaluate(()=>document.querySelector('#sr-body').getBoundingClientRect().height);console.log('sr height',H);
for(let y=0,i=0;y<H&&i<8;y+=1800,i++)await p.screenshot({path:`shots/sr_${i}.png`,clip:{x:0,y:y0+y,width:390,height:Math.min(1800,H-y)},fullPage:true});
console.log('errs',errs);await b.close()})();
