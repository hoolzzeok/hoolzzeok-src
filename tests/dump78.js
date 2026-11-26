const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));
await p.goto('file:///home/claude/www.hoolzzeok.com/index.html');await p.waitForTimeout(800);
const r=await p.evaluate(()=>PLACES.filter(p=>p.id!=='dokdo'&&!(INFO[p.id]&&INFO[p.id].spots&&INFO[p.id].spots.length)).map(p=>({id:p.id,ko:p.ko,prov:p.prov,lat:p.lat,lon:p.lon,hub:(((HUB[p.id]||[])[0])||HUB_ALT[p.id]||[]).map(h=>({name:h[0],kind:h[1],lon:h[2],lat:h[3]}))})));
fs.mkdirSync('/home/claude/hoolzzeok-src/db/pull',{recursive:true});
fs.writeFileSync('/home/claude/hoolzzeok-src/db/pull/targets_78.json',JSON.stringify(r,null,1));
console.log(r.length, r.reduce((a,x)=>a+x.hub.length,0));await b.close()})();
