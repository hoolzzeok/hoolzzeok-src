-- ============================================================================
-- 훌쩍(Hoolzzeok) 데이터베이스 설계 v2  (2026-11-13)
-- 대상: Supabase(PostgreSQL 15 이상). 로컬 PostgreSQL 16에서 적재·검증함.
--
-- 원칙
--  1) 모든 가격·사실 자료는 data_sources 의 출처 한 줄을 가리킨다(source_id).
--     confidence: A = 공식 통계·2곳 이상 대조 / B = 출처 1곳 또는 민간 통계 / C = 가정·임시 값
--  2) 개인정보는 저장하지 않는다. 사용자는 Supabase 로그인 id(uuid)로만 구분한다.
--     이름·이메일·전화번호 칸은 어떤 표에도 없다. 본업 관련 정보도 넣지 않는다.
--  3) 계산 가정값(하루 택시 몇 번 등)은 코드에 박지 않고 cost_params 에 둔다.
--     → 테스트·후기 자료가 쌓이면 표의 값만 바꾸면 된다.
--  4) 라이선스가 확인되지 않은 외부 자료(스크래핑)는 넣지 않는다.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- A. 출처
-- ----------------------------------------------------------------------------
CREATE TABLE data_sources (
  id             text PRIMARY KEY,                 -- 'src_food' 처럼 사람이 읽는 키
  title          text NOT NULL,
  publisher      text NOT NULL,
  url            text,
  as_of          text NOT NULL,                    -- '2026-11', '2026-3Q', '2026-가을' 등 출처 표기 그대로
  confidence     char(1) NOT NULL CHECK (confidence IN ('A','B','C')),
  refresh_cycle  text NOT NULL,                    -- '월 1회', '분기' ...
  note           text,
  checked_at     date NOT NULL DEFAULT CURRENT_DATE
);

-- ----------------------------------------------------------------------------
-- B. 지역
-- ----------------------------------------------------------------------------
CREATE TABLE provinces (                           -- 시·도 17곳
  code            text PRIMARY KEY,                -- '서울', '경북' ...
  name_en         text NOT NULL,
  lodging_region  text NOT NULL                    -- 숙박 통계 권역('경북권' 등)
);

CREATE TABLE places (                              -- 시·군 166곳 + 독도
  id                text PRIMARY KEY,              -- 'gyeongju'
  name_ko           text NOT NULL,
  name_en           text NOT NULL,
  province          text NOT NULL REFERENCES provinces(code),
  lat               numeric(8,5) NOT NULL CHECK (lat BETWEEN 33 AND 39),
  lon               numeric(8,5) NOT NULL CHECK (lon BETWEEN 124 AND 132),
  tier              smallint NOT NULL CHECK (tier IN (1,2,3)),   -- 지도 표시 우선순위
  kind              char(1) NOT NULL CHECK (kind IN ('c','g','d')), -- 시 / 군 / 독도
  island            text CHECK (island IN ('jeju','ulleung')),
  price_level       numeric(4,2),                  -- 물가 보정(서울 1.25 등). 근거 약함 → C
  half_price_pilot  boolean NOT NULL DEFAULT false,
  admin_code        text,                          -- 행정표준코드(이전 뒤 채움)
  source_id         text NOT NULL REFERENCES data_sources(id)
);

CREATE TABLE place_profiles (                      -- 도착지 소개 (90곳)
  place_id     text PRIMARY KEY REFERENCES places(id),
  desc_ko      text NOT NULL,
  desc_en      text NOT NULL,
  note_ko      text,  note_en text,                -- '경복궁은 화요일에 쉬어요' 등
  festival_ko  text,  festival_en text,            -- 대표 축제(연중)
  source_id    text NOT NULL REFERENCES data_sources(id)
);

CREATE TABLE place_spots (                         -- 대표 관광지 (추천 일정용)
  place_id       text NOT NULL REFERENCES places(id),
  seq            smallint NOT NULL,
  name_ko        text NOT NULL,
  name_en        text NOT NULL,
  is_night_view  boolean NOT NULL DEFAULT false,
  lat            numeric(8,5),                     -- TourAPI 연결 뒤 채움 → 가까운 순 일정
  lon            numeric(9,5),
  tour_api_id    text,
  PRIMARY KEY (place_id, seq)
);

