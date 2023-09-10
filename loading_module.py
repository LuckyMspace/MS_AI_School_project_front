import streamlit as st
import time
import requests

def result_backend_check():
    try:
        response = requests.get('http://localhost:5000/result_check', timeout=180)  # 엔드포인트
        response.raise_for_status()  # HTTP 에러 발생시 예외를 발생시킵니다.
        return response.json()
    except requests.RequestException as e:
        st.warning(f"백엔드로부터 응답이 없거나 잘못된 응답이 왔습니다: {e}")
        return None

def loading_session():
    left_column, right_column = st.columns(2)

    with left_column:
        st.image("./front_images/loading_image.jpg")

    with right_column:  # 여기도 꾸미는건 나중에
        st.write("AI가 의류를 분석중입니다.")
        st.write("잠시만 기다려주세요...")
    
        time_placeholder = st.empty()  # 시간을 업데이트할 플레이스홀더
        start_time = time.time()
        retries = 0  # 재시도 횟수를 제한하기 위한 변수

        while retries < 3:
            for i in range(60):  # 1분 동안 체크
                elapsed_time = int(time.time() - start_time)
                time_placeholder.write(f"⏳ 경과시간 : {elapsed_time}초")  # 사용자에게 경과시간 표시
                time.sleep(1)
        
            status = result_backend_check()
            if status is not None and status.get('ready', False):
                st.session_state['result'] = True
                st.session_state['loading'] = False
                break
            else:
                retries += 1
                st.write(f"서버에 재전송을 요청합니다. ({retries}/3)")
                
            if retries >= 3:
                st.error("백엔드로부터 응답이 없습니다. 다시 시도해 주세요.")
                st.session_state['loading'] = False
                break

# if __name__ == "__main__":
#     loading_session()
