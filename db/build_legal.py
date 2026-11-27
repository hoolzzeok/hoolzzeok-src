"""훌쩍 개인정보 처리방침(/privacy/)·이용약관(/terms/) 페이지 생성.
사용: python3 build_legal.py [사이트 폴더]
값은 legal.json: {"name": 보호책임자 이름, "email": 연락 이메일, "effective": "YYYY-MM-DD"}
셋 중 하나라도 비면 '작성 중'으로 표시하고 검색 차단(noindex)."""
import json, os, sys, html

OUT = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/www.hoolzzeok.com'
HERE = os.path.dirname(os.path.abspath(__file__))
cfg = json.load(open(os.path.join(HERE, 'legal.json'), encoding='utf-8')) if os.path.exists(os.path.join(HERE, 'legal.json')) else {}
name, email, eff = (cfg.get('name') or '').strip(), (cfg.get('email') or '').strip(), (cfg.get('effective') or '').strip()
ready = bool(name and email and eff)
E = html.escape
NAME = E(name) if name else '<mark>[공개 전 기재]</mark>'
MAIL = f'<a href="mailto:{E(email)}">{E(email)}</a>' if email else '<mark>[공개 전 기재]</mark>'
EFF = E(eff) if eff else '<mark>[공개 전 기재]</mark>'
# v134: 처리방침만 따로 시행일을 둠(약관은 그대로). 이전 판은 legal_archive/privacy-<시행일>.html 을 /privacy/<시행일>/ 에 그대로 보관
PEFF = E((cfg.get('privacy_effective') or eff).strip()) if (cfg.get('privacy_effective') or eff) else EFF
PNOTE = E((cfg.get('privacy_notice') or '').strip())
PPREV = E((cfg.get('privacy_prev') or '').strip())
GIFT_USD = 5

CSS = """:root{--ink:#12302E;--bg:#F8FAF9;--teal:#0B7A75;--line:#CFDCDA;--body:#3d4b50;--soft:#eef3f2}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.75 -apple-system,"Apple SD Gothic Neo","Noto Sans KR",system-ui,sans-serif}
header{border-bottom:2px solid var(--line);padding:14px max(16px,env(safe-area-inset-left))}header a{color:var(--teal);font-weight:800;text-decoration:none;font-size:20px}
main{max-width:760px;margin:0 auto;padding:28px max(16px,env(safe-area-inset-left)) 64px}
h1{font-size:28px;line-height:1.35;margin:0 0 6px}h2{font-size:19px;margin:34px 0 8px}p,li{color:var(--body)}p{margin:0 0 10px}ul,ol{padding-left:22px;margin:0 0 10px}
.wrap{overflow-x:auto;margin:8px 0 12px}table{border-collapse:collapse;width:100%;min-width:560px;font-size:14.5px}th,td{border-bottom:1px solid var(--line);padding:9px 8px;text-align:left;vertical-align:top}th{color:var(--teal)}
.draft{background:#fff4e5;border-radius:12px;padding:12px 14px;font-weight:600;margin:0 0 18px}mark{background:#fff4e5;color:inherit;padding:0 3px}
.meta{font-size:14px;color:#5b6b6e}a{color:var(--teal)}footer{border-top:2px solid var(--line);padding:18px max(16px,env(safe-area-inset-left));font-size:14px;color:#5b6b6e}"""

