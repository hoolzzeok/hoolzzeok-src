// v136 조합 전수: 일수 3~7 × 테마(1~2개) × 공항 × 두 번째 도시, 4개 언어 일부
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const bad=[];let n=0;
const TH=['food','shop','history','nature','kpop','rest'],AIR={icn:['','busan','jeju','gyeongju','jeonju','gangneung'],pus:['','gyeongju','jeju'],cju:['']};
for(const [lg,loc] of [['en','en-US'],['ja','ja-JP'],['zh','zh-CN'],['zt','zh-TW']]){
 const c=await b.newContext({viewport:{width:360,height:780},locale:loc});const p=await c.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await c.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));
 await p.goto('file:///home/claude/hoolzzeok_site/index.html');await p.waitForTimeout(800);
 for(const d of [3,4,5,6,7])for(const [ai,cs] of Object.entries(AIR))for(const ct of cs)for(const th of (lg==='en'?[...TH,'food+history','nature+rest','kpop+shop','history+food']:['food','nature+rest','kpop+shop'])){
  const q=`${d}.${th}.standard.${ct}.${ai}.${(lg==='en'&&d===6)?'20261207':''}`;
  const r=await p.evaluate(q=>{history.replaceState(null,'','?qt='+q);const [dd,t,bg,c2,a2,st]=q.split('.');return q},q);
  // 직접 상태 넣고 다시 그림
  await p.evaluate(q=>{const [dd,t,bg,c2,a2,st]=q.split('.');window.__qtSet&&window.__qtSet(q)},q);
  for(let t=0;t<3;t++){try{await p.goto('file:///home/claude/hoolzzeok_site/index.html?qt='+encodeURIComponent(q),{timeout:15000});break}catch(e){await p.waitForTimeout(300)}}await p.waitForTimeout(260);
  require("fs").appendFileSync("/tmp/qt4prog.txt",lg+" "+q+"\n");n++;const o=await p.evaluate(()=>{const q=document.getElementById('qt');if(!q||q.hidden)return {e:'closed'};const t=q.innerText;return {w:q.scrollWidth,dw:document.documentElement.scrollWidth,bad:(t.match(/NaN|undefined|null|\[object|\{c\}/g)||[]).slice(0,3),days:q.querySelectorAll('.qt-day').length,title:(document.getElementById('qt-title')||{}).textContent}});
  if(o.e||o.w>362||o.bad.length||o.days!==d)bad.push([lg,q,JSON.stringify(o)]);
 }
 if(errs.length)bad.push([lg,'errs',errs.slice(0,3).join(';')]);await c.close();}
console.log('checked',n,'bad',bad.length);bad.slice(0,20).forEach(x=>console.log(x.join(' | ')));await b.close()})();
