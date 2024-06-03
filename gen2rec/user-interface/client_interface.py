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
    "AllowedTypes": ["integer", "float", "string", "list", "date"],
}
SYSTEM_PROMPT: str = ""
EMBEDDING_MODELS: list[str] = []
LARGE_LANGUAGE_MODELS: list[str] = []
BACKEND_URL: str = "https://b8tbzq9k-8002.asse.devtunnels.ms"


def update_fields(dataset_file) -> dict:
    global FIELDS
    file = str(dataset_file)[2:-1]
    file = file.replace("\\t", ",").replace("\\n", "\n").replace("\\r", "")
    FIELDS = file.split('\n')[0].split(',')
    return gr.update(choices=FIELDS, value=FIELDS, visible=True)


def initialize(
        recommendation_category: str,
        dataset_file,
        improve_dataset: bool,
        document_content_description: str,
        selected_fields: list[str],
        system_prompt: str,
        recommendation_fields,
) -> tuple:
    print(recommendation_fields)
    global CATEGORY
    global INITIALIZED
    global FIELDS
    recommendation_fields = recommendation_fields.replace("", None)

    status = "Initialization not completed"
    if not recommendation_category:
        status = "No recommendation category provided"
    elif not dataset_file:
        status = "No dataset file provided"
    elif not document_content_description:
        status = "No document content description provided"
    elif not system_prompt:
        status = "No system prompt provided"
    elif recommendation_fields.isnull().values.any():
        status = "No recommendation fields provided"
    elif len(
            [
                element
                for element in recommendation_fields["Name"].values
                if element not in FIELDS
            ]
    ):
        status = "Unavailable fields provided"
    elif len(
            [
                element
                for element in recommendation_fields["Type"].values
                if element not in METADATA["AllowedTypes"]
            ]
    ):
        status = "Unallowed data type selected"
    else:
        print(selected_fields)
        try:
            CATEGORY = recommendation_category
            INITIALIZED = True
            FIELDS = selected_fields
            recommendation_fields.columns = [col.lower() for col in recommendation_fields.columns]
            metadata_json: json = recommendation_fields.to_json(orient="records")
            body = {
                "recommendation_category": recommendation_category.lower(),
                "dataset_file": dataset_file,
                "improve_dataset": improve_dataset,
                "system_prompt": system_prompt,
                "metadata_field_info": metadata_json,
                "document_content_description": document_content_description,
            }
            response = requests.post(
                BACKEND_URL + "/init",
                data=body,
            )
            if response.status_code == 200:
                status = "Successfully initialized"
            else:
                print(response)
                status = "Issue occurred in initialization"
        except Exception as e:
            print(e)
            status = "Issue occurred in initialization"
    INITIALIZED = True
    return (
        gr.update(interactive=INITIALIZED),
        gr.update(interactive=INITIALIZED),
        gr.update(value=status),
        gr.update(value=f"# {TITLE} - {CATEGORY.capitalize()} Recommendation"),
    )


def change_visibility(visible: list) -> tuple:
    VISIBILITY[LIST] = LIST in visible
    VISIBILITY[CHAT] = CHAT in visible
    return gr.update(visible=VISIBILITY[LIST]), gr.update(visible=VISIBILITY[CHAT])


def submit_configurations(user_details: str, web_search: bool) -> dict:
    try:
        body = {"user_details": user_details, "web_search": web_search}
        response = requests.post(
            BACKEND_URL + "/config",
            data=json.dumps(body),
        )
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
        body = {"number": number}
        response = requests.get(
            BACKEND_URL + "/recommendations",
            params=body,
        )
        if response.status_code == 200:
            recommendations = response.json()
        else:
            print(response)
            recommendations = [{"metadata": "Error receiving response"}]
    except Exception as e:
        print(e)
        recommendations = [{"metadata": "Error receiving response"}]

    recommendations_html = ""
    for rec in recommendations:
        recommendations_html += f"""
        <div class="card">
        {rec["metadata"]}
        </div>
        """
    return gr.update(value=recommendations_html)


def chat_response(message: str, history: list[str]) -> tuple[str, list]:
    history: list = history or []
    if message:
        try:
            body = {"query": message}
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


