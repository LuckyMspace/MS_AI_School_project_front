import streamlit as st
import requests
from PIL import Image
from io import BytesIO


def result_json():
    json_url = "http://localhost:5000/upload"  # 엔드포인트
    try:
        response = requests.get(json_url)
        response.raise_for_status()  # 200 OK 코드가 아니면 예외 발생
        data = response.json()
        if data is None:
            st.error("아무런 데이터 정보가 없습니다.")
            return None
        return data
    except requests.RequestException as e:
        st.error(f"json 파일을 가져올 수 없습니다. 에러: {e}")
        return None


def result_session():
    if not st.session_state.get("logged_in", False):
        st.warning("로그인이 필요한 서비스입니다.")
        st.experimental_rerun()

    # UI 나누기
    st.markdown(
        "<span style='color:blue; font-size:28px; font-family:Arial;'>AI가 추천합니다.(꾸미는 건 나중에 하기로)</span>",
        unsafe_allow_html=True,
    )
    left_column, right_column = st.columns(2)

    data = result_json()
    if data is None:
        st.error("No data available")
        return

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
        if st.button(" :rewind: 이미지 업로드 다시하기"):
            st.session_state["logged_in"] = False
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
