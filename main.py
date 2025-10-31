import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# 데이터 불러오기
# -----------------------------
file_path = "data/202509_주민등록인구및세대현황_월간.csv"

# ⚠️ 파일 인코딩 오류가 나면 encoding='utf-8-sig', 'cp949' 로 바꿔가며 시도
df = pd.read_csv(file_path, encoding='cp949')

st.title("📊 주민등록 인구 및 세대 현황 시각화")

# -----------------------------
# 데이터 확인
# -----------------------------
st.subheader("데이터 미리보기")
st.dataframe(df.head())

# -----------------------------
# 컬럼 선택 (⚠️ 여기서 네 CSV 컬럼명에 맞게 수정!)
# -----------------------------
# 예시 컬럼 → "행정구역", "총인구수", "세대수", "남자", "여자"
region_col = st.selectbox("지역(행정구역) 컬럼 선택", df.columns)
population_col = st.selectbox("총 인구수 컬럼 선택", df.columns)
household_col = st.selectbox("세대수 컬럼 선택", df.columns)

# -----------------------------
# 지역 선택 필터
# -----------------------------
regions = sorted(df[region_col].unique())
selected_region = st.selectbox("지역 선택", regions)

filtered_df = df[df[region_col] == selected_region]

st.write(f"### 📍 선택한 지역: **{selected_region}**")
st.write(filtered_df)

# -----------------------------
# 그래프 1: 지역별 총 인구 수
# -----------------------------
st.subheader("📈 지역별 총 인구 수 비교")

pop_chart = px.bar(
    df,
    x=region_col,
    y=population_col,
    title="지역별 총 인구수 비교",
)
st.plotly_chart(pop_chart)

# -----------------------------
# 그래프 2: 지역별 세대수
# -----------------------------
st.subheader("🏠 지역별 세대수 비교")

house_chart = px.line(
    df,
    x=region_col,
    y=household_col,
    markers=True,
    title="지역별 세대수 변화",
)
st.plotly_chart(house_chart)

st.write("✅ 시각화 완료! 원하는 그래프를 더 요청하면 추가해줄게 🙂")


