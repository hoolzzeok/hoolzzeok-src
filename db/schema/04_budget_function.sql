-- ============================================================================
-- 훌쩍 1인 예상 경비 계산 (사이트 calcBudget 와 같은 식)
-- 모든 값은 표에서 읽는다 → 가정값을 바꾸려면 cost_params 한 줄만 고치면 된다.
-- 사용 예: SELECT * FROM fn_trip_budget('seoul','goheung',1,'standard','transit',11,true);
-- ============================================================================

CREATE OR REPLACE FUNCTION fn_param(k text) RETURNS numeric
LANGUAGE sql STABLE AS $$ SELECT value FROM cost_params WHERE key = k $$;

CREATE OR REPLACE FUNCTION fn_round1000(v numeric) RETURNS integer
LANGUAGE sql IMMUTABLE AS $$ SELECT (round(v / 1000) * 1000)::integer $$;

-- 도로 거리(km) = 직선거리 × road_factor
CREATE OR REPLACE FUNCTION fn_road_km(a text, b text) RETURNS integer
LANGUAGE sql STABLE AS $$
  SELECT round(2 * 6371 * asin(sqrt(
           power(sin(radians(q.lat - p.lat) / 2), 2) +
           cos(radians(p.lat)) * cos(radians(q.lat)) * power(sin(radians(q.lon - p.lon) / 2), 2)
         )) * fn_param('road_factor'))::integer
  FROM places p, places q WHERE p.id = a AND q.id = b
$$;

CREATE OR REPLACE FUNCTION fn_bus_fare(km numeric) RETURNS numeric
LANGUAGE sql STABLE AS $$
  SELECT CASE WHEN km <= 0 THEN 0 ELSE fn_param('bus_fixed') + fn_param('bus_per_km') * km END
$$;

CREATE OR REPLACE FUNCTION fn_taxi_ride(prov text) RETURNS integer
LANGUAGE sql STABLE AS $$
  SELECT (t.base_fare + ceil((fn_param('taxi_ride_km') - t.base_km) * 1000 / t.meters_per_100won) * 100)::integer
  FROM taxi_fares t
  WHERE t.province = coalesce((SELECT province FROM taxi_fares WHERE province = prov), '충남')
$$;

CREATE OR REPLACE FUNCTION fn_trip_budget(
  p_origin text, p_dest text, p_nights int, p_style text,      -- style: budget / standard / comfort
  p_mode text DEFAULT 'transit',                               -- transit / car / flight / ferry
  p_month int DEFAULT EXTRACT(MONTH FROM CURRENT_DATE)::int,   -- 1~12 (숙박 월평균)
  p_half boolean DEFAULT false,                                -- 반값여행 신청 여부
  p_act int DEFAULT 0                                          -- 고른 체험비 합계
) RETURNS TABLE (
  road_km int, transport int, lodging_per_night int, lodging int,
  food int, local_transport int, activities int, souvenirs int,
  total int, refund int, final int
) LANGUAGE plpgsql STABLE AS $$
DECLARE
  o places; d places; days int := p_nights + 1;
  v_region text; room numeric; ltype text;
  food_day int; local_day int; souv_price int; souv_qty int;
  fl int; port text; grp text; land text;
