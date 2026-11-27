// 현재 후기 보기·쓰기 화면을 휴대폰 크기로 단계별 캡처 (가짜 Supabase, 로그인된 상태)
const {chromium}=require('playwright');const fs=require('fs');
const html=fs.readFileSync(process.argv[2]||'/home/claude/www.hoolzzeok.com/index.html','utf8');const out=process.argv[3]||'rv0';
(async()=>{const b=await chromium.launch();
const c=await b.newContext({viewport:{width:390,height:844},locale:'ko-KR',deviceScaleFactor:1});
const p=await c.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.addInitScript(()=>{const rows=[{id:'r1',title:'포항 1박 2일',origin:'jinju',dest:'pohang',region:'경상',nights:1,mode:'car',people:2,tags:[],cost:{total:122000},body:'좋았어요. 다시 가고 싶어요.',created_at:'2026-11-19T03:00:00Z',approved_at:'2026-11-20T03:00:00Z',mood:'good'},
{id:'r2',title:'강릉 2박 3일',origin:'seoul',dest:'gangneung',region:'강원',nights:2,mode:'transit',people:3,tags:['사진'],cost:{total:210000,lodging:90000,food:70000},body:'바다 뷰 숙소 최고. 커피거리 사람 많아요.',created_at:'2026-11-10T03:00:00Z',approved_at:'2026-11-11T03:00:00Z',mood:'ok'}];
window.__ins=[];
window.supabase={createClient(){const sess={user:{id:'u1',email:'test@gmail.com'}};return{auth:{getSession:async()=>({data:{session:sess}}),signInWithOAuth:async()=>({}),onAuthStateChange(){},signOut:async()=>({})},rpc:async()=>({data:false}),
 from(t){const q={_t:t,select(){return q},eq(){return q},neq(){return q},in(){return q},order(){return q},limit(){return q},range(){return q},
  insert(v){window.__ins.push(v);return Promise.resolve({data:null,error:null})},delete(){return q},
  then(r){r({data:t==='public_reviews'?rows:[],error:null})}};return q}}}};});
await c.route('https://www.hoolzzeok.com/**',r=>{const u=new URL(r.request().url());if(u.pathname==='/')return r.fulfill({body:html,contentType:'text/html'});return r.fulfill({status:404,body:''})});
await c.route(/cdn\.jsdelivr|unpkg|fonts\./,r=>r.fulfill({body:''}));
await p.goto('https://www.hoolzzeok.com/?join=1&from=seoul&to=gangneung&nights=2&people=2');await p.waitForTimeout(1800);

// 결과 화면: 실제와 비슷했나요 → 후기로 이어 쓰기
await p.click('#ui-junior').catch(()=>{});if(await p.isVisible('#calc-go'))await p.click('#calc-go');await p.waitForTimeout(1200);
console.log('went visible', await p.evaluate(()=>!document.getElementById('went-btn').hidden));
const fb=await p.$('#fb-box [data-fb="less"]');console.log('fb', !!fb);
await fb.scrollIntoViewIfNeeded();await fb.click();await p.waitForTimeout(300);
await p.fill('#fb-box .fb-amt','200000');
const el=await p.$('#fb-box');await el.screenshot({path:`${out}/05_fb.png`});
await p.click('#fb-box .fb-rv');await p.waitForTimeout(900);
console.log('rv open', await p.evaluate(()=>!document.getElementById('rv').hidden), 'route', await p.evaluate(()=>document.getElementById('cm-route-txt').textContent));
console.log('pick', await p.evaluate(()=>[...document.querySelectorAll('#cm-quick button')].map(b=>b.getAttribute('aria-pressed')+':'+b.innerText.split('\n')[0]).join(' | ')), 'total', await p.evaluate(()=>document.getElementById('cm-total').value));
// 쉽게 화면에서 후기 열고 닫아도 쉽게 그대로
await p.goto('https://www.hoolzzeok.com/?from=seoul&to=gangneung&nights=2&people=2');await p.waitForTimeout(1500);
await p.click('#ui-senior');await p.waitForTimeout(400);await p.evaluate(()=>{document.getElementById('rp-top').hidden=false});await p.click('#rp-top');await p.waitForTimeout(600);await p.click('#rp-close');await p.waitForTimeout(300);
await p.click('#rp-top');await p.waitForTimeout(600);await p.click('#cm-list [data-act="calc"]');await p.waitForTimeout(900);console.log('calc senior', await p.evaluate(()=>[document.documentElement.dataset.ui, document.getElementById('rp').hidden, (document.querySelector('#sr-body .sr-total, #sr-body .sr-big, #sr-body h3')||{}).textContent]));
console.log('ui after close', await p.evaluate(()=>document.documentElement.dataset.ui));
console.log('errs',errs);await b.close()})();
