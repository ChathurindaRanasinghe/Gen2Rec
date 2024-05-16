from time import sleep

import streamlit as st

# options
CATEGORY: str = "Category"

# datasets
LAPTOP: str = "Laptop"
NEWS: str = "News"
BOOK: str = "Book"


def sidebar() -> dict:
    with st.sidebar:
        st.header("Options")
        st.divider()
        options = {CATEGORY: st.selectbox(label="Category", options=[LAPTOP, NEWS, BOOK])}
        return options


def chat_interface(options: dict) -> None:
    st.subheader(options[CATEGORY] + " Recommendation")

    if "current_dataset" not in st.session_state or st.session_state.current_dataset != options[CATEGORY]:
        st.session_state.messages = []
        st.session_state.current_dataset = options[CATEGORY]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input(f"Ask for a {options[CATEGORY]} recommendation"):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.spinner(text="Please wait"):
            sleep(2)
            response = f"You said {prompt}"
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    st.title("Gen2Rec")
    options = sidebar()
    if options[CATEGORY]:
        chat_interface(options)
