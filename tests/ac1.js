const {chromium}=require('playwright');const fs=require('fs');
const html=fs.readFileSync('/home/claude/www.hoolzzeok.com/index.html','utf8');fs.mkdirSync('ac1',{recursive:true});
(async()=>{const b=await chromium.launch();
for(const [name,logged,scheme,w] of [['anon',false,'light',390],['anon_dark',false,'dark',390],['in',true,'light',390],['anon320',false,'light',320]]){
const c=await b.newContext({viewport:{width:w,height:844},locale:'ko-KR',colorScheme:scheme});const p=await c.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.addInitScript((logged)=>{window.supabase={createClient(){return{auth:{getSession:async()=>({data:{session:logged?{user:{id:'u1',email:'hoolzzeok.test@gmail.com'}}:null}}),signInWithOAuth:async(o)=>{window.__o=o;return{}},onAuthStateChange(){},signOut:async()=>({})},rpc:async()=>({data:false}),from(t){const q={select(){return q},eq(){return q},order(){return q},limit(){return q},then(r){r({data:[],error:null})}};return q}}}};},logged);
await c.route('https://www.hoolzzeok.com/**',r=>{const u=new URL(r.request().url());if(u.pathname==='/')return r.fulfill({body:html,contentType:'text/html'});return r.fulfill({status:404,body:''})});
await c.route(/cdn\.jsdelivr|unpkg|fonts\./,r=>r.fulfill({body:''}));
await p.goto('https://www.hoolzzeok.com/');await p.evaluate(()=>localStorage.setItem('hz-sbtest','1'));await p.reload();await p.waitForTimeout(1500);
await p.click('#ac-open');await p.waitForTimeout(400);
if(!logged){await p.click('.sso-kakao');await p.waitForTimeout(250);console.log(name,'msg:',await p.$eval('#ac-msg',e=>e.textContent),'oauth',await p.evaluate(()=>!!window.__o));}
await p.screenshot({path:`ac1/${name}.png`,fullPage:false});
if(!logged){await p.click('#ac-agree-row');await p.click('.sso-kakao');await p.waitForTimeout(200);console.log(' after agree oauth',await p.evaluate(()=>window.__o&&window.__o.provider),'overflow',await p.evaluate(()=>document.getElementById('ac').scrollWidth));}
console.log(' errs',errs);await c.close()}
await b.close()})();
