const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));
await p.goto('file:///home/claude/hoolzzeok_site/index.html');await p.waitForTimeout(800);
console.log(JSON.stringify(await p.evaluate(()=>{const out={};for(const [pid,cs] of Object.entries(COURSES))for(const c of cs)for(const x of c.stops)if(x.k!=='spot'&&x.menu){const m=Array.isArray(x.menu)?x.menu[0]:x.menu;if(menuTxt(m,'en')===m||menuTxt(m,'zh')===m)out[m]=pid+'/'+c.id}return out})));
console.log(JSON.stringify(await p.evaluate(()=>Object.keys(COURSES.jeju[0].stops.find(x=>x.k!=='spot')))));await b.close()})();
