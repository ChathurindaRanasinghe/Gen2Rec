from asyncio import sleep

import httpx
import panel as pn

pn.extension("perspective")

BACKEND_URL: str = "http://192.168.20.170:8000"
client = httpx.Client(timeout=60)


def create_card(data):
    return pn.Column(
        pn.Column(
            pn.pane.Markdown(f"""
                    ## {data["Title"]} ({data["Year"]})
                    """),
            align="center"
        ),
        pn.pane.Image(data["Poster"], width=180, align="center"),
        pn.Column(
            pn.pane.Markdown(f"""
                        Genre: {data["Genre"]}
                        Runtime: {data["Runtime"]}min
                        Language: {data["Language"]}
                        IMDB Rating: {data["imdbRating"]} ({data["imdbVotes"]})
                        """),
            align="center"
        ),
        width=320,
        margin=10,
        styles=dict(background='WhiteSmoke', text_align='center')
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


cards = get_recs(8)
cards_1 = [card for idx, card in enumerate(cards) if idx % 4 == 0]
cards_2 = [card for idx, card in enumerate(cards) if idx % 4 == 1]
cards_3 = [card for idx, card in enumerate(cards) if idx % 4 == 2]
cards_4 = [card for idx, card in enumerate(cards) if idx % 4 == 3]

chat_interface = pn.chat.ChatInterface(callback=gen2rec_callback, callback_user="Gen2Rec")
chat_panel = pn.Column(chat_interface, visible=False)
toggle_button = pn.widgets.Button(name='Show Chat', button_type='light')
card_set = pn.Row(pn.Column(*cards_1), pn.Column(*cards_2), pn.Column(*cards_3), pn.Column(*cards_4))


def toggle_chat(event):
    global card_set
    chat_panel.visible = not chat_panel.visible
    if chat_panel.visible:
        toggle_button.name = 'Hide Chat'
        card_set.objects = [pn.Column(*cards)]
    else:
        toggle_button.name = 'Show Chat'
        card_set.objects = [pn.Row(pn.Column(*cards_1), pn.Column(*cards_2), pn.Column(*cards_3), pn.Column(*cards_4))]


toggle_button.on_click(toggle_chat)

layout = pn.Column(
    pn.Row("# Movie Hub", align=("center")),
    pn.Row(toggle_button,
           align=("end")),
    pn.Row(
        card_set,
        pn.Spacer(width=100),
        chat_panel
    ),
    margin=(10, 50),
)

layout.servable(title="Movie Hub")
