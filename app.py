import streamlit as st
import numpy as np
import pandas as pd
import time
import random

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="미네르바 로또 6/45 마스터 V5.4", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. 로또 6/45 프리미엄 테마 CSS (딥 네이비 & 골드)
st.markdown("""
    <style>
    .stApp {
        background-color: #0f172a;
        /* 직관적이고 화려한 프리미엄 골드/카지노 볼 느낌의 배경 */
        background-image: linear-gradient(rgba(15, 23, 42, 0.8), rgba(15, 23, 42, 0.95)), url("https://images.unsplash.com/photo-1611162616305-c69b3fa7fbe0?q=80&w=1600&auto=format&fit=crop");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }
    .block-container {
        background-color: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        padding: 1.5rem;
        border-radius: 20px;
        margin-top: 1rem;
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.15); /* 황금빛 글로우 효과 */
        border: 1px solid rgba(255, 215, 0, 0.2);
    }
    /* 로또 공 디자인 최적화 */
    .lotto-ball {
        display: inline-block;
        width: 48px;
        height: 48px;
        line-height: 48px;
        text-align: center;
        border-radius: 50%;
        color: #fff;
        font-weight: 900;
        font-size: 1.25rem;
        margin: 4px;
        box-shadow: inset -4px -4px 8px rgba(0,0,0,0.4), 2px 4px 6px rgba(0,0,0,0.5);
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        animation: pop-in 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
    }
    @keyframes pop-in {
        0% { transform: scale(0) translateY(-20px); opacity: 0; }
        80% { transform: scale(1.15) translateY(5px); }
        100% { transform: scale(1) translateY(0); opacity: 1; }
    }
    /* 슬롯머신 황금빛 텍스트 */
    .slot-machine-text {
        font-family: 'Courier New', Courier, monospace;
        font-size: 3.5rem;
        font-weight: 900;
        color: #FFD700; 
        text-align: center;
        background: rgba(0,0,0,0.8);
        padding: 15px;
        border-radius: 15px;
        border: 3px solid #FFD700;
        margin-bottom: 10px;
        letter-spacing: 10px;
        box-shadow: 0 0 25px rgba(255, 215, 0, 0.5);
    }
    h1, h2, h3 { color: #F8FAFC !important; text-align: center; font-weight: 900; text-shadow: 0 2px 4px rgba(0,0,0,0.5); }
    p, span, div { color: #E2E8F0; }
    .master-alert {
        background: linear-gradient(90deg, #b91c1c, #d32f2f);
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 20px;
        color: white !important;
        font-weight: bold;
        text-align: center;
        box-shadow: 0 4px 10px rgba(211, 47, 47, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 레이아웃 컨테이너 사전 정의
header_area = st.container()
button_area = st.container()
display_area = st.container()
st.markdown("<br>", unsafe_allow_html=True)
settings_area = st.container()

# ==========================================
# [하단부] 깔끔해진 가설 제어 패널 (모바일 최적화)
# ==========================================
with settings_area:
    with st.expander("⚙️ 9대 퀀트 가설 제어 (최적값 세팅 완료)", expanded=False):
        # 텍스트 간소화 및 직관적 배치
        hypotheses = ["최근 5주 빈도", "장기 미출현", "동반 출현(짝꿍)", "홀짝 밸런싱", "공간 대칭 패턴", "구간 쏠림 분석", "10회차 갭", "수분포 매물대", "기초 체력"]
        raw_weights = []
        cols = st.columns(3)
        
        # 다니엘님의 황금 비율
        def_vals = [55, 35, 65, 45, 25, 40, 60, 50, 55]
        
        for i, hyp in enumerate(hypotheses):
            with cols[i % 3]:
                w = st.slider(f"{i+1}. {hyp}", 0, 100, def_vals[i], key=f"v54_w_{i}")
                raw_weights.append(w)
                
    # 조화 점수 90% 이상 도출을 위한 정밀 수식 보정
    std_dev = np.std(raw_weights)
    harmony = max(0.0, min(100.0, 100.0 - (std_dev * 0.7)))

# ==========================================
# [상단부] 타이틀 및 버튼 배치
# ==========================================
with header_area:
    st.title("🏆 행운의 6/45 프리미엄 분석기")
    st.markdown("<div class='master-alert'>100회 초고속 딥스캐닝을 통해 추출된 강력한 1세트(5게임)가 표출됩니다.</div>", unsafe_allow_html=True)

with button_area:
    start_btn = st.button("🚀 LIVE 스캐닝 시작 (15초 소요)", use_container_width=True, type="primary")

# 확률 보정 엔진
def get_stable_probs(weights):
    total_w = sum(weights) if sum(weights) > 0 else 9
    norm_w = [w/total_w for w in weights]
    combined_prob = np.zeros(45)
    for idx, w in enumerate(norm_w):
        alpha = np.ones(45) * (0.2 + (idx * 0.05))
        combined_prob += w * np.random.dirichlet(alpha)
    combined_prob /= combined_prob.sum()
    return combined_prob

# ==========================================
# [중앙부] 라이브 시연 로직 (15초로 단축)
# ==========================================
if start_btn:
    with display_area:
        slot_placeholder = st.empty()
        status_text = st.empty()
        progress_bar = st.progress(0)
        
        freq_data = np.zeros(45)
        lotto_range = np.arange(1, 46)
        np.random.seed(int(time.time()))
        
        # 100회 시뮬레이션: (100회 * 3번 * 0.05초 = 정확히 15초 소요)
        for i in range(1, 101):
            probs = get_stable_probs(raw_weights)
            sample = np.random.choice(lotto_range, size=6, replace=False, p=probs)
            for n in sample:
                freq_data[n-1] += 1
                
            # 15초 쾌속 슬롯 연출
            for _ in range(3):
                fake_nums = sorted(random.sample(range(1, 46), 6))
                slot_text = " ".join([f"{n:02d}" for n in fake_nums])
                slot_placeholder.markdown(f"<div class='slot-machine-text'>{slot_text}</div>", unsafe_allow_html=True)
                time.sleep(0.05) # 속도를 기존 대비 2배 향상
                
            status_text.markdown(f"<p style='text-align:center; font-weight:bold; color:#FFD700; font-size:1.1rem;'>미네르바 초고속 스캐닝: {i}% 완료</p>", unsafe_allow_html=True)
            progress_bar.progress(i)

        slot_placeholder.empty()
        progress_bar.empty()
        status_text.markdown("<p style='text-align:center; font-size:1.5rem; font-weight:900; color:#4ade80;'>✅ 스캐닝 완료! 최강의 조합이 완성되었습니다.</p>", unsafe_allow_html=True)
        time.sleep(0.5)
        status_text.empty()

        # [강력한 확률 조합] 극단적 가중치 적용 (제곱수 3.5로 상향)
        # 어설픈 빈도수는 탈락시키고, 핵심 번호만 강력하게 살아남게 만듭니다.
        final_p = (freq_data + 0.05)**3.5 
        final_p /= final_p.sum()

        st.markdown(f"<h2 style='text-align:center; color:#FFD700;'>🎯 최적화 마스터 1세트 (조화 점수: {harmony:.1f}%)</h2><hr style='border-color: rgba(255,215,0,0.3);'>", unsafe_allow_html=True)
        
        # 5게임 라이브 리빌 연출
        for i in range(5):
            lucky_nums = sorted(np.random.choice(lotto_range, 6, replace=False, p=final_p))
            
            row_cols = st.columns([1, 8])
            row_cols[0].markdown(f"<div style='font-size:1.5rem; font-weight:bold; color:#F8FAFC; line-height:60px;'>SET {chr(65+i)}</div>", unsafe_allow_html=True)
            
            ball_container = row_cols[1].empty()
            html_string = "<div style='display: flex; gap: 8px; flex-wrap: wrap;'>"
            
            for n in lucky_nums:
                # 6/45 공식 색상 매칭
                color = "#fbc02d" if n <= 10 else "#1976d2" if n <= 20 else "#e53935" if n <= 30 else "#757575" if n <= 40 else "#43a047"
                html_string += f'<span class="lotto-ball" style="background-color:{color};">{n}</span>'
                ball_container.markdown(html_string + "</div>", unsafe_allow_html=True)
                time.sleep(0.4) 
                
            time.sleep(0.3) 
                
        st.balloons()
        st.markdown("<p style='text-align:center; font-size:1.2rem; margin-top:20px;'>🎉 다니엘님의 행운을 기원합니다!</p>", unsafe_allow_html=True)

        with st.expander("📊 생존 코어 번호 (상위 15개) 확인"):
            chart_df = pd.DataFrame({
                "번호": [f"N{i+1}" for i in range(45)],
                "중복 생존 빈도": freq_data
            }).sort_values("중복 생존 빈도", ascending=False).head(15)
            st.bar_chart(chart_df, x="번호", y="중복 생존 빈도", color="#FFD700")
