alter table public.reviews add column if not exists mood text check (mood in ('good','ok','bad'));
create or replace view public.public_reviews as
  select id, title, origin, dest, region, nights, mode, people, tags, cost, body, created_at, approved_at, mood
  from public.reviews where status = 'approved';
grant select on public.public_reviews to anon, authenticated;
