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
await p.goto('https://www.hoolzzeok.com/?join=1&from=seoul&to=busan&nights=2&people=2');await p.waitForTimeout(1800);
const shot=async n=>{await p.waitForTimeout(350);await p.screenshot({path:`${out}/${n}.png`,fullPage:false});};
await p.click('#rp-top');await shot('01_list');
await p.evaluate(()=>document.querySelector('#rp .rv-panel').parentElement.scrollTo(0,9999));await shot('02_list_bottom');
await p.click('#rp-t-write');await shot('03_step1');
const st=async()=>p.evaluate(()=>{const s=[...document.querySelectorAll('#rv .rv-step')].find(x=>!x.hidden);return s&&s.dataset.step});
for(let i=0;i<8;i++){const s=await st();console.log('step',s);if(!s||s==='6')break;
 if(s==='1'){await p.click('#rv .rv-step[data-step="1"] [data-next]');}
 else if(s==='2'){await p.click('#cm-mood button');}
 else if(s==='3'){await p.click('#cm-quick button');await p.waitForTimeout(200);if(await st()==='3')await p.click('#rv-cost-next');}
 else if(s==='4'){await p.click('#cm-say button').catch(()=>{});await p.click('#rv-say-next');}
 else if(s==='5'){await p.click('#cm-send');}
 await shot('04_step'+(await st()));}
console.log('inserted',JSON.stringify(await p.evaluate(()=>window.__ins)).slice(0,500));
console.log('errs',errs);await b.close()})();
