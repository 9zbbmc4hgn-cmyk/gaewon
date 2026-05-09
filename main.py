import streamlit as st
import pandas as pd
import random

# --- 설정 및 초기화 ---
st.set_page_config(page_title="오늘의 명언 & 커뮤니티", layout="centered")

# 세션 상태 초기화
if 'quotes' not in st.session_state:
    st.session_state.quotes = [
        {"author": "스티브 잡스", "text": "계속 갈구하라, 여전히 우직하게.", "likes": 5, "saved_by": []},
        {"author": "알베르트 아인슈타인", "text": "어제와 똑같이 살면서 다른 미래를 기대하는 것은 정신병 초기 증세이다.", "likes": 12, "saved_by": []}
    ]

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = ""

# --- 사이드바: 로그인 섹션 ---
st.sidebar.title("👤 계정 서비스")
if not st.session_state.logged_in:
    with st.sidebar.form("login_form"):
        user_id = st.text_input("아이디")
        password = st.text_input("비밀번호", type="password")
        login_btn = st.form_submit_button("로그인")
        
        if login_btn:
            if user_id and password: 
                st.session_state.logged_in = True
                st.session_state.user_id = user_id
                st.rerun()
            else:
                st.error("정보를 모두 입력해주세요.")
else:
    st.sidebar.success(f"{st.session_state.user_id}님 환영합니다!")
    if st.sidebar.button("로그아웃"):
        st.session_state.logged_in = False
        st.rerun()

# --- 메인 화면: 오늘의 명언 추천 ---
st.title("🌟 오늘의 명언")
if st.button("랜덤 명언 가져오기"):
    daily_quote = random.choice(st.session_state.quotes)
    st.info(f"\"{daily_quote['text']}\" - {daily_quote['author']}")

st.divider()

# --- 명언 올리기 (로그인 시에만 가능) ---
if st.session_state.logged_in:
    st.subheader("📝 새로운 명언 등록")
    with st.form("add_quote_form", clear_on_submit=True):
        new_text = st.text_area("명언 내용")
        new_author = st.text_input("저자 (본인이면 닉네임)")
        submit_btn = st.form_submit_button("등록하기")
        
        if submit_btn and new_text:
            new_data = {"author": new_author, "text": new_text, "likes": 0, "saved_by": []}
            st.session_state.quotes.append(new_data)
            st.success("명언이 등록되었습니다!")
            st.rerun()
else:
    st.warning("명언을 등록하려면 로그인이 필요합니다.")

st.divider()

# --- 명언 피드 (좋아요 & 저장 기능) ---
st.subheader("🌈 모두의 명언함")
for idx, q in enumerate(st.session_state.quotes):
    with st.container(border=True):
        st.write(f"**\"{q['text']}\"**")
        st.caption(f"- {q['author']}")
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button(f"❤️ {q['likes']}", key=f"like_{idx}"):
                st.session_state.quotes[idx]['likes'] += 1
                st.rerun()
        with col2:
            if st.session_state.logged_in:
                is_saved = st.session_state.user_id in q['saved_by']
                save_label = "✅ 저장됨" if is_saved else "💾 저장하기"
                if st.button(save_label, key=f"save_{idx}"):
                    if not is_saved:
                        st.session_state.quotes[idx]['saved_by'].append(st.session_state.user_id)
                    else:
                        st.session_state.quotes[idx]['saved_by'].remove(st.session_state.user_id)
                    st.rerun()

# --- 내 저장함 섹션 ---
if st.session_state.logged_in:
    st.divider()
    st.subheader("📂 내가 저장한 명언")
    my_saved = [q for q in st.session_state.quotes if st.session_state.user_id in q['saved_by']]
    
    # 이 부분의 들여쓰기를 수정했습니다.
    if len(my_saved) > 0:
        for sq in my_saved:
            st.write(f"• {sq['text']} ({sq['author']})")
    else:
        st.write("아직 저장한 명언이 없습니다.")
