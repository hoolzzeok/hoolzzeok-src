#!/usr/bin/env python3
"""v142 보안 헤더 + 외부 라이브러리 사본. build_all.sh 맨 끝에서 실행(모든 페이지가 만들어진 뒤).
- vendor/ 사본을 사이트에 복사(supabase-js MIT, SheetJS CE Apache-2.0, 라이선스 파일 함께)
- 페이지 안 스크립트(<script> 본문)의 sha256을 모아 CSP에 넣음 → 그 밖의 스크립트는 실행 안 됨
- Cloudflare Web Analytics(켜면 자동 삽입)도 허용"""
import base64, glob, hashlib, os, re, shutil, sys
OUT = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/www.hoolzzeok.com'
SB = 'https://ppymgfvjtrtcatedhfxu.supabase.co'
os.makedirs(f'{OUT}/vendor', exist_ok=True)
for f in glob.glob('/home/claude/hoolzzeok_db/vendor/*'): shutil.copy(f, f'{OUT}/vendor/')
hashes = set()
for f in glob.glob(f'{OUT}/**/*.html', recursive=True):
    for m in re.finditer(r'<script([^>]*)>(.*?)</script>', open(f, encoding='utf-8').read(), re.S):
        a, body = m.group(1), m.group(2)
        if 'src=' in a or 'ld+json' in a: continue
        hashes.add("'sha256-" + base64.b64encode(hashlib.sha256(body.encode('utf-8')).digest()).decode() + "'")
CF = 'https://static.cloudflareinsights.com'
def csp(frame):
    return '; '.join([
        "default-src 'self'",
        "script-src 'self' " + ' '.join(sorted(hashes)) + f" {CF}",
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
        "font-src 'self' https://fonts.gstatic.com data:",
        "img-src 'self' data: blob:",
        f"connect-src 'self' {SB} {SB.replace('https', 'wss')} https://cloudflareinsights.com",
        "object-src 'none'", "base-uri 'self'", "form-action 'self'", f"frame-ancestors {frame}", "upgrade-insecure-requests"])
common = ('  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n'
          '  Strict-Transport-Security: max-age=31536000\n'
          '  Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=()\n')
H = ('/img/*\n  Cache-Control: public, max-age=31536000, immutable\n'
     '/vendor/*\n  Cache-Control: public, max-age=31536000, immutable\n'
     '/*\n' + common + '  X-Frame-Options: SAMEORIGIN\n  Content-Security-Policy: ' + csp("'self'") + '\n')
# 퍼가기(/embed)는 다른 사이트 안에 넣을 수 있게: 앞 규칙의 두 헤더를 먼저 떼고(파일 순서대로 적용), 다음 블록에서 새로 붙임
for path in ('/embed/*', '/embed/'):
    H += f'{path}\n  ! X-Frame-Options\n  ! Content-Security-Policy\n'
for path in ('/embed/*', '/embed/'):
    H += f'{path}\n  Content-Security-Policy: ' + csp('*') + '\n'
assert max(len(l) for l in H.split('\n')) < 2000   # Cloudflare: 한 줄 2,000자 제한
open(f'{OUT}/_headers', 'w').write(H)
print('headers: inline scripts', len(hashes), 'bytes', len(H))
