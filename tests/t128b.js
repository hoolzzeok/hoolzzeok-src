const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const errs=[];
const pg=await b.newPage({locale:'ko-KR',viewport:{width:390,height:844}});pg.on('pageerror',e=>errs.push(e.message));
await pg.route(/fonts\.|cdn\.jsdelivr|unpkg/,r=>r.fulfill({body:''}));
const btns=async()=>pg.$$eval('#sr-body .sr-btn',a=>a.map(x=>x.innerText.replace(/\n/g,'/')));
const pick=async(re)=>{const L=await btns();const i=L.findIndex(t=>re.test(t));if(i<0){console.log('NO',re,L.slice(0,12));throw 0;}await (await pg.$$('#sr-body .sr-btn'))[i].click();await pg.waitForTimeout(150);};
for(const [to,mode] of [['부산',/기차|버스/],['강릉',/^내 차/],['제주',/비행기/]]){
await pg.goto('file:///home/claude/hoolzzeok_site/index.html');await pg.waitForTimeout(700);
await pick(/^서울/);await pick(new RegExp(to));await pick(/추천/);await pg.$$('#sr-body .sr-btn').then(a=>a[0].click());await pg.waitForTimeout(150);
await pick(/^2박/);await pick(/^둘/);await pick(/상관/);await pick(mode);await pick(/보통/);await pg.waitForTimeout(400);
const r=await pg.$eval('.sr-ckf',e=>({sum:e.querySelector('summary').innerText.replace(/\n/g,' / '),items:[...e.querySelectorAll('li')].map(l=>l.innerText)})).catch(()=>null);
console.log(to,JSON.stringify(r,null,0));
}
await pg.click('.sr-ckf summary');await pg.click('.sr-ck li:first-child label');await pg.waitForTimeout(200);
await (await pg.$('.sr-ckf')).screenshot({path:'shots/ck.png'});
// english kit
await pg.goto('file:///home/claude/hoolzzeok_site/index.html?lang=en');await pg.waitForTimeout(600);
console.log('en train text present', await pg.evaluate(()=>document.documentElement.innerHTML.includes('코레일+ (Korail+)')));
console.log('errs',errs);await b.close()})();