CREATE TABLE place_foods (                         -- 꼭 먹고 사갈 것
  place_id  text NOT NULL REFERENCES places(id),
  seq       smallint NOT NULL,
  name_ko   text NOT NULL,
  name_en   text NOT NULL,
  PRIMARY KEY (place_id, seq)
);

-- ----------------------------------------------------------------------------
-- C. 때가 있는 정보 (축제·추천·제철·체험·공모전·기념품·쇼핑몰)
-- ----------------------------------------------------------------------------
CREATE TABLE events (
  id          text PRIMARY KEY,
  place_id    text NOT NULL REFERENCES places(id),
  kind        text NOT NULL CHECK (kind IN ('festival','experience')),
  name_ko     text NOT NULL,  name_en text NOT NULL,
  start_date  date,  end_date date,
  detail_ko   text,  detail_en text,
  source_id   text NOT NULL REFERENCES data_sources(id),
  CHECK (end_date IS NULL OR start_date IS NULL OR end_date >= start_date)
);

CREATE TABLE agent_picks (                         -- 훌쩍요원 추천 문구
  id        text PRIMARY KEY,
  audience  text NOT NULL CHECK (audience IN ('ko','foreign')),
  place_id  text NOT NULL REFERENCES places(id),
  until     date,                                  -- 지나면 자동 숨김
  tag       text,
  text_ko   text, text_en text, text_ja text, text_zh text
);

CREATE TABLE season_products (
  id         smallint PRIMARY KEY,
  name_ko    text NOT NULL,
  name_en    text NOT NULL,
  source_id  text NOT NULL REFERENCES data_sources(id)
);
CREATE TABLE season_months (
  product_id  smallint NOT NULL REFERENCES season_products(id),
  month       smallint NOT NULL CHECK (month BETWEEN 1 AND 12),
  PRIMARY KEY (product_id, month)
);
CREATE TABLE season_places (
  product_id  smallint NOT NULL REFERENCES season_products(id),
  place_id    text NOT NULL REFERENCES places(id),
  PRIMARY KEY (product_id, place_id)
);

CREATE TABLE activities (                          -- 전통체험·액티비티 73곳
  id             smallint PRIMARY KEY,
  place_id       text NOT NULL REFERENCES places(id),
  kind           text NOT NULL CHECK (kind IN ('traditional','activity')),
  type_ko        text NOT NULL,  type_en text,
  name_ko        text NOT NULL,
  price_text     text,                             -- 원문 가격 표기 그대로
  duration_text  text,
  note           text,
  source_url     text NOT NULL,
  source_as_of   text,
  rep_price      integer CHECK (rep_price >= 0)    -- 성인 1인 대표가(계산기용). 없으면 NULL
);

CREATE TABLE contests (
  id            smallint PRIMARY KEY,
  place_id      text REFERENCES places(id),
  province      text REFERENCES provinces(code),
  hub_place_id  text REFERENCES places(id),
  nationwide    boolean NOT NULL DEFAULT false,
  end_date      date NOT NULL,
  name_ko text NOT NULL, name_en text,
  type_ko text, type_en text, prize_ko text, prize_en text, who_ko text, who_en text,
  url           text NOT NULL
);

CREATE TABLE souvenirs (                           -- 실가격 조사된 22곳
  place_id    text PRIMARY KEY REFERENCES places(id),
  name_ko     text NOT NULL,
  name_en     text NOT NULL,
  price       integer NOT NULL CHECK (price > 0),
  basis       text,
  source_url  text
);

CREATE TABLE official_malls (                      -- 지자체 공식 쇼핑몰
  scope        text NOT NULL CHECK (scope IN ('province','place')),
  scope_key    text NOT NULL,                      -- 시·도 코드 또는 places.id
  name         text NOT NULL,
  description  text,
  url          text NOT NULL,
  source_id    text NOT NULL REFERENCES data_sources(id),
  PRIMARY KEY (scope, scope_key)
);