FOOT_KO = '<footer><a href="/privacy/">개인정보 처리방침</a> · <a href="/privacy/en/">Privacy (English)</a> · <a href="/terms/">이용약관</a> · <a href="/">훌쩍 홈</a></footer>'
FOOT_EN = '<footer><a href="/privacy/en/">Privacy policy</a> · <a href="/privacy/">개인정보 처리방침 (Korean, prevails)</a> · <a href="/">Hoolzzeok home</a></footer>'
def page(path, title, body, lang='ko'):
    url = f'https://www.hoolzzeok.com/{path}/'
    robots = '' if ready else '<meta name="robots" content="noindex">'
    draft = '' if ready else '<p class="draft">작성 중인 문서입니다. 운영자 정보와 시행일을 채운 뒤 정식으로 시행합니다.</p>'
    doc = f"""<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)} | {"Hoolzzeok" if lang == "en" else "훌쩍"}</title>{robots}<link rel="canonical" href="{url}"><meta name="theme-color" content="#0B7A75"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><style>{CSS}</style></head>
<body><header><a href="/">{"Hoolzzeok" if lang == "en" else "훌쩍"}</a></header><main>{draft}{body}</main>
{FOOT_EN if lang == "en" else FOOT_KO}</body></html>"""
    os.makedirs(os.path.join(OUT, path), exist_ok=True)
    open(os.path.join(OUT, path, 'index.html'), 'w', encoding='utf-8').write(doc)

