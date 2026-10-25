import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="포물선 운동 시뮬레이터", layout="wide")

st.title("⚽ 포물선 운동(Projectile Motion) 시뮬레이터")

# 1. 사이드바 조절 컨트롤
st.sidebar.header("⚙️ 운동 조건 설정")
v0 = st.sidebar.slider("초기 속도 (m/s)", 1.0, 100.0, 30.0)
angle_deg = st.sidebar.slider("발사 각도 (°)", 1.0, 90.0, 45.0)
g = st.sidebar.slider("중력 가속도 (m/s²)", 1.0, 25.0, 9.8)

# 2. 물리 공식으로 포물선 좌표 계산
angle_rad = np.radians(angle_deg)
t_flight = 2 * v0 * np.sin(angle_rad) / g  # 총 비행 시간
t = np.linspace(0, t_flight, 200)

x = v0 * np.cos(angle_rad) * t
y = v0 * np.sin(angle_rad) * t - 0.5 * g * (t**2)

# 핵심 지표 계산
max_height = (v0 * np.sin(angle_rad)) ** 2 / (2 * g)
max_distance = (v0**2 * np.sin(2 * angle_rad)) / g

# 3. 주요 결과 수치 출력
col1, col2, col3 = st.columns(3)
col1.metric("최고 높이", f"{max_height:.2f} m")
col2.metric("수평 도달 거리", f"{max_distance:.2f} m")
col3.metric("체류 시간", f"{t_flight:.2f} s")

# 4. Plotly 인터랙티브 그래프 그리기
fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=x,
        y=y,
        mode="lines",
        name="궤적",
        line=dict(width=3, color="#0080FF"),
    )
)

# 최고 높이 지점 표시
max_h_x = max_distance / 2
fig.add_trace(
    go.Scatter(
        x=[max_h_x],
        y=[max_height],
        mode="markers+text",
        name="최고점",
        text=["최고점"],
        textposition="top center",
        marker=dict(size=10, color="red"),
    )
)

fig.update_layout(
    title="포물선 궤적 그래프",
    xaxis_title="수평 거리 (m)",
    yaxis_title="수직 높이 (m)",
    xaxis=dict(range=[0, max(max_distance * 1.1, 10)]),
    yaxis=dict(range=[0, max(max_height * 1.2, 10)]),
    hovermode="x unified",
)

st.plotly_chart(fig, use_container_width=True)