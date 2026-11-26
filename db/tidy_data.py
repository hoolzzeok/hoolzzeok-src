"""v132 공공데이터 글 다듬기 (멱등): 주소·접근성 글의 겹친 공백, 끝의 ' .'·' -', '..', 반복된 행정구역('광양시 광양시'),
쉼표 앞 공백, 영어 관광 소개가 단어 중간에서 잘린 것('…' 앞 단어 자르기), 출처 오타 renowed.
데이터를 다시 만드는 스크립트(build_menu, build_century, build_lodging 등)를 돌린 뒤에도 build_all.sh 가 자동으로 다시 적용함."""
import re, json, sys
P = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/hoolzzeok_site/index.html'
s = open(P, encoding='utf-8').read()
def tidy(x, addr):
    t = re.sub(r'[ \t　]{2,}', ' ', x)
    t = re.sub(r'\s+,', ',', t)
    t = re.sub(r'\s+[.\-]\s*$', '', t)
    t = re.sub(r'(?<!\.)\.\.(?!\.)', '.', t)
    if addr:
        for _ in range(2): t = re.sub(r'(?:(?<=^)|(?<=\s))(\S{2,}) \1(?=\s|$)', r'\1', t)
    return t.strip()
def fix_en(t):
    # 단어 중간에서 잘린 '…'는 처음 한 번만 고침(v132, 원본에 표시를 남겨 다시 안 자름): 끝이 '\u2060…'면 이미 고친 것
    if re.search(r'[A-Za-z]…$', t) and not t.endswith('\u2060…'): t = re.sub(r'[\s,;:]*\S*…$', '\u2060…', t)
    t = t.replace('renowed', 'renowned')
    if t.count('(') > t.count(')'):
        t = t[:-len(' (alt.')].rstrip() + '.' if t.endswith('(alt.') else re.sub(r'\s*\([^)]*$', '', t)
    return t
total = {}
for name in ['GOOD', 'CENTURY', 'GOOD_STAY', 'ACC', 'TOUR', 'TOUR_I18N']:
    pre = 'const %s = ' % name
    if '\n' + pre not in s: continue
    i = s.index('\n' + pre) + 1; j = s.index('\n', i); line = s[i:j]
    semi = line.rstrip().endswith(';')
    obj = json.loads(line[len(pre):].rstrip().rstrip(';')); n = [0]
    def walk(x, en=False):
        if isinstance(x, str):
            y = fix_en(x) if en else tidy(x, bool(re.search(r'\d', x) and re.search(r'(구|시|군|로|길|동|읍|면)\b', x)))
            if y != x: n[0] += 1
            return y
        if isinstance(x, list): return [walk(v, en) for v in x]
        if isinstance(x, dict): return {k: walk(v, en or (name == 'TOUR_I18N' and k == 'en')) for k, v in x.items()}
        return x
    obj = walk(obj)
    s = s[:i] + pre + json.dumps(obj, ensure_ascii=False, separators=(',', ':')) + (';' if semi else '') + s[j:]
    total[name] = n[0]
open(P, 'w', encoding='utf-8').write(s)
print('tidy', total)
