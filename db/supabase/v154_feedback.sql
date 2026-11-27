-- 훌쩍 v154: "이 금액, 실제와 비슷했나요?" 경비 의견 (가입 없이, 개인 식별 정보 없음)
-- 받는 것: 여행 조건(출발·도착·일정·인원·이동·스타일), 계산된 1인 금액, 실제와 비교(더/비슷/덜), 실제 1인 금액(선택), 화면 언어, 시각
-- 받지 않는 것: 이름, 연락처, 이메일, 회원 id, IP, 기기 정보
-- 누구나 넣기만 가능, 읽기는 관리자(SQL 편집기)만. 전체 하루 2,000건 넘으면 거절(장난 입력 방지)

create table if not exists public.cost_feedback (
  id bigint generated always as identity primary key,
  created_at timestamptz not null default now(),
  origin text not null check (char_length(origin) between 1 and 40),
  dest text not null check (char_length(dest) between 1 and 40),
  nights smallint not null check (nights between 0 and 14),
  people smallint not null check (people between 1 and 30),
  mode text not null check (mode in ('transit','car','flight','ferry')),
  style text not null check (style in ('budget','standard','comfort')),
  est integer not null check (est between 0 and 5000000),
  verdict text not null check (verdict in ('more','same','less')),
  actual integer check (actual is null or actual between 0 and 5000000),
  lang text not null default 'ko' check (lang in ('ko','en','ja','zh'))
);

alter table public.cost_feedback enable row level security;
revoke all on public.cost_feedback from anon, authenticated;
grant insert on public.cost_feedback to anon, authenticated;

drop policy if exists cost_feedback_insert on public.cost_feedback;
create policy cost_feedback_insert on public.cost_feedback for insert to anon, authenticated with check (true);
-- 읽기 정책은 일부러 만들지 않음 → 사이트에서는 아무도 못 읽음

create or replace function public.cost_feedback_limit() returns trigger
language plpgsql security definer set search_path = '' as $$
begin
  if (select count(*) from public.cost_feedback where created_at > now() - interval '1 day') >= 2000 then
    raise exception 'cost_feedback daily limit';
  end if;
  return new;
end $$;
revoke all on function public.cost_feedback_limit() from public, anon, authenticated;

drop trigger if exists cost_feedback_limit on public.cost_feedback;
create trigger cost_feedback_limit before insert on public.cost_feedback
  for each row execute function public.cost_feedback_limit();

-- 확인용(관리자): 도착지별로 실제보다 비쌌다/쌌다
-- select dest, verdict, count(*), round(avg(actual)) from public.cost_feedback group by 1,2 order by 1,2;
