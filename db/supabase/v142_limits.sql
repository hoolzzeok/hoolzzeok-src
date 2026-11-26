-- 훌쩍 v142 도배 방지: 하루 작성·신고 횟수 제한. Supabase → SQL Editor에 통째로 붙여 넣고 Run. 여러 번 실행해도 안전.
-- 기존 '확인 중 5개' 제한은 그대로 두고, 아래 두 가지를 더함.

-- 1) 후기: 한 사람이 24시간 안에 3개까지
create or replace function public.reviews_daily_limit() returns trigger
language plpgsql security definer set search_path = '' as $$
begin
  if (select count(*) from public.reviews r
      where r.user_id = new.user_id and r.created_at > now() - interval '1 day') >= 3 then
    raise exception 'daily_limit';
  end if;
  return new;
end $$;
drop trigger if exists reviews_daily_limit on public.reviews;
create trigger reviews_daily_limit before insert on public.reviews
  for each row execute function public.reviews_daily_limit();

-- 2) 신고: 한 사람이 24시간 안에 20개까지
create or replace function public.reports_daily_limit() returns trigger
language plpgsql security definer set search_path = '' as $$
begin
  if (select count(*) from public.reports p
      where p.user_id = new.user_id and p.created_at > now() - interval '1 day') >= 20 then
    raise exception 'daily_limit';
  end if;
  return new;
end $$;
drop trigger if exists reports_daily_limit on public.reports;
create trigger reports_daily_limit before insert on public.reports
  for each row execute function public.reports_daily_limit();

create index if not exists reports_user_time_idx on public.reports (user_id, created_at);

-- 확인: 아래가 두 줄(reviews_daily_limit, reports_daily_limit)로 나오면 성공
select tgname from pg_trigger where tgname in ('reviews_daily_limit', 'reports_daily_limit');
