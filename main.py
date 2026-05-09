import streamlit as st
import requests
import pandas as pd

# --- 설정 및 API 키 ---
# 실무에서는 st.secrets["RIOT_API_KEY"]를 사용하는 것이 안전합니다.
RIOT_API_KEY = "YOUR_RIOT_API_KEY_HERE" 

st.set_page_config(page_title="LoL 전적 검색기", page_icon="🎯")

# --- 함수 정의: 데이터 가져오기 ---
def get_summoner_info(name, tag, api_key):
    # 1. Account-V1을 통해 PUUID 가져오기
    url = f"https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}?api_key={api_key}"
    res = requests.get(url)
    return res.json() if res.status_code == 200 else None

def get_match_ids(puuid, api_key, count=5):
    # 2. 최근 매치 ID 리스트 가져오기 (5개)
    url = f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}&api_key={api_key}"
    res = requests.get(url)
    return res.json() if res.status_code == 200 else []

# --- UI 부분 ---
st.title("🏹 LoL 전적 검색 사이트")
st.markdown("소환사명과 태그를 입력하여 최근 전적을 확인하세요.")

col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    name_input = st.text_input("소환사 이름", placeholder="Hide on bush")
with col2:
    tag_input = st.text_input("태그", placeholder="KR1")
with col3:
    st.write(" ") # 간격 맞춤
    search_btn = st.button("검색")

if search_btn:
    if not RIOT_API_KEY or RIOT_API_KEY == "YOUR_RIOT_API_KEY_HERE":
        st.error("Riot API Key를 설정해야 실제 데이터를 불러올 수 있습니다!")
    else:
        with st.spinner('데이터를 불러오는 중...'):
            user_data = get_summoner_info(name_input, tag_input, RIOT_API_KEY)
            
            if user_data and 'puuid' in user_data:
                puuid = user_data['puuid']
                st.success(f"**{user_data['gameName']}#{user_data['tagLine']}** 님을 찾았습니다!")
                
                # 매치 기록 가져오기
                match_ids = get_match_ids(puuid, RIOT_API_KEY)
                
                if match_ids:
                    st.subheader(" 최근 5게임 매치 기록")
                    for m_id in match_ids:
                        # 매치 상세 정보 (간략화)
                        st.info(f"매치 ID: {m_id} - 상세 정보 분석 중...")
                        # 상세 데이터는 match/v5/matches/{m_id} 를 통해 가져와서 가공 가능
                else:
                    st.warning("최근 게임 기록이 없습니다.")
            else:
                st.error("소환사를 찾을 수 없습니다. 이름과 태그를 다시 확인해주세요.")

# --- 가이드 (API 키 발급 방법) ---
with st.expander("ℹ️ 실제 전적 데이터가 나오게 하려면?"):
    st.write("""
    1. [Riot Developer Portal](https://developer.riotgames.com/) 접속 및 로그인
    2. 'Development API Key'를 복사합니다.
    3. 코드의 `RIOT_API_KEY = "..."` 부분에 붙여넣으세요.
    4. (주의) 개발용 키는 24시간마다 만료되므로 다시 갱신해야 합니다.
    """)
