import argparse
import json

import gradio as gr
import pandas
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


def metadata_to_json(metadata_fields) -> json:
    try:
        if type(metadata_fields) is pandas.DataFrame:
            metadata_fields.columns = [col.lower() for col in metadata_fields.columns]
            json_data = metadata_fields.to_json(orient="records")
        else:
            json_data = json.loads(metadata_fields)
    except:
        json_data = {"Error": "Invalid JSON provided"}
    return gr.update(value=json_data)


def initialize(
        recommendation_category: str,
        dataset_file,
        embedding_fields: list[str],
        improve_dataset: bool,
        document_content_description: str,
        metadata_fields: list,
        embedding_model: str,
        system_prompt: str,
) -> tuple:
    global CATEGORY
    global INITIALIZED
    global FIELDS

    if not recommendation_category:
        status = "No recommendation category provided"
    elif not dataset_file:
        status = "No dataset file provided"
    elif not embedding_fields:
        status = "No fields selected"
    elif not document_content_description:
        status = "No document content description provided"
    elif (type(metadata_fields) is not list or
          any(any(value == "" for value in item.values()) for item in metadata_fields)):
        status = "No valid metadata fields provided"
    elif any(set([item["name"] for item in metadata_fields]) - set(FIELDS)):
        status = "Unavailable field provided in metadata"
    elif any(set([item["type"] for item in metadata_fields]) - set(METADATA["AllowedTypes"])):
        status = "Unavailable data type provided in metadata"
    elif not embedding_model:
        status = "No embedding model selected"
    elif not system_prompt:
        status = "No system prompt provided"
    else:
        try:
            body = {
                "recommendation_category": recommendation_category.lower(),
                "dataset_file": dataset_file,
                "embedding_fields": embedding_fields,
                "improve_dataset": improve_dataset,
                "document_content_description": document_content_description,
                "metadata_fields": metadata_fields,
                "embedding_model": embedding_model,
                "system_prompt": system_prompt,
            }
            response = requests.post(
                BACKEND_URL + "/init",
                data=body,
            )
            if response.status_code == 200:
                status = "Successfully initialized"
                INITIALIZED = True
                CATEGORY = recommendation_category
                FIELDS = embedding_fields
            else:
                print(response)
                status = "Issue occurred in initialization"
        except Exception as e:
            print(e)
            status = "Issue occurred in initialization"
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


def submit_configurations(large_language_model: str, user_details: str) -> dict:
    try:
        body = {
            "large_language_model": large_language_model,
            "user_details": user_details
        }
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


def get_recommendations(number: int) -> dict:
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
            recommendations = [{"Error": "Error receiving response"}]
    except Exception as e:
        print(e)
        recommendations = [{"Error": "Error receiving response"}]
    return gr.update(value=recommendations)


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
.gradio-container {
    max-width: none !important;
}
      
footer {
    visibility: hidden;
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
                embedding_fields = gr.CheckboxGroup(label="Embedding Fields", interactive=True, visible=False)
                improve_dataset = gr.Checkbox(label="Improve dataset with additional data")
                document_content_description = gr.Textbox(label="Document Content Description", lines=2)
                gr.Markdown("Metadata Fields")
                with gr.Row():
                    with gr.Column(scale=2):
                        with gr.Tabs():
                            with gr.TabItem(label="Form Data"):
                                metadata_form_data = gr.Dataframe(
                                    show_label=False,
                                    headers=METADATA["Headings"],
                                    datatype=METADATA["Datatypes"],
                                    col_count=(3, "fixed"),
                                    interactive=True
                                )
                            with gr.TabItem(label="JSON Data"):
                                metadata_json_data = gr.Textbox(show_label=False, lines=4)
                    with gr.Column(scale=1):
                        metadata_json = gr.JSON(label="Metadata JSON")
                metadata_form_data.change(fn=metadata_to_json, inputs=metadata_form_data, outputs=metadata_json)
                metadata_json_data.change(fn=metadata_to_json, inputs=metadata_json_data, outputs=metadata_json)

                embedding_model = gr.Dropdown(label="Embedding Model", choices=EMBEDDING_MODELS)
                system_prompt = gr.Textbox(label="System Prompt", value=SYSTEM_PROMPT, lines=5)
                dataset_file.change(fn=update_fields, inputs=dataset_file, outputs=embedding_fields)
                with gr.Row():
                    message = gr.Button(value="Initialization not completed", interactive=False)
                    init = gr.Button(value="Initialize")
                    init.click(
                        fn=initialize,
                        inputs=[
                            recommendation_category,
                            dataset_file,
                            embedding_fields,
                            improve_dataset,
                            document_content_description,
                            metadata_json,
                            embedding_model,
                            system_prompt,
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
                    with gr.Column(visible=True, variant="panel", scale=2) as list_column:
                        gr.Markdown(value="Recommendation List")
                        number = gr.Slider(
                            label="Number of recommendations",
                            value=5,
                            minimum=1,
                            maximum=20,
                            step=1,
                        )
                        refresh = gr.Button(value="Get Recommendations", size="sm")
                        recommendation_list = gr.JSON()
                        refresh.click(
                            fn=get_recommendations,
                            inputs=number,
                            outputs=recommendation_list,
                        )
                    with gr.Column(visible=True, scale=3) as chat_column:
                        gr.Markdown(value="Recommendation Chat Interface")
                        chatbot = gr.Chatbot(height=700)
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
                    label="Visible Recommendation Options",
                    value=[LIST, CHAT],
                )
                visible.change(
                    fn=change_visibility, inputs=visible, outputs=[list_column, chat_column]
                )
                gr.Markdown(value="<hr>")
                gr.Markdown(value="Recommendation System Configurations")
                large_language_model = gr.Dropdown(label="Large Language Model",
                                                   choices=LARGE_LANGUAGE_MODELS)
                user_details = gr.Textbox(label="User Details", lines=5)
                with gr.Row():
                    status = gr.Button(value="Set configurations", interactive=False)
                    submit = gr.Button(value="Submit")
                submit.click(
                    fn=submit_configurations,
                    inputs=[large_language_model, user_details],
                    outputs=status,
                )
    demo.launch(server_port=server_port, show_api=False)


def get_default_values():
    global SYSTEM_PROMPT
    global EMBEDDING_MODELS
    global LARGE_LANGUAGE_MODELS
    try:
        response = requests.get(BACKEND_URL + "/default")
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
