import streamlit as st
import requests
import json
from PIL import Image
from io import BytesIO
from .reference import style_array


def result_session():
    if not st.session_state.get("logged_in", False):
        st.warning("로그인이 필요한 서비스입니다.")
        st.session_state["needs_rerun"] = True

    # UI 나누기
    left_column, right_column = st.columns(2)

    def show_set(data):
        with left_column:
            st.title(data["set_name"])
            st.write(" ")
            st.image(data["set_url"], use_column_width=True)

        item_names = [item["item"] for item in data["items"]]

        with right_column:
            selected_item_index = st.slider(
                " :heavy_check_mark: 슬라이더로 아이템을 선택하세요.", 0, len(item_names) - 1
            )
            selected_item = data["items"][selected_item_index]

            st.image(
                selected_item["thumb_url"],
                caption=selected_item["item"],
                use_column_width=True,
            )
            st.write(f"Price: {selected_item['curr_price']}")
            link = selected_item["link"]

            st.markdown(
                f"<a style='display:block;text-align:center;background-color:#4CAF50;color:white;padding:14px 20px;margin: 8px 0;width:100%;' href='{link}' target='_blank'>구매하러 가기</a>",
                unsafe_allow_html=True,
            )

    # data = result_json() # removed by acensia
    # change types
    print(st.session_state["result"])
    found = st.session_state["result"]["found"]
    style = st.session_state["result"]["style"]
    searched = st.session_state["result"]["sets"]
    if not found:
        st.write("해당하는 추천 set을 찾을 수 없습니다.")

    elif style not in searched:
        st.write(f"선택하신 스타일 {style_array[int(style)]}의 추천 set을 찾을 수 없습니다.")
        # st.error("No data available")
    else:
        show_set(searched[style][0])

    def click_sub(sub):
        st.session_state["result"]["style"] = sub
        st.session_state["needs_rerun"] = True

    if found:
        st.title("이런 스타일은 어떠세요?")
        for sub in searched:
            if sub == style:
                continue
            st.button(style_array[int(sub)], on_click=click_sub, args=sub)

    if st.button(":rewind: 이미지 다시 올리기"):
        # st.session_state["loading"] = False
        st.session_state["current_page"] = "image_upload"
        st.experimental_rerun()
