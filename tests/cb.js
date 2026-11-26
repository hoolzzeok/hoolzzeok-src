const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));
await p.goto('file:///home/claude/hoolzzeok_site/index.html');await p.waitForTimeout(800);
console.log(await p.evaluate(()=>['busan','gyeongju','jeonju','gangneung'].map(c=>{const r=calcBudget(byId('seoul'),byId(c),2,'transit','standard',false,null);return c+':'+r.transport+' '+(r.transportNote||r.tNote||'')}).join('\n')));await b.close()})();
