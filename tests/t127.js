const {chromium}=require('playwright');const fs=require('fs');
const html=fs.readFileSync('/home/claude/www.hoolzzeok.com/index.html','utf8');
(async()=>{const b=await chromium.launch();
for(const w of [320,375,430,1024]){const c=await b.newContext({viewport:{width:w,height:700},locale:'ko-KR'});const p=await c.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.addInitScript(()=>{window.supabase={createClient(){return{auth:{getSession:async()=>({data:{session:null}}),signInWithOAuth:async()=>({}),onAuthStateChange(){}},rpc:async()=>({data:false}),from(){const q={select(){return q},eq(){return q},order(){return q},limit(){return q},range(){return q},then(r){r({data:[],error:null})}};return q}}}};});
await c.route('https://www.hoolzzeok.com/**',r=>{const u=new URL(r.request().url());if(u.pathname==='/')return r.fulfill({body:html,contentType:'text/html'});return r.fulfill({status:404,body:''})});
await c.route(/cdn\.jsdelivr|unpkg/,r=>r.fulfill({body:'',contentType:'text/javascript'}));
for(const ui of ['junior','senior']){
await p.goto('https://www.hoolzzeok.com/?join=1');await p.waitForTimeout(2500);if(w===320&&ui==='junior')console.log(await p.evaluate(()=>({sb:!!(window.cm&&cm.sb),h:document.querySelector('#ac-open').hidden,lang:document.documentElement.lang,cf:!!window.HZ_SUPA})));
await p.click('#ui-'+ui);await p.waitForTimeout(300);
const r=await p.evaluate(()=>({sw:document.documentElement.scrollWidth,top:document.querySelector('#rp-top').getBoundingClientRect().toJSON(),ac:document.querySelector('#ac-open').getBoundingClientRect().toJSON(),txt:document.querySelector('#rp-top').innerText,hdrH:document.querySelector('header.top').offsetHeight}));
console.log(w,ui,'scrollW',r.sw,'hdrH',r.hdrH,'btn',r.txt,Math.round(r.top.x),Math.round(r.top.y),'ac',Math.round(r.ac.x),Math.round(r.ac.y));
await p.screenshot({path:`shots/h_${w}_${ui}.png`,clip:{x:0,y:0,width:w,height:70}});}
await p.click('#rp-top');await p.waitForTimeout(400);console.log(' rp open',await p.evaluate(()=>!document.getElementById('rp').hidden),errs);
await c.close()}
await b.close()})();
