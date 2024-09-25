from asyncio import sleep

import httpx
import panel as pn

pn.extension("perspective")

BACKEND_URL: str = "http://192.168.194.170:8000"
client = httpx.Client(timeout=60)


async def gen2rec_callback(contents, user, instance):
    message = ""
    with client.stream(
            "GET",
            BACKEND_URL + "/chat-stream",
            params={"query": contents},
    ) as response:
        for chunk in response.iter_text(chunk_size=1):
            await sleep(0.005)
            message += chunk
            yield message


chat_interface = pn.chat.ChatInterface(callback=gen2rec_callback, callback_user="Gen2Rec")
chat_panel = pn.Column(chat_interface)

layout = pn.Column(
    pn.Row("# News Center"),
    chat_panel,
    margin=(40, 160),
)

layout.servable(title="News Center")
