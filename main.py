import streamlit as st
import pandas as pd
import requests

# 페이지 설정
st.set_page_config(page_title="LoL 데이터 센터", page_icon="⚔️", layout="wide")

# 로고 및 타이틀
st.title("🎮 League of Legends 전적 & 데이터 대시보드")
st.markdown("---")

# --- 사이드바: 소환사 검색 기능 ---
st.sidebar.header("🔍 소환사 검색")
summoner_name = st.sidebar.text_input("소환사명 입력", placeholder="예: Hide on bush")
tag_line = st.sidebar.text_input("태그 입력", placeholder="예: KR1")

if st.sidebar.button("전적 불러오기"):
    if summoner_name and tag_line:
        st.sidebar.success(f"{summoner_name}#{tag_line} 데이터를 찾는 중...")
        # 여기에 추후 Riot API 연동 코드를 추가할 수 있습니다.
    else:
        st.sidebar.error("이름과 태그를 모두 입력해주세요.")

# --- 메인 화면: 챔피언 정보 조회 ---
st.header("🏆 챔피언 도감")

@st.cache_data
def get_champion_data():
    # 최신 데이터 드래곤 버전 가져오기
    version_url = "https://ddragon.leagueoflegends.com/api/versions.json"
    version = requests.get(version_url).json()[0]
    
    # 전체 챔피언 데이터 가져오기
    url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/ko_KR/champion.json"
    response = requests.get(url).json()
    return response['data'], version

champions, current_version = get_champion_data()
champion_names = sorted([champions[c]['name'] for c in champions])

# 검색창 및 선택
col1, col2 = st.columns([1, 2])
with col1:
    selected_champ_name = st.selectbox("챔피언을 선택하세요", champion_names)

# 선택된 챔피언 상세 정보 표시
selected_id = [k for k, v in champions.items() if v['name'] == selected_champ_name][0]
champ_info = champions[selected_id]

with col2:
    st.subheader(f"{selected_champ_name} : {champ_info['title']}")
    st.write(f"**역할:** {', '.join(champ_info['tags'])}")
    st.write(champ_info['blurb'])

# 챔피언 이미지 출력
img_url = f"https://ddragon.leagueoflegends.com/cdn/{current_version}/img/champion/{selected_id}.png"
col1.image(img_url, width=200)

# --- 통계 시각화 (더미 데이터 예시) ---
st.markdown("---")
st.header("📊 현재 메타 분석 (샘플)")

data = {
    'Champion': ['Aatrox', 'Ahri', 'Jinx', 'Lee Sin', 'Thresh'],
    'Pick Rate (%)': [12.5, 8.4, 15.2, 20.1, 10.7],
    'Win Rate (%)': [51.2, 49.8, 52.5, 48.9, 50.1]
}
df = pd.DataFrame(data)

col_a, col_b = st.columns(2)
with col_a:
    st.write("### 픽률 순위")
    st.bar_chart(df.set_index('Champion')['Pick Rate (%)'])
with col_b:
    st.write("### 승률 데이터")
    st.dataframe(df, use_container_width=True)

st.divider()
st.caption(f"Data Source: Riot Games Data Dragon (Ver {current_version})")
