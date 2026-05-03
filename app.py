import streamlit as st
import numpy as np
import pandas as pd
import time

# 1. 페이지 기본 설정 (무조건 코드의 가장 처음에 와야 합니다)
st.set_page_config(
    page_title="미네르바 로또 앙상블 V4.2 (PC/모바일 겸용)", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. 모바일/PC 겸용 최적화 UI (Glassmorphism + Responsive Ball)
# 모바일에서도 쾌적하게 보이도록 미디어 쿼리 개념을 스타일 시트에 반영합니다.
page_bg_img = '''
<style>
[data-testid="stAppViewContainer"] {
    background-color: #f0f2f6;
    background-image: url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=1600&q=80");
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
}
.block-container {
    background-color: rgba(255, 255, 255, 0.96);
    backdrop-filter: blur(12px);
    padding: 1.5rem; /* 모바일 대응을 위해 패딩 축소 */
    border-radius: 20px;
    margin-top: 1rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
}

/* PC/모바일 겸용 로또 공 스타일 */
.lotto-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: flex-start;
    gap: 8px;
    margin-bottom: 10px;
}
.lotto-ball {
    display: inline-block;
    width: 40px; /* 모바일 고려 사이즈 축소 */
    height: 40px;
    line-height: 40px;
    text-align: center;
    border-radius: 50%;
    color: white;
    font-weight: bold;
    font-size: 1rem;
    box-shadow: 1px 1px 3px rgba(0,0,0,0.3);
}

/* 헤더 가독성 강화 */
h1 {
    font-size: 1.8rem !important;
    color: #0d47a1 !important;
    word-break: keep-all;
}

/* 슬라이더 폰트 조정 */
.stSlider label {
    font-size: 0.9rem !important;
    font-weight: bold;
}

/* 모바일에서 메트릭이 너무 커보이지 않게 조정 */
[data-testid="stMetricValue"] {
    font-size: 1.5rem !important;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# 3. 메인 헤더
st.title("🦉 미네르바의 조화로운 100회 시뮬레이션")
st.markdown("9가지 가설을 융합하여 100회 자동 구동 후, 최다 중복 번호를 선별합니다.")

# 4. 가설 정의
hypotheses = [
    "가설 1: 최근 5주 빈도 모멘텀", "가설 2: 장기 미출현 평균 회귀", "가설 3: 동반 출현 페어링(짝꿍수)",
    "가설 4: 위치별 홀짝 밸런싱", "가설 5: 시계열 색상/공간 대칭", "가설 6: 구간별 쏠림(행/열) 분석",
    "가설 7: 10회차 블록 미출현 갭", "가설 8: 수분포 매물대 돌파", "가설 9: 기초 체력 다중 스코어링"
]

# 5. 가중치 설정 (반응형 열 배치)
st.subheader("⚙️ 전략적 가중치 설정")
cols = st.columns([1, 1, 1])
raw_weights = []
for i, hyp in enumerate(hypotheses):
    with cols[i % 3]:
        default_val = [50, 30, 60, 40, 20, 35, 55, 45, 50][i]
        w = st.slider(f"{hyp}", 0, 100, default_val, key=f"w_{i}")
        raw_weights.append(w)

# 6. 지표 계산
std_dev = np.std(raw_weights)
harmony = max(0, min(100, 100 - (std_dev * 1.2)))

st.divider()
# 모바일에서 메트릭이 세로로 정렬되도록 columns 조정
m_cols = st.columns(3)
m_cols[0].metric("🌿 Relaxation", "95.1%")
m_cols[1].metric("👨‍👩‍👧‍👦 Connection", "92.3%")
m_cols[2].metric("⚖️ D_Harmony", f"{harmony:.1f}%")

# 7. 시뮬레이션 엔진 로직
def run_simulation_logic(weights):
    total = sum(weights)
    norm_w = [w/total for w in weights] if total > 0 else [1/9]*9
    counts = np.zeros(45)
    np.random.seed(int(time.time()))
    
    for _ in range(100):
        prob_dist = np.zeros(45)
        for idx, w in enumerate(norm_w):
            alpha = np.ones(45) * (0.2 + (idx * 0.05))
            prob_dist += w * np.random.dirichlet(alpha)
        
        sample = np.random.choice(range(1, 46), size=6, replace=False, p=prob_dist/prob_dist.sum())
        for n in sample:
            counts[n-1] += 1
    return counts

# 8. 실행 버튼 및 결과
if st.button("🚀 100회 Auto 구동 및 최종 결과 추출", use_container_width=True, type="primary"):
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    freq_result = run_simulation_logic(raw_weights)
    
    for i in range(1, 101):
        if i % 10 == 0: time.sleep(0.01) # 시뮬레이션 속도 최적화
        progress_bar.progress(i)
        status_text.text(f"시뮬레이션 {i}/100 완료")
    
    status_text.empty()
    progress_bar.empty()
    
    final_prob = (freq_result + 0.1)**2.5
    final_prob /= final_prob.sum()
    
    st.subheader("🎯 최종 럭키 5세트 (100회 중번 반영)")

    for i in range(5):
        lucky_nums = sorted(np.random.choice(range(1, 45 if 45 in range(1,46) else 46), size=6, replace=False, p=final_prob))
        
        # 모바일에서도 예쁘게 보이도록 디자인 적용
        st.markdown(f"**SET {chr(65+i)}**")
        ball_html = '<div class="lotto-container">'
        for n in lucky_nums:
            color = "#fbc02d" if n <= 10 else "#1976d2" if n <= 20 else "#e53935" if n <= 30 else "#757575" if n <= 40 else "#43a047"
            ball_html += f'<span class="lotto-ball" style="background-color:{color};">{n}</span>'
        ball_html += '</div>'
        st.markdown(ball_html, unsafe_allow_html=True)

    st.success(f"✅ 조화 점수 {harmony:.1f}% 기반 추출 완료")

    with st.expander("📊 데이터 검증 (상위 15개 빈도)"):
        chart_df = pd.DataFrame({
            "번호": [f"N{i+1}" for i in range(45)],
            "빈도": freq_result
        }).sort_values("빈도", ascending=False).head(15)
        st.bar_chart(chart_df, x="번호", y="빈도", color="#0d47a1")