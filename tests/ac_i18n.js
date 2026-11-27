const {chromium}=require('playwright');
const CASES={ja:['統営','統営市','釜山','慶州','済州','済州島','全州','江陵','麗水','ソウル','プサン','トンヨン','ソウル市','安東','ぷさん','チョンジュ','统营','統營','タニャン','済州特別自治道'],
 zh:['统营','统营市','釜山','庆州','济州','济州岛','全州','江陵','丽水','首尔','安东','統營','統営','济州特别自治道','首尔特别市','丹阳郡'],
 'zh-tw':['統營','慶州','濟州','濟州島','麗水','首爾','安東','统营','統営','首爾特別市','花蓮'],
 en:['Tongyeong','tongyeong-si','Gyeongju','Jeju Island','Busan City','Yeosu','Seoul','Andong-si','Pusan','Kyongju','Jeonju-si','Jeju-do','Taegu','Cheju','tong','Danyang-gun','Tokyo']};
(async()=>{const b=await chromium.launch();const out={};
for(const [lg,qs] of Object.entries(CASES)){const c=await b.newContext({viewport:{width:390,height:844},locale:'en-US'});await c.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));const p=await c.newPage();
 await p.goto(`file:///home/claude/www.hoolzzeok.com/index.html?lang=${lg}`);await p.waitForTimeout(1200);
 if(await p.$('#ui-senior')){await p.click('#ui-senior').catch(()=>{});await p.waitForTimeout(400);}
 if(!await p.$('#sr-q')){console.log(lg,'no sr-q');continue;}
 for(const q of qs){await p.fill('#sr-q','');await p.type('#sr-q',q);await p.waitForTimeout(150);
  const r=await p.$$eval('#sr-body .sr-more .sr-grid .sr-btn b, #sr-body .sr-more .sr-grid .sr-btn, #sr-body .sr-more .sr-note',a=>a.map(x=>x.innerText.split('\n')[0]).slice(0,3));
  console.log(lg.padEnd(6),q.padEnd(14),'→',r.join(' | ')||'(없음)');}
 await c.close();}
await b.close()})();
