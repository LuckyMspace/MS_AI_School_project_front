import streamlit as st
import time

def fail():    
    st.image("./front_images/fail_session.jpg", width=400) 
    st.markdown("<h1 style='font-size: 18px;'>앗! 죄송합니다. 통신오류가 발생했습니다.</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-size: 18px;'>잠시 후 이미지 업로드 세션으로 다시 이동합니다.</h1>", unsafe_allow_html=True)
    time.sleep(5)
    st.session_state['fail'] = False
    st.experimental_rerun()

# if __name__ == "__main__":
#     fail()