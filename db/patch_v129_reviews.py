# v129 여행 후기 새로 만들기: 후기 보기(요약·카드) + 후기 쓰기(한 화면, 별점·탭 몇 번)
# 참고한 방식: 네이버 키워드 리뷰(눌러서 고르기), 구글 지도(별점 누르면 시작 + 미리 정한 답을 탭으로),
# 에어비앤비(별점에 따라 좋았던 점/아쉬운 점 고르기). DB 칸은 그대로(별점은 cost.star, 키워드는 tags 'k:'),
import re, sys
p = '/home/claude/hoolzzeok_site/index.html'
s = open(p, encoding='utf-8').read()
def R(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (a[:80], c)
    s = s.replace(a, b)

# ---------- HTML: 후기 보기 ----------
a = s.index('<div class="rv rp" id="rp"')
b = s.index('<div class="rv acct" id="ac"')
s = s[:a] + '''<div class="rv rp" id="rp" role="dialog" aria-modal="true" aria-labelledby="rp-title" hidden>
  <div class="rv-panel">
    <div class="rv-head"><span class="hp-k">훌쩍</span><button type="button" class="rv-x" id="rp-close">닫기</button></div>
    <h2 class="hp-h" id="rp-title">여행 후기</h2>
    <p class="rv-sm">실제로 다녀온 사람이 쓴 돈과 한마디예요.</p>
    <div class="rl-sum" id="rl-sum"></div>
    <div class="chips on-bg rl-filter" id="cm-regions" role="group" aria-label="지역"></div>
    <div class="rl-tagon" id="cm-tags" hidden></div>
    <p class="cm-status" id="cm-status" aria-live="polite"></p>
    <div class="cm-admin" id="cm-admin" hidden></div>
    <ol class="cm-list rl-list" id="cm-list"></ol>
    <div class="rl-fab" id="cm-write"><button type="button" class="rl-fab-b" data-rv-open><span aria-hidden="true">✏️</span> 내 여행 후기 쓰기 <small>30초</small></button></div>
  </div>
</div>
''' + s[b:]

# ---------- HTML: 후기 쓰기 ----------
a = s.index('<div class="rv" id="rv"')
b = s.index('<div id="junior"')
s = s[:a] + '''<div class="rv rw" id="rv" role="dialog" aria-modal="true" aria-labelledby="rv-title" hidden>
  <div class="rv-panel">
    <div class="rv-head"><button type="button" class="rv-x" id="rv-close">닫기</button><b class="rw-hd">후기 쓰기</b><span class="rw-time">30초면 끝나요</span></div>
    <h2 class="sr" id="rv-title">후기 쓰기</h2>
    <form class="rw-form" id="cm-form" novalidate>
      <section class="rw-trip">
        <span class="rw-trip-ic" aria-hidden="true">🧳</span>
        <div class="rw-trip-t"><small>다녀온 여행</small><b id="cm-route-txt"></b></div>
        <button type="button" class="rw-link" id="cm-route-edit" aria-expanded="false" aria-controls="cm-route-box">바꾸기</button>
      </section>
      <div class="cm-route-box rw-routebox" id="cm-route-box" hidden>
        <div class="cm-row">
          <div class="ac cm-ac"><span class="cm-l">출발</span><input id="cm-origin-q" class="ac-in" type="text" role="combobox" aria-label="출발" aria-autocomplete="list" aria-expanded="false" aria-controls="cm-origin-list" autocomplete="off" autocorrect="off" spellcheck="false" enterkeyhint="done" placeholder="한 글자만 써도 돼요"><ul class="ac-list" id="cm-origin-list" role="listbox" hidden></ul><input type="hidden" id="cm-origin"></div>
          <div class="ac cm-ac"><span class="cm-l">도착</span><input id="cm-dest-q" class="ac-in" type="text" role="combobox" aria-label="도착" aria-autocomplete="list" aria-expanded="false" aria-controls="cm-dest-list" autocomplete="off" autocorrect="off" spellcheck="false" enterkeyhint="done" placeholder="한 글자만 써도 돼요"><ul class="ac-list" id="cm-dest-list" role="listbox" hidden></ul><input type="hidden" id="cm-dest"></div>
        </div>
        <div class="cm-q2"><span class="cm-l">일정</span><div class="chips cm-wrap" id="cm-nights-c" role="group" aria-label="일정"></div><input type="hidden" id="cm-nights" value="1"></div>
        <div class="cm-q2"><span class="cm-l">이동</span><div class="chips cm-wrap" id="cm-mode-c" role="group" aria-label="이동"></div><input type="hidden" id="cm-mode" value="transit"></div>
        <div class="cm-q2"><span class="cm-l">인원</span><div class="cm-step"><button type="button" id="cm-p-minus" aria-label="한 명 줄이기">−</button><b id="cm-p-txt" aria-live="polite">2명</b><button type="button" id="cm-p-plus" aria-label="한 명 늘리기">+</button></div><input type="hidden" id="cm-people" value="2"></div>
        <button type="button" class="rw-routedone" id="cm-route-done">이 여행으로 할게요</button>
      </div>
      <section class="rw-q rw-q-star">
        <h3 id="rw-star-h">여행은 어땠어요?</h3>
        <div class="rw-stars" id="cm-stars" role="radiogroup" aria-labelledby="rw-star-h"></div>
        <p class="rw-star-t" id="cm-star-t" aria-live="polite">별을 눌러 주세요</p>
      </section>
      <div class="rw-more" id="rw-more" hidden>
        <section class="rw-q">
          <h3>한 사람이 쓴 돈은요? <small>대충이어도 돼요</small></h3>
          <p class="rw-sm" id="cm-est-txt"></p>
          <div class="rw-seg" id="cm-quick" role="group" aria-label="쓴 돈"></div>
          <div class="rw-amt" id="rw-amt" hidden>
            <button type="button" data-d="-10000" aria-label="1만 원 줄이기">−1만</button>
            <label><span class="sr">한 사람이 쓴 돈 (원)</span><input id="cm-total" type="text" inputmode="numeric" autocomplete="off" placeholder="0"><i>원</i></label>
            <button type="button" data-d="10000" aria-label="1만 원 늘리기">+1만</button>
          </div>
          <details class="cm-more cm-rc-wrap"><summary>항목별로 적기 <small>교통·숙박·식비 따로, 선택</small></summary><div class="cm-rc" id="cm-costs"></div></details>
        </section>
        <section class="rw-q">
          <h3 id="rw-kw-h">좋았던 점 <small>여러 개 골라도 돼요</small></h3>
          <div class="rw-kw" id="cm-say" role="group" aria-labelledby="rw-kw-h"></div>
          <h4 class="rw-kw-h2" id="rw-kw-h2">아쉬웠던 점</h4>
          <div class="rw-kw" id="cm-say2" role="group" aria-labelledby="rw-kw-h2"></div>
        </section>
        <section class="rw-q">
          <h3>한마디 <small>안 써도 돼요</small></h3>
          <textarea id="cm-text" rows="3" maxlength="1500" placeholder="다음 사람에게 줄 팁 한 줄이면 충분해요.&#10;예) 해운대는 아침 일찍 가면 한적해요"></textarea>
          <details class="cm-more"><summary>취미 태그 <small>캠핑·낚시·등산 등, 선택</small></summary><div class="chips cm-wrap" id="cm-tagpick"></div></details>
        </section>
      </div>
      <div class="rw-foot" id="rw-foot">
        <p class="rw-paid" id="rv-paid-note">지인 베타 기간이라 공개될 때 맨 위에 "보상을 받고 쓴 후기" 표시가 붙어요. 좋고 나쁨과 상관없이 같은 보상이니 솔직하게 써 주세요.</p>
        <label class="check cm-agree" id="cm-agree-row"><input type="checkbox" id="cm-agree"><span id="cm-agree-txt">직접 다녀온 사실만 골랐어요.</span></label>
        <p class="rv-sm" id="rv-agreed" hidden>처음 쓸 때 동의하셨어요.</p>
        <div class="rv-login" id="rv-login" hidden></div>
        <button type="submit" class="rv-main" id="cm-send">후기 올리기</button>
        <p class="hint rv-msg" id="cm-msg" aria-live="polite"></p>
      </div>
    </form>
    <section class="rw-done" id="rw-done" hidden>
      <div class="rw-done-ic" aria-hidden="true">✓</div>
      <h3 id="rw-done-h">올렸어요. 고마워요!</h3>
      <p class="rv-sm">확인한 뒤 공개돼요. 다음 사람이 경비를 짤 때 큰 도움이 돼요.</p>
      <div class="rv-acts"><button type="button" class="rv-main" id="rv-done-list">다른 사람 후기 보기</button><button type="button" class="rv-sub" id="rv-done">닫기</button></div>
    </section>
    <small class="cm-fine">글의 저작권은 작성자에게 있고, 훌쩍은 서비스 안에서만 보여 줘요. 권리 침해 신고가 들어오면 확인할 때까지 숨길 수 있어요. 얼굴·이름·카드번호는 쓰지 마세요.</small>
  </div>
</div>

''' + s[b:]

# ---------- CSS ----------
css = '''
/* ===== v129 여행 후기 새 화면 ===== */
:root{--star:#f2a100;--star-off:#d8dce3}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--star:#ffc53d;--star-off:#3a404b}}
:root[data-theme="dark"]{--star:#ffc53d;--star-off:#3a404b}
.rl-sum{display:grid;gap:12px;background:var(--ink);color:var(--bg);border-radius:var(--r-lg);padding:18px;margin:14px 0 12px}
.rl-sum-top{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}
.rl-sum-star{font-size:34px;font-weight:800;letter-spacing:-.03em;line-height:1}
.rl-sum-star i{font-style:normal;color:var(--star)}
.rl-sum-n{font-size:15px;opacity:.8}
.rl-sum-diff{margin:0;font-size:15px;line-height:1.5}
.rl-sum-diff b{color:var(--star)}
.rl-sum-cta{border:0;border-radius:14px;background:var(--bg);color:var(--ink);min-height:52px;font-size:17px;font-weight:800;cursor:pointer}
.rl-sum-cta small{font-weight:600;color:var(--muted);margin-left:6px;font-size:13px}
.rl-sum-empty{margin:0;font-size:15px;line-height:1.55}
.rl-filter{margin:0 0 6px}
.rl-filter button small{font-size:12px;opacity:.7;margin-left:2px}
.rl-tagon{margin:2px 0 6px}
.rl-tagon button{border:0;border-radius:999px;background:var(--accent-soft);color:var(--accent);font-weight:700;font-size:14px;min-height:36px;padding:4px 12px;cursor:pointer}
.rl-list{padding-bottom:84px}
.rl-card{gap:10px;padding:16px 16px 12px;box-shadow:0 1px 0 var(--line)}
.rl-card .cm-paid{margin:0;padding:7px 10px;font-size:12.5px;font-weight:600;line-height:1.45;border-left:3px solid var(--muted)}
.rl-top{display:grid;grid-template-columns:42px minmax(0,1fr) auto;gap:10px;align-items:center}
.rl-av{width:42px;height:42px;border-radius:50%;display:grid;place-items:center;background:var(--accent-soft);color:var(--accent);font-weight:800;font-size:17px}
.rl-tt{min-width:0;display:grid;gap:2px}
.rl-tt h3{margin:0;font-size:17px;font-weight:800;letter-spacing:-.02em}
.rl-meta{font-size:12.5px;color:var(--muted);overflow-wrap:anywhere}
.rl-star{font-weight:800;font-size:15px;white-space:nowrap}
.rl-star i{font-style:normal;color:var(--star)}
.rl-mood{font-size:12px;font-weight:700;border-radius:999px;padding:3px 9px;background:var(--surface-2);white-space:nowrap}
.rl-kws{display:flex;flex-wrap:wrap;gap:6px}
.rl-kw{font-size:13px;font-weight:600;border-radius:999px;padding:4px 10px;background:var(--surface-2)}
.rl-kw.bad{background:var(--deal-soft)}
.rl-tag{border:0;font:inherit;font-size:13px;font-weight:600;border-radius:999px;padding:4px 10px;background:var(--accent-soft);color:var(--accent);cursor:pointer}
.rl-money{display:grid;gap:8px;background:var(--surface-2);border-radius:14px;padding:12px 14px}
.rl-money-row{display:flex;justify-content:space-between;align-items:baseline;gap:10px}
.rl-money-row small{font-size:12.5px;color:var(--muted)}
.rl-money-row b{font-size:19px;font-variant-numeric:tabular-nums}
.rl-money-row .est{font-size:14px;font-weight:600;color:var(--muted)}
.rl-bar{position:relative;height:8px;border-radius:99px;background:var(--line);overflow:hidden}
.rl-bar i{position:absolute;left:0;top:0;bottom:0;border-radius:99px;background:var(--accent)}
.rl-bar u{position:absolute;top:-2px;bottom:-2px;width:2px;background:var(--ink);text-decoration:none}
.rl-diff{margin:0;font-size:13px;font-weight:700}
.rl-diff.less{color:var(--accent)}.rl-diff.more{color:var(--deal)}
.rl-acts{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.rl-acts .go{border:0;border-radius:999px;background:var(--ink);color:var(--bg);min-height:42px;padding:6px 16px;font-size:14px;font-weight:700;cursor:pointer}
.rl-acts .sub{border:0;background:none;color:var(--muted);font-size:13px;font-weight:600;min-height:42px;padding:0 6px;cursor:pointer}
.rl-acts .sub.warn{color:var(--deal)}
.rl-acts .sp{flex:1}
.rl-fab{position:sticky;bottom:0;padding:12px 0 calc(env(safe-area-inset-bottom,0px) + 12px);background:linear-gradient(to top,var(--bg) 70%,transparent);margin-top:auto}
.rl-fab[hidden]{display:none}
.rl-fab-b{width:100%;border:0;border-radius:16px;background:var(--accent);color:#fff;min-height:58px;font-size:18px;font-weight:800;cursor:pointer;box-shadow:0 6px 18px rgba(11,122,117,.28)}
.rl-fab-b small{font-size:13px;font-weight:600;opacity:.85;margin-left:4px}
.rl-empty{background:var(--surface);border-radius:var(--r-lg);padding:28px 18px;text-align:center;display:grid;gap:8px;justify-items:center}
.rl-empty b{font-size:17px}.rl-empty span{font-size:14px;color:var(--muted)}
/* 쓰기 */
.rw .rv-head{justify-content:space-between}
.rw-hd{font-size:16px;font-weight:800}
.rw-time{font-size:12.5px;font-weight:700;color:var(--accent);background:var(--accent-soft);border-radius:999px;padding:4px 10px}
.rw-form{display:grid;gap:14px}
.rw-trip{display:grid;grid-template-columns:auto minmax(0,1fr) auto;align-items:center;gap:12px;background:var(--surface);border-radius:var(--r-lg);padding:14px 14px 14px 16px}
.rw-trip-ic{font-size:26px}
.rw-trip-t{display:grid;gap:2px;min-width:0}
.rw-trip-t small{font-size:12.5px;color:var(--muted);font-weight:600}
.rw-trip-t b{font-size:16px;line-height:1.4;overflow-wrap:anywhere}
.rw-link{border:0;border-radius:999px;background:var(--surface-2);color:var(--ink);font-size:14px;font-weight:700;min-height:40px;padding:0 14px;cursor:pointer}
.rw-routebox{background:var(--surface);border-radius:var(--r-lg);padding:14px}
.rw-routedone{border:0;border-radius:12px;background:var(--ink);color:var(--bg);min-height:48px;font-size:15px;font-weight:800;cursor:pointer}
.rw-q{display:grid;gap:10px;background:var(--surface);border-radius:var(--r-lg);padding:18px 16px}
.rw-q h3{margin:0;font-size:20px;font-weight:800;letter-spacing:-.03em}
.rw-q h3 small{font-size:13px;font-weight:600;color:var(--muted);margin-left:6px;letter-spacing:0}
.rw-q-star{text-align:center;justify-items:center;padding:22px 16px}
.rw-stars{display:flex;gap:4px;justify-content:center}
.rw-stars button{width:56px;height:56px;border:0;background:none;padding:0;cursor:pointer;color:var(--star-off);display:grid;place-items:center;border-radius:12px;transition:transform .12s}
.rw-stars button svg{width:46px;height:46px}
.rw-stars button.on{color:var(--star)}
.rw-stars button:active{transform:scale(.9)}
.rw-stars button:focus-visible{outline:3px solid var(--accent);outline-offset:1px}
.rw-star-t{margin:0;font-size:17px;font-weight:800;min-height:1.4em}
.rw-star-t.empty{font-weight:600;color:var(--muted)}
.rw-more{display:grid;gap:14px}
.rw-sm{margin:0;font-size:14px;color:var(--muted)}
.rw-seg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}
.rw-seg button{border:2px solid var(--line);border-radius:14px;background:var(--surface);min-height:64px;padding:6px 4px;font-size:15px;font-weight:700;color:var(--ink);cursor:pointer;display:grid;gap:2px;align-content:center;line-height:1.25}
.rw-seg button small{font-size:12px;font-weight:600;color:var(--muted)}
.rw-seg button[aria-pressed="true"]{border-color:var(--ink);background:var(--ink);color:var(--bg)}
.rw-seg button[aria-pressed="true"] small{color:var(--bg);opacity:.8}
.rw-skip{justify-self:start;border:0;background:none;color:var(--muted);font-size:13px;font-weight:600;text-decoration:underline;padding:4px 0;min-height:36px;cursor:pointer}
.rw-amt{display:grid;grid-template-columns:64px minmax(0,1fr) 64px;gap:8px;align-items:stretch}
.rw-amt button{border:0;border-radius:12px;background:var(--surface-2);font-size:15px;font-weight:800;color:var(--ink);min-height:52px;cursor:pointer}
.rw-amt label{display:flex;align-items:center;gap:4px;border:2px solid var(--ink);border-radius:12px;padding:0 12px;background:var(--surface)}
.rw-amt input{width:100%;min-width:0;border:0;background:transparent;text-align:right;font-size:22px;font-weight:800;color:var(--ink);outline:0;font-variant-numeric:tabular-nums}
.rw-amt i{font-style:normal;font-size:15px;font-weight:700;color:var(--muted)}
.rw-kw{display:flex;flex-wrap:wrap;gap:8px}
.rw-kw button{border:1.5px solid var(--line);border-radius:999px;background:var(--surface);min-height:44px;padding:6px 14px;font-size:15px;font-weight:600;color:var(--ink);cursor:pointer}
.rw-kw button[aria-pressed="true"]{border-color:var(--accent);background:var(--accent-soft);color:var(--accent);font-weight:800}
.rw-kw.bad button[aria-pressed="true"]{border-color:var(--deal);background:var(--deal-soft);color:var(--deal)}
.rw-kw-h2{margin:6px 0 0;font-size:15px;font-weight:800;color:var(--muted)}
.rw-q textarea{width:100%;border:1.5px solid var(--line);border-radius:12px;padding:12px;background:var(--surface-2);font-size:16px;line-height:1.5;color:var(--ink);resize:vertical;min-height:88px}
.rw-q textarea:focus{outline:0;border-color:var(--ink);background:var(--surface)}
.rw-foot{position:sticky;bottom:0;z-index:4;display:grid;gap:8px;padding:12px 0 calc(env(safe-area-inset-bottom,0px) + 10px);background:linear-gradient(to top,var(--bg) 82%,transparent)}
.rw-paid{margin:0;font-size:12.5px;color:var(--muted);line-height:1.45}
.rw-foot .rv-main[aria-disabled="true"]{background:var(--surface-2);color:var(--muted)}
.rw-foot .cm-agree{padding:10px 12px}
.rw-done{display:grid;gap:12px;justify-items:center;text-align:center;padding:40px 0 20px}
.rw-done[hidden]{display:none}
.rw-done-ic{width:76px;height:76px;border-radius:50%;background:var(--accent);color:#fff;display:grid;place-items:center;font-size:40px;font-weight:800}
.rw-done h3{margin:0;font-size:24px;font-weight:800}
.rw-done .rv-acts{width:100%}
.rw .cm-fine{display:block;margin-top:10px}
'''
R('</style>\n\n<header class="top">', css + '</style>\n\n<header class="top">')

open(p, 'w', encoding='utf-8').write(s)
print('html+css ok')
