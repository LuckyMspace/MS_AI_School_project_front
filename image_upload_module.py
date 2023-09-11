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
        st.markdown("<h1 style='font-size: 32px;'>AI패션 추천 서비스</h1>", unsafe_allow_html=True)
        
        # Multiselect 위젯 추가
        options = ["고프코어", "포멀", "걸리시", "스트릿", "스포츠", "캐주얼", "레트로", "골프", "로맨틱"]
        selected_options = st.multiselect("원하는 스타일을 선택해주세요. (최대 2개)", options)

        # 몇개까지 선택되게 할 것인지
        if len(selected_options) > 2:
            st.warning(" 스타일은 최대 2개까지 선택할 수 있습니다. 선택한 순서대로 2개 스타일이 지정됩니다.")
            selected_options = selected_options[:2]  # 처음 2개의 선택 항목만 유지, 초과 선택된 것을 강제 취소시키는건 안되는 것 같음
        
        uploaded_file = st.file_uploader("아래에서 이미지를 업로드 하세요.", type=["jpg", "jpeg", "png"])
        
        if uploaded_file is not None:
            ext = mimetypes.guess_extension(uploaded_file.type)
            if ext not in ['.jpg', '.jpeg', '.png']:
                st.error("업로드 파일을 다시 확인해주시고, 의류 이미지를 업로드 해주세요.")
            else:
                file_stream = BytesIO(uploaded_file.read())
                uploaded_file.seek(0)
                st.image(file_stream, caption="업로드된 이미지", use_column_width=True)

                if st.button('AI에게 이미지와 원하는 스타일 정보 보내기'):
                    flask_server_url = "http://localhost:5000/upload" # 엔드포인트

                    # 딕셔너리에 체크박스 정보 추가
                    data_to_send = {option: index for index, option in enumerate(selected_options)}
                    st.write(f"딕셔너리 디버깅 : {data_to_send}")  # 디버깅 용도

                    files = {"file": (uploaded_file.name, file_stream)}
                    response = requests.post(flask_server_url, json=data_to_send, files=files)

                    if response.status_code == 200:
                        st.session_state['loading'] = True                                                
                        st.experimental_rerun()
                    else:
                        st.error("이미지 전송 실패")

    with right_column:
        st.image("./front_images/upload_session_image.jpg", use_column_width=True)
# {"email" : email, "image": test08.png, "style": street, } 
    # 디버깅
    st.write(f"스타일 선택 디버깅: {selected_options}")
                    

if __name__ == "__main__":
    image_upload_section()