-- ----------------------------------------------------------------------------
-- D. 가격 (계산기 입력)
-- ----------------------------------------------------------------------------
CREATE TABLE lodging_rates (                       -- 권역 × 숙소종류 × 월 평균 객실요금
  lodging_type  text NOT NULL CHECK (lodging_type IN ('motel','hotel','pension')),
  region        text NOT NULL,                     -- '전국', '경북권' ...
  month         smallint NOT NULL CHECK (month BETWEEN 1 AND 12),
  adr_krw       integer NOT NULL CHECK (adr_krw > 0),
  data_year     smallint NOT NULL,
  day_type      text NOT NULL DEFAULT 'all' CHECK (day_type IN ('all','weekday','weekend')),  -- 지금은 all만. 평일·주말 자료 생기면 추가
  source_id     text NOT NULL REFERENCES data_sources(id),
  PRIMARY KEY (lodging_type, region, month, day_type)
);

CREATE TABLE dorm_bed_rates (
  region_key  text PRIMARY KEY,                    -- '서울', '제주', 'other'
  price       integer NOT NULL CHECK (price > 0),
  source_id   text NOT NULL REFERENCES data_sources(id)
);

CREATE TABLE food_prices (                         -- 시·도 × 외식 품목
  province   text NOT NULL,                        -- '전국'은 커피
  item       text NOT NULL,
  price      integer NOT NULL CHECK (price > 0),
  source_id  text NOT NULL REFERENCES data_sources(id),
  PRIMARY KEY (province, item)
);

CREATE TABLE meal_baskets (                        -- 씀씀이별 하루 세 끼 구성(가정)
  style      text NOT NULL CHECK (style IN ('budget','standard','comfort')),
  item       text NOT NULL,
  qty        numeric(3,1) NOT NULL CHECK (qty > 0),
  source_id  text NOT NULL REFERENCES data_sources(id),
  PRIMARY KEY (style, item)
);

CREATE TABLE city_bus_fares (
  province   text PRIMARY KEY REFERENCES provinces(code),
  fare       integer NOT NULL CHECK (fare > 0),
  source_id  text NOT NULL REFERENCES data_sources(id)
);

CREATE TABLE taxi_fares (
  province            text PRIMARY KEY REFERENCES provinces(code),
  base_fare           integer NOT NULL,
  base_km             numeric(3,1) NOT NULL,
  meters_per_100won   integer NOT NULL,
  source_id           text NOT NULL REFERENCES data_sources(id)
);

CREATE TABLE flight_fares (                        -- 국내선 편도 1인
  from_place  text NOT NULL REFERENCES places(id),
  to_place    text NOT NULL REFERENCES places(id),
  fare        integer NOT NULL CHECK (fare > 0),
  basis       text NOT NULL,
  source_id   text NOT NULL REFERENCES data_sources(id),
  PRIMARY KEY (from_place, to_place)
);

CREATE TABLE ferry_fares (
  island_group   text NOT NULL CHECK (island_group IN ('jeju','ulleung')),
  port_place_id  text NOT NULL REFERENCES places(id),
  fare           integer NOT NULL CHECK (fare > 0),
  source_id      text NOT NULL REFERENCES data_sources(id),
  PRIMARY KEY (island_group, port_place_id)
);

CREATE TABLE intercity_bus_fares (                 -- 비어 있음: 노선별 실제 요금표 수집 뒤 채움.
  from_place  text NOT NULL REFERENCES places(id), -- 있으면 요금 식(bus_fixed + bus_per_km)보다 우선
  to_place    text NOT NULL REFERENCES places(id),
  grade       text NOT NULL CHECK (grade IN ('일반','우등','프리미엄','시외')),
  fare        integer NOT NULL CHECK (fare > 0),
  source_id   text NOT NULL REFERENCES data_sources(id),
  PRIMARY KEY (from_place, to_place, grade)
);

