from time import sleep

import streamlit as st

datasets = ["Laptop", "News", "Book"]


def sidebar() -> str:
    with st.sidebar:
        st.header("Options")
        st.divider()
        dataset = st.selectbox(label="Select category", options=datasets)
        return dataset


def chat_interface(dataset: str) -> None:
    st.subheader(dataset + " Recommendation")

    if "current_dataset" not in st.session_state or st.session_state.current_dataset != dataset:
        st.session_state.messages = []
        st.session_state.current_dataset = dataset

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input(f"Ask for a {dataset} recommendation"):
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
    category = sidebar()
    if category:
        chat_interface(category)
