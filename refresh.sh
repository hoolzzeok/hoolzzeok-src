#!/bin/bash
# 훌쩍 자동 갱신: 공공데이터 다시 받기 → 사이트 만들기 → 점검 → (통과하면) 배포
# 쓰는 법: bash refresh.sh daily|weekly [--dry]   (DATA_KEY·TOURAPI_KEY 환경변수 필요. 키는 화면·파일에 쓰지 않음)
#   daily : 기상청 날씨
#   weekly: 날씨 + 관광지 혼잡 예측 + KTX 시간표 + 공휴일
# 점검(딸깍 950개, 보안 헤더 위반 0)에서 하나라도 실패하면 배포하지 않고 멈춤.
set -euo pipefail
MODE=${1:-daily}; DRY=${2:-}
SRC=$(cd "$(dirname "$0")" && pwd)
WWW=${WWW:-/home/claude/www.hoolzzeok.com}
log(){ echo "[$(TZ=Asia/Seoul date +%H:%M)] $*"; }
[ -n "${DATA_KEY:-}" ] && [ -n "${TOURAPI_KEY:-}" ] || { echo "실패: 환경변수 DATA_KEY·TOURAPI_KEY 없음"; exit 2; }
[ -d "$WWW/.git" ] || { echo "실패: 사이트 저장소($WWW) 없음"; exit 2; }
# 스크립트들이 쓰는 고정 경로
for p in hoolzzeok_db:db hoolzzeok_site:site tests:tests; do
  t=/home/claude/${p%%:*}; s=$SRC/${p##*:}
  if [ -L "$t" ] || [ ! -e "$t" ]; then ln -sfn "$s" "$t"; elif [ "$(readlink -f "$t")" != "$s" ]; then echo "실패: $t 가 이미 있음(다른 폴더)"; exit 2; fi
done
npm ls -g opencc-js >/dev/null 2>&1 || npm i -g opencc-js@1.0.5 >/dev/null 2>&1
cd "$SRC/db"
log "날씨"; python3 weather/fetch_weather.py | tail -1
if [ "$MODE" = weekly ]; then
  log "혼잡 예측"; python3 crowd/fetch_crowd.py | tail -1
  log "KTX"; python3 train/fetch_train.py | tail -1
  Y=$(TZ=Asia/Seoul date +%Y); log "공휴일"; python3 holiday/fetch_holiday.py "$Y" "$((Y+1))" | head -1
fi
python3 crowd/build_qtdata.py
log "사이트 만들기"; bash build_all.sh "$WWW" | tail -1
log "점검"
cd "$SRC/tests"
R1=$(timeout 1500 node qt4.js 2>&1 | grep -v '^    at' | grep 'checked' | tail -1 || true)
R2=$(timeout 400 node csp.js 2>&1 | grep 'VIOLATIONS' || true)
echo "  $R1 / $R2"
echo "$R1" | grep -q 'bad 0' && echo "$R2" | grep -q 'VIOLATIONS 0' || { echo "실패: 점검 통과 못 함 → 배포 안 함"; exit 3; }
[ "$DRY" = --dry ] && { echo "점검 통과(--dry라 배포 안 함)"; exit 0; }
cd "$WWW"; git add -A
if git diff --cached --quiet; then echo "바뀐 것 없음"; else
  git -c user.name="hoolzzeok-bot" -c user.email="hoolzzeok-bot@users.noreply.github.com" commit -q -m "자동 갱신($MODE): 공공데이터 $(TZ=Asia/Seoul date +%F)"; git push -q origin HEAD 2>&1 | grep -v 'moved\|new location' || true; log "배포함 $(git rev-parse --short HEAD)"; fi
cd "$SRC"; git add -A
if ! git diff --cached --quiet; then git -c user.name="hoolzzeok-bot" -c user.email="hoolzzeok-bot@users.noreply.github.com" commit -q -m "자동 갱신($MODE) 데이터 $(TZ=Asia/Seoul date +%F)"; git -c push.negotiate=true push -q origin HEAD 2>&1 | grep -v 'moved\|new location' || true; fi
echo "완료"
