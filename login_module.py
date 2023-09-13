import streamlit as st
import requests
from image_upload_module import image_upload_section
from io import BytesIO
import mimetypes


def login_section():
    left_column, right_column = st.columns(2)

    # 로그인 상태마다 다른 UI 적용하기
    if st.session_state["logged_in"]:
        with left_column:
            # st.markdown(
            #     "<h1 style='font-size: 32px;'>AI패션 추천 서비스</h1>", unsafe_allow_html=True
            # )
            st.subheader(":robot_face:   AI패션 추천 서비스", divider="grey")  # ln1

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
                " :heavy_check_mark: 원하는 스타일을 하나만 선택해주세요", options, max_selections=1
            )
            # st.subheader(" ", divider="rainbow")  # ln2

            uploaded_file = st.file_uploader(
                ":heavy_check_mark: 아래에서 이미지를 업로드 하세요. :camera:",
                type=["jpg", "jpeg", "png"],
            )

            if uploaded_file is not None:
                ext = mimetypes.guess_extension(uploaded_file.type)
                if ext not in [".jpg", ".jpeg", ".png"]:
                    st.error(
                        ":ballot_box_with_check: 업로드 파일을 다시 확인해주시고, 의류 이미지를 업로드 해주세요."
                    )
                else:
                    file_stream = BytesIO(uploaded_file.read())
                    st.write(file_stream)
                    uploaded_file.seek(0)
                    st.image(file_stream, caption="업로드된 이미지", use_column_width=True)

                    if st.button(":postbox: AI에게 이미지 보내기"):
                        flask_server_url = "http://localhost:5000/upload"

                        # 파일 데이터를 bytes로 읽어옵니다.
                        file_bytes = file_stream.getvalue()
                        # 스타일 정보를 딕셔너리에 넣습니다.
                        data_to_send = {
                            "style": ",".join(
                                selected_options
                            )  # 스타일 정보를 쉼표로 구분된 문자열로 변환
                        }
                        # 파일 바이트 데이터
                        files = {
                            "email": st.session_state["email"],
                            "style": ",".join(selected_options),
                            "image": file_bytes,
                        }
                        st.session_state["flask_upload_url"] = flask_server_url
                        st.session_state["request_form"] = files
                        # st.write(f"딕셔너리 디버깅 : {data_to_send}, {files}")
                        # data_to_send 딕셔너리는 'data' 파라미터로, 파일은 'files' 파라미터로 전달
                        st.write(st.session_state["email"])

                        st.session_state["loading"] = True
                        st.session_state["current_page"] = "loading"  # dummy page value
                        st.experimental_rerun()

            st.subheader(" ", divider="grey")  # ln3
            if st.button(":x:로그아웃"):
                st.session_state["logged_in"] = False
                st.experimental_rerun()
    else:
        left_column.subheader(":robot_face:   AI패션 추천 서비스", divider="grey")
        email = left_column.text_input(
            ":e-mail: 이메일 주소", key="unique_login_email"
        )  # ln4
        password = left_column.text_input(
            ":closed_lock_with_key:비밀번호", type="password", key="login_password"
        )

        if left_column.button(":key:  로그인"):
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

        if left_column.button(":man-woman-girl-boy:회원가입"):
            st.session_state["sign_up"] = True
            st.experimental_rerun()

    if st.session_state["logged_in"]:
        right_column.image(
            "./front_images/upload_session_image.jpg", use_column_width=True
        )
    else:
        right_column.image("./front_images/main_image.jpg", use_column_width=True)


# if __name__ == '__main__':
#     login_section()
