const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const errs=[];
const ctx=async(loc)=>{const c=await b.newContext({viewport:{width:390,height:844},hasTouch:true,isMobile:true,locale:loc});await c.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));const p=await c.newPage();p.on('pageerror',e=>errs.push(e.message));return p;};
let p=await ctx('ko-KR');
await p.goto('file:///home/claude/www.hoolzzeok.com/index.html');await p.waitForTimeout(1000);await p.click('#ui-junior');await p.waitForTimeout(300);
for(const q of ['영월','담양','부산','화천','함양']){
 await p.fill('#dest','');await p.type('#dest',q,{delay:20});await p.waitForTimeout(200);await p.tap('#dest-list li:visible >> nth=0');await p.waitForTimeout(300);
 const info=await p.$eval('#dest-info',e=>e.innerText.replace(/\s+/g,' '));
 const m=info.match(/(크리스마스 빌리지[^.]{0,40}|해운대 빛축제[^.]{0,30}|반값[^.]{0,60}|휴무[^.]{0,20})/g)||[];
 console.log(q,'info:',m.slice(0,4).join(' || '));
 await p.click('#calc-go');await p.waitForTimeout(1500);
 const t=await p.evaluate(()=>document.body.textContent.replace(/\s+/g,' '));
 console.log('  결과 휴무:',(t.match(/[^ ]{0,12} ?[월화수목금토일]요일 휴무|매월[^,)]{0,16}휴무/g)||[]).slice(0,4).join(' | '));
 await p.goto('file:///home/claude/www.hoolzzeok.com/index.html');await p.waitForTimeout(800);await p.click('#ui-junior');await p.waitForTimeout(300);}
// 공모전·축제 목록 (첫 화면)
const home=await p.evaluate(()=>document.body.innerText.replace(/\s+/g,' '));
console.log('통영 공모전:',/통영관광 전국사진/.test(home),' 수원 지난공모전:',/수원 방문의 해/.test(home),' 고흥유자:',/고흥유자축제/.test(home));
// 외국어 딸깍 음성 해설
for(const [lg,q] of [['en','4.history+food.standard.busan.icn.20261210'],['ja','5.history.standard..icn.20261212'],['zh-tw','4.history.standard..icn.']]){
 const pp=await ctx('en-US');await pp.goto(`file:///home/claude/www.hoolzzeok.com/index.html?lang=${lg}&qt=${q}`);await pp.waitForTimeout(1500);
 const au=await pp.$$eval('.qt-au',a=>a.map(x=>x.innerText.replace(/\s+/g,' ').slice(0,90)));
 const fest=await pp.evaluate(()=>(document.body.innerText.match(/Christmas Village|Haeundae Lighting|Seoul Winter|クリスマス|冬/g)||[]).length);
 console.log(lg,'음성',au.length,au.slice(0,2).join(' || '));}
console.log('errs',errs);await b.close()})();
