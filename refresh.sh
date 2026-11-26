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
TOURAPI_KEY=${TOURAPI_KEY:-${DATA_KEY:-}}; export TOURAPI_KEY   # 두 키는 같은 data.go.kr 일반 인증키
[ -n "${DATA_KEY:-}" ] && [ -n "${TOURAPI_KEY:-}" ] || { echo "실패: 환경변수 DATA_KEY·TOURAPI_KEY 없음"; exit 2; }
[ -d "$WWW/.git" ] || { echo "실패: 사이트 저장소($WWW) 없음"; exit 2; }
# 스크립트들이 쓰는 고정 경로
for p in hoolzzeok_db:db hoolzzeok_site:site tests:tests; do
  t=/home/claude/${p%%:*}; s=$SRC/${p##*:}
  if [ -L "$t" ] || [ ! -e "$t" ]; then ln -sfn "$s" "$t"; elif [ "$(readlink -f "$t")" != "$s" ]; then echo "실패: $t 가 이미 있음(다른 폴더)"; exit 2; fi
done
npm ls -g opencc-js >/dev/null 2>&1 || npm i -g opencc-js@1.0.5 >/dev/null 2>&1
export SKIP_SYNC=1   # 방금 받은 데이터가 최신이므로 build_all의 가져오기 생략
cd "$SRC/db"
log "날씨"; (cd weather && python3 fetch_weather.py | tail -1)
if [ "$MODE" = weekly ]; then
  log "혼잡 예측"; (cd crowd && python3 fetch_crowd.py | tail -1)
  log "KTX"; (cd train && python3 fetch_train.py | tail -1)
  Y=$(TZ=Asia/Seoul date +%Y); log "공휴일"; (cd holiday && python3 fetch_holiday.py "$Y" "$((Y+1))" | head -1)
fi
python3 crowd/build_qtdata.py
log "사이트 만들기"; bash build_all.sh "$WWW" | tail -1
log "점검"
cd "$SRC/tests"
R1=$(timeout 1500 node qt4.js 2>&1 | grep -v '^    at' | grep 'checked' | tail -1 || true)
R2=$(timeout 400 node csp.js 2>&1 | grep 'VIOLATIONS' || true)
echo "  $R1 / $R2"
echo "$R1" | grep -q 'bad 0' && echo "$R2" | grep -q 'VIOLATIONS 0' || { echo "실패: 점검 통과 못 함 → 배포 안 함"; exit 3; }
safe(){ # 커밋 직전: 인증키 값 자체가 섞였으면 중단
  if git diff --cached -U0 | grep -qF -- "$DATA_KEY" || git diff --cached -U0 | grep -qF -- "$TOURAPI_KEY"; then echo "실패: 인증키가 파일에 섞임 → 커밋 안 함"; git reset -q; exit 4; fi; }
[ "$DRY" = --dry ] && { echo "점검 통과(--dry라 배포 안 함)"; exit 0; }
if [ "${SKIP_SRC_PUSH:-}" = 1 ]; then   # GitHub Actions: 원본 저장소엔 못 올리므로 받은 데이터를 사이트 저장소에 같이 보관(다음 수동 빌드가 이걸 씀)
  mkdir -p "$WWW/.github/srcdata"; for f in weather/weather.json crowd/crowd.json crowd/crowd_names.json holiday/holidays.json train/train.json; do
    mkdir -p "$WWW/.github/srcdata/$(dirname $f)"; cp "$SRC/db/$f" "$WWW/.github/srcdata/$f"; done
fi
cd "$WWW"; git add -A; safe
if git diff --cached --quiet; then echo "바뀐 것 없음"; else
  git -c user.name="hoolzzeok-bot" -c user.email="hoolzzeok-bot@users.noreply.github.com" commit -q -m "자동 갱신($MODE): 공공데이터 $(TZ=Asia/Seoul date +%F)"; git -c push.negotiate=true push -q origin HEAD 2>&1 | grep -v 'moved\|new location' || true; log "배포함 $(git rev-parse --short HEAD)"; fi
[ "${SKIP_SRC_PUSH:-}" = 1 ] && { echo "완료"; exit 0; }
cd "$SRC"; git add -A; safe
if ! git diff --cached --quiet; then git -c user.name="hoolzzeok-bot" -c user.email="hoolzzeok-bot@users.noreply.github.com" commit -q -m "자동 갱신($MODE) 데이터 $(TZ=Asia/Seoul date +%F)"; git -c push.negotiate=true push -q origin HEAD 2>&1 | grep -v 'moved\|new location' || true; fi
echo "완료"
