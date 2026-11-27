const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const errs=[];
const c=await b.newContext({viewport:{width:390,height:844},hasTouch:true,isMobile:true,locale:'ko-KR'});await c.route(/fonts\.|unpkg|supabase|jsdelivr/,r=>r.fulfill({body:''}));const p=await c.newPage();p.on('pageerror',e=>errs.push(e.message));
for(const q of ['영월','담양','함양','단양']){
 await p.goto('file:///home/claude/www.hoolzzeok.com/index.html');await p.waitForTimeout(900);await p.click('#ui-junior');await p.waitForTimeout(300);
 await p.fill('#dest','');await p.type('#dest',q,{delay:20});await p.waitForTimeout(200);await p.tap('#dest-list li:visible >> nth=0');await p.waitForTimeout(300);
 await p.click('#calc-go');await p.waitForTimeout(1200);
 for(let k=0;k<8;k++){const bt=await p.$('button:has-text("추천해 주세요")');if(bt&&await bt.isVisible()){await bt.click();await p.waitForTimeout(700);break;}
   const any=await p.$('#junior button.wide:visible, #junior .sr-opt:visible');if(!any)break;await any.click();await p.waitForTimeout(500);}
 const t=await p.evaluate(()=>[...document.querySelectorAll('.tl li, .tl-b')].map(e=>e.textContent).join(' ').replace(/\s+/g,' '));
 const hits=(t.match(/[^ ]{1,14} ?[^ ]{0,10} ?(?:[월화수목금토일]요일|매월[^휴]{0,16}) 휴무/g)||[]); console.log("  plan chars",t.length);
 console.log(q,'일정 휴무 표시:',hits.slice(0,4).join(' | ')||'-');}
console.log('errs',errs);await b.close()})();
