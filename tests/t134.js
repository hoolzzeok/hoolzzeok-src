// v134: 관리자 대기 배지, 외국인 보상 신청, 보상 표시, 공지 줄
const {chromium}=require('playwright');const fs=require('fs');const html=fs.readFileSync('/home/claude/www.hoolzzeok.com/index.html','utf8');
const today=process.argv[2]||'2026-12-03';
(async()=>{const b=await chromium.launch();
const mk=async(loc,admin,rows)=>{const c=await b.newContext({viewport:{width:390,height:844},locale:loc});const p=await c.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.addInitScript(([admin,rows,today])=>{const RD=Date;window.Date=class extends RD{constructor(...a){super(...(a.length?a:[today+'T03:00:00Z']))}static now(){return new RD(today+'T03:00:00Z').getTime()}};
  window.__ins=[];window.supabase={createClient(){return{auth:{getSession:async()=>({data:{session:{user:{id:'u1',email:'abc@x.com'}}}}),onAuthStateChange(){},signOut:async()=>{}},rpc:async n=>({data:n==='is_admin'?admin:false}),
  from(t){let st=null;const q={select(){return q},eq(k,v){if(k==='status')st=v;return q},order(){return q},limit(){return q},gte(){return q},insert(r){window.__ins.push(r);return Promise.resolve({error:null})},upsert(){return Promise.resolve({error:null})},update(){return q},delete(){return q},
   then(r){const d=t==='public_reviews'?rows.pub:t==='reviews'&&st==='pending'&&admin?rows.pend:[];r({data:d,error:null})}};return q}}}};},[admin,rows,today]);
 await c.route('https://www.hoolzzeok.com/**',r=>{const u=new URL(r.request().url());if(u.pathname==='/')return r.fulfill({body:html,contentType:'text/html; charset=utf-8'});return r.fulfill({status:404,body:''})});
 await c.route(/cdn\.jsdelivr|unpkg|fonts\./,r=>r.fulfill({body:''}));
 await p.goto('https://www.hoolzzeok.com/');await p.evaluate(()=>localStorage.setItem('hz-sbtest','1'));await p.reload();await p.waitForTimeout(1500);if(errs.length)console.log('EARLY',errs);return {p,c,errs};};
const rv=(id,gift,ap,uid)=>({id,user_id:uid||'u9',title:'t',origin:'seoul',dest:'busan',region:'gyeongnam',nights:1,mode:'transit',people:2,tags:['k:food','l:en'],cost:gift?{star:4,total:200000,gift:5}:{star:3},body:'Nice trip',created_at:'2026-12-02T01:00:00Z',approved_at:ap,status:'approved'});
const rows={pub:[rv('a1',1,'2026-12-02T02:00:00Z'),rv('a2',0,'2026-12-02T02:00:00Z'),rv('a3',1,'2026-11-28T02:00:00Z')],pend:[rv('p1',1,null,'uid-777'),rv('p2',0,null)]};
// 관리자
{const {p,c,errs}=await mk('ko-KR',true,rows);
 console.log('notice',await p.$eval('#hz-notice',e=>e.hidden?'hidden':e.innerText));
 console.log('badge',await p.$eval('#rp-top',e=>[e.querySelector('.adm-n')?.textContent,e.getAttribute('aria-label')]));
 await p.screenshot({path:'qt/adm_head.png',clip:{x:0,y:0,width:390,height:110}});
 await p.click('#rp-top');await p.waitForTimeout(300);
 console.log('admin h3',await p.$eval('#cm-admin h3',e=>e.textContent),'|',await p.$$eval('#cm-admin .cm-gift-adm',a=>a.map(x=>x.innerText)));
 console.log('pub paid',await p.$$eval('#cm-list .cm-paid',a=>a.map(x=>x.innerText.slice(0,40))));
 await p.screenshot({path:'qt/adm_list.png'});
 await p.click('#rp-close').catch(()=>{});await p.click('#ac-open');await p.waitForTimeout(300);
 console.log('me adm',await p.$eval('#ac-adm',e=>e.innerText.replace(/\n/g,' ')));await p.screenshot({path:'qt/adm_me.png'});
 await p.click('#ac-adm');await p.waitForTimeout(500);console.log('rp open',await p.$eval('#rp',e=>!e.hidden));
 await p.click('#notice-x').catch(()=>{});console.log('errs',errs);await c.close();}
// 외국인 쓰기 (영어)
{const {p,c,errs}=await mk('en-US',false,rows);
 await p.click('#rp-top');await p.click('#rl-sum [data-rv-open]');await p.click('#cm-stars [data-n="5"]');await p.waitForTimeout(200);
 console.log('gift',await p.$eval('#rw-gift',e=>e.hidden?'hidden':e.innerText.replace(/\n/g,' ')));
 await p.screenshot({path:'qt/gift_en.png',fullPage:false});
 if(await p.$('#cm-gift')){await p.check('#cm-gift');}
 await p.$eval('#cm-agree',e=>{e.checked=true});await p.click('#cm-send');await p.waitForTimeout(500);
 console.log('ins cost',JSON.stringify(await p.evaluate(()=>window.__ins.map(r=>r.cost))));
 console.log('notice en',await p.$eval('#hz-notice',e=>e.hidden?'hidden':e.innerText));
 console.log('pub paid en',await p.evaluate(()=>{document.querySelector('#rv-close')?.click();return 1}),await p.$$eval('#cm-list .cm-paid-tr',a=>a.map(x=>x.innerText.slice(0,50))));
 console.log('errs',errs);await c.close();}
// 한국어 쓰기: 보상 칸 없음
{const {p,c,errs}=await mk('ko-KR',false,rows);await p.click('#rp-top');await p.click('#rl-sum [data-rv-open]');await p.waitForTimeout(200);
 console.log('ko gift',await p.$eval('#rw-gift',e=>e.hidden));console.log('errs',errs);await c.close();}
await b.close()})();
