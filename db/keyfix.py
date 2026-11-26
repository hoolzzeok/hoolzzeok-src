"""공공데이터포털 인증키: Decoding(원래 값)·Encoding(%가 든 값) 어느 것을 넣어도 주소에는 한 번만 인코딩해서 붙이도록."""
import os, urllib.parse
def key(name):
    k = os.environ[name].strip()
    return k if '%' in k else urllib.parse.quote(k, safe='')
