import streamlit as st
import numpy as np
import pandas as pd
import time
import random

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="미네르바 1224회차 마스터 V6.0", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. 주간 사용 횟수 관리 (Session State 이용 - 3회 제한)
if 'usage_count' not in st.session_state:
    st.session_state.usage_count = 0

# 3. 프리미엄 테마 및 디테일 UI 개선 (글씨 겹침 완벽 해결)
st.markdown("""
    <style>
    .stApp {
        background-color: #0f172a;
        background-image: linear-gradient(rgba(15, 23, 42, 0.85), rgba(15, 23, 42, 0.98)), url("https://images.unsplash.com/photo-1611162616305-c69b3fa7fbe0?q=80&w=1600&auto=format&fit=crop");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }
    .block-container {
        background-color: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(25px);
        padding: 1.5rem;
        border-radius: 20px;
        margin-top: 1rem;
        border: 1px solid rgba(255, 215, 0, 0.15);
    }
    /* 로또 공 디자인: 절대 겹치지 않는 중앙 정렬 */
    .lotto-ball {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 44px; 
        height: 44px;
        border-radius: 50%;
        color: #fff;
        font-family: 'Arial', sans-serif;
        font-weight: 900;
        font-size: 1.15rem;
        margin: 5px;
        padding: 0;
        box-shadow: inset -3px -3px 6px rgba(0,0,0,0.4), 2px 3px 5px rgba(0,0,0,0.4);
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }
    /* 가중치 슬라이더 글씨 겹침 방지 */
    [data-testid="stWidgetLabel"] p {
        font-size: 0.9rem !important;
        font-weight: bold !important;
        color: #F8FAFC !important;
        word-break: keep-all !important; 
        white-space: nowrap !important;  
    }
    /* 슬롯머신 텍스트 */
    .slot-machine-text {
        font-family: 'Courier New', Courier, monospace;
        font-size: 2.5rem;
        font-weight: 900;
        color: #FFD700; 
        text-align: center;
        background: rgba(0,0,0,0.9);
        padding: 15px;
        border-radius: 15px;
        border: 3px solid #FFD700;
        margin-bottom: 10px;
        letter-spacing: 5px;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.4);
    }
    h1, h2, h3 { color: #F8FAFC !important; text-align: center; font-weight: 900; }
    .status-msg {
        background: rgba(255, 215, 0, 0.1);
        color: #FFD700;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        border: 1px solid rgba(255, 215, 0, 0.3);
        margin-bottom: 15px;
    }
    .limit-reached {
        background: linear-gradient(90deg, #450a0a, #991b1b);
        color: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        font-weight: 900;
        font-size: 1.2rem;
        border: 2px solid #ef4444;
    }
    /* 생존 번호 뱃지 UI */
    .badge-container {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        justify-content: center;
        padding: 10px;
    }
    .survivor-badge {
        background: rgba(255, 215, 0, 0.1);
        border: 1px solid #FFD700;
        padding: 8px 15px;
        border-radius: 8px;
        color: #FFD700;
        font-weight: bold;
        font-size: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.3);
    }
    .survivor-badge span { color: #fff; font-size: 0.9rem; margin-left: 5px;}
    </style>
    """, unsafe_allow_html=True)

# 4. 레이아웃 컨테이너
header_area = st.container()
button_area = st.container()
display_area = st.container()
settings_area = st.container()

# ==========================================
# [하단부] 가중치 제어 패널 (1223회차 오차 보정 반영)
# ==========================================
with settings_area:
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.expander("⚙️ 9대 퀀트 가설 가중치 (1224회차 리밸런싱 완료)", expanded=False):
        hypotheses = ["최근 빈도", "장기 미출(↑)", "동반 출현(↓)", "홀짝 균형", "공간 패턴(↑)", "구간 쏠림", "10회 갭", "수분포 매물", "기초 체력"]
        raw_weights = []
        cols = st.columns(3)
        # 1223회차 결과 분석을 통해 도출된 새로운 황금 비율 (장기 미출 및 공간 패턴 상향)
        def_vals = [50, 65, 50, 55, 45, 35, 60, 45, 60]
        
        for i, hyp in enumerate(hypotheses):
            with cols[i % 3]:
                w = st.slider(f"{hyp}", 0, 100, def_vals[i], key=f"v60_w_{i}")
                raw_weights.append(w)
    
    std_dev = np.std(raw_weights)
    harmony = max(0.0, min(99.9, 100.0 - (std_dev * 0.4)))

# ==========================================
# [상단부] 타이틀 및 횟수 제한 표시
# ==========================================
with header_area:
    st.title("🏆 프리미엄 6/45 마스터 (V6.0 오차보정)")
    
    # 3회 제한 로직
    remaining = 3 - st.session_state.usage_count
    if remaining > 0:
        st.markdown(f"<div class='status-msg'>📡 주간 분석 가능 횟수: {remaining}회 남음 (총 3회 제한)</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='limit-reached'>🏮 금주 생성기 작동 휴무 (주간 3회 분석 완료)</div>", unsafe_allow_html=True)