CREATE TABLE cost_params (                         -- 계산 가정값·계수
  key        text PRIMARY KEY,
  value      numeric NOT NULL,
  unit       text NOT NULL,
  note       text,
  source_id  text NOT NULL REFERENCES data_sources(id)
);

CREATE TABLE fx_rates (
  rate_date     date NOT NULL,
  currency      char(3) NOT NULL,
  krw_per_unit  numeric(10,4) NOT NULL CHECK (krw_per_unit > 0),
  source        text NOT NULL,                     -- '하나은행 매매기준율' 고정
  PRIMARY KEY (rate_date, currency)
);

-- ----------------------------------------------------------------------------
-- E. 착한가격업소 (행정안전부)
-- ----------------------------------------------------------------------------
CREATE TABLE goodprice_eateries (
  id              integer PRIMARY KEY,
  place_id        text NOT NULL REFERENCES places(id),
  name            text NOT NULL,
  category        text NOT NULL CHECK (category IN ('한식','중식','일식','양식','기타요식','베이커리')),
  subcategory     text NOT NULL CHECK (subcategory IN ('국밥·탕·찌개','면','고기구이','백반·정식','해산물','치킨·돈가스','분식','카페·디저트','중식','일식','양식','기타')),
  address         text NOT NULL,
  district        text,                            -- 구·군 (주소에서 추출)
  neighborhood    text,                            -- 읍·면·동·리
  road            text,                            -- 도로명
  lat             numeric(8,5),                    -- 지오코딩 뒤 채움 → 숙소 반경 계산
  lon             numeric(9,5),
  min_meal_price  integer,                         -- 끼니 메뉴(3천 원 이상, 김밥·공기밥·음료·간식 제외) 최저가
  price_band      text,
  is_full_meal    boolean NOT NULL,                -- 5천 원 이상 끼니 메뉴가 있음(추천 일정 점심·저녁 후보)
  has_grill       boolean NOT NULL,                -- 고기 구이 메뉴 있음(🥩)
  source_id       text NOT NULL REFERENCES data_sources(id),
  UNIQUE (place_id, name, address)
);
CREATE TABLE goodprice_menus (
  eatery_id  integer NOT NULL REFERENCES goodprice_eateries(id) ON DELETE CASCADE,
  seq        smallint NOT NULL,
  menu       text NOT NULL,
  price      integer NOT NULL CHECK (price >= 500),   -- 500원 미만은 입력 오류로 보고 제외함
  is_meal    boolean NOT NULL,
  PRIMARY KEY (eatery_id, seq)
);

CREATE TABLE goodprice_stays (
  id               integer PRIMARY KEY,
  place_id         text NOT NULL REFERENCES places(id),
  name             text NOT NULL,
  min_night_price  integer NOT NULL CHECK (min_night_price > 0),
  address          text NOT NULL,
  district text, neighborhood text, road text,
  lat numeric(8,5), lon numeric(9,5),
  source_id        text NOT NULL REFERENCES data_sources(id)
);
CREATE TABLE goodprice_stay_rates (
  stay_id  integer NOT NULL REFERENCES goodprice_stays(id) ON DELETE CASCADE,
  seq      smallint NOT NULL,
  item     text NOT NULL,
  price    integer NOT NULL CHECK (price > 0),
  PRIMARY KEY (stay_id, seq)
);

-- ----------------------------------------------------------------------------
-- F. 수익 (제휴·광고)
-- ----------------------------------------------------------------------------
CREATE TABLE checklist_items (                     -- 여행 준비물
  key            text NOT NULL,
  audience       text NOT NULL CHECK (audience IN ('ko','foreign')),
  name           text NOT NULL,
  reason         text,
  partner        text NOT NULL CHECK (partner IN ('coupang','klook')),
  affiliate_url  text,                             -- 비어 있으면 일반 검색 링크(수수료 없음)
  PRIMARY KEY (key, audience)
);

