// v133: 간체(zh) 글자를 대만식 번체로 바꾸는 작은 사전을 만들어 index.html 의 `const ZHTW = ...;` 줄에 넣음(멱등).
// 사이트에 실제로 있는 글자·문구만 넣어 크기를 줄임. OpenCC(cn→tw, Apache-2.0) 결과에 대만에서 쓰는 말 몇 개를 덧붙임.
const OpenCC = require('opencc-js'); const fs = require('fs');
const f = process.argv[2]; let s = fs.readFileSync(f, 'utf8');
const LINE = /^const ZHTW = .*;.*$/m; if (!LINE.test(s)) { console.error('ZHTW line missing'); process.exit(1); }
const body = s.replace(LINE, '');
const conv = OpenCC.Converter({from: 'cn', to: 'tw'});
// 대만 화면에서 더 자연스러운 말(서비스 문구에만 해당) + 잘못 바뀌는 것 되돌리기
const FIX = [['出租車', '計程車'], ['粗麵', '粗面'], ['衚衕', '巷弄'], ['人民幣', '新台幣'], ['網卡', '網路卡'], ['公交車', '公車'], ['公交', '公車'], ['鏈接', '連結'], ['便利店', '便利商店'], ['視頻', '影片'], ['信息', '資訊'], ['默認', '預設'], ['在線', '線上'], ['質量', '品質'], ['善良价格店', '善良價格店'], ['扶余', '扶餘'], ['甯越', '寧越'], ['註銷賬號', '刪除帳號'], ['退出登錄', '登出'], ['賬號', '帳號'], ['賬戶', '帳戶'], ['登錄', '登入'], ['發佈', '發布'], ['打車', '搭計程車'], ['短信', '簡訊'], ['軟件', '軟體'], ['網絡', '網路'], ['激活', '啟用'], ['用戶', '使用者'], ['屏幕', '螢幕'], ['打印', '列印'], ['設置', '設定'], ['搜索', '搜尋'], ['點擊', '點選'], ['二維碼', 'QR碼'], ['充電寶', '行動電源']];   // v141 대만식 낱말
const tw = r => FIX.reduce((t, [a, b]) => t.split(a).join(b), conv(r));
const chars = new Set(body.match(/[㐀-鿿]/g)); const runs = new Set(body.match(/[㐀-鿿]+/g));
const cm = {}; for (const c of chars) { const t = conv(c); if (t !== c && t.length === 1) cm[c] = t; }
const cw = r => [...r].map(c => cm[c] || c).join('');
const p = {}; for (const r of runs) { if (r.length < 2) continue; const t = tw(r); if (t !== cw(r)) p[r] = t; }
p['出租车'] = '計程車';   // 문장 조각이 이어 붙을 때도 바뀌게
const m = Math.max(2, ...Object.keys(p).map(k => k.length));
const json = JSON.stringify({c: Object.entries(cm).map(([a, b]) => a + b).join(''), p, m});
s = s.replace(LINE, () => `const ZHTW = ${json};   // gen_zhtw.cjs 가 간체→번체(대만) 사전으로 채움. 손으로 고치지 말 것`);
fs.writeFileSync(f, s);
console.log('zhtw chars', Object.keys(cm).length, 'phrases', Object.keys(p).length, 'bytes', json.length);
