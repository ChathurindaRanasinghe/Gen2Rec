import requests
import streamlit as st
from streamlit_card import card

BACKEND_URL: str = "https://b8tbzq9k-8008.asse.devtunnels.ms"


def get_recs(number):
    body = {"number": number}
    response = requests.get(
        BACKEND_URL + "/recommendations",
        params=body,
    )

    if response.status_code != 200:
        raise RuntimeError()

    return response.json()


# def get_chat():
#     return json.loads("""{
#       "input": "I am interested in action movies can you recommend me 5 moviees",
#       "chat_history": [
#         {
#           "content": "I am interested in action movies can you recommend me 5 moviees",
#           "additional_kwargs": {},
#           "response_metadata": {},
#           "type": "human",
#           "name": null,
#           "id": null,
#           "example": false
#         },
#         "Based on your interest in action movies, here are the recommendations from the given set of movies:\\n\\n1. **The Terminator (1984)**\\n   - **Description:** A relentless cyborg assassin is sent from the future to kill a woman whose unborn son is destined to save humanity from extinction. A human soldier is also sent back to protect her.\\n   - **Rating:** 3.90\\n   - **Genres:** Action, Sci-Fi, Thriller\\n\\n2. **Tron: Legacy (2010)**\\n   - **Description:** The son of a virtual world designer goes looking for his father and ends up inside the digital world that his father designed. He meets his father's corrupted creation and a unique ally who was born inside the digital world.\\n   - **Rating:** 3.24\\n   - **Genres:** Action, Adventure, Sci-Fi, IMAX\\n\\nUnfortunately, I can only recommend 2 action movies from the given set. The other movies do not fall under the action genre."
#       ],
#       "answer": "Based on your interest in action movies, here are the recommendations from the given set of movies:\\n\\n1. **The Terminator (1984)**\\n   - **Description:** A relentless cyborg assassin is sent from the future to kill a woman whose unborn son is destined to save humanity from extinction. A human soldier is also sent back to protect her.\\n   - **Rating:** 3.90\\n   - **Genres:** Action, Sci-Fi, Thriller\\n\\n2. **Tron: Legacy (2010)**\\n   - **Description:** The son of a virtual world designer goes looking for his father and ends up inside the digital world that his father designed. He meets his father's corrupted creation and a unique ally who was born inside the digital world.\\n   - **Rating:** 3.24\\n   - **Genres:** Action, Adventure, Sci-Fi, IMAX\\n\\nUnfortunately, I can only recommend 2 action movies from the given set. The other movies do not fall under the action genre."
#     }""")


def recommendation_interface(recs):
    def card_ui(data):
        return card(
            key=data["movie"],
            title=data["movie"] + " " + data["year"],
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

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask for a Laptop recommendation"):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # response = get_chat()  # Mocked function to get chat response
        # response_dict = response
        # answer = response_dict["answer"]

        # Display user message
        # st.session_state.messages.append({"role": "user", "content": prompt})
        # st.chat_message("user").markdown(prompt)

        # Simulate streaming assistant response
        assistant_response = ""
        message_placeholder = st.empty()

        with requests.get(
                url=BACKEND_URL + "/chat-stream", stream=True, params={"query": prompt}
        ) as r:
            for chunk in r.iter_content():
                print(chunk)
                assistant_response += chunk + " "
                with message_placeholder:
                    st.chat_message("assistant").markdown(assistant_response)

        st.session_state.messages.append(
            {"role": "assistant", "content": assistant_response}
        )


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    st.title("Laptop Shop")
    col1, col2 = st.columns([2, 1])
    with col1:
        recommendation_interface(get_recs(4))
    with col2:
        chat_interface()
