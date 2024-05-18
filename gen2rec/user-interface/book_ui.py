from streamlit_float import *
from streamlit_card import card

st.set_page_config(layout="wide")

float_init(theme=True, include_unstable_primary=False)

if "contents" not in st.session_state:
    st.session_state.contents = []

col1, col2 = st.columns([2, 1])
with col1:
    with st.container():
        st.header("Gen2Rec")
        st.subheader("Book Recommendations")
        card(
            title="Streamlit Card",
            text=["This is a test card", "This is a subtext"],
            image="https://placekitten.com/500/500",
            styles={
                "card": {
                    "width": "100%",
                    "height": "100px",
                    "border-radius": "10px",
                    "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                    "margin-left": "0",
                    "text-align": "left",  # Aligns text to the left within the card
                    "padding": "10px"  # Adds padding to ensure content is not flush with the edge
                },
                "title": {
                    "text-align": "left",  # Aligns the title to the left
                },
                "text": {
                    "text-align": "left",  # Aligns the text to the left
                }
            }
        )

with col2:
    with st.expander("Chat Interface"):
        with st.container():
            if prompt := st.chat_input("Ask for recommendations"):
                st.session_state.contents.append({"role": "user", "content": prompt})
                with st.spinner(text="Please wait"):
                    response = f"You said {prompt}"
                    st.session_state.contents.append({"role": "assistant", "content": response})
            button_css = float_css_helper(width="2.2rem", bottom="2rem", transition=0)
            float_parent(css=button_css)
        if content := st.session_state.contents:
            for message in st.session_state.contents:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
