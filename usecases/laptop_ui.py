import json

import requests
import streamlit as st
from streamlit_card import card

BACKEND_URL: str = "http://0.0.0.0:8001"

metadata_fields = [
    {"name": "name", "description": "Name of the laptop.", "type": "string"},
    {"name": "thumbnail", "description": "Link to the thumbnail.", "type": "string"},
    {
        "name": "launch_year",
        "description": "Launch year of the laptop.",
        "type": "integer",
    },
    {
        "name": "total_storage_capacity",
        "description": "Total storage of the laptop in GB(gigabytes).",
        "type": "integer",
    },
    {
        "name": "battery_life_hours",
        "description": "Expected battery life of the laptop in hours.",
        "type": "float",
    },
    {
        "name": "operating_system",
        "description": "Operating System of the laptop.",
        "type": "string",
    },
    {"name": "price", "description": "Price of the laptop in USD.", "type": "float"},
    {"name": "cpu_prod", "description": "Producer of the CPU.", "type": "string"},
    {"name": "cpu_model", "description": "Model of the CPU.", "type": "string"},
    {
        "name": "cpu_lithography",
        "description": "Process lithography of the CPU in nano meters.",
        "type": "integer",
    },
    {"name": "cpu_cache", "description": "Cache of the CPU in MB.", "type": "integer"},
    {
        "name": "cpu_base_speed",
        "description": "Base speed of the CPU in GHz.",
        "type": "float",
    },
    {
        "name": "cpu_boost_speed",
        "description": "Boost speed of the CPU in GHz.",
        "type": "float",
    },
    {
        "name": "cpu_cores",
        "description": "Number of cores in the CPU.",
        "type": "integer",
    },
    {
        "name": "cpu_tdp",
        "description": "Thermal Design Power(TDP) of the CPU.",
        "type": "integer",
    },
    {
        "name": "cpu_rating",
        "description": "Defined rating for the CPU.",
        "type": "float",
    },
    {"name": "gpu_prod", "description": "Producer of the GPU.", "type": "string"},
    {"name": "gpu_model", "description": "Model of the GPU.", "type": "string"},
    {
        "name": "gpu_architecture",
        "description": "Architecture of the GPU.",
        "type": "string",
    },
    {
        "name": "gpu_lithography",
        "description": "Process lithography of the GPU in nano meters.",
        "type": "integer",
    },
    {
        "name": "gpu_shaders",
        "description": "Number of shaders in the GPU.",
        "type": "integer",
    },
    {
        "name": "gpu_base_speed",
        "description": "Base speed of the GPU in MHz.",
        "type": "integer",
    },
    {
        "name": "gpu_boost_speed",
        "description": "Boost speed of the GPU in MHz.",
        "type": "integer",
    },
    {
        "name": "gpu_memory_speed",
        "description": "Memory speed of the GPU in MHz.",
        "type": "integer",
    },
    {
        "name": "gpu_memory_bandwidth",
        "description": "Memory bandwidth of the GPU.",
        "type": "integer",
    },
    {
        "name": "gpu_memory_size",
        "description": "Memory size of the GPU in MB.",
        "type": "integer",
    },
    {
        "name": "gpu_memory_type",
        "description": "Memory type of the GPU.",
        "type": "string",
    },
    {
        "name": "gpu_tdp",
        "description": "Thermal Design Power(TDP) of the GPU.",
        "type": "integer",
    },
    {
        "name": "gpu_rating",
        "description": "Defined rating for the GPU.",
        "type": "float",
    },
    {
        "name": "display_size",
        "description": "Diagonal display size in inches.",
        "type": "float",
    },
    {
        "name": "display_horizontal_resolution",
        "description": "Horizantal display resolution in pixels.",
        "type": "integer",
    },
    {
        "name": "display_vertical_resolution",
        "description": "Vertical display resolution in pixels.",
        "type": "integer",
    },
    {
        "name": "display_type",
        "description": "Type of the display technology.",
        "type": "string",
    },
    {
        "name": "memory_size",
        "description": "Size of the memory in GB.",
        "type": "integer",
    },
    {
        "name": "memory_speed",
        "description": "Speed of the memory in MHz.",
        "type": "integer",
    },
    {"name": "memory_type", "description": "Type of the memory.", "type": "string"},
    {
        "name": "primary_storage_model",
        "description": "Primary storage technology.",
        "type": "string",
    },
    {
        "name": "primary_storage_cap",
        "description": "Primary storage capacity in GB.",
        "type": "integer",
    },
    {
        "name": "primary_storage_read_speed",
        "description": "Primary storage speed in MBps.",
        "type": "integer",
    },
    {
        "name": "primary_storage_read_speed",
        "description": "Primary storage speed in MBps.",
        "type": "integer",
    },
    {
        "name": "wireless_card_model",
        "description": "Model of the wireless card.",
        "type": "string",
    },
    {
        "name": "wireless_card_speed",
        "description": "Speed of the wireless card in Mbps.",
        "type": "integer",
    },
    {
        "name": "chassis_height_cm",
        "description": "Height of the laptop chassis in cm.",
        "type": "float",
    },
    {
        "name": "chassis_depth_cm",
        "description": "Depth of the laptop chassis in cm.",
        "type": "float",
    },
    {
        "name": "chassis_width_cm",
        "description": "Width of the laptop chassis in cm.",
        "type": "float",
    },
    {
        "name": "chassis_weight_kg",
        "description": "Weight of the laptop in KG.",
        "type": "float",
    },
    {
        "name": "battery_capacity",
        "description": "Capacity of the battery in Wh.",
        "type": "float",
    },
    {
        "name": "warranty_years",
        "description": "Information related to the warrenty of the laptop.",
        "type": "integer",
    },
]


document_content_description = "Description about the laptop indicating key features, use cases, and types of people that may use the laptops. Description also included some additional information about specs as well."


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
            url="http://localhost:8000", stream=True, params={"query": prompt}
        ) as r:
            for chunk in r.iter_content():
                assistant_response += chunk + " "
                with message_placeholder:
                    st.chat_message("assistant").markdown(assistant_response)

        st.session_state.messages.append(
            {"role": "assistant", "content": assistant_response}
        )


if __name__ == "__main__":
    system_prompt = ""
    with open("laptop_prompt.txt", "r") as f:
        system_prompt = f.read()
    body = {
        "recommendation_category": "laptops",
        "document_content_description": json.dumps(document_content_description),
        "metadata_fields": json.dumps(metadata_fields),
        "system_prompt": system_prompt,
    }
    response = requests.post(
        BACKEND_URL + "/init",
        data=body,
    )
    if response.status_code != 200:
        raise RuntimeError()
    st.set_page_config(layout="wide")
    st.title("Laptop Shop")
    col1, col2 = st.columns([2, 1])
    with col1:
        recommendation_interface(get_recs(4))
    with col2:
        chat_interface()
