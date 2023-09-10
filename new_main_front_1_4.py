import streamlit as st
from login_module import login_section
from image_upload_module import image_upload_section
from signup_module import signup_section
from result_module import result_session  
from loading_module import loading_session
from fail_module import fail

# 로그인 상태 여부 표시
if st.session_state.get('logged_in', False):
    st.markdown(f"<div style='text-align: right; font-size: 12px;'>로그인 유저: {st.session_state.get('email','이메일 없음')}</div>", unsafe_allow_html=True) # get 다음 원래 'email'
else:
    st.markdown("<div style='text-align: right; font-size: 12px;'>로그인 유저: Guest(비회원)</div>", unsafe_allow_html=True)

# 세션 상태 초기화
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if 'loading' not in st.session_state:
    st.session_state['loading'] = False

if 'sign_up' not in st.session_state:
    st.session_state['sign_up'] = False

if 'result' not in st.session_state:
    st.session_state['result'] = False

if 'fail' not in st.session_state:
    st.session_state['fail'] = False


# 메인 앱 로직
if not st.session_state['logged_in']:  # 로그인 상태가 아니라면
    if st.session_state['sign_up']:  # 회원가입 폼 표시하고
        signup_section()
    else:   # 그게 아니라면 로그인 폼 표시
        login_section()
else:    # 로그인 상태라면 
    if st.session_state['loading']:  # 이게 True라면
        loading_session()
    elif st.session_state['result']:  # 이게 True라면
        result_session()
    elif st.session_state['fail']:  # 이게 True라면
        fail()
    
    else:
        if not st.session_state['loading']:
            image_upload_section()