import streamlit as st
import requests

# 여기에 로그인 된 상태 세션을 정의해야할 듯

def login_section():
    left_column, right_column = st.columns(2)
    # 로그인 폼
    left_column.markdown("<h1 style='font-size: 36px;'>AI패션 추천 서비스</h1>", unsafe_allow_html=True)
    email = left_column.text_input("이메일 주소", key='login_email')
    password = left_column.text_input("비밀번호", type="password", key='login_password')    

    if left_column.button("로그인"):
        try:                                            # 엔드포인트 
            response = requests.post("http://localhost:5000/login", data={"email": email, "password": password}) # 추후 협의 후 json으로 변경
            if response.status_code == 200:  # 이 if문 코드는 로그인이 성공하면 어느 세션을 가도 로그인 상태가 유지되는 것으로 파악됨.
                # 다만 로그인 상태라는 것을 확인할 수 있는 UI를 구성하지 않아서 헷갈리는 것 같음.
                # 해결 가능성이 보임.
                left_column.success("로그인 성공")
                st.session_state['logged_in'] = True
                st.experimental_rerun()                
                # st.write("Debug: Session State after login", st.session_state)  # 디버깅 코드
            else:
                left_column.error("로그인 실패")
        except Exception as e:
            st.error(f"서버와 통신 중 문제가 발생했습니다: {e}")

    elif left_column.button("회원가입"):
        st.session_state['sign_up'] = True

    right_column.image("./front_images/main_image.jpg", use_column_width=True)
