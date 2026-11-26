const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const c=await b.newContext({viewport:{width:390,height:844},locale:process.argv[2]||'en-US'});const p=await c.newPage();
await c.route(/fonts\.|cdn\.jsdelivr|unpkg/,r=>r.fulfill({body:''}));
await p.goto('file:///home/claude/hoolzzeok_site/index.html?qt=6.culture.standard');await p.waitForTimeout(900);
const H=await p.evaluate(()=>document.getElementById('qt').scrollHeight);console.log('H',H);
let i=0;for(let y=700;y<H&&i<5;y+=800,i++){await p.evaluate(y=>document.getElementById('qt').scrollTo(0,y),y);await p.waitForTimeout(150);await p.screenshot({path:`qt/s${i}.png`});}
console.log(await p.$$eval('.qt-day h3',a=>a.map(x=>x.innerText.replace(/\n/g,' ')).join(' / ')));
await b.close()})();