CREATE TABLE affiliate_links (                     -- 특산품·숙소·체험 등 제휴 링크
  id           serial PRIMARY KEY,
  partner      text NOT NULL,                      -- coupang, klook, agoda ...
  target_type  text NOT NULL CHECK (target_type IN ('season_product','place','activity','stay','other')),
  target_key   text NOT NULL,                      -- 예: '고흥 유자'
  url          text NOT NULL,
  active       boolean NOT NULL DEFAULT true,
  created_at   timestamptz NOT NULL DEFAULT now(),
  UNIQUE (partner, target_type, target_key)
);

CREATE TABLE ads (                                 -- 유료 광고. 화면에 '광고 · 광고주' 자동 표시
  id           serial PRIMARY KEY,
  slot         text NOT NULL CHECK (slot IN ('home','dest','senior')),
  place_id     text REFERENCES places(id),         -- NULL이면 전체
  advertiser   text NOT NULL,
  is_government boolean NOT NULL DEFAULT false,    -- 지자체 광고는 한국언론진흥재단 경유(정부광고법)
  title_ko text NOT NULL, title_en text, sub_ko text, sub_en text, cta_ko text, cta_en text,
  url          text NOT NULL,
  starts_on    date NOT NULL,
  ends_on      date NOT NULL,
  price_krw    integer,
  status       text NOT NULL DEFAULT 'draft' CHECK (status IN ('draft','live','ended')),
  CHECK (ends_on >= starts_on)
);

CREATE TABLE ad_events (                           -- 노출·클릭 집계(하루 단위, 개인 식별 없음)
  ad_id    integer NOT NULL REFERENCES ads(id),
  day      date NOT NULL,
  views    integer NOT NULL DEFAULT 0,
  clicks   integer NOT NULL DEFAULT 0,
  PRIMARY KEY (ad_id, day)
);

-- ----------------------------------------------------------------------------
-- G. 사용자 참여 (Supabase 로그인 필요. 개인정보 칸 없음)
-- ----------------------------------------------------------------------------
CREATE TABLE reviews (                             -- 여행 후기 (관리자 승인 뒤 공개)
  id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  author_id     uuid NOT NULL,                     -- auth.users.id (이름·이메일 저장 안 함)
  origin_id     text NOT NULL REFERENCES places(id),
  dest_id       text NOT NULL REFERENCES places(id),
  nights        smallint NOT NULL CHECK (nights BETWEEN 0 AND 6),
  people        smallint CHECK (people BETWEEN 1 AND 20),
  trip_month    char(7),                           -- 'YYYY-MM'
  title         text NOT NULL CHECK (char_length(title) <= 60),
  body          text NOT NULL CHECK (char_length(body) <= 2000),
  tags          text[] NOT NULL DEFAULT '{}',
  status        text NOT NULL DEFAULT 'pending' CHECK (status IN ('pending','approved','rejected','hidden')),
  created_at    timestamptz NOT NULL DEFAULT now(),
  approved_at   timestamptz
);
CREATE TABLE review_costs (                        -- 후기에 적은 실제 경비(1인) → 계산값 검증·보정 자료
  review_id  uuid NOT NULL REFERENCES reviews(id) ON DELETE CASCADE,
  item       text NOT NULL CHECK (item IN ('trans','lodge','food','local','act','souv')),
  amount     integer NOT NULL CHECK (amount >= 0 AND amount <= 5000000),
  PRIMARY KEY (review_id, item)
);
CREATE TABLE review_reports (
  review_id    uuid NOT NULL REFERENCES reviews(id) ON DELETE CASCADE,
  reporter_id  uuid NOT NULL,
  reason       text NOT NULL CHECK (reason IN ('광고','욕설','개인정보','거짓','기타')),
  created_at   timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (review_id, reporter_id)
);
CREATE TABLE content_rewards (                     -- 리워드 지급 기록(세금 신고용 합계만)
  id          serial PRIMARY KEY,
  review_id   uuid REFERENCES reviews(id),
  author_id   uuid NOT NULL,
  kind        text NOT NULL CHECK (kind IN ('adopted','weekly_rank')),
  amount_krw  integer NOT NULL CHECK (amount_krw > 0),
  paid_on     date
);

