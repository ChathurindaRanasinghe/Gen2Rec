import json
import time

import requests
import streamlit as st
from streamlit_card import card

BACKEND_URL: str = "http://0.0.0.0:8001"


def get_recs():
    return [
        {
            "page_content": "tags: Action, artificial intelligence, robots, Sci-Fi, special effects, tense, time travel, robots\n",
            "metadata": {
                "movie": "Terminator, The",
                "thumbnail": "https://noteb.com/res/img/models/thumb/t_3733_1.jpg",
                "year": "1984",
                "genres": "Action, Sci-Fi, Thriller",
                "average_rating": 3.896946565,
                "source": 939,
                "_id": "a04c041de83f4fb8ba5db2e983c95ee9",
                "_collection_name": "movies"
            },
            "type": "Document"
        },
        {
            "page_content": "tags: action choreography, Horrid characterisation, Poor plot development, sequel, soundtrack\n",
            "metadata": {
                "movie": "Tron: Legacy",
                "year": "2010",
                "thumbnail": "https://noteb.com/res/img/models/thumb/t_2048_1.jpg",
                "genres": "Action, Adventure, Sci-Fi, IMAX",
                "average_rating": 3.236842105,
                "source": 7484,
                "_id": "9d4554305c2c459a8b83eaabc34512d3",
                "_collection_name": "movies"
            },
            "type": "Document"
        },
        {
            "page_content": "tags: \n",
            "metadata": {
                "movie": "Family Guy Presents Stewie Griffin: The Untold Story",
                "year": "2005",
                "thumbnail": "https://noteb.com/res/img/models/thumb/t_2430_1.jpg",
                "genres": "Adventure, Animation, Comedy",
                "average_rating": 3.708333333,
                "source": 5989,
                "_id": "622de1e97b2e405b9087981e7e8d4bdd",
                "_collection_name": "movies"
            },
            "type": "Document"
        }
    ]


def get_chat():
    return json.loads("""{
      "input": "I am interested in action movies can you recommend me 5 moviees",
      "chat_history": [
        {
          "content": "I am interested in action movies can you recommend me 5 moviees",
          "additional_kwargs": {},
          "response_metadata": {},
          "type": "human",
          "name": null,
          "id": null,
          "example": false
        },
        "Based on your interest in action movies, here are the recommendations from the given set of movies:\\n\\n1. **The Terminator (1984)**\\n   - **Description:** A relentless cyborg assassin is sent from the future to kill a woman whose unborn son is destined to save humanity from extinction. A human soldier is also sent back to protect her.\\n   - **Rating:** 3.90\\n   - **Genres:** Action, Sci-Fi, Thriller\\n\\n2. **Tron: Legacy (2010)**\\n   - **Description:** The son of a virtual world designer goes looking for his father and ends up inside the digital world that his father designed. He meets his father's corrupted creation and a unique ally who was born inside the digital world.\\n   - **Rating:** 3.24\\n   - **Genres:** Action, Adventure, Sci-Fi, IMAX\\n\\nUnfortunately, I can only recommend 2 action movies from the given set. The other movies do not fall under the action genre."
      ],
      "answer": "Based on your interest in action movies, here are the recommendations from the given set of movies:\\n\\n1. **The Terminator (1984)**\\n   - **Description:** A relentless cyborg assassin is sent from the future to kill a woman whose unborn son is destined to save humanity from extinction. A human soldier is also sent back to protect her.\\n   - **Rating:** 3.90\\n   - **Genres:** Action, Sci-Fi, Thriller\\n\\n2. **Tron: Legacy (2010)**\\n   - **Description:** The son of a virtual world designer goes looking for his father and ends up inside the digital world that his father designed. He meets his father's corrupted creation and a unique ally who was born inside the digital world.\\n   - **Rating:** 3.24\\n   - **Genres:** Action, Adventure, Sci-Fi, IMAX\\n\\nUnfortunately, I can only recommend 2 action movies from the given set. The other movies do not fall under the action genre."
    }""")


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
            }
        )

    col1, col2, col3 = st.columns(3)

    for i, rec in enumerate(recs):
        data = rec["metadata"]

        if i % 3 == 0:
            with col1:
                card_ui(data)
        if i % 3 == 1:
            with col2:
                card_ui(data)
        if i % 3 == 2:
            with col3:
                card_ui(data)


def chat_interface() -> None:
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input(f"Ask for a Movie recommendation"):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = get_chat()  # Mocked function to get chat response
        response_dict = response
        answer = response_dict["answer"]

        # Display user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").markdown(prompt)

        # Simulate streaming assistant response
        assistant_response = ""
        message_placeholder = st.empty()

        for chunk in answer.split():
            assistant_response += chunk + " "
            with message_placeholder:
                st.chat_message("assistant").markdown(assistant_response)
            time.sleep(0.1)  # Simulate delay for streaming effect

        st.session_state.messages.append({"role": "assistant", "content": assistant_response})


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    st.title("Laptop Shop")
    col1, col2 = st.columns([2, 1])
    with col1:
        recommendation_interface(get_recs())
    with col2:
        chat_interface()
