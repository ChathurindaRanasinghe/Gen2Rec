from asyncio import sleep

import httpx
import panel as pn

pn.extension("perspective")

BACKEND_URL: str = "http://192.168.164.171:8000"
client = httpx.Client(timeout=60)


def create_card(data):
    return pn.Row(
        pn.pane.Image(data["thumbnail"], width=240, height=240),
        pn.Column(
            pn.pane.Markdown(f"""
                        ### {data["name"]} ({data["launch_year"]})
                        Processor: {data["cpu_prod"]} {data["cpu_model"]}
                        RAM: {data["memory_size"]}GB {data["memory_type"]}
                        Storage: {data["primary_storage_cap"]}GB {data["primary_storage_model"]}
                        Display: {data["display_size"]}-inch {data["display_type"]} {data["display_horizontal_resolution"]}x{data["display_vertical_resolution"]}
                        Graphics: {data["gpu_prod"]} {data["gpu_model"]}
                        Battery Life: {data["battery_life_hours"]:.2f}h
                        Weight: {data["chassis_weight_kg"]}kg
                        Operating System: {data["operating_system"]}
                        Price: ${data["price"]}
                        """),
            margin=10
        ),
        width=580,
        margin=10,
        styles=dict(background='WhiteSmoke')
    )


def get_recs(number):
    body = {"number": number}
    response = client.get(
        BACKEND_URL + "/recommendations",
        params=body,
    )
    if response.status_code != 200:
        raise RuntimeError()

    cards = []
    for each in response.json():
        cards.append(create_card(each["metadata"]))
    return cards


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


cards = get_recs(2)
odd_cards = [card for idx, card in enumerate(cards) if idx % 2 != 0]
even_cards = [card for idx, card in enumerate(cards) if idx % 2 == 0]

chat_interface = pn.chat.ChatInterface(callback=gen2rec_callback, callback_user="Gen2Rec")
chat_panel = pn.Column(chat_interface, visible=False)
toggle_button = pn.widgets.Button(name='Show Chat', button_type='light')
card_set = pn.Row(pn.Column(*even_cards), pn.Column(*odd_cards))


def toggle_chat(event):
    global card_set
    chat_panel.visible = not chat_panel.visible
    if chat_panel.visible:
        toggle_button.name = 'Hide Chat'
        card_set.objects = [pn.Column(*cards)]
    else:
        toggle_button.name = 'Show Chat'
        card_set.objects = [pn.Row(pn.Column(*even_cards), pn.Column(*odd_cards))]


toggle_button.on_click(toggle_chat)

layout = pn.Column(
    pn.Row("# Laptop Arcade", align=("center")),
    pn.Row(toggle_button,
           align=("end")),
    pn.Row(
        card_set,
        pn.Spacer(width=100),
        chat_panel
    ),
    margin=(10, 50),
)

layout.servable()
