import argparse
from time import sleep

import gradio as gr

INITIALIZED = False
CATEGORY = ""
TITLE = "Gen2Rec"
LIST = "List"
CHAT = "Chat"
VISIBILITY = {LIST: True, CHAT: True}
FIELDS = []


def get_fields(recommendation_fields):
    # return list(json.loads(recommendation_fields).keys())
    return ["movie", "year", "genres", "average_rating"]


def initialize(recommendation_category, recommendation_fields):
    FIELDS = get_fields(recommendation_fields)
    print(FIELDS)

    if recommendation_category != "":
        print(recommendation_category)

    CATEGORY = recommendation_category
    INITIALIZED = True
    return gr.update(interactive=INITIALIZED), gr.update(interactive=INITIALIZED), gr.update(
        value="Successfully initialized"), gr.update(value=f"# {TITLE} - {CATEGORY.capitalize()} Recommendation")


def change_visibility(visible):
    VISIBILITY[LIST] = LIST in visible
    VISIBILITY[CHAT] = CHAT in visible
    return gr.update(visible=VISIBILITY[LIST]), gr.update(visible=VISIBILITY[CHAT])


def submit_configurations(system_prompt, user_details, web_search):
    print(system_prompt)
    print(user_details)
    print(web_search)
    sleep(2)
    response = True
    return "Configurations updated" if response else "Error in configuration"


def get_recommendation_list():
    return [
        {
            "page_content": "tags: \n",
            "metadata": {
                "movie": "Family Guy Presents Stewie Griffin: The Untold Story",
                "year": "2005",
                "genres": "Adventure, Animation, Comedy",
                "average_rating": 3.708333333,
                "source": 5989,
                "_id": "622de1e97b2e405b9087981e7e8d4bdd",
                "_collection_name": "movies"
            },
            "type": "Document"
        },
        {
            "page_content": "tags: \n",
            "metadata": {
                "movie": "Toy Story 3",
                "year": "2010",
                "genres": "Adventure, Animation, Children, Comedy, Fantasy, IMAX",
                "average_rating": 4.109090909,
                "source": 7355,
                "_id": "d9158014658840adab71089128a96dab",
                "_collection_name": "movies"
            },
            "type": "Document"
        },
        {
            "page_content": "tags: \n",
            "metadata": {
                "movie": "Comedian",
                "year": "2002",
                "genres": "Comedy, Documentary",
                "average_rating": 3.0,
                "source": 4013,
                "_id": "23eb175895ea45dfa7417711984ac697",
                "_collection_name": "movies"
            },
            "type": "Document"
        }
    ]


def chat_response(message, history):
    history = history or []
    if message:
        bot_response = f"{message[::-1]}"
        history.append([message, bot_response])
        sleep(2)
    return "", history


css = """
footer {
    visibility: hidden
}

.card {
    background-color: rgb(120,120,120);
    margin: 10px;
    padding: 10px;
    border-radius:10px;
}
"""

with gr.Blocks(css=css, title=TITLE) as demo:
    title_display = gr.Markdown(value=f"# {TITLE}")

    with gr.Tabs():
        init_tab = gr.TabItem("Initialization")
        configuration_tab = gr.TabItem("Configurations", interactive=INITIALIZED)
        recommendation_tab = gr.TabItem("Recommendations", interactive=INITIALIZED)

        with init_tab:
            with gr.Row():
                with gr.Column():
                    recommendation_category = gr.Textbox(label="Recommendation Category")
                    with gr.Row():
                        dataset_file = gr.UploadButton("Upload dataset", type="binary")
                        improve_dataset = gr.Checkbox(label="Improve dataset with additional data")
                    recommendation_fields = gr.Textbox(label="Specify the fields in JSON format", lines=5)
                with gr.Column():
                    gr.Markdown("Configurations List")
            with gr.Row():
                message = gr.Button("Initialize to continue", interactive=False)
                init = gr.Button("Initialize")
                init.click(initialize, inputs=[recommendation_category, recommendation_fields],
                           outputs=[recommendation_tab, configuration_tab, message, title_display])

        with recommendation_tab:
            with gr.Row():
                list_column = gr.Column(scale=1, visible=True, variant="panel")
                with list_column:
                    def update_recommendations():
                        recommendations_html = ""
                        for rec in get_recommendation_list():
                            recommendations_html += f'''
                            <div class="card">
                            {rec}
                            </div>
                            '''
                        return gr.update(value=recommendations_html)


                    refresh = gr.Button("Recommendation List")
                    recommendation_list = gr.HTML()
                    refresh.click(update_recommendations, outputs=recommendation_list)

                chat_column = gr.Column(scale=1, visible=True)
                with chat_column:
                    gr.Markdown("Recommendation Chat Interface")
                    chatbot = gr.Chatbot()
                    message = gr.Textbox(show_label=False)
                    submit = gr.Button("Send")
                    submit.click(chat_response, inputs=[message, chatbot], outputs=[message, chatbot])

        with configuration_tab:
            visible = gr.CheckboxGroup([LIST, CHAT], label="Visible recommendation options", value=[LIST, CHAT])
            visible.change(change_visibility, inputs=visible, outputs=[list_column, chat_column])
            gr.Markdown("<hr>")
            gr.Markdown("Recommendation System Configurations")
            system_prompt = gr.Textbox(label="System prompt")
            user_details = gr.Textbox(label="User details")
            web_search = gr.Checkbox(label="Enable web search", value=False)
            with gr.Row():
                status = gr.Button("Set configurations", interactive=False)
                submit = gr.Button("Submit")
            submit.click(submit_configurations, inputs=[system_prompt, user_details, web_search], outputs=status)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Launch Client Interface")
    parser.add_argument("--server_port", type=int, default=8001, help="Port number to host the app")
    args = parser.parse_args()
    demo.launch(server_port=args.server_port, show_api=False)
