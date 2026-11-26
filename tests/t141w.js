// v141 외국어 후기 쓰기 흐름 점검: 보낸 뒤 문구, 한글 섞임
const {chromium}=require('playwright');const fs=require('fs');const html=fs.readFileSync('/home/claude/www.hoolzzeok.com/index.html','utf8');
(async()=>{const b=await chromium.launch();
const scan=(id)=>{const out=[];const root=document.getElementById(id);if(!root)return['NO '+id];const w=document.createTreeWalker(root,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){const t=n.textContent.trim();if(!t||!/[가-힣]/.test(t))continue;const el=n.parentElement;if(el.closest('[hidden]')||el.closest('[lang="ko"],.ko-chip,option'))continue;const cs=getComputedStyle(el);if(cs.display==='none'||cs.visibility==='hidden')continue;let a=el,vis=true;while(a&&a!==root){if(a.hidden||getComputedStyle(a).display==='none'){vis=false;break}a=a.parentElement}if(vis)out.push(t.slice(0,50))}return[...new Set(out)].slice(0,30)};
for(const [loc,q] of [['en-US','?lang=en'],['ja-JP','?lang=ja'],['zh-CN','?lang=zh'],['zh-TW','?lang=zh-tw']]){
 const c=await b.newContext({viewport:{width:390,height:844},locale:loc,deviceScaleFactor:1.5});const p=await c.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.addInitScript(()=>{window.__ins=[];const mine=[];window.supabase={createClient(){return{auth:{getSession:async()=>({data:{session:{user:{id:'u1',email:'tester@gmail.com'}}}}),onAuthStateChange(){},signOut:async()=>{}},rpc:async n=>({data:false,error:null}),
  from(t){let uidF=null;const q={select(){return q},eq(k,v){if(k==='user_id')uidF=v;return q},order(){return q},limit(){return q},gte(){return q},delete(){return q},insert(r){window.__ins.push(r);mine.unshift({...r,status:'pending',created_at:new Date().toISOString()});return Promise.resolve({error:null})},upsert(){return Promise.resolve({error:null})},
   then(r){r({data:t==='reviews'&&uidF?mine:[],error:null})}};return q}}}};});
 await c.route('https://www.hoolzzeok.com/**',r=>{const u=new URL(r.request().url());if(u.pathname==='/')return r.fulfill({body:html,contentType:'text/html; charset=utf-8'});return r.fulfill({status:404,body:''})});
 await c.route(/cdn\.jsdelivr|unpkg|fonts\./,r=>r.fulfill({body:''}));
 await p.goto('https://www.hoolzzeok.com/'+q);await p.evaluate(()=>localStorage.setItem('hz-sbtest','1'));await p.reload();await p.waitForTimeout(1500);
 await p.click('#ac-open');await p.waitForTimeout(400);console.log('==',loc,'account panel:',await p.$eval('#ac',e=>e.innerText.replace(/\n+/g,' | ').slice(0,200)),'hangul',JSON.stringify(await p.evaluate(scan,'ac')));await p.screenshot({path:`shots/v141w_me_${loc}.jpg`,type:'jpeg',quality:70});await p.click('#ac-my');await p.waitForTimeout(600);console.log(loc,'my-click(0개) → write open',await p.$eval('#rv',e=>!e.hidden));await p.click('#rv-close').catch(()=>{});await p.waitForTimeout(300);
 await p.evaluate(()=>{const r=document.getElementById('rp');if(r.hidden)document.getElementById('rp-top').click()});await p.waitForTimeout(300);
 console.log('==',loc,'list panel hangul:',JSON.stringify(await p.evaluate(scan,'rp')));
 await p.click('#rl-sum [data-rv-open]');await p.waitForTimeout(300);
 console.log(loc,'write panel hangul (star step):',JSON.stringify(await p.evaluate(scan,'rv')));
 await p.click('#cm-stars [data-n="4"]');await p.waitForTimeout(300);
 console.log(loc,'write panel hangul (form):',JSON.stringify(await p.evaluate(scan,'rv')));
 await p.screenshot({path:`shots/v141w_form_${loc}.jpg`,type:'jpeg',quality:70,fullPage:false});
 await p.$eval('#cm-agree',e=>{e.checked=true});await p.click('#cm-send');await p.waitForTimeout(800);
 console.log(loc,'ins title:',await p.evaluate(()=>window.__ins.map(r=>r.title+' | '+r.body)));
 console.log(loc,'msg:',await p.$eval('#cm-msg',e=>e.textContent),'| done:',await p.$eval('#rw-done',e=>e.hidden?'hidden':e.innerText.replace(/\n+/g,' | ')));
 console.log(loc,'after-send hangul:',JSON.stringify(await p.evaluate(scan,'rv')));
 if(!(await p.$eval('#rw-done',e=>e.hidden))){await p.screenshot({path:`shots/v141w_done_${loc}.jpg`,type:'jpeg',quality:70});await p.click('#rv-done-list');await p.waitForTimeout(700);
  console.log(loc,'after done-list: rp open',await p.$eval('#rp',e=>!e.hidden),'my:',await p.$eval('#cm-my',e=>e.hidden?'HIDDEN':e.innerText.slice(0,120).replace(/\n+/g,' | ')));}
 console.log('errs',errs);await c.close();}
await b.close()})();
