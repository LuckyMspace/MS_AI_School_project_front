import streamlit as st
import requests


def login_section():
    left_column, right_column = st.columns(2)

    # 로그인 상태마다 다른 UI 적용하기
    if st.session_state["logged_in"]:
        left_column.success("이미 로그인 되어 있습니다.")
        if left_column.button("로그아웃"):
            st.session_state["logged_in"] = False
            st.experimental_rerun()
    else:
        left_column.markdown(
            "<h1 style='font-size: 36px;'>AI패션 추천 서비스</h1>", unsafe_allow_html=True
        )
        email = left_column.text_input("이메일 주소", key="login_email")
        password = left_column.text_input("비밀번호", type="password", key="login_password")

        if left_column.button("로그인"):
            try:
                response = requests.post(
                    "http://localhost:5000/login",
                    json={"email": email, "pw": password},
                )
                if response.status_code == 200:
                    left_column.success("로그인 성공")

                    # 로그인 성공 시, 세션 상태를 업데이트합니다.
                    st.session_state["logged_in"] = True
                    st.session_state["email"] = email  # 사용자가 입력한 이메일. 여기 함수에서만 정의됨

                    st.experimental_rerun()
                else:
                    left_column.error("로그인 실패")
            except Exception as e:
                st.error(f"서버와 통신 중 문제가 발생했습니다: {e}")

        elif left_column.button("회원가입"):
            st.session_state["sign_up"] = True

    right_column.image("./front_images/main_image.jpg", use_column_width=True)


# if __name__ == '__main__':
#     login_section()
