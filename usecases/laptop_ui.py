import requests
import streamlit as st
from streamlit_card import card

BACKEND_URL: str = "http://127.0.0.1:8000"


def get_recs(number):
    body = {"number": number}
    response = requests.get(
        BACKEND_URL + "/recommendations",
        params=body,
    )

    if response.status_code != 200:
        raise RuntimeError()

    return response.json()


def recommendation_interface(recs):
    def card_ui(data):
        return card(
            key=data["name"],
            title=data["name"],
            text=data["genres"] + " | " + str(data["average_rating"]),
            image=data["thumbnail"],
            styles={
                "card": {
                    "width": "300px",
                    "height": "200px",
                    "border-radius": "20px",
                    "margin": "0",
                    "padding": "0",
                }
            },
        )

    col1, col2, col3 = st.columns(3)

    for i, rec in enumerate(recs):
        data = rec["metadata"]

        if i % 3 == 0:
            with col1:
                card_ui(data)
        elif i % 3 == 1:
            with col2:
                card_ui(data)
        elif i % 3 == 2:
            with col3:
                card_ui(data)


def chat_interface() -> None:
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    # for message in st.session_state.messages:
    #     with st.chat_message(message["role"]):
    #         st.markdown(message["content"])
    if prompt := st.chat_input("Ask for a Laptop recommendation"):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        response = ""
        message_placeholder = st.empty()
        with requests.get(BACKEND_URL + "/query-stream", stream=True) as r:
            for chunk in r.iter_content():
                if chunk:
                    response += chunk.decode('utf-8')
                with message_placeholder:
                    st.chat_message("assistant").markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    st.title("Laptop Shop")
    col1, col2 = st.columns([2, 1])
    with col1:
        recommendation_interface(get_recs(4))
    with col2:
        chat_interface()
