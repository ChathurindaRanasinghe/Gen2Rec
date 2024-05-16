from streamlit_float import *

st.set_page_config(layout="wide")

float_init(theme=True, include_unstable_primary=False)


def chat_content():
    st.session_state["contents"].append(st.session_state.content)


if "contents" not in st.session_state:
    st.session_state["contents"] = []

col1, col2 = st.columns([2, 1])
with col1:
    with st.container():
        st.write("Hello streamlit")

with col2:
    with st.container(border=True, height=700):
        st.subheader("Chat interface")
        with st.container():
            if prompt := st.chat_input("Ask recommendations"):
                st.session_state.contents.append({"role": "user", "content": prompt})
                with st.spinner(text="Please wait"):
                    response = f"You said {prompt}"
                    st.session_state.contents.append({"role": "assistant", "content": response})
            button_b_pos = "2rem"
            button_css = float_css_helper(width="2.2rem", bottom=button_b_pos, transition=0)
            float_parent(css=button_css)
        if content := st.session_state.contents:
            for message in st.session_state.contents:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
