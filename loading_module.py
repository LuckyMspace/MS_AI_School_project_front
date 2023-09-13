import streamlit as st
import time
import requests

def result_backend():
    if not st.session_state["flask_upload_url"]:
        print("No url")
    if not st.session_state["request_form"]:
        print("No files")
    
    response = requests.post(
        st.session_state["flask_upload_url"],
        files=st.session_state["request_form"],
    )
    if response.status_code == 200:
        st.session_state["current_page"] = "result"
        st.session_state["loading"] = False
        print("Go to result")
        st.experimental_rerun()
    else:
        error_message = response.json().get("error")
        st.error(f"이미지 전송 실패: {error_message}")

def result_backend_check():
    try:
        response = requests.get(
            "http://localhost:5000/result_check", timeout=180
        )  # 엔드포인트
        response.raise_for_status()  # HTTP 에러 발생시 예외를 발생시킵니다.
        return response.json()
    except requests.RequestException as e:
        st.warning(f"백엔드로부터 응답이 없거나 잘못된 응답이 왔습니다: {e}")
        return None


def loading_session():
    st.markdown(
        f"<div style='text-align: right; font-size: 12px;'>로그인 유저: {st.session_state.get('email', '이메일 없음')}</div>",
        unsafe_allow_html=True,
    )
    st.subheader("AI패션 추천 서비스", divider="grey")

    st.image("./front_images/loading_ai_6.gif", use_column_width=True)

    st.write("AI가 열심히 분석중입니다.")
    st.write("잠시만 기다려주세요...")

    st.subheader(" ", divider="grey")

    if st.button(":rewind: 이미지 다시 올리기"):
        # st.session_state["loading"] = False
        st.session_state["current_page"] = "image_upload"
        st.experimental_rerun()

    if st.button(":x: 로그아웃"):
        st.session_state["logged_in"] = False
        st.experimental_rerun()
        
    result_backend()


if __name__ == "__main__":
    if "loading" not in st.session_state:
        st.session_state["loading"] = True
    loading_session()
