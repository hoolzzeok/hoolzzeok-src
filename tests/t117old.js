const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const errs=[];
const pg=await b.newPage({locale:'ko-KR',viewport:{width:390,height:844}});pg.on('pageerror',e=>errs.push(e.message));
await pg.goto('file:///home/claude/hoolzzeok_site/index_v124_backup.html');await pg.waitForTimeout(700);
const btns=async()=>pg.$$eval('#sr-body .sr-btn',a=>a.map(x=>x.innerText.replace(/\n/g,'/')));
const pick=async(re)=>{const L=await btns();const i=L.findIndex(t=>re.test(t));await (await pg.$$('#sr-body .sr-btn'))[i].click();await pg.waitForTimeout(120);};
await pick(/^서울/); await pick(/^강릉/); await pick(/정했어요/); await pick(/다음 달/); await pick(/^2박/); await pick(/^둘/); await pick(/상관없/); await pick(/^버스/); await pick(/보통/);
const rd=async()=>pg.$$eval('#sr-body .sr-rows li .sr-ln',a=>a.map(x=>x.innerText.replace(/\n/g,' ')).join(' | '));
for (const k of ['avg','none','fri','sat','both']) { await pg.click(`.sr-week [data-sat="${k}"]`); await pg.waitForTimeout(150);
  console.log(k, await pg.$eval('.sr-big',e=>e.innerText.replace(/\n/g,' ')), '|', await rd());
  console.log('  note:', await pg.$eval('.sr-week .sr-note',e=>e.textContent)); }
await pg.click('.sr-calc summary'); console.log('calc lodge:', await pg.$$eval('.sr-calc li',a=>a.map(x=>x.innerText.replace(/\n/g,' ')).filter(t=>/숙박|잠/.test(t)).join(' / ')));
await (await pg.$('.sr-week')).screenshot({path:'shots/v116_week.png'});
// junior
const p2=await b.newPage({locale:'ko-KR',viewport:{width:390,height:844}});p2.on('pageerror',e=>errs.push(e.message));
await p2.addInitScript(()=>{try{localStorage.setItem('hz-ui','junior')}catch(e){}});
for (const [to,n] of [['jeju',1],['busan',1],['gangneung',0]]) {
await p2.goto(`file:///home/claude/hoolzzeok_site/index_v124_backup.html?from=seoul&to=${to}&nights=${n}&people=2`);await p2.waitForTimeout(700);
console.log(to, 'field hidden', await p2.$eval('#sat-field',e=>e.hidden), await p2.$$eval('#sat-seg button',a=>a.map(x=>x.textContent+(x.getAttribute('aria-pressed')==='true'?'*':'')).join('|')));
if(n){ for(const k of ['none','fri','sat']){ await p2.$eval(`#sat-seg [data-sat="${k}"]`,e=>e.click()); await p2.waitForTimeout(120); console.log('  ',k, await p2.$eval('#t-meta',e=>e.textContent), await p2.$eval('#sum',e=>e.innerText.split('\n').filter(t=>/숙박|합계|1인/.test(t)).slice(0,4).join(' / '))); } }
}
console.log('errs',errs);await b.close();})();
