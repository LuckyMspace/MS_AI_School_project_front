import streamlit as st
from login_module import login_section
from image_upload_module import image_upload_section
from signup_module import signup_section
from result_module import result_session
from loading_module import loading_session


# Initialize session states if not already done

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "loading" not in st.session_state:
    st.session_state["loading"] = False
if "result" not in st.session_state:
    st.session_state["result"] = False
if "sign_up" not in st.session_state:
    st.session_state["sign_up"] = False
if "fail" not in st.session_state:
    st.session_state["fail"] = False
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "login"

# 유저 정보 상태
if st.session_state.get("logged_in", False):
    st.markdown(
        f"<div style='text-align: right; font-size: 12px;'>로그인 유저: {st.session_state.get('email','이메일 없음')}</div>",
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        "<div style='text-align: right; font-size: 12px;'>로그인 유저: Guest(비회원)</div>",
        unsafe_allow_html=True,
    )

# 메인 앱 로직
if not st.session_state["logged_in"]:  # 비 로그인상태
    if st.session_state["sign_up"]:  # 회원가입 폼
        signup_section()
    else:  # 로그인 폼
        login_section()

else:  # Logged in
    if st.session_state["current_page"] == "login":
        login_section()
    elif st.session_state["current_page"] == "image_upload":
        image_upload_section()
    elif st.session_state["loading"]:  # Loading session
        loading_session()
    elif st.session_state["result"]:  # Result session
        result_session()
    else:  # Default to image upload section
        image_upload_section()

        if not st.session_state.get("loading", False):
            image_upload_section()
