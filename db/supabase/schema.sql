-- 훌쩍 후기 저장 (Supabase). SQL Editor에 통째로 붙여 넣고 Run.
-- 저장하는 것: 로그인 계정(공급자가 주는 이메일, Supabase auth가 보관), 후기, 신고. 그 밖의 개인정보는 받지 않음.
-- 탈퇴(delete_my_account)하면 계정·후기·신고가 함께 지워짐.

-- 관리자 목록 (화면에서 못 바꿈. SQL Editor에서만 추가)
create table if not exists public.admins (
  user_id uuid primary key references auth.users(id) on delete cascade
);
alter table public.admins enable row level security;

create or replace function public.is_admin() returns boolean
language sql stable security definer set search_path = '' as $$
  select exists (select 1 from public.admins a where a.user_id = auth.uid());
$$;

-- 후기
create table if not exists public.reviews (
  id          text primary key check (char_length(id) between 6 and 40),
  user_id     uuid not null default auth.uid() references auth.users(id) on delete cascade,
  status      text not null default 'pending' check (status in ('pending','approved','rejected')),
  title       text not null check (char_length(title) between 1 and 60),
  origin      text not null check (char_length(origin) <= 30),
  dest        text not null check (char_length(dest) <= 30),
  region      text not null check (char_length(region) <= 20),
  nights      int  not null check (nights between 0 and 6),
  mode        text not null check (mode in ('transit','car','flight','ferry')),
  people      int  not null check (people between 1 and 20),
  tags        text[] not null default '{}' check (cardinality(tags) <= 9),
  cost        jsonb not null default '{}'::jsonb check (pg_column_size(cost) < 2000),
  body        text not null check (char_length(body) between 1 and 2000),
  age14       boolean not null check (age14),          -- 만 14세 이상·처리방침 동의 체크
  mood        text check (mood in ('good','ok','bad')), -- 어땠어요 (좋았어요/괜찮았어요/아쉬웠어요)
  created_at  timestamptz not null default now(),
  approved_at timestamptz
);
create index if not exists reviews_status_idx on public.reviews (status, approved_at desc);
create index if not exists reviews_user_idx on public.reviews (user_id);
alter table public.reviews enable row level security;

drop policy if exists "본인 또는 관리자 읽기" on public.reviews;
create policy "본인 또는 관리자 읽기" on public.reviews for select
  using (user_id = auth.uid() or public.is_admin());
drop policy if exists "본인 후기 보내기" on public.reviews;
create policy "본인 후기 보내기" on public.reviews for insert to authenticated
  with check (user_id = auth.uid() and status = 'pending' and approved_at is null);
drop policy if exists "관리자만 승인·반려" on public.reviews;
create policy "관리자만 승인·반려" on public.reviews for update to authenticated
  using (public.is_admin()) with check (public.is_admin());
drop policy if exists "본인 또는 관리자 삭제" on public.reviews;
create policy "본인 또는 관리자 삭제" on public.reviews for delete to authenticated
  using (user_id = auth.uid() or public.is_admin());

-- 확인 중인 후기는 1인 5개까지
create or replace function public.reviews_pending_limit() returns trigger
language plpgsql security definer set search_path = '' as $$
begin
  if (select count(*) from public.reviews r where r.user_id = new.user_id and r.status = 'pending') >= 5 then
    raise exception '확인 중인 후기가 5개 있어요';
  end if;
  return new;
end $$;
drop trigger if exists reviews_pending_limit on public.reviews;
create trigger reviews_pending_limit before insert on public.reviews
  for each row execute function public.reviews_pending_limit();

-- 공개용: 승인된 후기만, 작성자 id는 빼고
create or replace view public.public_reviews as
  select id, title, origin, dest, region, nights, mode, people, tags, cost, body, created_at, approved_at, mood
  from public.reviews where status = 'approved';
grant select on public.public_reviews to anon, authenticated;

-- 신고
create table if not exists public.reports (
  review_id  text not null references public.reviews(id) on delete cascade,
  user_id    uuid not null default auth.uid() references auth.users(id) on delete cascade,
  created_at timestamptz not null default now(),
  primary key (review_id, user_id)
);
alter table public.reports enable row level security;
drop policy if exists "본인 또는 관리자 읽기" on public.reports;
create policy "본인 또는 관리자 읽기" on public.reports for select
  using (user_id = auth.uid() or public.is_admin());
drop policy if exists "본인 신고" on public.reports;
create policy "본인 신고" on public.reports for insert to authenticated
  with check (user_id = auth.uid());
drop policy if exists "관리자 삭제" on public.reports;
create policy "관리자 삭제" on public.reports for delete to authenticated
  using (public.is_admin());

-- 탈퇴: 내 계정 삭제 → 후기·신고도 연쇄 삭제
create or replace function public.delete_my_account() returns void
language plpgsql security definer set search_path = '' as $$
begin
  if auth.uid() is null then raise exception 'not signed in'; end if;
  delete from auth.users where id = auth.uid();
end $$;
revoke all on function public.delete_my_account() from public, anon;
grant execute on function public.delete_my_account() to authenticated;

-- 접근 허락 (프로젝트 생성 때 "새 표에 API 접근 자동 허용"을 껐으므로 직접 지정)
grant usage on schema public to anon, authenticated;
grant select, insert, delete on public.reviews to authenticated;
grant update (status, approved_at) on public.reviews to authenticated;   -- 실제 수정은 RLS로 관리자만
grant select, insert, delete on public.reports to authenticated;
grant select on public.public_reviews to anon, authenticated;
revoke all on public.admins from anon, authenticated;
grant execute on function public.is_admin() to anon, authenticated;

-- 관리자 등록 (본인이 처음 로그인한 뒤, Authentication > Users에서 내 UID를 복사해 아래 실행)
-- insert into public.admins (user_id) values ('여기에-내-UID');
