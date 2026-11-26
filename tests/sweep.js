// 전체 여행지 × 이동수단 × 언어 돌리며 화면 오류 찾기
const {chromium}=require('playwright');const fs=require('fs');
const FILE='file:///home/claude/hoolzzeok_site/index.html';
const html=fs.readFileSync('/home/claude/hoolzzeok_site/index.html','utf8');
const ids=[...html.matchAll(/\["([a-z0-9-]+)","[가-힣()]+","[^"]+","[가-힣]+",[\d.]+,[\d.]+/g)].map(m=>m[1]);
const LANGS=(process.argv[2]||'ko,en,ja,zh').split(',');const LOC={ko:'ko-KR',en:'en-US',ja:'ja-JP',zh:'zh-CN',zt:'zh-TW'};
const ZL=html.match(/^const ZHTW = (\{.*?\});/m);const SIMP=ZL?[...JSON.parse(ZL[1]).c].filter((_,i)=>i%2===0).filter(c=>!'佣里岩余干后台面只发'.includes(c)).join(''):'';
const BAD=/NaN|undefined|\[object|Infinity|\$\{|null원|null명|\bnull\b/;
const scan=(BADS)=>{const BAD=new RegExp(BADS);const out=[];const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;
 while(n=w.nextNode()){const t=n.nodeValue;if(!BAD.test(t))continue;const el=n.parentElement;if(!el||el.closest('script,style,[hidden]'))continue;if(!el.checkVisibility())continue;const h=el.closest('[id]');out.push((h?'#'+h.id:'')+': '+t.trim().slice(0,90));}
 document.querySelectorAll('button,a').forEach(b=>{if(!b.checkVisibility()||b.closest('[hidden]'))return;if(!(b.innerText||'').trim()&&!b.getAttribute('aria-label')&&!b.querySelector('svg,img'))out.push('EMPTY BTN '+(b.id||b.className));});
 if(document.documentElement.scrollWidth>innerWidth+1)out.push('OVERFLOW '+document.documentElement.scrollWidth);
 return out;};
(async()=>{const b=await chromium.launch();const issues={};
for(const L of LANGS){const c=await b.newContext({viewport:{width:390,height:844},locale:LOC[L]});const p=await c.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await c.route(/fonts\.|cdn\.jsdelivr|unpkg/,r=>r.fulfill({body:''}));
 const list=(L==='ko'||L==='en')?ids:ids.filter((_,i)=>i%4===0);
 for(let i=0;i<list.length;i++){const id=list[i];if(id==='seoul')continue;const n=i%4;
  await p.goto(`${FILE}?from=seoul&to=${id}&nights=${n}&people=${1+i%4}`);await p.waitForTimeout(250);
  await p.evaluate(()=>document.querySelectorAll('details').forEach(d=>d.open=true));
  const modes=await p.$$eval('#mode button',a=>a.map((x,k)=>k));
  (globalThis.cnt=(globalThis.cnt||0)+modes.length);
  for(const k of modes){await p.$$eval('#mode button',(a,k)=>a[k].click(),k);await p.waitForTimeout(60);
   const r=await p.evaluate(scan,L==='zt'?BAD.source+'|['+SIMP+']':BAD.source);for(const x of r){(issues[L+' '+x]=issues[L+' '+x]||[]).push(id+'/'+n+'/m'+k);}}
 }
 for(const e of errs)(issues[L+' PAGEERROR '+e]=issues[L+' PAGEERROR '+e]||[]).push('');
 await c.close();}
console.log('checked',LANGS.join(','),'views',globalThis.cnt);const keys=Object.keys(issues);console.log('issue kinds',keys.length);for(const k of keys)console.log(k,'×',issues[k].length,issues[k].slice(0,4).join(' '));
fs.writeFileSync('sweep_out.json',JSON.stringify(issues,null,1));await b.close()})();
