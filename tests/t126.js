const {chromium}=require('playwright');const fs=require('fs');
const html=fs.readFileSync('/home/claude/www.hoolzzeok.com/index.html','utf8');
(async()=>{const b=await chromium.launch();const c=await b.newContext();const p=await c.newPage();
let calls=[];
await p.exposeFunction('logOAuth',x=>calls.push(x));
await p.addInitScript(()=>{window.supabase={createClient(){return{auth:{
  getSession:async()=>({data:{session:null}}),
  signInWithOAuth:async(o)=>{window.logOAuth(o.options.redirectTo);return{}},
  onAuthStateChange(){}},rpc:async()=>({data:false}),from(){const q={select(){return q},eq(){return q},order(){return q},limit(){return q},then(r){r({data:[],error:null})}};return q}}}};});
await c.route('https://www.hoolzzeok.com/**',r=>{const u=new URL(r.request().url());if(u.pathname==='/'||u.pathname==='/index.html')return r.fulfill({body:html,contentType:'text/html'});return r.fulfill({status:404,body:''})});
await c.route(/cdn\.jsdelivr|unpkg/,r=>r.fulfill({body:'',contentType:'text/javascript'}));
await p.goto('https://www.hoolzzeok.com/?join=1&to=busan');await p.waitForTimeout(1500);
const ok=await p.evaluate(()=>typeof cmLogin);console.log('cmLogin',ok);
await p.evaluate(()=>cmLogin('kakao','5'));await p.waitForTimeout(300);
console.log('redirectTo',calls,'saved',await p.evaluate(()=>sessionStorage.getItem('hz-back-q')));
// simulate return
await p.goto('https://www.hoolzzeok.com/?code=abc');await p.waitForTimeout(2000);
console.log('after return url',p.url(),'rv open flag kept/consumed',await p.evaluate(()=>[sessionStorage.getItem('hz-back-q'),sessionStorage.getItem('hz-rv-open'),!document.getElementById('rv').hidden]));
await b.close()})();
