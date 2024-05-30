import argparse
import json

import gradio as gr
import requests

TITLE: str = "Gen2Rec"
INITIALIZED: bool = False
CATEGORY: str = ""
LIST: str = "List"
CHAT: str = "Chat"
VISIBILITY: dict = {LIST: True, CHAT: True}
FIELDS: list = []
METADATA: dict = {
    "Headings": ["Name", "Type", "Description"],
    "Datatypes": ["str", "str", "str"],
    "AllowedTypes": ["int", "float", "str"]
}
BACKEND_URL: str = "https://b8tbzq9k-8000.asse.devtunnels.ms"


def initialize(recommendation_category: str, dataset_file, improve_dataset: bool, system_prompt: str,
               recommendation_fields) -> tuple:
    global CATEGORY
    global INITIALIZED
    global FIELDS
    recommendation_fields = recommendation_fields.replace("", None)

    if not recommendation_category:
        status = "No recommendation category provided"
    elif not dataset_file:
        status = "No dataset file provided"
    elif not system_prompt:
        status = "No system prompt provided"
    elif recommendation_fields.isnull().values.any():
        status = "No recommendation fields provided"
    elif len([element for element in recommendation_fields["Type"].values if element not in METADATA["AllowedTypes"]]):
        status = "Unallowed data type selected"
    else:
        try:
            CATEGORY = recommendation_category
            INITIALIZED = True
            FIELDS = recommendation_fields.columns.tolist()
            body = {
                "recommendation_category": recommendation_category,
                "dataset_file": dataset_file,
                "improve_dataset": improve_dataset,
                "system_prompt": system_prompt,
                "recommendation_fields": recommendation_fields
            }
            response = requests.post(BACKEND_URL + "/init", data=body)
            if response.status_code == 200:
                status = "Successfully initialized"
            else:
                print(response)
                status = "Issue occurred in initialization"
        except Exception as e:
            print(e)
            status = "Issue occurred in initialization"
    INITIALIZED = True
    return gr.update(interactive=INITIALIZED), gr.update(interactive=INITIALIZED), gr.update(
        value=status), gr.update(value=f"# {TITLE} - {CATEGORY.capitalize()} Recommendation")


def change_visibility(visible: list) -> tuple:
    VISIBILITY[LIST] = LIST in visible
    VISIBILITY[CHAT] = CHAT in visible
    return gr.update(visible=VISIBILITY[LIST]), gr.update(visible=VISIBILITY[CHAT])


def submit_configurations(user_details: str, web_search: bool) -> dict:
    try:
        body = {
            "user_details": user_details,
            "web_search": web_search
        }
        response = requests.post(BACKEND_URL + "/config", data=json.dumps(body))
        if response.status_code == 200:
            status = "Configurations updated successfully"
        else:
            print(response)
            status = "Issue occurred in configuration"
    except Exception as e:
        print(e)
        status = "Issue occurred in configuration"
    return gr.update(value=status)


def update_recommendations(number: int) -> dict:
    try:
        body = {
            "number": number
        }
        response = requests.get(BACKEND_URL + "/recommendations", params=body)
        if response.status_code == 200:
            recommendations = response.json()["answer"]
        else:
            print(response)
            recommendations = [{"metadata": "Error receiving response"}]
    except Exception as e:
        print(e)
        recommendations = [{"metadata": "Error receiving response"}]

    recommendations_html = ""
    for rec in recommendations:
        recommendations_html += f'''
        <div class="card">
        {rec["metadata"]}
        </div>
        '''
    return gr.update(value=recommendations_html)


def chat_response(message: str, history: list[str]) -> tuple[str, list]:
    history: list = history or []
    if message:
        try:
            body = {
                "query": message
            }
            response = requests.get(BACKEND_URL + "/chat", params=body)
            if response.status_code == 200:
                history.append([message, response.json()["answer"]])
            else:
                print(response)
                history.append([message, "Error receiving response"])
        except Exception as e:
            print(e)
            history.append([message, "Error receiving response"])
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
            recommendation_category = gr.Textbox(label="Recommendation Category")
            with gr.Row():
                dataset_file = gr.UploadButton(label="Upload dataset", type="binary")
                improve_dataset = gr.Checkbox(label="Improve dataset with additional data")
            system_prompt = gr.Textbox(label="System prompt", lines=5)
            recommendation_fields = gr.Dataframe(label="Metadata Fields", headers=METADATA["Headings"],
                                                 datatype=METADATA["Datatypes"], col_count=(3, "fixed"))
            with gr.Row():
                message = gr.Button(value="Initialize to continue", interactive=False)
                init = gr.Button(value="Initialize")
                init.click(fn=initialize, inputs=[recommendation_category, dataset_file, improve_dataset, system_prompt,
                                                  recommendation_fields],
                           outputs=[recommendation_tab, configuration_tab, message, title_display])

        with recommendation_tab:
            with gr.Row():
                with gr.Column(visible=True, variant="panel", scale=1) as list_column:
                    gr.Markdown(value="Recommendation List")
                    number = gr.Slider(label="Number of recommendations", value=5, minimum=1, maximum=20, step=1)
                    refresh = gr.Button(value="Get Recommendations", size="sm")
                    recommendation_list = gr.HTML()
                    refresh.click(fn=update_recommendations, inputs=number, outputs=recommendation_list)

                with gr.Column(visible=True, scale=2) as chat_column:
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
            user_details = gr.Textbox(label="User details", lines=5)
            web_search = gr.Checkbox(label="Enable web search", value=False)
            with gr.Row():
                status = gr.Button(value="Set configurations", interactive=False)
                submit = gr.Button(value="Submit")
            submit.click(fn=submit_configurations, inputs=[user_details, web_search], outputs=status)

if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Launch Client Interface")
    parser.add_argument("--server_port", type=int, default=8001, help="Port number to host the app")
    args = parser.parse_args()
    demo.launch(server_port=args.server_port, show_api=False)
