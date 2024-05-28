import argparse
import json
from time import sleep

import gradio as gr

TITLE: str = "Gen2Rec"
INITIALIZED: bool = False
CATEGORY: str = ""
LIST: str = "List"
CHAT: str = "Chat"
VISIBILITY: dict = {LIST: True, CHAT: True}
FIELDS: list = []


def get_fields(recommendation_fields: json) -> list[str]:
    # return list(json.loads(recommendation_fields).keys())
    return ["movie", "year", "genres", "average_rating"]


def initialize(recommendation_category: str, recommendation_fields: json) -> tuple:
    FIELDS = get_fields(recommendation_fields)
    print(FIELDS)

    if recommendation_category != "":
        print(recommendation_category)

    CATEGORY = recommendation_category
    INITIALIZED = True
    return gr.update(interactive=INITIALIZED), gr.update(interactive=INITIALIZED), gr.update(
        value="Successfully initialized"), gr.update(value=f"# {TITLE} - {CATEGORY.capitalize()} Recommendation")


def change_visibility(visible: list) -> tuple:
    VISIBILITY[LIST] = LIST in visible
    VISIBILITY[CHAT] = CHAT in visible
    return gr.update(visible=VISIBILITY[LIST]), gr.update(visible=VISIBILITY[CHAT])


def submit_configurations(system_prompt: str, user_details: str, web_search: bool) -> dict:
    status: str = "Error in configuration"
    print(system_prompt)
    print(user_details)
    print(web_search)
    sleep(2)
    status = "Configurations updated"
    return gr.update(value=status)


def get_recommendation_list() -> list[dict]:
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


def chat_response(message: str, history: list[str]) -> tuple[str, list]:
    history: list = history or []
    if message:
        bot_response: str = f"{message[::-1]}"
        history.append([message, bot_response])
        sleep(2)
    return "", history


css: str = '''
footer {
    visibility: hidden
}

.card {
    background-color: rgb(120,120,120);
    margin: 10px;
    padding: 10px;
    border-radius:10px;
}
'''

with gr.Blocks(css=css, title=TITLE) as demo:
    title_display = gr.Markdown(value=f"# {TITLE}")

    with gr.Tabs():
        init_tab = gr.TabItem(label="Initialization")
        configuration_tab = gr.TabItem(label="Configurations", interactive=INITIALIZED)
        recommendation_tab = gr.TabItem(label="Recommendations", interactive=INITIALIZED)

        with init_tab:
            with gr.Row():
                with gr.Column():
                    recommendation_category = gr.Textbox(label="Recommendation Category")
                    with gr.Row():
                        dataset_file = gr.UploadButton(label="Upload dataset", type="binary")
                        improve_dataset = gr.Checkbox(label="Improve dataset with additional data")
                    recommendation_fields = gr.Textbox(label="Specify the fields in JSON format", lines=5)
                with gr.Column():
                    gr.Markdown(value="Configurations List")
            with gr.Row():
                message = gr.Button(value="Initialize to continue", interactive=False)
                init = gr.Button(value="Initialize")
                init.click(fn=initialize, inputs=[recommendation_category, recommendation_fields],
                           outputs=[recommendation_tab, configuration_tab, message, title_display])

        with recommendation_tab:
            with gr.Row():
                with gr.Column(visible=True, variant="panel") as list_column:
                    def update_recommendations():
                        recommendations_html = ""
                        for rec in get_recommendation_list():
                            recommendations_html += f'''
                            <div class="card">
                            {rec}
                            </div>
                            '''
                        return gr.update(value=recommendations_html)


                    refresh = gr.Button(value="Recommendation List")
                    recommendation_list = gr.HTML()
                    refresh.click(fn=update_recommendations, outputs=recommendation_list)

                with gr.Column(visible=True) as chat_column:
                    gr.Markdown(value="Recommendation Chat Interface")
                    chatbot = gr.Chatbot()
                    message = gr.Textbox(show_label=False)
                    submit = gr.Button(value="Send")
                    submit.click(fn=chat_response, inputs=[message, chatbot], outputs=[message, chatbot])

        with configuration_tab:
            visible = gr.CheckboxGroup(choices=[LIST, CHAT], label="Visible recommendation options", value=[LIST, CHAT])
            visible.change(fn=change_visibility, inputs=visible, outputs=[list_column, chat_column])
            gr.Markdown(value="<hr>")
            gr.Markdown(value="Recommendation System Configurations")
            system_prompt = gr.Textbox(label="System prompt")
            user_details = gr.Textbox(label="User details")
            web_search = gr.Checkbox(label="Enable web search", value=False)
            with gr.Row():
                status = gr.Button(value="Set configurations", interactive=False)
                submit = gr.Button(value="Submit")
            submit.click(fn=submit_configurations, inputs=[system_prompt, user_details, web_search], outputs=status)

if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Launch Client Interface")
    parser.add_argument("--server_port", type=int, default=8001, help="Port number to host the app")
    args = parser.parse_args()
    demo.launch(server_port=args.server_port, show_api=False)