PRIVACY = f"""
<h1>개인정보 처리방침</h1>
<p class="meta">시행일 {PEFF}{f' · <a href="/privacy/{PPREV}/">이전 처리방침({PPREV} 시행)</a> · <a href="/notice/privacy-{PEFF}/">변경 안내</a>' if PPREV else ''}</p>
<p>훌쩍(이하 "서비스")은 「개인정보 보호법」에 따라 이용자의 개인정보를 보호하고 관련 고충을 빠르게 처리하기 위해 이 처리방침을 둡니다.</p>

<h2>1. 처리하는 개인정보, 목적, 보유 기간</h2>
<div class="wrap"><table><thead><tr><th>구분</th><th>항목</th><th>목적</th><th>보유 기간</th></tr></thead><tbody>
<tr><td>경비 계산·추천 (가입 없이)</td><td>서버에 저장하지 않음</td><td>-</td><td>-</td></tr>
<tr><td>가입·로그인 (카카오·구글)</td><td>필수: 로그인 서비스의 회원 식별값, 이메일<br>카카오에서 동의한 경우: 닉네임, 프로필 사진 주소</td><td>회원 구분, 본인 확인, 탈퇴 처리</td><td>탈퇴할 때까지</td></tr>
<tr><td>여행 후기 작성</td><td>출발지, 도착지, 일정, 이동 방법, 인원, 별점, 쓴 돈, 고른 키워드(좋았던 점·아쉬웠던 점)·취미, 직접 쓴 글, 글을 쓴 화면의 언어, 작성일</td><td>후기 게시, 경비 계산을 다듬기 위한 통계(개인을 알아볼 수 없게)</td><td>후기를 지우거나 탈퇴할 때까지</td></tr>
<tr><td>외국인 후기 보상 신청 (선택, 외국어 화면)</td><td>가입 이메일, 신청한 후기, 보상 금액</td><td>미화 {GIFT_USD}달러 디지털 기프트카드 발송, 중복 지급 확인</td><td>신청 표시는 후기를 지우거나 탈퇴할 때까지. 발송 기록은 아래 발송 업체 보관 기간</td></tr>
<tr><td>후기 신고</td><td>신고한 후기, 신고한 회원, 신고 시각</td><td>부적절한 후기 처리</td><td>그 후기가 지워지거나 탈퇴할 때까지</td></tr>
<tr><td>경비 의견 (선택, 가입 없이)</td><td>여행 조건(출발지·도착지·일정·인원·이동 방법·스타일), 계산된 1인 금액, 실제와 비교(더 들었음·비슷함·덜 들었음), 실제 쓴 1인 금액(적은 경우), 화면 언어, 보낸 시각. 이름·연락처·회원 정보는 함께 저장하지 않음</td><td>경비 계산 정확도 개선</td><td>받은 날부터 2년</td></tr>
<tr><td>서비스 이용 중 자동 생성</td><td>접속 IP, 접속 시각, 브라우저 정보</td><td>보안, 장애 확인</td><td>아래 처리 위탁 업체의 기록 보관 기간</td></tr>
</tbody></table></div>
<ul><li>이름, 전화번호, 주소, 생년월일, 결제 정보, 민감정보는 받지 않습니다.</li><li>만 14세 미만은 가입할 수 없습니다.</li><li>정식 사이트에는 AI 답변 기능이 없으며, 입력 내용을 AI에 보내지 않습니다.</li></ul>

<h2>2. 제3자 제공</h2>
<p>이용자의 개인정보를 제3자에게 제공하지 않습니다. 법령에 따라 수사기관 등이 정해진 절차로 요청하는 경우만 예외입니다.</p>

<h2>3. 처리 위탁과 국외 이전</h2>
<p>서비스 운영을 위해 아래 업체에 처리를 맡깁니다. 모두 미국 회사이므로 국외 이전에 해당할 수 있습니다.</p>
<div class="wrap"><table><thead><tr><th>받는 곳 (연락처)</th><th>하는 일</th><th>이전 국가·시기·방법</th><th>항목</th><th>보유 기간</th></tr></thead><tbody>
<tr><td>Supabase Inc. (<a href="https://supabase.com/privacy" target="_blank" rel="noopener">supabase.com/privacy</a>)</td><td>회원 인증, 후기·신고·경비 의견 보관</td><td>저장 위치 대한민국(서울 리전). 미국 회사가 운영. 가입·후기 작성 때 네트워크로 전송</td><td>회원 식별값, 이메일, 닉네임·프로필 사진 주소, 후기, 신고, 접속 기록</td><td>탈퇴·삭제할 때까지, 백업은 업체 보관 주기에 따라 자동 삭제</td></tr>
<tr><td>Cloudflare, Inc. (<a href="https://www.cloudflare.com/privacypolicy/" target="_blank" rel="noopener">cloudflare.com/privacypolicy</a>)</td><td>사이트 전송, 보안</td><td>미국 및 전 세계 데이터센터. 사이트에 접속할 때 네트워크로 전송</td><td>접속 IP, 접속 시각, 브라우저 정보</td><td>업체 기록 보관 기간</td></tr>
<tr><td>Tremendous, LLC (미국 뉴욕, <a href="https://www.tremendous.com/privacy/" target="_blank" rel="noopener">tremendous.com/privacy</a>)</td><td>외국인 후기 보상 기프트카드 발송</td><td>미국. 보상을 신청한 후기가 승인된 뒤, 운영자가 발송 화면에 입력해 네트워크로 전송</td><td>이메일, 보상 금액</td><td>업체 보관 기간</td></tr>
</tbody></table></div>
<p>기프트카드 발송(Tremendous)은 후기 쓰기 화면에서 보상을 직접 고른 사람만 해당합니다. 고르지 않으면 이메일을 보내지 않습니다.</p>
<p>국외 이전을 원하지 않으면 가입하지 않고 이용할 수 있습니다. 이 경우 후기 쓰기 기능만 쓸 수 없습니다. 사이트 접속 자체에는 Cloudflare 전송이 필요합니다.</p>
<p>카카오와 구글은 로그인 수단입니다. 이용자가 그 회사에 로그인하고 동의한 정보만 훌쩍이 받습니다.</p>

<h2>4. 파기</h2>
<ul><li>탈퇴하면 계정, 후기, 신고 기록을 바로 지웁니다.</li><li>카카오계정 페이지에서 훌쩍 연결을 끊어도 훌쩍 계정과 후기는 자동으로 지워지지 않을 수 있습니다. 사이트 맨 위 "내 정보"에서 탈퇴하거나 아래 이메일로 요청하면 바로 지웁니다.</li><li>전자 파일은 복구할 수 없는 방법으로 지웁니다. 업체 백업에 남은 사본은 백업 보관 주기가 끝나면 자동으로 지워집니다.</li></ul>

<h2>5. 이용자의 권리와 행사 방법</h2>
<ul><li>언제든 자신의 개인정보 열람, 정정, 삭제, 처리 정지를 요구할 수 있습니다.</li><li>사이트 맨 위 "내 정보"에서 로그아웃과 탈퇴를 바로 할 수 있습니다. 그 밖의 요청은 아래 연락처로 보내 주시면 10일 안에 처리합니다.</li><li>법정대리인이나 위임받은 사람도 요청할 수 있습니다.</li></ul>

<h2>6. 자동 수집 장치 (브라우저 저장)</h2>
<ul><li>찜 목록, 화면 설정, 쓰던 후기 임시 저장, 로그인 유지 정보는 이용자 브라우저(로컬 저장소)에 저장됩니다. 로그인 유지 정보 말고는 서버로 보내지 않습니다.</li><li>방문 통계·광고 추적 도구는 쓰지 않습니다.</li><li>브라우저 설정에서 사이트 데이터를 지우면 모두 지워집니다. 지우면 로그아웃됩니다.</li></ul>

<h2>7. 안전성 확보 조치</h2>
<ul><li>비밀번호를 받지 않고 카카오·구글 로그인만 씁니다.</li><li>데이터 접근 규칙(행 단위 권한)으로 본인 자료만 고칠 수 있고, 공개 화면에는 작성자 정보를 보여 주지 않습니다.</li><li>관리자 계정에 2단계 인증을 쓰고, 관리 권한을 최소로 둡니다.</li><li>모든 전송 구간을 암호화(HTTPS)합니다.</li><li>개인정보 유출이 의심되면 72시간 안에 이용자와 관계 기관에 알립니다.</li></ul>

<h2>8. 개인정보 보호책임자</h2>
<p>담당: {NAME}<br>이메일: {MAIL}</p>

<h2>9. 권익 침해 구제</h2>
<ul><li>개인정보 분쟁조정위원회: 1833-6972 (www.kopico.go.kr)</li><li>개인정보침해신고센터: 국번 없이 118 (privacy.kisa.or.kr)</li><li>대검찰청: 국번 없이 1301 (www.spo.go.kr)</li><li>경찰청: 국번 없이 182 (ecrm.police.go.kr)</li></ul>

<h2>10. 변경</h2>
<p>이 처리방침을 바꾸면 시행 7일 전에 사이트에 알립니다. 이용자에게 불리한 변경은 30일 전에 알립니다.</p>
<h2>11. 변경 이력</h2>
<ul><li>{PEFF} 시행 ({PNOTE} 안내): 외국인 후기 보상(기프트카드) 신청 항목과 발송 업체(Tremendous) 추가, 후기 항목 이름을 실제 저장에 맞게 고침(별점, 키워드, 글을 쓴 화면의 언어), 영어 요약본 추가. <a href="/notice/privacy-{PEFF}/">자세히</a></li><li>{PPREV} 시행: 처음 제정. <a href="/privacy/{PPREV}/">보기</a></li></ul>
"""

