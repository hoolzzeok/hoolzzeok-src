const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const errs=[];
const c=await b.newContext({viewport:{width:390,height:844},locale:'ko-KR',deviceScaleFactor:2,acceptDownloads:true});await c.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));
const p=await c.newPage();p.on('pageerror',e=>errs.push(e.message));
await p.goto('file:///home/claude/www.hoolzzeok.com/index.html?from=seoul&to=hwacheon&nights=1&people=2');await p.waitForTimeout(1300);
await p.click('#ui-junior').catch(()=>{});await p.waitForTimeout(300);if(await p.isVisible('#calc-go'))await p.click('#calc-go');await p.waitForTimeout(1300);
console.log('직접 half-cal:',await p.$eval('#half-cal',e=>e.innerText.replace(/\s+/g,' ')));
const [dl]=await Promise.all([p.waitForEvent('download',{timeout:5000}).catch(()=>null),p.click('#half-cal .hp-cal-b')]);
if(dl){const f=await dl.path();console.log('파일:',dl.suggestedFilename());console.log(fs.readFileSync(f,'utf8').split('\r\n').filter(l=>/DTSTART|SUMMARY|TRIGGER|DESCRIPTION:여행/.test(l)).join('\n'));}else console.log('download 없음');
console.log('google:',await p.$eval('#half-cal .hp-cal-g',e=>e.href.slice(0,140)));
// 반값여행 패널
await p.goto('file:///home/claude/www.hoolzzeok.com/index.html');await p.waitForTimeout(1200);await p.click('#ui-junior').catch(()=>{});await p.waitForTimeout(300);
const hb=await p.$('#qk [data-qk="2"]');await hb.click();await p.waitForTimeout(700);
const rows=await p.$$eval('#hp-body .hp-row',a=>a.map(x=>(x.querySelector('.hp-rk b')||{}).textContent+' | '+((x.querySelector('.hp-cal small')||{}).textContent||'-')));
console.log('패널:',rows.length);rows.slice(0,10).forEach(r=>console.log('  ',r));
const y=await p.evaluate(()=>{const e=document.querySelector('#hp-body .hp-list');return e.getBoundingClientRect().top+document.querySelector('#hp-body').scrollTop});
await p.locator('#hp-body .hp-list').first().screenshot({path:'shots/cal153.png'});
console.log('errs',errs);await b.close()})();
