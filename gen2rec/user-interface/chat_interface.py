import datetime
from time import sleep
from gen2rec.src.recommendation_engine import load

import streamlit as st

# options
CATEGORY: str = "Category"
USER_PROFILE: str = "UserProfile"
LOCATION: str = "Location"
DATE_RANGE: str = "DateRange"

# datasets
LAPTOP: str = "Laptop"
NEWS: str = "News"
BOOK: str = "Book"


def sidebar() -> dict:
    with st.sidebar:
        st.header("Options")
        st.divider()
        options = {CATEGORY: st.selectbox(label="Category", options=[LAPTOP, NEWS, BOOK])}
        if options[CATEGORY] == NEWS:
            options[USER_PROFILE] = st.text_area(label="User Profile")
            options[LOCATION] = st.text_input(label="Location")
            options[DATE_RANGE] = st.text_input(
                label="Date",
            )
        # if options[CATEGORY] == BOOK:
        #     options[USER_PROFILE] = st.text_area(label="User Profile")
        return options


def chat_interface(options: dict) -> None:
    dataset = options[CATEGORY].lower()
    qa_chain = load(dataset)
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
            if dataset == "news":
                prompt = f"""I am interested in {options[USER_PROFILE]}.
LOCATION: {options[LOCATION]}
DATE: 2022 November"""
            response = qa_chain.invoke(input=prompt)['result']
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    st.title("Gen2Rec")
    options = sidebar()
    if options[CATEGORY]:
        chat_interface(options)
