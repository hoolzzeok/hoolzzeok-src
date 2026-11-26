const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));
await p.goto('file:///home/claude/hoolzzeok_site/index.html');await p.waitForTimeout(800);
const r=await p.evaluate(()=>{const ids=PLACES.filter(p=>p.id!=='dokdo'&&!(INFO[p.id]&&INFO[p.id].spots&&INFO[p.id].spots.length)).map(p=>p.id);
 return {n:ids.length, hasInfo:ids.filter(i=>INFO[i]).length, sample:JSON.stringify(INFO[ids.find(i=>INFO[i])]||null).slice(0,300), keys:[...new Set(Object.values(INFO).flatMap(o=>Object.keys(o)))], tourHas:ids.filter(i=>TOUR[i]).length}});
console.log(JSON.stringify(r,null,1));await b.close()})();