css: str = """
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


def run_client_interface(server_port: int) -> None:
    with gr.Blocks(css=css, title=TITLE) as demo:
        title_display = gr.Markdown(value=f"# {TITLE}")

        with gr.Tabs():
            init_tab = gr.TabItem(label="Initialization")
            configuration_tab = gr.TabItem(label="Configurations", interactive=INITIALIZED)
            recommendation_tab = gr.TabItem(label="Recommendations", interactive=INITIALIZED)
            with init_tab:
                recommendation_category = gr.Textbox(label="Recommendation Category")
                dataset_file = gr.File(label="Upload dataset", type="binary", file_types=[".csv"])
                selected_fields = gr.CheckboxGroup(label="Dataset Fields", interactive=True, visible=False)
                improve_dataset = gr.Checkbox(label="Improve dataset with additional data")
                document_content_description = gr.Textbox(label="Document Content Description", lines=2)
                system_prompt = gr.Textbox(label="System Prompt", lines=5)
                gr.Markdown("Metadata Fields")
                recommendation_fields = gr.Dataframe(
                    show_label=False,
                    headers=METADATA["Headings"],
                    datatype=METADATA["Datatypes"],
                    col_count=(3, "fixed"),
                    interactive=True
                )
                dataset_file.change(fn=update_fields, inputs=dataset_file, outputs=selected_fields)
                with gr.Row():
                    message = gr.Button(value="Initialize to continue", interactive=False)
                    init = gr.Button(value="Initialize")
                    init.click(
                        fn=initialize,
                        inputs=[
                            recommendation_category,
                            dataset_file,
                            improve_dataset,
                            document_content_description,
                            selected_fields,
                            system_prompt,
                            recommendation_fields,
                        ],
                        outputs=[
                            recommendation_tab,
                            configuration_tab,
                            message,
                            title_display,
                        ],
                    )
            with recommendation_tab:
                with gr.Row():
                    with gr.Column(visible=True, variant="panel", scale=1) as list_column:
                        gr.Markdown(value="Recommendation List")
                        number = gr.Slider(
                            label="Number of recommendations",
                            value=5,
                            minimum=1,
                            maximum=20,
                            step=1,
                        )
                        refresh = gr.Button(value="Get Recommendations", size="sm")
                        recommendation_list = gr.HTML()
                        refresh.click(
                            fn=update_recommendations,
                            inputs=number,
                            outputs=recommendation_list,
                        )
                    with gr.Column(visible=True, scale=2) as chat_column:
                        gr.Markdown(value="Recommendation Chat Interface")
                        chatbot = gr.Chatbot()
                        message = gr.Textbox(show_label=False)
                        submit = gr.Button(value="Send")
                        submit.click(
                            fn=chat_response,
                            inputs=[message, chatbot],
                            outputs=[message, chatbot],
                        )
            with configuration_tab:
                visible = gr.CheckboxGroup(
                    choices=[LIST, CHAT],
                    label="Visible recommendation options",
                    value=[LIST, CHAT],
                )
                visible.change(
                    fn=change_visibility, inputs=visible, outputs=[list_column, chat_column]
                )
                gr.Markdown(value="<hr>")
                gr.Markdown(value="Recommendation System Configurations")
                user_details = gr.Textbox(label="User details", lines=5)
                web_search = gr.Checkbox(label="Enable web search", value=False)
                with gr.Row():
                    status = gr.Button(value="Set configurations", interactive=False)
                    submit = gr.Button(value="Submit")
                submit.click(
                    fn=submit_configurations,
                    inputs=[user_details, web_search],
                    outputs=status,
                )
    demo.launch(server_port=server_port, show_api=False)


def get_default_values():
    global SYSTEM_PROMPT
    global EMBEDDING_MODELS
    global LARGE_LANGUAGE_MODELS
    try:
        response = requests.post(BACKEND_URL + "/default")
        if response.status_code == 200:
            SYSTEM_PROMPT = response.json()["system_prompt"]
            EMBEDDING_MODELS = response.json()["embedding_models"]
            LARGE_LANGUAGE_MODELS = response.json()["large_language_models"]
            return True
        else:
            print(response)
    except Exception as e:
        print(e)
    return False


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Launch Client Interface")
    parser.add_argument("--server_port", type=int, default=8001, help="Port number to host the app")
    args = parser.parse_args()
    pass_connection: bool = get_default_values()
    if pass_connection:
        run_client_interface(server_port=args.server_port)
    else:
        print("Backend connection failed")
