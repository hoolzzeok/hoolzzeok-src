"""v159: Lucide(ISC) 아이콘을 CSS mask용 data URI로 만든다. 출력: db/ui/icons.css (index.html의 v159 블록에 붙임)
사용: <i class="ico ico-이름" aria-hidden="true"></i> — 글자색을 따라감."""
import re, sys, urllib.parse, os
SRC = sys.argv[1] if len(sys.argv) > 1 else '/tmp/lu/node_modules/lucide-static/icons'
NAMES = """sliders-horizontal pen-line user-round luggage check landmark soup armchair shopping-bag mic-vocal waves house moon-star castle sunrise leaf fish coffee compass utensils chart-column trash-2 mail bell-off shield-check megaphone x piggy-bank scale message-circle-question circle-check bus bed-double car-taxi-front ticket receipt coins mountain-snow camera baby heart-handshake backpack repeat credit-card languages wallet users construction bed car cloud-rain banknote smartphone gift star calendar-plus plus sun cloud-sun cloud cloud-snow headphones umbrella triangle-alert sheet copy share-2 flag train-front wifi chevron-right message-circle hotel train-front-tunnel shirt accessibility""".split()
out = ['.ico{display:inline-block;width:1.15em;height:1.15em;flex:none;vertical-align:-.2em;background:currentColor;-webkit-mask:var(--i) center/contain no-repeat;mask:var(--i) center/contain no-repeat}']
def uri(svg):
    return 'url("data:image/svg+xml,' + urllib.parse.quote(svg, safe=" =:/'-.,") + '")'
for n in NAMES:
    s = open(os.path.join(SRC, n + '.svg')).read()
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    s = re.sub(r'\s*class="[^"]*"', '', s)
    s = re.sub(r'\s+', ' ', s).replace('> <', '><').strip().replace('"', "'")
    s = s.replace("stroke='currentColor'", "stroke='black'")
    out.append(f'.ico-{n}{{--i:{uri(s)}}}')
    if n == 'star':
        out.append(f".ico-star-f{{--i:{uri(s.replace(chr(39)+'none'+chr(39), chr(39)+'black'+chr(39), 1))}}}")
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icons.css'), 'w').write('\n'.join(out) + '\n')
print(len(NAMES), sum(len(x) for x in out))
