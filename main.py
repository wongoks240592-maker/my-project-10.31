import streamlit as st
import pandas as pd
import plotly.express as px

# CSV 불러오기
file_path = "202509_202509_주민등록인구및세대현황_월간.csv"
df = pd.read_csv(file_path, encoding='cp949')

# 숫자형 데이터 쉼표 제거 및 정수 변환
for col in df.columns:
    if "인구수" in col or "세대수" in col or "총인구수" in col:
        df[col] = df[col].astype(str).str.replace(",", "").astype(int)

# UI
st.title("📊 주민등록 인구 및 세대 현황 시각화 (Plotly)")
st.write("데이터 출처: 행정안전부 주민등록 인구 통계")

# 지역 선택
region = st.selectbox("🔍 지역을 선택하세요", df["행정구역"].unique())
selected = df[df["행정구역"] == region].iloc[0]

st.subheader(f"✅ 선택한 지역: {region}")

col1, col2, col3 = st.columns(3)
col1.metric("총 인구 수", f"{selected['2025년09월_총인구수']:,} 명")
col2.metric("총 세대 수", f"{selected['2025년09월_세대수']:,} 세대")
col3.metric("성비 (남/여)", f"{selected['2025년09월_남자 인구수']:,} / {selected['2025년09월_여자 인구수']:,}")

# ---------------------------
# 1) 자치구별 총 인구수 bar 차트 (plotly)
# ---------------------------
st.subheader("📈 서울 자치구별 총 인구수 비교")
sorted_df = df.sort_values("2025년09월_총인구수", ascending=False)

fig1 = px.bar(
    sorted_df,
    x="행정구역",
    y="2025년09월_총인구수",
    title="자치구별 총 인구수",
    labels={"행정구역": "행정구역", "2025년09월_총인구수": "총 인구 수"},
)
st.plotly_chart(fig1, use_container_width=True)

# ---------------------------
# 2) 선택 지역 남/여 인구 비교 bar 차트
# ---------------------------
st.subheader(f"👨‍🦰 남자 vs 👩 여자 인구수 비교 ({region})")

gender_df = pd.DataFrame({
    "성별": ["남자", "여자"],
    "인구수": [selected["2025년09월_남자 인구수"], selected["2025년09월_여자 인구수"]]
})

fig2 = px.bar(
    gender_df,
    x="성별",
    y="인구수",
    color="성별",
    title=f"{region} 남녀 인구 비교",
    text="인구수"
)
fig2.update_traces(texttemplate="%{text:,} 명", textposition="outside")
st.plotly_chart(fig2, use_container_width=True)
