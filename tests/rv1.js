const {chromium}=require('playwright');const fs=require('fs');
const html=fs.readFileSync('/home/claude/www.hoolzzeok.com/index.html','utf8');const out=process.argv[2]||'rv1';fs.mkdirSync(out,{recursive:true});
const logged=process.argv[3]!=='anon';
(async()=>{const b=await chromium.launch();
const c=await b.newContext({viewport:{width:390,height:844},locale:'ko-KR',deviceScaleFactor:1});
const p=await c.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.addInitScript((logged)=>{const rows=[{id:'r1',title:'포항 1박 2일',origin:'jinju',dest:'pohang',region:'gyeongsang',nights:1,mode:'car',people:2,tags:[],cost:{total:122000},body:'좋았어요. 다시 가고 싶어요.',created_at:'2026-11-19T03:00:00Z',approved_at:'2026-11-20T03:00:00Z',mood:'good'},
{id:'r2',title:'강릉 2박 3일',origin:'seoul',dest:'gangneung',region:'gangwon',nights:2,mode:'transit',people:3,tags:['k:view','k:food','k:crowd','사진'],cost:{total:210000,star:4},body:'바다 뷰 숙소 최고. 커피거리는 주말에 사람 많아요. 아침 일찍 가면 한적해요.',created_at:'2026-11-10T03:00:00Z',approved_at:'2026-11-11T03:00:00Z',mood:'good'},
{id:'r3',title:'부산 2박 3일',origin:'seoul',dest:'busan',region:'gyeongsang',nights:2,mode:'transit',people:2,tags:['k:value','k:easy'],cost:{total:230000,star:5},body:'가성비 좋아요. 다니기 편해요.',created_at:'2026-11-08T03:00:00Z',approved_at:'2026-11-09T03:00:00Z',mood:'good'}];
window.__ins=[];
window.supabase={createClient(){const sess=logged?{user:{id:'u1',email:'test@gmail.com'}}:null;return{auth:{getSession:async()=>({data:{session:sess}}),signInWithOAuth:async(o)=>{window.__oauth=o;return{}},onAuthStateChange(){},signOut:async()=>({})},rpc:async()=>({data:false}),
 from(t){const q={select(){return q},eq(){return q},neq(){return q},in(){return q},order(){return q},limit(){return q},range(){return q},upsert(){return Promise.resolve({error:null})},
  insert(v){window.__ins.push(v);return Promise.resolve({data:null,error:null})},delete(){return q},
  then(r){r({data:t==='public_reviews'?rows:[],error:null})}};return q}}}};},logged);
await c.route('https://www.hoolzzeok.com/**',r=>{const u=new URL(r.request().url());if(u.pathname==='/')return r.fulfill({body:html,contentType:'text/html'});return r.fulfill({status:404,body:''})});
await c.route(/cdn\.jsdelivr|unpkg|fonts\./,r=>r.fulfill({body:''}));
await p.goto('https://www.hoolzzeok.com/?from=seoul&to=busan&nights=2&people=2');await p.evaluate(()=>localStorage.setItem('hz-sbtest','1'));await p.reload();await p.waitForTimeout(1800);
const shot=async n=>{await p.waitForTimeout(300);await p.screenshot({path:`${out}/${n}.png`});};
const full=async n=>{await p.waitForTimeout(300);const el=await p.$(n.sel);};
await p.click('#rp-top');await shot('01_list');
await p.evaluate(()=>document.getElementById('rp').scrollTo(0,700));await shot('02_list_mid');
await p.click('.rl-tag');await p.waitForTimeout(200);console.log('tag filter status:',await p.$eval('#cm-status',e=>e.textContent),'| cards',await p.$$eval('#cm-list .rl-card',a=>a.length));
await p.click('#cm-tags button');await p.waitForTimeout(150);
await p.evaluate(()=>document.getElementById('rp').scrollTo(0,0));
await p.click('#rl-sum [data-rv-open]');await shot('03_write_start');
console.log('send label:',await p.$eval('#cm-send',e=>e.textContent+' hidden='+e.hidden),'| more hidden',await p.$eval('#rw-more',e=>e.hidden));
await p.click('#cm-stars [data-n="5"]');await p.waitForTimeout(500);await shot('04_star5');
await p.click('#cm-quick [data-k="same"]');await p.click('#rw-amt [data-d="10000"]');
console.log('total:',await p.$eval('#cm-total',e=>e.value));
await p.click('#cm-say [data-k="food"]');await p.click('#cm-say [data-k="value"]');await p.click('#cm-say2 [data-k="crowd"]');
await p.evaluate(()=>document.getElementById('rv').scrollTo(0,600));await shot('05_mid');
await p.fill('#cm-text','자갈치시장 회센터는 2층 식당이 더 싸요.');
await p.evaluate(()=>document.getElementById('rv').scrollTo(0,99999));await shot('06_bottom');
if(logged){ const ag=await p.$('#cm-agree'); if(!(await p.$eval('#cm-agree-row',e=>e.hidden))) await ag.check();
 await p.click('#cm-send');await p.waitForTimeout(500);await shot('07_done');
 console.log('done shown',await p.$eval('#rw-done',e=>!e.hidden));
 console.log('inserted',JSON.stringify(await p.evaluate(()=>window.__ins)));
} else {
 console.log('login box',await p.$eval('#rv-login',e=>!e.hidden+' '+e.innerText.replace(/\n/g,' / ')));
 await p.check('#cm-agree');await p.click('#rv-login [data-login="kakao"]').catch(e=>console.log('no kakao btn'));await p.waitForTimeout(300);
 console.log('oauth',JSON.stringify(await p.evaluate(()=>window.__oauth)),'auto',await p.evaluate(()=>sessionStorage.getItem('hz-rv-auto')),'draft',await p.evaluate(()=>localStorage.getItem('hz-cm-draft')));
}
console.log('errs',errs);await b.close()})();
