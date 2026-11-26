  /* v136 딸깍 일정 전국판: 테마 6개(2025 외래관광객 참여활동 통계), 도착 공항 3곳, 두 번째 도시 5곳, 수원 당일치기, 휴무 피하기, 비 대안 */
  const QT_THEMES = {food: "🍜", shop: "🛍️", history: "🏯", nature: "🌊", kpop: "🎤", rest: "🌿"};
  const QT_OLD = {culture: "history", sea: "nature", easy: "rest", food: "food"};   // 예전 공유 링크(?qt=5.food…)
  const QT_AIR = {icn: {base: "seoul", second: ["busan", "jeju", "gyeongju", "jeonju", "gangneung"]}, pus: {base: "busan", second: ["gyeongju", "jeju"]}, cju: {base: "jeju", second: []}};
  const QT_PICK = {food: "busan", shop: "busan", history: "gyeongju", nature: "jeju", kpop: "busan", rest: "jeju"};   // 첫 테마 → 두 번째 도시 기본값
  /* 비 오는 날 실내 대안 (관광공사 중심관광지·공식 누리집에 있는 곳. 운영시간은 가기 전 확인) */
  const QT_RAIN = {seoul: [["국립중앙박물관", "National Museum of Korea"]], busan: [["신세계 센텀시티", "Shinsegae Centum City"]], jeju: [["아르떼뮤지엄 제주", "ARTE MUSEUM Jeju"], ["아쿠아플라넷 제주", "Aqua Planet Jeju"]],
    gyeongju: [["국립경주박물관", "Gyeongju National Museum"]], jeonju: [["국립전주박물관", "National Jeonju Museum"]], gangneung: [["아르떼뮤지엄 강릉", "ARTE MUSEUM Gangneung"]], suwon: [["화성행궁", "Hwaseong Haenggung Palace"]]};
