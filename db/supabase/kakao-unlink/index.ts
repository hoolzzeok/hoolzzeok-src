// 훌쩍: 카카오 연결 해제 웹훅 (Supabase Edge Function 이름: kakao-unlink)
// 카카오가 사용자의 연결 해제·카카오계정 탈퇴를 알려 주면, 그 사용자의 훌쩍 계정과 후기를 지운다.
// 필요한 비밀값(Edge Functions > Secrets): KAKAO_ADMIN_KEY(카카오 대표 어드민 키), KAKAO_APP_ID(카카오 앱 ID 숫자)
// 이 함수는 카카오가 부르므로 'JWT 검증'을 꺼야 한다.
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
