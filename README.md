# hoolzzeok-src (비공개)

훌쩍(www.hoolzzeok.com) 원본. 사이트 저장소에는 완성본만 올라가고, 여기에는 만드는 프로그램과 데이터가 있음.

- `site/index.html` — 사이트 본문(한 파일). 공공데이터는 빌드 때 이 안에 들어감
- `db/` — 데이터 받기·정리·빌드 스크립트 (`db/build_all.sh`가 전체 빌드)
- `tests/` — 점검(딸깍 조합, 화면, 보안 헤더)
- `refresh.sh daily|weekly [--dry]` — 자동 갱신(예약 작업이 실행)

규칙
- 인증키는 파일에 쓰지 않음. 환경변수 `DATA_KEY`, `TOURAPI_KEY`(같은 data.go.kr 일반 인증키)
- 점검을 통과해야만 배포
- 원본 공공데이터 덩어리(raw/), 받은 파일(inbox/)은 올리지 않음
