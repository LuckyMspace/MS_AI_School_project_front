import streamlit as st
import re
import requests


# 임시 코드
def signup_section():
    st.success("회원가입 임시 세션", icon="✅")
    # 회원가입 세션 활성화 여부에 따라 다른 UI를 보여줌
    if st.session_state["sign_up"]:  # p_4
        st.markdown("<h1 style='font-size: 32px;'>회원가입</h1>", unsafe_allow_html=True)

        signup_username = st.text_input("username")
        signup_id = st.text_input("email", key="signup_email")
        signup_pw = st.text_input("password", type="password")
        signup_confirm_pw = st.text_input("confirm_password", type="password")
        signup_gender = st.selectbox("gender", ["Male", "Female"])

        # 형식검증 없애자고 했던 것 같음
        # 이메일 형식 검증
        def validate_email(email):
            regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$"  # 이거 더 고쳐야됨...
            if re.search(regex, email):
                return True
            else:
                return False

        # 비밀번호 형식 검증
        def validate_password(password):
            regex = r"^.{6,}$"  # 일단 6자리 이상이어야함
            if re.search(regex, password):
                return True
            else:
                return False

        # 회원가입 버튼 클릭 후 세션 이동
        if st.button("회원가입 신청"):  # HJ_01
            if signup_pw == signup_confirm_pw:
                if validate_email(signup_id) and validate_password(
                    signup_pw
                ):  # 이메일 형식 및 비밀번호 형식 검증
                    response = requests.post(
                        "http://localhost:5000/sign-up",
                        json={
                            "username": signup_username,
                            "email": signup_id,
                            "pw": signup_pw,
                            "gender": signup_gender,
                        },
                    )
                    if response.status_code == 200:
                        st.success("회원가입 성공")
                        st.session_state["sign_up"] = False
                        st.session_state["logged_in"] = True
                        st.experimental_rerun()
                    else:
                        st.error("회원가입 실패: " + response.json().get("msg", ""))
                else:
                    st.error("이메일 형식으로 입력해주세요.")
            else:
                st.error("비밀번호가 일치하지 않습니다.")
        if st.button("돌아가기"):
            st.session_state["sign_up"] = False
            st.experimental_rerun()
