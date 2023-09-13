# image_upload_module.py
import streamlit as st
import requests
from io import BytesIO
import mimetypes

# from requests_toolbelt.multipart.encoder import MultipartEncoder


def image_upload_section():
    # if st.button("돌아가기"):
    #     st.session_state["current_page"] = "login"
    #     st.experimental_rerun()

    if st.session_state["loading"]:
        return

    left_column, right_column = st.columns(2)

    with left_column:
        st.markdown(
            "<h1 style='font-size: 32px;'>AI패션 추천 서비스</h1>", unsafe_allow_html=True
        )

        options = [
            "casual",
            "dandy",
            "formal",
            "girlish",
            "gorpcore",
            "retro",
            "romantic",
            "sports",
            "street",
        ]
        selected_options = st.multiselect(
            " :heavy_check_mark: 원하는 스타일을 하나만 선택해주세요", options
        )

        if len(selected_options) > 1:
            st.warning("스타일은 최대 1개까지 선택할 수 있습니다. 가장 먼저 선택된 ")
            selected_options = selected_options[:1]

        uploaded_file = st.file_uploader(
            ":heavy_check_mark: 아래에서 이미지를 업로드 하세요. :camera:",
            type=["jpg", "jpeg", "png"],
        )

        if uploaded_file is not None:
            ext = mimetypes.guess_extension(uploaded_file.type)
            if ext not in [".jpg", ".jpeg", ".png"]:
                st.error(":ballot_box_with_check: 업로드 파일을 다시 확인해주시고, 의류 이미지를 업로드 해주세요.")
            else:
                file_stream = BytesIO(uploaded_file.read())
                st.write(file_stream)
                uploaded_file.seek(0)
                st.image(file_stream, caption="업로드된 이미지", use_column_width=True)

                if st.button("AI에게 이미지 보내기"):
                    flask_server_url = "http://localhost:5000/upload"

                    # 파일 데이터를 bytes로 읽어옵니다.
                    file_bytes = file_stream.getvalue()

                    # 스타일 정보를 딕셔너리에 넣습니다.
                    data_to_send = {
                        "style": ",".join(selected_options)  # 스타일 정보를 쉼표로 구분된 문자열로 변환
                    }

                    # 파일 바이트 데이터
                    files = {"image": file_stream}

                    # st.write(f"딕셔너리 디버깅 : {data_to_send}, {files}")

                    # data_to_send 딕셔너리는 'data' 파라미터로, 파일은 'files' 파라미터로 전달
                    st.write(st.session_state["email"])
                    response = requests.post(
                        flask_server_url,
                        files={
                            "email": st.session_state["email"],
                            "style": ",".join(selected_options),
                            "image": file_bytes,
                        },
                    )

                    if response.status_code == 200:
                        st.session_state["loading"] = True
                        st.experimental_rerun()
                    else:
                        error_message = response.json().get("error")
                        st.error(f"이미지 전송 실패: {error_message}")

    with right_column:
        st.image("./front_images/upload_session_image.jpg", use_column_width=True)
        if st.button("로그아웃"):
            st.session_state["logged_in"] = False
            st.experimental_rerun()
        # if st.button(":rewind:돌아가기"):
        #     st.session_state["logged_in"] = False
        #     st.experimental_rerun()