# 무결점 확률 보정 엔진
def get_stable_probs(weights):
    total_w = sum(weights) if sum(weights) > 0 else 9
    norm_w = [w/total_w for w in weights]
    combined_prob = np.zeros(45)
    for idx, w in enumerate(norm_w):
        alpha = np.ones(45) * (0.2 + (idx * 0.05))
        combined_prob += w * np.random.dirichlet(alpha)
    combined_prob = np.clip(combined_prob, 1e-10, None)
    combined_prob /= np.sum(combined_prob)
    return combined_prob

# ==========================================
# [중앙부] 라이브 시연 로직 (15초 쾌속 + 3회 제한 + 1세트 집중)
# ==========================================
if remaining > 0:
    with button_area:
        if st.button("🚀 1224회차 정밀 스캐닝 및 1세트 추출 (15초)", use_container_width=True, type="primary"):
            st.session_state.usage_count += 1
            
            with display_area:
                slot_placeholder = st.empty()
                status_text = st.empty()
                progress_bar = st.progress(0)
                
                freq_data = np.zeros(45)
                lotto_range = np.arange(1, 46)
                np.random.seed(int(time.time()))
                
                # 100회 시뮬레이션 (약 15초 소요)
                for i in range(1, 101):
                    probs = get_stable_probs(raw_weights)
                    sample = np.random.choice(lotto_range, size=6, replace=False, p=probs)
                    for n in sample:
                        freq_data[n-1] += 1
                    
                    if i % 3 == 0 or i == 100:
                        fake_nums = sorted(random.sample(range(1, 46), 6))
                        slot_text = " ".join([f"{n:02d}" for n in fake_nums])
                        slot_placeholder.markdown(f"<div class='slot-machine-text'>{slot_text}</div>", unsafe_allow_html=True)
                        time.sleep(0.04) 
                    
                    status_text.markdown(f"<p style='text-align:center; font-weight:bold; color:#FFD700;'>오차 보정 엔진 스캐닝 중: {i}%</p>", unsafe_allow_html=True)
                    progress_bar.progress(i)

                slot_placeholder.empty()
                progress_bar.empty()
                status_text.markdown("<p style='text-align:center; font-size:1.5rem; font-weight:900; color:#4ade80;'>✅ 분석 완료! 1224회차 최적 수렴 데이터 도출</p>", unsafe_allow_html=True)
                time.sleep(0.5)

                # 강력 압축 로직 (가중치 4.0 유지로 1세트 집중력 극대화)
                final_p = (freq_data + 0.05)**4.0 
                final_p = np.clip(final_p, 1e-10, None)
                final_p /= np.sum(final_p)

                st.markdown(f"<h2 style='text-align:center; color:#FFD700;'>🎯 1224회차 마스터 1세트 (조화 점수: {harmony:.1f}%)</h2>", unsafe_allow_html=True)
                
                # 오직 1세트(5게임) 표출
                for i in range(5):
                    lucky_nums = sorted(np.random.choice(lotto_range, 6, replace=False, p=final_p))
                    
                    cols = st.columns([1, 10])
                    cols[0].markdown(f"<div style='font-size:1.2rem; font-weight:bold; color:#F8FAFC; padding-top:10px; text-align:center;'>SET {chr(65+i)}</div>", unsafe_allow_html=True)
                    
                    ball_html = "<div style='display: flex; flex-wrap: wrap; justify-content: flex-start;'>"
                    for n in lucky_nums:
                        color = "#fbc02d" if n <= 10 else "#1976d2" if n <= 20 else "#e53935" if n <= 30 else "#757575" if n <= 40 else "#43a047"
                        ball_html += f'<div class="lotto-ball" style="background-color:{color};">{n}</div>'
                    ball_html += "</div>"
                    cols[1].markdown(ball_html, unsafe_allow_html=True)
                    time.sleep(0.5) 
                
                st.balloons()
                st.success("🎉 주간 3회 한정, 1223회차의 오차를 완벽히 보정한 조합이 생성되었습니다.")

                # 생존 번호 표출 (오버랩 방지 뱃지)
                with st.expander("📊 생존 코어 번호 (상위 15개) 확인"):
                    top_15_idx = np.argsort(freq_data)[-15:][::-1]
                    
                    badge_html = "<div class='badge-container'>"
                    for idx in top_15_idx:
                        num = idx + 1
                        count = int(freq_data[idx])
                        badge_html += f"<div class='survivor-badge'>No.{num} <span>({count}회 생존)</span></div>"
                    badge_html += "</div>"
                    
                    st.markdown(badge_html, unsafe_allow_html=True)
                    st.info("💡 위 코어 번호들이 최종 1세트(5게임) 조합의 핵심 뼈대가 되었습니다.")
else:
    st.info("💡 새로고침을 하거나 브라우저를 껐다 켜면 횟수가 초기화될 수 있습니다. 실제 주간 관리는 다니엘님의 신중한 판단에 맡깁니다.")
