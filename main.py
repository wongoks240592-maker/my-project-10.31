import streamlit as st
import pandas as pd
import altair as alt

# 🔹 CSV 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("202509_202509_주민등록인구및세대현황_월간.csv", encoding="cp949")
    
    # 숫자 컬럼에서 쉼표 제거하고 정수형 변환
    for col in ["2025년09월_총인구수", "2025년09월_세대수", "2025년09월_남자 인구수", "2025년09월_여자 인구수"]:
        df[col] = df[col].astype(str).str.replace(",", "").astype(int)
    
    # 행정구역명 정리 (괄호 제거)
    df["행정구역"] = df["행정구역"].str.replace(r"\s*\(.*\)", "", regex=True)
    
    return df

df = load_data()

st.title("📊 2025년 9월 주민등록 인구 및 세대 현황 대시보드")
st.write("데이터 출처: 행정안전부 주민등록 인구 통계")

# 🔹 지역 선택 기능
region = st.selectbox("지역을 선택하세요", df["행정구역"].unique())
selected = df[df["행정구역"] == region]

st.subheader(f"✅ 선택한 지역: {region}")
st.write(selected)

# 🔹 전체 지역별 인구수 바 그래프
st.subheader("📍 전체 지역 인구 비교")
chart = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x=alt.X("행정구역:N", sort="-y"),
        y="2025년09월_총인구수:Q",
        tooltip=["행정구역", "2025년09월_총인구수"]
    )
)
st.altair_chart(chart, use_container_width=True)

# 🔹 성별 인구 비교 (선택지역)
st.subheader("👫 선택 지역 성별 인구 비교")
gender_df = selected.melt(
    id_vars="행정구역",
    value_vars=["2025년09월_남자 인구수", "2025년09월_여자 인구수"],
    var_name="성별",
    value_name="인구수"
)

gender_chart = (
    alt.Chart(gender_df)
    .mark_bar()
    .encode(
        x="성별:N",
        y="인구수:Q",
        color="성별:N",
        tooltip=["성별", "인구수"]
    )
)
st.altair_chart(gender_chart, use_container_width=True)
