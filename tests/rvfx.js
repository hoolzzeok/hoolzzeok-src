const {chromium}=require('playwright');const fs=require('fs');
const html=fs.readFileSync('/home/claude/www.hoolzzeok.com/index.html','utf8');fs.mkdirSync('rvfx',{recursive:true});
const scan=sel=>{const root=document.querySelector(sel);const out=[];const w=document.createTreeWalker(root,NodeFilter.SHOW_TEXT);let n;
 while(n=w.nextNode()){const t=n.nodeValue;if(!/[가-힣]/.test(t))continue;const el=n.parentElement;if(el.closest('[lang="ko"],[hidden],script'))continue;if(!el.checkVisibility())continue;out.push(t.trim().slice(0,60));}return [...new Set(out)];};
(async()=>{const b=await chromium.launch();
for(const [L,loc] of [['en','en-US'],['ja','ja-JP'],['zh','zh-CN']]){
for(const logged of [true,false]){
const c=await b.newContext({viewport:{width:390,height:844},locale:loc});const p=await c.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.addInitScript((logged)=>{const rows=[{id:'r1',title:'x',origin:'jinju',dest:'pohang',region:'gyeongsang',nights:1,mode:'car',people:2,tags:[],cost:{total:122000},body:'좋았어요. 다시 가고 싶어요.',created_at:'2026-11-19T03:00:00Z',approved_at:'2026-11-20T03:00:00Z',mood:'good'},
{id:'r2',title:'x',origin:'seoul',dest:'gangneung',region:'gangwon',nights:2,mode:'transit',people:3,tags:['k:view','k:food','k:crowd','사진','l:en'],cost:{total:210000,star:4},body:'Ocean view hotel was great. Coffee street is busy on weekends.',created_at:'2026-11-10T03:00:00Z',approved_at:'2026-11-11T03:00:00Z',mood:'good'}];
window.__ins=[];window.supabase={createClient(){const sess=logged?{user:{id:'u1',email:'visitor@example.com'}}:null;return{auth:{getSession:async()=>({data:{session:sess}}),signInWithOAuth:async(o)=>{window.__o=o;return{}},onAuthStateChange(){},signOut:async()=>({})},rpc:async()=>({data:false}),
 from(t){const q={select(){return q},eq(){return q},order(){return q},limit(){return q},insert(v){window.__ins.push(v);return Promise.resolve({error:null})},upsert(){return Promise.resolve({error:null})},then(r){r({data:t==='public_reviews'?rows:[],error:null})}};return q}}}};},logged);
await c.route('https://www.hoolzzeok.com/**',r=>{const u=new URL(r.request().url());if(u.pathname==='/')return r.fulfill({body:html,contentType:'text/html'});return r.fulfill({status:404,body:''})});
await c.route(/cdn\.jsdelivr|unpkg|fonts\./,r=>r.fulfill({body:''}));
await p.goto('https://www.hoolzzeok.com/?from=seoul&to=busan&nights=2&people=2');await p.evaluate(()=>localStorage.setItem('hz-sbtest','1'));await p.reload();await p.waitForTimeout(1500);
const tag=`${L}_${logged?'in':'anon'}`;
console.log('==',tag,'header:',await p.$eval('#rp-top',e=>e.hidden?'HIDDEN':e.innerText),'|',await p.$eval('#ac-open',e=>e.hidden?'HIDDEN':e.innerText));
if(logged){
 await p.click('#rp-top');await p.waitForTimeout(400);await p.screenshot({path:`rvfx/${tag}_list.png`});
 console.log(' list leaks',JSON.stringify(await p.evaluate(scan,'#rp')));
 await p.click('#rl-sum [data-rv-open]');await p.click('#cm-stars [data-n="4"]');await p.waitForTimeout(400);
 await p.click('#cm-quick [data-k="less"]');await p.click('#cm-say button');await p.waitForTimeout(150);
 await p.screenshot({path:`rvfx/${tag}_write.png`});console.log(' write leaks',JSON.stringify(await p.evaluate(scan,'#rv')));
 await p.evaluate(()=>{document.querySelectorAll('#rv details').forEach(d=>d.open=true)});console.log(' write(open) leaks',JSON.stringify(await p.evaluate(scan,'#rv')));
 if(!(await p.$eval('#cm-agree-row',e=>e.hidden))) await p.check('#cm-agree');
 await p.click('#cm-send');await p.waitForTimeout(400);console.log(' done',await p.$eval('#rw-done',e=>!e.hidden),'ins',JSON.stringify((await p.evaluate(()=>window.__ins))[0]).slice(0,260));
 await p.screenshot({path:`rvfx/${tag}_done.png`});
} else {
 await p.click('#ac-open');await p.waitForTimeout(400);await p.screenshot({path:`rvfx/${tag}_join.png`});console.log(' join leaks',JSON.stringify(await p.evaluate(scan,'#ac')),'first btn',await p.$eval('.sso',e=>e.innerText));
}
console.log(' errs',errs);await c.close()}}
await b.close()})();
