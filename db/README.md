# 훌쩍 데이터베이스 v2 (2026-11-13)

사이트(v49)에 들어 있던 모든 자료를 표 39개로 나눠 옮긴 것. Supabase(PostgreSQL)에 그대로 넣을 수 있다.

## 넣는 순서
1. `schema/01_schema.sql` — 표 39개, 보기 7개
2. `schema/02_supabase_rls.sql` — 접근 규칙(공개 자료는 읽기만, 후기는 승인된 것만 공개)
3. `schema/03_load_seed.psql` — `seed/` 의 CSV 30개 적재 (psql로 실행)
4. `schema/04_budget_function.sql` — 경비 계산 함수 `fn_trip_budget()`

예: `SELECT * FROM fn_trip_budget('seoul','goheung',1,'standard','transit',11,true);`
→ 교통 64,000 / 숙박 29,000 / 식비 86,000 / 현지 14,000 / 기념품 24,000 = 217,000원, 반값 환급 후 117,000원

## 검증 결과 (로컬 PostgreSQL 16)
- 표·제약(외래키, 값 범위) 위반 없이 적재 완료, 15MB
- 사이트 계산기와 DB 함수 비교: 무작위 798건(대중교통·자차·배 588건 + 항공 210건) 전부 원 단위까지 일치

## 표 구성
| 묶음 | 표 |
|---|---|
| 출처 | data_sources (22개 출처, 신뢰도 A 5 / B 14 / C 3) |
| 지역 | provinces, places, place_profiles, place_spots, place_foods |
| 때가 있는 정보 | events, agent_picks, season_products·months·places, activities, contests, souvenirs, official_malls |
| 가격 | lodging_rates, dorm_bed_rates, food_prices, meal_baskets, city_bus_fares, taxi_fares, flight_fares, ferry_fares, intercity_bus_fares(빈 표), cost_params, fx_rates |
| 착한가격 | goodprice_eateries·menus, goodprice_stays·stay_rates |
| 수익 | checklist_items, affiliate_links, ads, ad_events |
| 사용자 | reviews, review_costs, review_reports, content_rewards (개인정보 칸 없음) |
| 운영 | job_log |

## 이번에 세분화·정밀화한 것
- 밥집 9,364곳에 세부 분류 12개(국밥·탕·찌개 / 면 / 고기구이 / 백반·정식 / 해산물 / 치킨·돈가스 / 분식 / 카페·디저트 / 중식 / 일식 / 양식 / 기타)
- 밥집·숙소 주소를 구·군 / 읍·면·동 / 도로명으로 나눔 → 숙소와 같은 동네 밥집 673쌍(숙소 103곳)
- "한 끼 최저가"를 끼니 메뉴만으로 다시 계산(김밥 한 줄·공기밥·음료·간식 제외), 가격대 4단계
- 입력 오류 정리: 500원 미만 메뉴 5건(1원·0원 등), 중복 가게 1건
- 계산 가정값 22개를 cost_params 표로 뺌 → 값만 바꾸면 전체 계산이 바뀜
- 모든 가격·사실에 출처 id와 신뢰도 등급

## 비어 있어서 채워야 할 곳
| 무엇 | 비어 있는 양 | 채울 방법 |
|---|---|---|
| 관광지 좌표 | 265곳 전부 | 한국관광공사 TourAPI |
| 도착지 소개·관광지 | 166곳 중 77곳 | TourAPI |
| 밥집·숙소 좌표 | 전부 | 주소 지오코딩 |
| 밥집 동네 정보 | 1,004곳 | 지오코딩으로 보완 |
| 기념품 실가격 | 166곳 중 145곳 | 지자체몰·온라인몰 조사 |
| 고속·시외버스 실제 요금 | 0노선 (식으로 추정 중) | 노선별 요금표 |
| 숙박 평일·주말 구분 | 없음 | 민간 통계 추가 |
| 체험 대표가 | 73곳 중 7곳 | 시설 안내 재확인 |
