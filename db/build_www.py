"""훌쩍 정식판(자체 도메인) 빌드: Claude 페이지용 index.html을 독립 웹페이지로 감싸고 img/와 기본 파일을 만든다.
Claude 전용 기능(AI 요원 질문, Claude 음성, 음성 입력, 후기 DB)은 window.claude가 없으면 자동으로 숨거나 기기 기능으로 바뀐다."""
import os, re, shutil, sys
SRC = '/home/claude/hoolzzeok_site'
OUT = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/hoolzzeok_www'
SITE = 'https://www.hoolzzeok.com'
os.makedirs(OUT, exist_ok=True)
body = open(f'{SRC}/index.html', encoding='utf-8').read()
body = body.replace('<title>훌쩍</title>\n', '').replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
for key in [k for k in (os.environ.get('TOURAPI_KEY', '')[:16], os.environ.get('DATA_KEY', '')[:16]) if k] + ['serviceKey=']:   # 키는 파일에 적지 않고 환경변수에서만 비교
    assert key not in body, f'secret-like text found: {key}'
desc = '출발지와 도착지만 넣으면 국내여행 1인 예상 경비가 바로 나와요. 교통·숙박·식비·현지 교통을 공공데이터로 계산하고, 시니어 큰 글씨 모드와 영어·일본어·중국어 화면을 지원해요.'
head = f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>훌쩍 | 국내여행 경비 계산기</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="훌쩍">
<meta property="og:title" content="훌쩍 | 국내여행, 얼마 들까?">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE}/">
<meta property="og:locale" content="ko_KR">
<meta name="theme-color" content="#0B7A75">
<meta name="naver-site-verification" content="d8f46a25f8edebbe20448fe0b5b4d7b45c6ebd60" />
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"WebApplication","name":"훌쩍","alternateName":"Hoolzzeok","url":"{SITE}/","applicationCategory":"TravelApplication","operatingSystem":"Web","inLanguage":["ko","en","ja","zh"],"description":"{desc}","offers":{{"@type":"Offer","price":"0","priceCurrency":"KRW"}}}}</script>
<style>:root{{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0;font:14px system-ui,sans-serif}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
</head>
<body>
'''
import json as _j
_sc = _j.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'supa_config.json'))) if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'supa_config.json')) else {'on': False, 'url': '', 'key': ''}
assert 'service_role' not in _j.dumps(_sc), 'service_role key must never go in the site'
head = head.replace('<body>', '<body>\n<script>window.HZ_SUPA=' + _j.dumps({'on': bool(_sc.get('on')), 'url': _sc.get('url', ''), 'key': _sc.get('key', ''), 'providers': _sc.get('providers', ['google']), 'fb': bool(_sc.get('feedback'))}) + ';</script>', 1)
open(f'{OUT}/index.html', 'w', encoding='utf-8').write(head + body + '\n<nav class="sfoot" aria-label="더 보기"><a class="sfoot-main" href="/gyeongbi/"><i class="ico ico-receipt" aria-hidden="true"></i>구간별 1박 2일 경비 모아보기<i class="ico" style="--i:var(--chev)" aria-hidden="true"></i></a><div class="sfoot-row"><a href="/en/korea-itinerary/" lang="en">Korea itineraries</a><a href="/ja/korea-itinerary/" lang="ja">韓国モデルコース</a><a href="/zh-tw/korea-itinerary/" lang="zh-Hant">韓國行程</a></div><div class="sfoot-row sfoot-legal"><a href="/privacy/">개인정보 처리방침</a><a href="/terms/">이용약관</a><a href="/privacy/en/">Privacy</a></div><p class="sfoot-mail">문의 <a href="mailto:help@hoolzzeok.com">help@hoolzzeok.com</a></p></nav>\n</body>\n</html>\n')
# v113: 지자체 누리집 끼워 넣기 화면 (검색 노출 안 함, 로그인·후기 끔)
os.makedirs(f'{OUT}/embed', exist_ok=True)
eh = head.replace(f'<link rel="canonical" href="{SITE}/">', f'<link rel="canonical" href="{SITE}/">\n<meta name="robots" content="noindex">')
eh = re.sub(r'<script>window.HZ_SUPA=.*?</script>', '<script>window.HZ_SUPA={"on":false};window.HZ_EMBED=1;</script>', eh, flags=re.S)
eh = eh.replace('<title>훌쩍 | 국내여행 경비 계산기</title>', '<title>여행 경비 계산기 | 훌쩍</title>')
open(f'{OUT}/embed/index.html', 'w', encoding='utf-8').write(eh + body.replace('src="img/', 'src="/img/').replace('"img/', '"/img/') + '\n</body>\n</html>\n')
open(f'{OUT}/llms.txt', 'w', encoding='utf-8').write(f'''# 훌쩍 (Hoolzzeok)

> 국내여행 1인 예상 경비 계산기. 출발지·도착지·박수·인원·이동 수단으로 교통·숙박·식비·현지 교통·체험·기념품을 계산한다. 버스 요금은 국토교통부 TAGO 실제 요금, 식비는 한국소비자원 참가격, 날씨는 기상청 평년값, 반값여행은 한국관광공사 공식 안내 기준. 금액은 예상치다.

## 구간별 1박 2일 경비
- [전체 목록]({SITE}/gyeongbi/): 서울·부산·대구·광주·대전 출발 50개 구간, 교통 방법별·여행 스타일별 1인 경비

## 계산기
- [훌쩍 계산기]({SITE}/): 주소 형식 {SITE}/?from=seoul&to=gangneung&nights=1&people=2
''')
if os.path.isdir(f'{OUT}/img'): shutil.rmtree(f'{OUT}/img')
shutil.copytree(f'{SRC}/img', f'{OUT}/img')
m = re.search(r'<svg class="logo-mark"[^>]*>(.*?)</svg>', body, re.S)
fav = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">' + (m.group(1).replace('var(--accent)', '#0B7A75') if m else '<circle cx="100" cy="100" r="98" fill="#0B7A75"/>') + '</svg>'
open(f'{OUT}/favicon.svg', 'w', encoding='utf-8').write(fav)
open(f'{OUT}/robots.txt', 'w').write(f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n')
open(f'{OUT}/sitemap.xml', 'w').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n<url><loc>{SITE}/</loc></url>\n</urlset>\n')
open(f'{OUT}/_headers', 'w').write('/img/*\n  Cache-Control: public, max-age=31536000, immutable\n/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  X-Frame-Options: SAMEORIGIN\n/embed/*\n  ! X-Frame-Options\n  Content-Security-Policy: frame-ancestors *\n/embed/\n  ! X-Frame-Options\n  Content-Security-Policy: frame-ancestors *\n')
open(f'{OUT}/README.md', 'w', encoding='utf-8').write('# 훌쩍 (hoolzzeok.com)\n\n국내여행 1인 경비 계산 사이트. 정적 파일만 있으며 Cloudflare Pages가 이 저장소를 그대로 배포합니다.\n\n- index.html: 사이트 전체 (데이터 포함)\n- img/: 관광공사 사진 (공공누리 1유형, 출처 표시)\n- 빌드 명령 없음, 출력 폴더는 저장소 최상위(/)\n')
print('built', OUT, os.path.getsize(f'{OUT}/index.html'), len(os.listdir(f'{OUT}/img')), 'imgs')
