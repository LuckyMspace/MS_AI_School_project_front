# image_upload_module.py
import streamlit as st
import requests
from io import BytesIO
import mimetypes

def image_upload_section():
    # 로딩 중이라면 이 함수의 나머지 부분을 실행하지 않는다.
    if st.session_state['loading']:
        return
    
    # 로딩 중이 아니라면, 원래 하려던 작업을 수행합니다.
    left_column, right_column = st.columns(2)
    
    with left_column:
        st.markdown("<h1 style='font-size: 32px;'>AI에게 내 옷 보여주기</h1>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("이미지 업로드", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            ext = mimetypes.guess_extension(uploaded_file.type)
            if ext not in ['.jpg', '.jpeg', '.png']:
                st.error("업로드 파일을 다시 확인해주시고, 의류 이미지를 업로드 해주세요.")
            else:
                file_stream = BytesIO(uploaded_file.read())
                uploaded_file.seek(0)
                st.image(file_stream, caption="업로드된 이미지", use_column_width=True)

                if st.button('AI에게 사진 보내기'):
                    flask_server_url = "http://localhost:5000/upload"
                    files = {"file": (uploaded_file.name, file_stream)}
                    response = requests.post(flask_server_url, files=files)                    
                    if response.status_code == 200:
                        st.session_state['loading'] = True                                                
                        st.experimental_rerun()
                    else:
                        st.error("이미지 전송 실패")

    with right_column:
        st.image("./front_images/upload_session_image.jpg", use_column_width=True)

# if __name__ == "__main__":
    # image_upload_section()
