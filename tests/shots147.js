const {chromium}=require('playwright');
const L=[['phone','휴대폰 / 폴드 접힘',412,915,false],['duo_v','아이폰 듀오 펼침(세로)',626,890,false],['fold','갤럭시 폴드 펼침',884,1104,false],['duo_h','아이폰 듀오 펼침(가로)',890,626,false],['tri','트라이폴드 펼침',1080,792,false],['hinge','폴드 반쯤 접어 세움',884,1104,true]];
(async()=>{const b=await chromium.launch();
for(const [k,,w,h,seg] of L){const c=await b.newContext({viewport:{width:w,height:h},locale:'ko-KR',deviceScaleFactor:1});const p=await c.newPage();
await c.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));
await p.goto('file:///home/claude/www.hoolzzeok.com/index.html');await p.waitForTimeout(900);
await p.evaluate(()=>{const x=document.querySelector('.notice-x,#notice-x,[data-close]');});
await p.click('#ui-junior');await p.waitForTimeout(300);await p.click('#calc-go');await p.waitForTimeout(1800);
if(seg){const cdp=await c.newCDPSession(p);await cdp.send('Emulation.setDeviceMetricsOverride',{width:w,height:h,deviceScaleFactor:1,mobile:true,displayFeature:{orientation:'vertical',offset:432,maskLength:20}});await p.waitForTimeout(600);}
await p.evaluate(()=>scrollTo(0,0));await p.waitForTimeout(200);
if(seg){const cdp2=await c.newCDPSession(p);const r=await cdp2.send('Page.captureScreenshot',{format:'png'});require('fs').writeFileSync('shots/v147_'+k+'.png',Buffer.from(r.data,'base64'));console.log('seg',await p.evaluate(()=>matchMedia('(horizontal-viewport-segments: 2)').matches))}else await p.screenshot({path:'shots/v147_'+k+'.png'});await c.close()}
await b.close()})();
