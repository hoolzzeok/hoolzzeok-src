const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:390,height:844},locale:'ko-KR'});
await p.route(/fonts\.|cdn\.jsdelivr|unpkg/,r=>r.fulfill({body:''}));
await p.goto('file:///home/claude/hoolzzeok_site/index.html?from=seoul&to=yeosu&nights=1&people=2');await p.waitForTimeout(700);
await p.evaluate(()=>document.querySelectorAll('details').forEach(d=>d.open=true));
const t=await p.evaluate(()=>[...document.querySelectorAll('.good-list li, [class*=good] li')].slice(0,6).map(x=>x.innerText.replace(/\n/g,' / ')));
console.log(t.join('\n'));await b.close()})();
