import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="주민등록 인구 현황 시각화", layout="wide")

# CSV 불러오기
file_path = "202509_202509_주민등록인구및세대현황_월간.csv"
df = pd.read_csv(file_path, encoding='cp949')

# 숫자 데이터형 변환
for col in df.columns:
    if any(key in col for key in ["인구수", "세대수", "총인구"]):
        df[col] = df[col].astype(str).str.replace(",", "").astype(int)

# 제목
st.title("📊 주민등록 인구 및 세대 현황 데이터 시각화")
st.write("행정안전부 주민등록 인구통계 기반 · Plotly & Streamlit")

# 지역 선택
region = st.selectbox("🔍 조회할 지역을 선택하세요:", df["행정구역"].unique())
selected = df[df["행정구역"] == region].iloc[0]

# 지표 카드 표시
col1, col2, col3 = st.columns(3)
col1.metric("총 인구 수", f"{selected['2025년09월_총인구수']:,} 명")
col2.metric("총 세대 수", f"{selected['2025년09월_세대수']:,} 세대")
col3.metric("성비 (남 / 여)", 
            f"{selected['2025년09월_남자 인구수']:,} / {selected['2025년09월_여자 인구수']:,}")

# ---------------------------
# 1) 전체 구별 총 인구 비교
# ---------------------------
st.subheader("🏙️ 자치구별 총 인구수 비교")

sorted_df = df.sort_values("2025년09월_총인구수", ascending=False)
fig1 = px.bar(
    sorted_df,
    x="행정구역",
    y="2025년09월_총인구수",
    title="서울 자치구별 총 인구수",
    labels={"2025년09월_총인구수": "총 인구 수", "행정구역": "지역"},
)
st.plotly_chart(fig1, use_container_width=True)

# ---------------------------
# 2) 선택 지역 남녀 인구 비교
# ---------------------------
st.subheader(f"👨‍🦰 남녀 인구 비교 ({region})")

gender_df = pd.DataFrame({
    "성별": ["남자", "여자"],
    "인구수": [selected["2025년09월_남자 인구수"], selected["2025년09월_여자 인구수"]]
})

fig2 = px.bar(
    gender_df,
    x="성별",
    y="인구수",
    color="성별",
    text="인구수",
    title=f"{region} 남녀 인구 비교"
)
fig2.update_traces(texttemplate="%{text:,} 명", textposition="outside")
st.plotly_chart(fig2, use_container_width=True)


