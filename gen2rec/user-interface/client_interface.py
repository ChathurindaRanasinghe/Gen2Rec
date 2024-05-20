import argparse

import gradio as gr

parser = argparse.ArgumentParser(description="Launch Client Interface for a Category")
parser.add_argument("--category", type=str, required=True, help="Category to use in the recommendation")
parser.add_argument("--server_port", type=int, default=8001, help="Port number to host the app")
args = parser.parse_args()

CATEGORY = args.category
LIST = "List"
CHAT = "Chat"
VISIBILITY = {LIST: True, CHAT: True}


def chat_response(message, history):
    history = history or []
    if message:
        bot_response = f"{message[::-1]}"
        history.append([message, bot_response])
    return "", history


def change_visibility(visible):
    VISIBILITY[LIST] = LIST in visible
    VISIBILITY[CHAT] = CHAT in visible
    return gr.update(visible=VISIBILITY[LIST]), gr.update(visible=VISIBILITY[CHAT])


css = """
.card {
    background-color: gray;
    padding: 10px;
    border-radius:10px;
}
"""

with gr.Blocks(css=css) as demo:
    gr.Markdown(f"# {CATEGORY.capitalize()} Recommendation with Gen2Rec")
    with gr.Tabs():
        with gr.TabItem("Recommendations"):
            with gr.Row():
                list_column = gr.Column(scale=1, visible=True, variant="panel")
                with list_column:
                    for c in range(0, 5):
                        with gr.Row(elem_classes="card"):
                            with gr.Column():
                                gr.Markdown("data")
                                gr.Button(value="link")
                chat_column = gr.Column(scale=1, visible=True)
                with chat_column:
                    chatbot = gr.Chatbot()
                    message = gr.Textbox(label="Message")
                    submit = gr.Button("Send")
                    submit.click(chat_response, inputs=[message, chatbot], outputs=[message, chatbot])

        with gr.TabItem("Configurations"):
            visible = gr.CheckboxGroup([LIST, CHAT], label="Visible recommendation options", value=[LIST, CHAT])
            visible.change(change_visibility, inputs=visible, outputs=[list_column, chat_column])

if __name__ == "__main__":
    demo.launch(server_port=args.server_port)
