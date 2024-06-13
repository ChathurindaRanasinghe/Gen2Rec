import json
from pathlib import Path

from fastapi import BackgroundTasks, FastAPI, Request, Response, status
from loguru import logger

from .engine import RecommendationEngine
from .schemas import DefaultConfig

app = FastAPI(title="Gen2Rec")
recommendation_engine = RecommendationEngine()


@app.get("/default-config")
async def get_default_config() -> DefaultConfig:
    return DefaultConfig(
        llms=recommendation_engine.available_llms,
        embedding_models=recommendation_engine.available_embedding_models,
    )


@app.get("/chat-stream")
async def chat_stream(query: str):
    raise NotImplementedError("Streaming not supported")


@app.get("/chat")
async def chat(query: str):
    # TODO: Add guard rails
    # TODO: Get evaluation
    output = recommendation_engine.run_recommendation_system(query=query)
    return output


@app.post("/config")
async def config(request: Request):
    data = await request.form()

    recommendation_engine.llm = data["large_language_model"]

    # TODO: Process user details

    return "Config successfully updated"


@app.get("/recommendations")
async def recommendations(number: int):
    # TODO: Process user details
    return recommendation_engine.run_recommendation_system(
        query=f"Give me {number} {recommendation_engine.category} recommendations",
        recommendation_only=True,
    )


@app.get("/init-status")
async def init_status(response: Response):
    if not recommendation_engine.recommendation_pipeline:
        message = "Ongoing"
        response.status_code = status.HTTP_201_OK
    else:
        message = "Completed"
        response.status_code = status.HTTP_200_OK

    return message


@app.post("/init")
async def init(request: Request, background_task: BackgroundTasks):
    data = await request.form()

    recommendation_engine.document_content_description = data[
        "document_content_description"
    ]
    recommendation_engine.system_prompt = data["system_prompt"]
    recommendation_engine.metadata_field_info = json.loads(data["metadata_field_info"])
    recommendation_engine.embeddings = data["embedding_model"]
    recommendation_engine.category = data["category"]

    dataset = data["dataset_file"]
    logger.debug(dataset)

    recommendation_engine.dataset_file_path = Path(f"datasets/{dataset.filename}")

    with open(recommendation_engine.dataset_file_path, "w") as dataset_file:
        dataset_file.write(dataset.content)

    recommendation_engine.add_task(
        recommendation_engine.initialize_recommendation_pipeline()
    )

    return "Initialization successful"