BEGIN
  SELECT * INTO o FROM places WHERE id = p_origin;
  SELECT * INTO d FROM places WHERE id = p_dest;
  IF o.id IS NULL OR d.id IS NULL OR o.id = d.id THEN RAISE EXCEPTION '출발지·도착지를 확인하세요'; END IF;
  road_km := fn_road_km(o.id, d.id);

  -- 왕복 교통
  IF p_mode = 'transit' THEN
    transport := fn_round1000(2 * fn_bus_fare(road_km));
  ELSIF p_mode = 'car' THEN
    transport := fn_round1000(2 * (road_km * fn_param('fuel_per_l') / fn_param('km_per_l')
                                   + fn_param('toll_base') + fn_param('toll_per_km') * road_km) / fn_param('car_share'));
  ELSIF p_mode = 'flight' THEN
    IF o.island IS NOT NULL OR d.island IS NOT NULL THEN
      SELECT f.fare INTO fl FROM flight_fares f
       WHERE f.to_place = 'jeju' AND f.from_place = CASE WHEN o.island IS NOT NULL THEN d.id ELSE o.id END;
      fl := coalesce(fl, fn_param('flight_jeju_default')::int);
    ELSE
      SELECT f.fare INTO fl FROM flight_fares f
       WHERE (f.from_place, f.to_place) IN ((o.id, d.id), (d.id, o.id));
      IF fl IS NULL THEN RAISE EXCEPTION '이 구간 항공 운임이 없어요'; END IF;
    END IF;
    transport := 2 * fl;
  ELSIF p_mode = 'ferry' THEN
    grp  := coalesce(o.island, d.island);
    land := CASE WHEN o.island IS NOT NULL THEN d.id ELSE o.id END;
    SELECT f.port_place_id INTO port FROM ferry_fares f WHERE f.island_group = grp
     ORDER BY fn_road_km(land, f.port_place_id) LIMIT 1;
    road_km := fn_road_km(land, port);
    transport := fn_round1000(2 * fn_bus_fare(road_km)
                 + 2 * (SELECT fare FROM ferry_fares WHERE island_group = grp AND port_place_id = port));
  ELSE RAISE EXCEPTION '알 수 없는 이동 수단: %', p_mode;
  END IF;

  -- 숙박(1인 몫)
  v_region := coalesce((SELECT lodging_region FROM provinces WHERE code = d.province), '전국');
  IF p_style = 'budget' THEN
    lodging_per_night := coalesce((SELECT price FROM dorm_bed_rates WHERE region_key = d.province),
                                  (SELECT price FROM dorm_bed_rates WHERE region_key = 'other'));
  ELSE
    ltype := CASE WHEN p_style = 'standard' THEN 'motel'
                  WHEN d.kind = 'c' OR NOT EXISTS (SELECT 1 FROM lodging_rates WHERE lodging_type = 'pension' AND lodging_rates.region = v_region) THEN 'hotel'
                  ELSE 'pension' END;
    SELECT adr_krw INTO room FROM lodging_rates
     WHERE lodging_type = ltype AND lodging_rates.region = v_region AND month = p_month AND day_type = 'all';
    lodging_per_night := fn_round1000(room / 2);
  END IF;
  lodging := lodging_per_night * p_nights;

  -- 식비(하루 세 끼, 세종 등 값 없는 곳은 충남)
  SELECT fn_round1000(sum(b.qty * coalesce(fp.price, fn.price, fc.price)))
    INTO food_day
  FROM meal_baskets b
  LEFT JOIN food_prices fp ON fp.province = d.province AND fp.item = b.item
  LEFT JOIN food_prices fn ON fn.province = '충남'       AND fn.item = b.item
  LEFT JOIN food_prices fc ON fc.province = '전국'       AND fc.item = b.item
  WHERE b.style = p_style;
  food := food_day * days;

  -- 현지 교통
  IF p_mode = 'car' THEN
    local_day := fn_round1000(fn_param('local_drive_km') * fn_param('fuel_per_l') / fn_param('km_per_l') / fn_param('car_share'));
  ELSE
    local_day := fn_round1000(
        fn_param('bus_rides_' || p_style) * coalesce((SELECT fare FROM city_bus_fares WHERE province = d.province), 1300)
      + fn_param('taxi_rides_' || p_style) * fn_taxi_ride(d.province) / 2.0);
  END IF;
  local_transport := local_day * days;

  -- 체험·기념품
  activities := coalesce(p_act, 0);
  souv_price := coalesce((SELECT price FROM souvenirs WHERE place_id = d.id), fn_param('souvenir_default')::int);
  souv_qty   := fn_param('souvenir_qty_' || p_style)::int;
  souvenirs  := fn_round1000(souv_price * souv_qty);

  total  := transport + lodging + food + local_transport + activities + souvenirs;
  refund := CASE WHEN p_half AND d.half_price_pilot
                 THEN least(floor(total * 0.5)::int, fn_param('half_cap_per_person')::int) ELSE 0 END;
  final  := total - refund;
  RETURN NEXT;
END $$;
