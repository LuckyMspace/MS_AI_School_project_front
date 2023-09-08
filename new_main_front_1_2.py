import streamlit as st

from login_module import login_section
from image_upload_module import image_upload_section
from signup_section import signup_section


# 세션 상태 초기화
if 'logged_in' not in st.session_state:   # p_1
    st.session_state['logged_in'] = False

if 'loading' not in st.session_state: # p_2
    st.session_state['loading'] = False

if 'sign_up' not in st.session_state: # p_3
    st.session_state['sign_up'] = False

if 'result' not in st.session_state: # p_4
    st.session_state['result'] = False

if 'fail' not in st.session_state: # p_5
    st.session_state['fail'] = False

# 메인 앱 로직
if not st.session_state['logged_in']:
    if st.session_state['sign_up']:
        signup_section()  # 회원가입 UI 및 로직 처리
    else:
        login_section()  # 로그인 UI 및 로직 처리
else:
    
    if st.session_state['loading']:
        pass
        # 로딩 로직 처리 (예: 로딩 이미지 표시)
    elif st.session_state['result']:
        pass
        # 결과 표시 로직 처리
    elif st.session_state['fail']:
        pass
        # 실패 처리 로직
    else:
        image_upload_section()  # 이미지 업로드 UI 및 로직 처리