-- ----------------------------------------------------------------------------
-- H. 운영
-- ----------------------------------------------------------------------------
CREATE TABLE job_log (
  id           serial PRIMARY KEY,
  job_name     text NOT NULL,                      -- 'fx_daily', 'tourapi_spots' ...
  started_at   timestamptz NOT NULL DEFAULT now(),
  finished_at  timestamptz,
  status       text NOT NULL CHECK (status IN ('ok','partial','failed','skipped')),
  row_count    integer,
  note         text
);

-- ----------------------------------------------------------------------------
-- 색인
-- ----------------------------------------------------------------------------
CREATE INDEX ON places (province);
CREATE INDEX ON goodprice_eateries (place_id, subcategory);
CREATE INDEX ON goodprice_eateries (place_id, neighborhood);
CREATE INDEX ON goodprice_eateries (place_id, min_meal_price);
CREATE INDEX ON goodprice_stays (place_id, neighborhood);
CREATE INDEX ON events (end_date);
CREATE INDEX ON contests (end_date);
CREATE INDEX ON season_places (place_id);
CREATE INDEX ON activities (place_id);
CREATE INDEX ON reviews (status, approved_at DESC);
CREATE INDEX ON reviews (dest_id) WHERE status = 'approved';

-- ============================================================================
-- 보기(VIEW): 화면이 바로 쓰는 묶음
-- ============================================================================

-- 1) 숙소와 같은 동네의 착한가격 밥집 (숙소 근처 저녁 · 걸어서 한잔 후보)
CREATE VIEW v_stay_nearby_eateries AS
SELECT s.id AS stay_id, s.place_id, s.name AS stay_name, s.neighborhood,
       e.id AS eatery_id, e.name AS eatery_name, e.subcategory, e.has_grill, e.min_meal_price
FROM goodprice_stays s
JOIN goodprice_eateries e
  ON e.place_id = s.place_id
 AND e.neighborhood = s.neighborhood
 AND coalesce(e.district,'') = coalesce(s.district,'')
WHERE s.neighborhood IS NOT NULL AND e.is_full_meal;

-- 2) 지역별 밥집 요약 (도착지 소개 칸의 "○곳 · 한 끼 ○원부터")
CREATE VIEW v_place_eatery_summary AS
SELECT place_id,
       count(*)                                             AS eateries,
       count(*) FILTER (WHERE has_grill)                    AS grill_places,
       min(min_meal_price) FILTER (WHERE category IN ('한식','중식')) AS cheapest_meal,
       percentile_cont(0.5) WITHIN GROUP (ORDER BY min_meal_price)   AS median_meal
FROM goodprice_eateries
GROUP BY place_id;

-- 3) 지금 보여 줄 축제·추천·공모전 (날짜 지난 것 제외)
CREATE VIEW v_live_events AS
SELECT * FROM events WHERE end_date IS NULL OR end_date >= CURRENT_DATE;
CREATE VIEW v_live_contests AS
SELECT * FROM contests WHERE end_date >= CURRENT_DATE;

-- 4) 이번 달 제철 산지
CREATE VIEW v_season_now AS
SELECT sp.place_id, p.name_ko, p.name_en
FROM season_months m
JOIN season_products p ON p.id = m.product_id
JOIN season_places  sp ON sp.product_id = p.id
WHERE m.month = EXTRACT(MONTH FROM CURRENT_DATE);

-- 5) 출처 신뢰도 한눈에 (C등급 = 우선 보강 대상)
CREATE VIEW v_source_quality AS
SELECT confidence, count(*) AS sources, string_agg(title, ' / ' ORDER BY title) AS titles
FROM data_sources GROUP BY confidence;

-- 6) 후기 경비 vs 계산값 비교용: 도착지·항목별 후기 평균(승인된 것만, 표본 수 포함)
CREATE VIEW v_review_cost_stats AS
SELECT r.dest_id, c.item, count(*) AS samples, round(avg(c.amount)) AS avg_amount
FROM reviews r JOIN review_costs c ON c.review_id = r.id
WHERE r.status = 'approved'
GROUP BY r.dest_id, c.item;
