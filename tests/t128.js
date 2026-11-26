const {chromium}=require('playwright');const fs=require('fs');
const html=fs.readFileSync('/home/claude/www.hoolzzeok.com/index.html','utf8');
(async()=>{const b=await chromium.launch();
for(const kt of [true,false]){
const c=await b.newContext({viewport:{width:375,height:740},locale:'ko-KR',userAgent:kt?'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 KAKAOTALK 10.5.0':undefined});
const p=await c.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));let calls=[];await p.exposeFunction('logOAuth',x=>calls.push(x));
await p.addInitScript(()=>{window.supabase={createClient(){return{auth:{getSession:async()=>({data:{session:null}}),signInWithOAuth:async(o)=>{window.logOAuth(o.provider);return{}},onAuthStateChange(){}},rpc:async()=>({data:false}),from(){const q={select(){return q},eq(){return q},order(){return q},limit(){return q},range(){return q},then(r){r({data:[],error:null})}};return q}}}};});
await c.route('https://www.hoolzzeok.com/**',r=>{const u=new URL(r.request().url());if(u.pathname==='/')return r.fulfill({body:html,contentType:'text/html'});return r.fulfill({status:404,body:''})});
await c.route(/cdn\.jsdelivr|unpkg|fonts\./,r=>r.fulfill({body:''}));
await p.goto('https://www.hoolzzeok.com/?to=busan');await p.evaluate(()=>{localStorage.setItem('hz-sbtest','1')});await p.goto('https://www.hoolzzeok.com/');await p.waitForTimeout(2000);
await p.click('#ac-open');await p.waitForTimeout(400);
const agree=await p.$('#ac-sheet input[type=checkbox], #ac input[type=checkbox]'); if(agree) await agree.check().catch(()=>{});
const g=await p.$('[data-p="google"]');console.log('kt',kt,'google btn',!!g, 'disabled',g&&await g.isDisabled());
if(g){await g.click({force:true});await p.waitForTimeout(400);}
const dlg=await p.evaluate(()=>{const d=document.getElementById('kt-out');return d?{shown:!d.hidden,url:ktOutUrl()}:null});
console.log(' dialog',dlg,'calls',calls);
if(dlg&&dlg.shown){await p.screenshot({path:'shots/kt.png'});await p.click('#kt-kakao');await p.waitForTimeout(300);console.log(' after kakao',calls);}
console.log(' errs',errs);await c.close()}
await b.close()})();
