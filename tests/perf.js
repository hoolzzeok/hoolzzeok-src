const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));
await p.goto('file:///home/claude/www.hoolzzeok.com/index.html?from=seoul&to=yeosu&nights=2&people=2');await p.waitForTimeout(1500);
const t=await p.evaluate(()=>{const b=document.querySelector('#mode-car');const t0=performance.now();for(let i=0;i<10;i++){document.querySelector(i%2?'#mode-car':'#mode-transit').click();}return (performance.now()-t0)/10});
console.log('ms per render',t.toFixed(1));await b.close()})();
