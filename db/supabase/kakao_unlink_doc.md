# 카카오 연결 해제 웹훅 (2026-11-19 설정 완료)

카카오계정 페이지에서 훌쩍 연결을 끊거나 카카오계정을 탈퇴하면 카카오가 알려 주고, 훌쩍 계정·후기·신고를 지운다.
규격(카카오 공식): GET/POST, 헤더 `Authorization: KakaoAK {대표 어드민 키}`, 파라미터 app_id·user_id·referrer_type, 3초 안에 200(오류여도 200). 설정 위치: 카카오 [앱] > [웹훅] > [연결 해제 웹훅].
시험: Node로 GET·POST폼·POST JSON 정상 삭제 호출, 키 틀림 401, 다른 앱 무시, 깨진 요청 200 확인.

## 현재 설정
- SQL 함수 delete_user_by_kakao_id 실행 완료
- Edge Function 이름: **rapid-handler** (대시보드가 자동으로 붙인 이름. 휴대폰 편집기로는 코드 교체가 안 돼서 Supabase AI 도우미로 배포함. Code 탭 1번 줄 import { createClient } 확인)
- JWT 검증 끔, Secrets: KAKAO_ADMIN_KEY, KAKAO_APP_ID 등록
- 카카오 연결 해제 웹훅 주소: https://ppymgfvjtrtcatedhfxu.supabase.co/functions/v1/rapid-handler
- 확인 방법: rapid-handler > Logs 에 kakao_unlink 기록, Authentication > Users 에서 해당 카카오 회원 삭제 여부
- 주의: 대시보드 Code 탭에서 고치다 만 내용을 Deploy updates 하면 덮어써짐

## SQL
```sql
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
```

## Edge Function 코드
```ts
import { createClient } from "jsr:@supabase/supabase-js@2";

const ok = () => new Response("OK", { status: 200 });

Deno.serve(async (req) => {
  try {
    const adminKey = Deno.env.get("KAKAO_ADMIN_KEY") ?? "";
    const auth = req.headers.get("authorization") ?? "";
    // 카카오가 보낸 요청인지 확인 (대표 어드민 키). 아니면 거절
    if (!adminKey || auth !== `KakaoAK ${adminKey}`) return new Response("Unauthorized", { status: 401 });

    let p: URLSearchParams;
    if (req.method === "GET") p = new URL(req.url).searchParams;
    else {
      const ct = req.headers.get("content-type") ?? "", body = await req.text();
      p = ct.includes("json") ? new URLSearchParams(Object.entries(JSON.parse(body || "{}")).map(([k, v]) => [k, String(v)])) : new URLSearchParams(body);
    }
    const appId = Deno.env.get("KAKAO_APP_ID");
    if (appId && p.get("app_id") !== appId) return ok();          // 다른 앱이면 무시 (카카오 요구: 그래도 200)
    const userId = p.get("user_id");
    if (!userId) return ok();

    const sb = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });
    const { data, error } = await sb.rpc("delete_user_by_kakao_id", { kakao_id: userId });
    console.log(JSON.stringify({ event: "kakao_unlink", referrer: p.get("referrer_type"), deleted: data ?? 0, error: error?.message ?? null }));
    return ok();                                                     // 카카오 요구: 오류가 나도 200, 3초 안에
  } catch (e) {
    console.log(JSON.stringify({ event: "kakao_unlink_error", error: String(e) }));
    return ok();
  }
});
```

## 함께 만든 것
- 개인정보 처리방침 /privacy/, 이용약관 /terms/ (hoolzzeok_db/build_legal.py, 값은 legal.json: name·email·effective). 비어 있으면 '작성 중' 표시 + 검색 차단
- 처리방침 반영 사항: 카카오 닉네임·프로필 사진(동의 시), 접속 기록(Cloudflare·Supabase), 국외 이전 표(Supabase 서울 저장·미국 회사, Cloudflare 미국), 브라우저 저장, 카카오 연결 해제 시 삭제, 72시간 유출 통지, 구제기관 1833-6972·118·1301·182(타사 처리방침과 대조 확인)
