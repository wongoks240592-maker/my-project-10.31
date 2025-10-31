import streamlit as st
import pandas as pd
import plotly.express as px

# CSV 파일 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv('202509_202509_주민등록인구및세대현황_월간.csv', encoding='cp949')

    # 컬럼명 변경 (데이터 파일에 따라 이름이 다를 수 있어 자동 처리)
    df.columns = ['지역', '총인구', '남자', '여자', '세대수']

    # 숫자형 컬럼에서 쉼표 제거 후 정수형으로 변환
    numeric_cols = ['총인구', '남자', '여자', '세대수']
    for col in numeric_cols:
        df[col] = df[col].astype(str).str.replace(",", "").astype(int)

    return df

df = load_data()

st.title("📊 대한민국 주민등록 인구 및 세대 현황 시각화")
st.write("데이터 출처: 행정안전부 주민등록 인구 통계")

# 지역 선택
selected_region = st.selectbox("지역을 선택하세요:", df['지역'])

# 선택된 지역 데이터 표시
region_data = df[df['지역'] == selected_region]

st.subheader(f"▶ {selected_region} 데이터")
st.write(region_data)

# -------------------------------
# Plotly 시각화
# -------------------------------
st.subheader("👨‍👩‍👧 성별 인구 비중")

fig1 = px.bar(region_data.melt(id_vars='지역', value_vars=['남자', '여자']),
              x='variable', y='value', color='variable',
              labels={'variable': '성별', 'value': '인구 수'},
              title=f"{selected_region} 성별 인구 비교")

st.plotly_chart(fig1)

st.subheader("🏠 총 인구 대비 세대 수")
fig2 = px.scatter(region_data, x='총인구', y='세대수', size='세대수',
                  hover_name='지역',
                  title=f"{selected_region} 인구 대비 세대수 관계")
st.plotly_chart(fig2)

# 전체 지역 인구 순위 그래프
st.subheader("📍 전체 지역 인구 순위 Top 10")

top10 = df.sort_values(by='총인구', ascending=False).head(10)
fig3 = px.bar(top10, x='지역', y='총인구', title="인구수 상위 10개 지역")
st.plotly_chart(fig3)
