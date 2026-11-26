const {chromium}=require('playwright');const fs=require('fs');
const html=fs.readFileSync('/home/claude/www.hoolzzeok.com/index.html','utf8');
(async()=>{const b=await chromium.launch();
for(const [w,h,scheme,name] of [[390,844,'dark','dark'],[1280,860,'light','desk']]){
const c=await b.newContext({viewport:{width:w,height:h},locale:'ko-KR',colorScheme:scheme});const p=await c.newPage();
await p.addInitScript(()=>{const rows=[{id:'r2',title:'강릉',origin:'seoul',dest:'gangneung',region:'gangwon',nights:2,mode:'transit',people:3,tags:['k:view','k:food','k:crowd','사진'],cost:{total:210000,star:4},body:'바다 뷰 숙소 최고.',created_at:'2026-11-10T03:00:00Z',approved_at:'2026-11-11T03:00:00Z',mood:'good'}];
window.supabase={createClient(){return{auth:{getSession:async()=>({data:{session:{user:{id:'u1',email:'a@b.c'}}}}),onAuthStateChange(){}},rpc:async()=>({data:false}),from(t){const q={select(){return q},eq(){return q},order(){return q},limit(){return q},then(r){r({data:t==='public_reviews'?rows:[],error:null})}};return q}}}};});
await c.route('https://www.hoolzzeok.com/**',r=>{const u=new URL(r.request().url());if(u.pathname==='/')return r.fulfill({body:html,contentType:'text/html'});return r.fulfill({status:404,body:''})});
await c.route(/cdn\.jsdelivr|unpkg|fonts\./,r=>r.fulfill({body:''}));
await p.goto('https://www.hoolzzeok.com/?from=seoul&to=busan&nights=2');await p.evaluate(()=>localStorage.setItem('hz-sbtest','1'));await p.reload();await p.waitForTimeout(1500);
await p.click('#rp-top');await p.waitForTimeout(300);await p.screenshot({path:`rv1/${name}_list.png`});
await p.click('#rl-sum [data-rv-open]');await p.click('#cm-stars [data-n="2"]');await p.waitForTimeout(400);await p.evaluate(()=>document.getElementById('rv').scrollTo(0,0));await p.screenshot({path:`rv1/${name}_write.png`});
console.log(name,'first kw group:',await p.$eval('#rw-kw-h',e=>e.textContent),'|',await p.$eval('#cm-say button',e=>e.textContent), 'overflow',await p.evaluate(()=>document.getElementById('rv').scrollWidth));
await c.close()}
await b.close()})();
