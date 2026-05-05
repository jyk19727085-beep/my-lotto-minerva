<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>DANIEL COMMAND CENTER V16.8</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/lucide@latest"></script>
  <style>
    /* 모바일 스크롤 멈춤(먹통) 원천 차단 */
    body { background-color: #020202; color: #e2e8f0; font-family: sans-serif; overflow-x: hidden; touch-action: auto; }
    /* 위젯이 터치를 가로채지 않도록 안정화 */
    iframe { border: none; width: 100%; height: 100%; pointer-events: auto !important; }
    .widget-box { background: #0a0a0a; border: 1px solid #1e293b; border-radius: 12px; overflow: hidden; position: relative; z-index: 10; }
    /* 버튼/링크 터치 우선순위 최상단으로 격상 */
    .touch-target { position: relative; z-index: 50; touch-action: manipulation; -webkit-tap-highlight-color: transparent; }
  </style>
</head>
<body class="p-3 md:p-6 pb-20">
  <div class="max-w-[1200px] mx-auto space-y-5">
    
    <!-- 1. 헤더 & 강제 업데이트 버튼 -->
    <header class="flex flex-col gap-4 border-b border-slate-800 pb-5">
      <div class="flex items-center gap-3">
        <div class="bg-indigo-600 p-2 rounded-xl shadow-lg shadow-indigo-500/30">
          <i data-lucide="globe" class="text-white w-6 h-6"></i>
        </div>
        <h1 class="text-2xl font-black text-white uppercase tracking-tighter">Daniel Terminal <span class="text-emerald-400 text-sm">V16.8</span></h1>
      </div>
      <button id="updateBtn" class="touch-target w-full bg-indigo-600 hover:bg-indigo-500 text-white py-5 rounded-xl font-black shadow-xl active:scale-95 flex items-center justify-center gap-2 transition-all text-lg">
        <i data-lucide="refresh-cw" id="updateIcon"></i> 실시간 데이터 강제 업데이트
      </button>
    </header>

    <!-- 2. 글로벌 티커 -->
    <div class="h-14 widget-box">
      <iframe src="https://s.tradingview.com/embed-widget/ticker-tape/?locale=kr&colorTheme=dark&isTransparent=true&displayMode=regular&showSymbolLogo=true&symbols=%5B%7B%22proName%22%3A%22NASDAQ%3AIXIC%22%2C%22title%22%3A%22나스닥%22%7D%2C%7B%22proName%22%3A%22SP%3ASPX%22%2C%22title%22%3A%22S%26P%20500%22%7D%2C%7B%22proName%22%3A%22KRX%3AKOSPI%22%2C%22title%22%3A%22KOSPI%22%7D%2C%7B%22proName%22%3A%22FX_IDC%3AUSDKRW%22%2C%22title%22%3A%22원%2F달러%22%7D%5D"></iframe>
    </div>

    <!-- 3. 한국 시장(KRX) 히트맵 -->
    <div class="h-[550px] widget-box flex flex-col">
      <div class="p-3 border-b border-slate-800 flex justify-between items-center bg-[#0d0d0d]">
        <span class="text-sm font-black text-emerald-400 flex items-center gap-1"><i data-lucide="layout-grid" class="w-4 h-4"></i> 실시간 국내 증시 (KRX)</span>
      </div>
      <div class="flex-grow w-full relative">
        <!-- 터치 스크롤 방해 방지를 위한 여백 래퍼 -->
        <iframe id="krxMap" src="https://s.tradingview.com/embed-widget/stock-heatmap/?locale=kr&dataSource=KRX&colorTheme=dark&hasSymbolLogo=true&grouping=sector&market=all&symbolBy=market_cap&size=market_cap&color=change"></iframe>
      </div>
    </div>

    <!-- 4. 나스닥 & 실시간 뉴스 -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div class="h-[400px] widget-box">
        <iframe src="https://s.tradingview.com/embed-widget/technical-analysis/?locale=kr&colorTheme=dark&symbol=NASDAQ%3AIXIC&interval=1h&isTransparent=true"></iframe>
      </div>
      <div class="h-[450px] widget-box">
        <iframe src="https://s.tradingview.com/embed-widget/timeline/?locale=kr&colorTheme=dark&isTransparent=true&displayMode=regular"></iframe>
      </div>
    </div>

    <!-- 5. 4대 핵심 전략 외부 링크 (복구 및 터치 최적화) -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-3 pt-4">
      <a href="https://whalewisdom.com/" target="_blank" class="touch-target p-5 bg-[#0c0c0c] border border-slate-700 hover:border-indigo-500 rounded-2xl flex flex-col items-center text-center shadow-lg active:scale-95 transition-all">
        <i data-lucide="target" class="w-8 h-8 text-indigo-400 mb-2"></i>
        <span class="font-black text-white uppercase text-sm">WhaleWisdom</span>
        <span class="text-[10px] text-slate-400 mt-1">13F 기관 공시</span>
      </a>
      <a href="https://finance.naver.com/sise/" target="_blank" class="touch-target p-5 bg-[#0c0c0c] border border-slate-700 hover:border-emerald-500 rounded-2xl flex flex-col items-center text-center shadow-lg active:scale-95 transition-all">
        <i data-lucide="bar-chart-3" class="w-8 h-8 text-emerald-400 mb-2"></i>
        <span class="font-black text-white uppercase text-sm">Naver 증권</span>
        <span class="text-[10px] text-slate-400 mt-1">국내 장중 수급</span>
      </a>
      <a href="https://edition.cnn.com/markets/fear-and-greed" target="_blank" class="touch-target p-5 bg-[#0c0c0c] border border-slate-700 hover:border-rose-500 rounded-2xl flex flex-col items-center text-center shadow-lg active:scale-95 transition-all">
        <i data-lucide="zap" class="w-8 h-8 text-rose-400 mb-2"></i>
        <span class="font-black text-white uppercase text-sm">Fear & Greed</span>
        <span class="text-[10px] text-slate-400 mt-1">글로벌 심리 지표</span>
      </a>
      <a href="https://www.cmegroup.com/markets/interest-rates/target-rate-probabilities.html" target="_blank" class="touch-target p-5 bg-[#0c0c0c] border border-slate-700 hover:border-blue-500 rounded-2xl flex flex-col items-center text-center shadow-lg active:scale-95 transition-all">
        <i data-lucide="shield-check" class="w-8 h-8 text-blue-400 mb-2"></i>
        <span class="font-black text-white uppercase text-sm">CME FedWatch</span>
        <span class="text-[10px] text-slate-400 mt-1">연준 금리 확률</span>
      </a>
    </div>

  </div>

  <script>
    lucide.createIcons();
    const btn = document.getElementById('updateBtn');
    const icon = document.getElementById('updateIcon');
    
    // 버튼 터치 시 무조건 캐시 파괴 후 새 데이터 로딩
    btn.addEventListener('click', () => {
      icon.classList.add('animate-spin');
      
      document.querySelectorAll('iframe').forEach(f => {
        const baseUrl = f.src.split('?')[0];
        const params = new URLSearchParams(f.src.split('?')[1]);
        params.set('cb', Date.now()); // 강력한 난수 캐시 버스팅
        f.src = baseUrl + '?' + params.toString();
      });
      
      setTimeout(() => icon.classList.remove('animate-spin'), 1000);
    });
  </script>
</body>
</html>