TERMS = f"""
<h1>이용약관</h1>
<p class="meta">시행일 {EFF}</p>
<h2>제1조 목적</h2><p>훌쩍이 제공하는 국내 여행 경비 계산·추천 서비스의 이용 조건을 정합니다.</p>
<h2>제2조 서비스 성격</h2><ol><li>경비, 시간, 요금은 공공데이터와 공개 자료로 계산한 추정치이며 실제와 다를 수 있습니다.</li><li>운영시간, 요금, 행사, 반값여행 같은 지원 정보는 바뀔 수 있으니 이용 전에 해당 기관에 확인하세요.</li><li>훌쩍은 숙박, 교통, 체험을 예약·판매·대행하지 않습니다. 예약은 각 업체에서 이용자가 직접 합니다.</li><li>훌쩍은 정부·지자체의 공식 서비스가 아닙니다.</li></ol>
<h2>제3조 회원</h2><ol><li>경비 계산과 추천은 가입 없이 쓸 수 있습니다.</li><li>후기 쓰기는 카카오·구글 로그인이 필요합니다.</li><li>만 14세 미만은 가입할 수 없습니다.</li><li>언제든 "내 정보"에서 탈퇴할 수 있고, 탈퇴하면 계정과 후기가 지워집니다.</li></ol>
<h2>제4조 광고와 제휴 링크</h2><ol><li>일부 링크는 제휴 링크일 수 있고, 이용자가 구매하면 훌쩍이 수수료를 받을 수 있습니다. 해당 링크에는 표시를 붙입니다.</li><li>광고에는 "광고"와 광고주를 표시합니다.</li></ol>
<h2>제5조 후기</h2><ol><li>직접 다녀온 여행만 쓸 수 있습니다. 대가를 받고 쓴 후기는 그 사실을 밝혀야 하며, 거짓 후기와 다른 사람 글 복사는 금지합니다.</li><li>후기는 운영자 확인 뒤 공개됩니다.</li><li>후기의 저작권은 작성자에게 있습니다. 작성자는 훌쩍이 서비스 안에서 후기를 게시·표시하는 것을 허락합니다.</li><li>욕설, 개인정보 노출, 광고, 불법 내용, 권리 침해 신고가 들어온 후기는 숨기거나 지울 수 있습니다.</li></ol>
<h2>제6조 금지 행위</h2><p>자동 프로그램으로 대량 수집하기, 서비스 방해, 다른 사람 계정 사용, 법령 위반.</p>
<h2>제7조 책임</h2><ol><li>추정치와 실제 비용의 차이, 제휴 업체와 이용자 사이의 거래에 대해 훌쩍은 고의나 중대한 과실이 없으면 책임지지 않습니다.</li><li>무료 서비스이며, 점검이나 장애로 잠시 멈출 수 있습니다.</li></ol>
<h2>제8조 자료 출처</h2><p>한국관광공사, 공공데이터포털 등 공공누리 자료를 쓰며 각 화면에 출처를 표시합니다.</p>
<h2>제9조 문의와 분쟁</h2><p>문의: {MAIL}. 대한민국 법을 따르며, 분쟁은 민사소송법에 따른 관할 법원에서 해결합니다.</p>
<p class="meta">부칙: 이 약관은 {EFF}부터 시행합니다.</p>
"""

