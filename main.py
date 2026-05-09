import streamlit as st
import requests

# 1. 여기에 새로 발급받은 키를 넣으세요
RIOT_API_KEY = "RGAPI-XXXX-XXXX-XXXX" 

st.title("LoL 전적 검색 디버거")

name = st.text_input("소환사명")
tag = st.text_input("태그 (예: KR1)")

if st.button("연결 테스트"):
    # API 호출
    url = f"https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}?api_key={RIOT_API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        st.success("연결 성공!")
        st.json(response.json()) # 가져온 데이터 결과 출력
    elif response.status_code == 403:
        st.error("오류 403: API 키가 만료되었거나 권한이 없습니다. 키를 갱신하세요.")
    elif response.status_code == 404:
        st.error("오류 404: 해당 소환사를 찾을 수 없습니다. 이름과 태그를 확인하세요.")
    elif response.status_code == 429:
        st.error("오류 429: 너무 많은 요청을 보냈습니다. 잠시 후 시도하세요.")
    else:
        st.error(f"알 수 없는 오류 발생: {response.status_code}")
