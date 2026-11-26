-- ============================================================================
-- 훌쩍 Supabase 접근 규칙(RLS)  —  01_schema.sql 다음에 실행
--  · 공개 자료(지역·가격·착한가격 등): 누구나 읽기, 쓰기는 서버(service_role)만
--  · 후기: 승인된 것만 누구나 읽기. 로그인한 사람은 자기 후기를 쓰고 자기 것만 읽기
--  · 신고: 로그인한 사람이 자기 이름으로만 쓰기. 읽기는 관리자(service_role)만
--  · 관리자 작업(승인·광고 등록)은 Supabase 대시보드 또는 service_role 키를 쓰는 서버에서만
-- ============================================================================

-- 1) 공개 자료: 읽기 전용
DO $$
DECLARE t text;
BEGIN
  FOREACH t IN ARRAY ARRAY[
    'data_sources','provinces','places','place_profiles','place_spots','place_foods',
    'events','agent_picks','season_products','season_months','season_places','activities',
    'contests','souvenirs','official_malls','lodging_rates','dorm_bed_rates','food_prices',
    'meal_baskets','city_bus_fares','taxi_fares','flight_fares','ferry_fares',
    'intercity_bus_fares','cost_params','fx_rates','goodprice_eateries','goodprice_menus',
    'goodprice_stays','goodprice_stay_rates','checklist_items','affiliate_links']
  LOOP
    EXECUTE format('ALTER TABLE %I ENABLE ROW LEVEL SECURITY', t);
    EXECUTE format('CREATE POLICY public_read ON %I FOR SELECT USING (true)', t);
  END LOOP;
END $$;

-- 2) 광고: 게시 중인 것만 공개
ALTER TABLE ads ENABLE ROW LEVEL SECURITY;
CREATE POLICY ads_live_read ON ads FOR SELECT
  USING (status = 'live' AND CURRENT_DATE BETWEEN starts_on AND ends_on);
ALTER TABLE ad_events ENABLE ROW LEVEL SECURITY;          -- 집계는 서버만

-- 3) 후기
ALTER TABLE reviews ENABLE ROW LEVEL SECURITY;
CREATE POLICY reviews_public_read ON reviews FOR SELECT
  USING (status = 'approved' OR author_id = auth.uid());
CREATE POLICY reviews_insert_own ON reviews FOR INSERT
  WITH CHECK (author_id = auth.uid() AND status = 'pending' AND approved_at IS NULL);
CREATE POLICY reviews_delete_own ON reviews FOR DELETE
  USING (author_id = auth.uid());                          -- 탈퇴·삭제 요청 대응

ALTER TABLE review_costs ENABLE ROW LEVEL SECURITY;
CREATE POLICY review_costs_read ON review_costs FOR SELECT
  USING (EXISTS (SELECT 1 FROM reviews r WHERE r.id = review_id AND (r.status = 'approved' OR r.author_id = auth.uid())));
CREATE POLICY review_costs_insert_own ON review_costs FOR INSERT
  WITH CHECK (EXISTS (SELECT 1 FROM reviews r WHERE r.id = review_id AND r.author_id = auth.uid() AND r.status = 'pending'));

ALTER TABLE review_reports ENABLE ROW LEVEL SECURITY;
CREATE POLICY reports_insert_own ON review_reports FOR INSERT
  WITH CHECK (reporter_id = auth.uid());

ALTER TABLE content_rewards ENABLE ROW LEVEL SECURITY;   -- 서버만
ALTER TABLE job_log ENABLE ROW LEVEL SECURITY;           -- 서버만