PRIVACY_EN = f"""
<h1>Privacy policy (English summary)</h1>
<p class="meta">Effective {PEFF}. This is a summary of the Korean <a href="/privacy/">개인정보 처리방침</a>. If the two differ, the Korean version applies.</p>
<p>Hoolzzeok ("the service") protects your personal information under the Personal Information Protection Act of the Republic of Korea.</p>
<h2>1. What we collect, why, and for how long</h2>
<div class="wrap"><table><thead><tr><th>When</th><th>What</th><th>Why</th><th>How long</th></tr></thead><tbody>
<tr><td>Cost calculator and suggestions (no sign-up)</td><td>Nothing is stored on our servers</td><td>-</td><td>-</td></tr>
<tr><td>Sign-up and sign-in (Kakao, Google)</td><td>Required: the account ID from the sign-in provider, email<br>If you agree on Kakao: nickname, profile picture URL</td><td>Identify members, confirm identity, handle account deletion</td><td>Until you delete your account</td></tr>
<tr><td>Writing a trip review</td><td>Start and destination, trip length, transport, number of people, star rating, money spent, chosen keywords and hobby tags, your text, the language of the page, date</td><td>Publishing the review; statistics to improve cost estimates (not identifying you)</td><td>Until you delete the review or your account</td></tr>
<tr><td>Asking for a review gift card (optional, non-Korean pages)</td><td>Your sign-in email, the review, the gift amount</td><td>Sending a US${GIFT_USD} digital gift card, preventing double payment</td><td>The request mark: until you delete the review or account. Delivery record: as kept by Tremendous</td></tr>
<tr><td>Reporting a review</td><td>The review, the member who reported, time</td><td>Handling inappropriate reviews</td><td>Until the review or your account is deleted</td></tr>
<tr><td>Cost feedback (optional, no sign-up)</td><td>Trip settings (start, destination, length, group size, transport, style), the estimated cost per person, how it compared (more, about the same, less), the actual cost per person if you enter it, page language, time sent. Not linked to any name, contact or account</td><td>Making cost estimates more accurate</td><td>2 years from receipt</td></tr>
<tr><td>Automatically, while you use the site</td><td>IP address, access time, browser information</td><td>Security and troubleshooting</td><td>As kept by the processors below</td></tr>
</tbody></table></div>
<ul><li>We don't collect your name, phone number, address, date of birth, payment details or sensitive information.</li><li>People under 14 can't sign up.</li></ul>
<h2>2. Sharing with third parties</h2><p>We don't give your information to third parties, except when Korean law requires it through proper legal process.</p>
<h2>3. Processors and transfers outside Korea</h2>
<div class="wrap"><table><thead><tr><th>Recipient</th><th>Task</th><th>Where, when, how</th><th>Data</th><th>How long</th></tr></thead><tbody>
<tr><td>Supabase Inc. (<a href="https://supabase.com/privacy" target="_blank" rel="noopener">supabase.com/privacy</a>)</td><td>Sign-in, storing reviews, reports and cost feedback</td><td>Stored in Korea (Seoul region), run by a US company; sent over the network when you sign up or write</td><td>Account ID, email, nickname and picture URL, reviews, reports, access logs</td><td>Until deletion; backups expire on the provider's schedule</td></tr>
<tr><td>Cloudflare, Inc. (<a href="https://www.cloudflare.com/privacypolicy/" target="_blank" rel="noopener">cloudflare.com/privacypolicy</a>)</td><td>Delivering the site, security</td><td>US and data centers worldwide; whenever you open the site</td><td>IP address, access time, browser information</td><td>As kept by the provider</td></tr>
<tr><td>Tremendous, LLC (New York, USA, <a href="https://www.tremendous.com/privacy/" target="_blank" rel="noopener">tremendous.com/privacy</a>)</td><td>Sending review gift cards</td><td>USA; after a review that asked for a gift card is approved, we enter it on their site</td><td>Email, gift amount</td><td>As kept by the provider</td></tr>
</tbody></table></div>
<p>Your email goes to Tremendous only if you tick the gift card box when writing a review.</p>
<p>If you don't want your data transferred, you can use the site without signing up. You just can't write reviews.</p>
<h2>4. Deletion</h2><ul><li>Deleting your account (Account → Delete account) removes your account, reviews and reports right away.</li><li>Unlinking Hoolzzeok on your Kakao account page may not delete your Hoolzzeok data automatically. Delete your account on the site or email us.</li></ul>
<h2>5. Your rights</h2><ul><li>You can ask to see, correct, delete or stop the processing of your information at any time. We answer within 10 days.</li><li>Sign out and account deletion are available under "Account" at the top of the site.</li></ul>
<h2>6. Browser storage</h2><ul><li>Saved places, display settings, review drafts and your sign-in session are kept in your browser. Only the sign-in session is sent to our servers.</li><li>We don't use analytics or ad-tracking tools.</li></ul>
<h2>7. Security</h2><ul><li>No passwords. Sign-in is through Kakao or Google only.</li><li>Row-level access rules: only you can change your data, and public pages never show who wrote a review.</li><li>All connections are encrypted (HTTPS). If we suspect a leak, we notify you and the authorities within 72 hours.</li></ul>
<h2>8. Contact</h2><p>Privacy contact: {NAME}<br>Email: {MAIL}</p>
<h2>9. Help in Korea</h2><ul><li>Personal Information Dispute Mediation Committee: +82-1833-6972 (www.kopico.go.kr)</li><li>Personal Information Infringement Report Center: 118 (privacy.kisa.or.kr)</li></ul>
<h2>10. Changes</h2><p>We announce changes 7 days before they take effect, or 30 days before changes that affect you negatively.</p>
<ul><li>{PEFF} (announced {PNOTE}): added optional review gift cards and the delivery provider (Tremendous); renamed review items to match what we store; added this English summary. <a href="/notice/privacy-{PEFF}/">Details (Korean and English)</a></li><li>{PPREV}: first version (Korean only).</li></ul>
"""
NOTICE = f"""
<h1>개인정보 처리방침 변경 안내</h1>
<p class="meta">안내일 {PNOTE} · 시행일 {PEFF}</p>
<p>훌쩍 개인정보 처리방침이 {PEFF}부터 아래와 같이 바뀝니다. 이용자에게 불리한 변경은 없습니다. 바뀐 내용에 동의하지 않으면 사이트 맨 위 "내 정보"에서 언제든 탈퇴할 수 있습니다.</p>
<div class="wrap"><table><thead><tr><th>바뀌는 곳</th><th>전 ({PPREV} 시행)</th><th>후 ({PEFF} 시행)</th></tr></thead><tbody>
<tr><td>1. 처리 항목: 외국인 후기 보상 신청 (새로)</td><td>없음</td><td>외국어 화면에서 후기를 쓰며 보상을 직접 고른 경우만: 가입 이메일, 신청한 후기, 보상 금액. 목적: 미화 {GIFT_USD}달러 디지털 기프트카드 발송</td></tr>
<tr><td>3. 처리 위탁·국외 이전 (추가)</td><td>Supabase, Cloudflare</td><td>+ Tremendous, LLC (미국): 기프트카드 발송. 이메일·보상 금액. 보상을 고른 사람만</td></tr>
<tr><td>1. 후기 작성 항목 이름</td><td>어땠는지, 고른 한마디</td><td>별점, 고른 키워드(좋았던 점·아쉬웠던 점), 글을 쓴 화면의 언어 (실제 저장하는 것에 맞춰 이름을 고침. 새로 받는 정보 아님)</td></tr>
<tr><td>영어 요약본</td><td>없음</td><td><a href="/privacy/en/">/privacy/en/</a> 추가 (한국어판이 우선)</td></tr>
<tr><td>11. 변경 이력 (새로)</td><td>없음</td><td>이전 판 보기 링크</td></tr>
</tbody></table></div>
<p><a href="/privacy/">바뀐 처리방침 전문</a> · <a href="/privacy/{PPREV}/">이전 처리방침</a></p>
<p>문의: {MAIL}</p>
<h2 lang="en">Privacy policy update (English)</h2>
<div lang="en"><p>From {PEFF}, our privacy policy changes as follows. Nothing changes to your disadvantage. If you don't agree, you can delete your account at any time under "Account" at the top of the site.</p>
<ul><li>New, optional: if you write a review on a non-Korean page and tick the gift card box, we use your sign-in email to send a US${GIFT_USD} digital gift card through Tremendous, LLC (USA).</li>
<li>Review items are renamed to match what we actually store (star rating, keywords, page language). We don't collect anything new.</li>
<li>Added an English summary: <a href="/privacy/en/">/privacy/en/</a> (the Korean version prevails).</li></ul></div>
"""
page('privacy', '개인정보 처리방침', PRIVACY)
page(f'notice/privacy-{PEFF}', '개인정보 처리방침 변경 안내', NOTICE)
_arch = os.path.join(HERE, 'legal_archive', f'privacy-{PPREV}.html')
if PPREV and os.path.exists(_arch):
    old = open(_arch, encoding='utf-8').read()
    old = old.replace('<link rel="canonical" href="https://www.hoolzzeok.com/privacy/">', f'<meta name="robots" content="noindex"><link rel="canonical" href="https://www.hoolzzeok.com/privacy/">', 1)
    old = old.replace('<main>', f'<main><p class="draft">이전 처리방침입니다({PPREV} 시행, {PEFF} 전날까지 적용). 지금 처리방침은 <a href="/privacy/">여기</a>.</p>', 1)
    os.makedirs(os.path.join(OUT, 'privacy', PPREV), exist_ok=True)
    open(os.path.join(OUT, 'privacy', PPREV, 'index.html'), 'w', encoding='utf-8').write(old)
page('terms', '이용약관', TERMS)
page('privacy/en', 'Privacy policy', PRIVACY_EN, 'en')
print('legal', 'ready' if ready else 'draft')
