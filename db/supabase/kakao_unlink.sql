-- 카카오 연결 해제 웹훅용: 카카오 회원번호로 우리 계정을 찾아 삭제 (후기·신고는 연쇄 삭제)
-- 서버 함수(Edge Function)만 부를 수 있게 service_role 에만 권한을 줌
create or replace function public.delete_user_by_kakao_id(kakao_id text) returns integer
language plpgsql security definer set search_path = '' as $$
declare n integer;
begin
  if kakao_id is null or kakao_id !~ '^[0-9]{1,20}$' then return 0; end if;
  delete from auth.users u
   where u.id in (select i.user_id from auth.identities i where i.provider = 'kakao' and i.provider_id = kakao_id);
  get diagnostics n = row_count;
  return n;
end $$;
revoke all on function public.delete_user_by_kakao_id(text) from public, anon, authenticated;
grant execute on function public.delete_user_by_kakao_id(text) to service_role;
