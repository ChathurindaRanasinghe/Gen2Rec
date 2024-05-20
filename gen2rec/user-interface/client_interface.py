import argparse

import gradio as gr

parser = argparse.ArgumentParser(description='Launch Client Interface for a Category')
parser.add_argument('--category', type=str, default='BOOK', help='Category to use in the recommendation')
parser.add_argument('--server_name', type=str, default='Gen2Rec', help='Server name to host the app')
parser.add_argument('--server_port', type=int, default=7861, help='Port number to host the app')
args = parser.parse_args()

CATEGORY = args.category


def chat_response(message, history):
    history = history or []
    bot_response = f"{message[::-1]}"
    history.append([message, bot_response])
    return "", history


def option1():
    return "Option 1 selected"


def option2():
    return "Option 2 selected"


with gr.Blocks() as demo:
    # gr.Markdown(f"# Gen2Rec")
    gr.Markdown(f"# {CATEGORY.capitalize()} Recommendation with Gen2Rec")
    with gr.Tabs():
        with gr.TabItem("Recommendations"):
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("recs")

                with gr.Column(scale=1):
                    with gr.Accordion("See Details"):
                        gr.Markdown("### Chat App")
                        chatbot = gr.Chatbot()
                        msg = gr.Textbox(label="Message")
                        submit = gr.Button("Send")
                        submit.click(chat_response, inputs=[msg, chatbot], outputs=[msg, chatbot])

        with gr.TabItem("Configurations"):
            with gr.Tabs():
                with gr.TabItem("Option 1"):
                    btn1 = gr.Button("Option 1")
                    output1 = gr.Textbox(label="Selected Option")
                    btn1.click(option1, inputs=None, outputs=output1)
                    gr.Markdown("Content for Option 1")
                with gr.TabItem("Option 2"):
                    btn2 = gr.Button("Option 2")
                    output2 = gr.Textbox(label="Selected Option")
                    btn2.click(option2, inputs=None, outputs=output2)
                    gr.Markdown("Content for Option 2")

if __name__ == "__main__":
    args.server_name = ""
    args.server_port = 7861
    demo.launch(server_name=args.server_name, server_port=args.server_port)
