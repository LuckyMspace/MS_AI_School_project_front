import streamlit as st
import requests
import json
from PIL import Image
from io import BytesIO
from reference import style_array


def result_session():
    if not st.session_state.get("logged_in", False):
        st.warning("로그인이 필요한 서비스입니다.")
        st.experimental_rerun()

    # UI 나누기
    st.title("이런 스타일은 어떠세요?")
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
        st.write("해당하는 추천 set을 찾을 수 없습니다 ;ㅅ;")

    elif style not in searched:
        st.write(f"선택하신 스타일 {style_array[int(style)]}의 추천 set을 찾을 수 없습니다 ;ㅅ;")
        # st.error("No data available")
    else:
        show_set(searched[style][0])

    def click_sub(sub):
        st.session_state["result"]["style"] = sub
        st.experimental_rerun()

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


# ------------------------------프론트 예시코드-----------------------------------------------------------------

# def result():
#     # UI 나누기
#     st.markdown("<span style='color:blue; font-size:28px; font-family:Arial;'>AI가 추천합니다.(어떻게 꾸밀지 고민중)</span>", unsafe_allow_html=True)
#     left_column, right_column = st.columns(2)

#     # 근데 이 json파일을 받으면 어떻게
#     data = {
#         "_id": {
#             "$oid": "object1hash"
#         },
#         "set_url": "https://image.msscdn.net/images/codimap/detail/25457/detail_25457_1_500.jpg?202309071509",
#         "set_name": "캠핑 룩은 이거지",
#         "items": [
#             {
#                 "thumb_url": "https://image.msscdn.net/images/goods_img/20220329/2452700/2452700_10_220.jpg",
#                 "brand": "아웃도어 프로덕츠",
#                 "item": "유틸리티 피싱 베스트 UTILITY FISHING VEST",
#                 "curr_price": "159,200원 199,000원\n20%",
#                 "link": "https://www.musinsa.com/app/goods/2452700/0",
#                 "url": "https://image.msscdn.net/images/goods/_img/20220329/2452700/2452700_10_500.jpg",
#                 "type": "아우터",
#                 "label": "베스트"
#             },
#             {
#                 "thumb_url": "https://image.msscdn.net/images/goods_img/20220915/2794019/2794019_1_220.jpg",
#                 "brand": "팀코믹스",
#                 "item": "하얀색 상의",
#                 "curr_price": "36,750원 49,000원\n25%",
#                 "link": "https://www.musinsa.com/app/goods/2452700/0",
#                 "url": "https://image.msscdn.net/images/goods/_img/20220329/2452700/2452700_10_500.jpg",
#                 "type": "아우터",
#                 "label": "베스트"
#             }
#         ]
#     }

#     with left_column:
#         st.title(data['set_name'])
#         st.write(' ')
#         st.image(data['set_url'], use_column_width=True)

#     item_names = [item['item'] for item in data['items']]

#     with right_column:
#         selected_item_index = st.slider("슬라이더로 아이템을 선택하세요.", 0, len(item_names)-1)
#         selected_item = data['items'][selected_item_index]

#         st.image(selected_item['thumb_url'], caption=selected_item['item'], use_column_width=True)
#         st.write(f"Price: {selected_item['curr_price']}")
#         link = selected_item['link']

#         st.markdown(f"<a style='display:block;text-align:center;background-color:#4CAF50;color:white;padding:14px 20px;margin: 8px 0;width:100%;' href='{link}' target='_blank'>구매하러 가기</a>", unsafe_allow_html=True)


# if __name__ == "__main__":
#     result()
# ------------------------------------------------- 프론트 예시 코드-------------------------------------------------------
