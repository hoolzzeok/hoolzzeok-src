// v141: 내가 쓴 후기(상태별) 확인
const {chromium}=require('playwright');const fs=require('fs');const html=fs.readFileSync('/home/claude/www.hoolzzeok.com/index.html','utf8');
(async()=>{const b=await chromium.launch();
const rv=(id,st,ap,title)=>({id,user_id:'u1',status:st,title,origin:'seoul',dest:'busan',region:'gyeongnam',nights:1,mode:'transit',people:2,tags:['k:food','l:ko'],cost:{star:4},body:'좋았어요',created_at:'2026-11-25T02:00:00Z',approved_at:ap,mood:'good'});
const mine=[rv('m1','pending',null,'부산 1박 2일, 2명'),rv('m2','approved','2026-11-25T05:00:00Z','강릉 당일, 1명'),rv('m3','rejected',null,'경주 1박 2일, 3명')];
const pub=[{...mine[1]}];
for(const [loc,shot,q] of [['ko-KR','ko',''],['en-US','en','?lang=en'],['ja-JP','ja','?lang=ja'],['zh-CN','zh','?lang=zh'],['zh-TW','zt','?lang=zh-tw']]){
 const c=await b.newContext({viewport:{width:390,height:844},locale:loc,deviceScaleFactor:1.5});const p=await c.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.addInitScript(([mine,pub])=>{window.__del=[];window.supabase={createClient(){return{auth:{getSession:async()=>({data:{session:{user:{id:'u1',email:'tester@gmail.com'}}}}),onAuthStateChange(){},signOut:async()=>{}},rpc:async n=>({data:false,error:null}),
  from(t){let uidF=null,del=false,st=null;const q={select(){return q},eq(k,v){if(k==='user_id')uidF=v;if(k==='status')st=v;if(del&&k==='id'){window.__del.push(v)}return q},order(){return q},limit(){return q},gte(){return q},delete(){del=true;return q},insert(){return Promise.resolve({error:null})},upsert(){return Promise.resolve({error:null})},
   then(r){const d=t==='public_reviews'?pub:(t==='reviews'&&uidF&&!del)?mine.filter(x=>!window.__del.includes(x.id)):[];r({data:d,error:null})}};return q}}}};},[mine,pub]);
 await c.route('https://www.hoolzzeok.com/**',r=>{const u=new URL(r.request().url());if(u.pathname==='/')return r.fulfill({body:html,contentType:'text/html; charset=utf-8'});return r.fulfill({status:404,body:''})});
 await c.route(/cdn\.jsdelivr|unpkg|fonts\./,r=>r.fulfill({body:''}));
 await p.goto('https://www.hoolzzeok.com/'+q);await p.evaluate(()=>localStorage.setItem('hz-sbtest','1'));await p.reload();await p.waitForTimeout(1500);
 await p.click('#ac-open');await p.waitForTimeout(300);
 console.log(loc,'me:',await p.$eval('#ac-my',e=>e.innerText.replace(/\n/g,' ')));
 await p.screenshot({path:`shots/v141_me_${shot}.jpg`,type:'jpeg',quality:75});
 await p.click('#ac-my');await p.waitForTimeout(600);
 console.log(loc,'my box:',await p.$eval('#cm-my',e=>e.hidden?'HIDDEN':e.innerText.replace(/\n+/g,' | ')));
 await p.screenshot({path:`shots/v141_my_${shot}.jpg`,type:'jpeg',quality:75});
 console.log(loc,'HANGUL in rp:',JSON.stringify(await p.evaluate(()=>{const out=[];const w=document.createTreeWalker(document.getElementById('rp'),NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){const t=n.textContent.trim();if(!t||!/[가-힣]/.test(t))continue;const el=n.parentElement;if(el.closest('[hidden]')||el.closest('.cm-text,.cm-body,.rl-body,blockquote,[lang="ko"]'))continue;if(getComputedStyle(el).display==='none')continue;out.push(t.slice(0,40))}return [...new Set(out)].slice(0,30)})));
 await p.click('[data-my-see="m2"]');await p.waitForTimeout(500);
 console.log(loc,'flash:',await p.$$eval('#cm-list .cm-flash',a=>a.length));
 await p.click('[data-my-del="m3"]');await p.click('[data-my-del="m3"]');await p.waitForTimeout(500);
 console.log(loc,'after del:',await p.evaluate(()=>window.__del),await p.$$eval('#cm-my .cm-my-row',a=>a.length));
 console.log('errs',errs);await c.close();}
await b.close()})();
