#!/bin/bash
# 사이트 전체 빌드: 본문 + 검색용 경비 페이지. 결과는 /home/claude/www.hoolzzeok.com
set -e
OUT=${1:-/home/claude/www.hoolzzeok.com}
cd /home/claude/hoolzzeok_db
python3 tidy_data.py /home/claude/hoolzzeok_site/index.html   # v132 공공데이터 글 다듬기(멱등)
NODE_PATH=$(npm root -g) node gen_zhtw.cjs /home/claude/hoolzzeok_site/index.html   # v133 번체 사전(멱등)
python3 build_www.py "$OUT"
NODE_PATH=$(npm root -g) node build_seo.js "$OUT"
NODE_PATH=$(npm root -g) node build_trip.js "$OUT"   # v135 외국인 일정·경비 페이지(영·일·번체), 사이트맵에 덧붙임
python3 build_legal.py "$OUT"
python3 build_headers.py "$OUT"   # v142 보안 헤더(CSP 해시)·라이브러리 사본. 반드시 마지막
