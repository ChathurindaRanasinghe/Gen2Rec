import json
from pathlib import Path
from time import perf_counter

from fastapi import BackgroundTasks
from fastapi import FastAPI
from fastapi import Request
from fastapi import Response
from fastapi import status
from fastapi.responses import StreamingResponse

from .engine import RecommendationEngine
from .log import logger
from .schemas import DefaultConfig

app = FastAPI(title="Gen2Rec")
recommendation_engine: RecommendationEngine | None = None


@app.on_event("startup")
async def startup_event():
    global recommendation_engine
    recommendation_engine = RecommendationEngine()


@app.get("/default")
async def get_default_config() -> DefaultConfig:
    return DefaultConfig(
        llms=recommendation_engine.available_llms,
        embedding_models=recommendation_engine.available_embedding_models,
    )


@app.get("/chat-stream")
async def chat_stream(query: str):
    return StreamingResponse(
        recommendation_engine.run_recommendation_system_stream(query=query),
        media_type="text/event-stream",
    )


@app.get("/chat")
async def chat(query: str):
    start = perf_counter()
    # TODO: Add guard rails
    # TODO: Get evaluation
    output = await recommendation_engine.run_recommendation_system(query=query)
    elapsed = perf_counter() - start
    logger.info(f"Time elapsed: {elapsed:.2f}s")
    return output


@app.post("/config")
async def config(request: Request):
    data = await request.form()
    logger.info(data)
    recommendation_engine.llm = data["large_language_model"]

    recommendation_engine.user_details = data["user_details"]

    return "Config successfully updated"


@app.get("/recommendations")
async def recommendations(number: int):
    # TODO: Process user details
    if recommendation_engine.user_details is None:
        query = f"Give me {number} {recommendation_engine.category} recommendations"
    else:
        query = f"Give {number} {recommendation_engine.category} recommendations for following user details.\n{recommendation_engine.user_details}"
    logger.info(f"{query=}")
    output = await recommendation_engine.run_recommendation_system(
        query=query
    )
    # assert len(output["context"]) == number
    return output["context"]


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
    recommendation_engine.metadata_field_info = json.loads(data["metadata_fields"])
    recommendation_engine.embeddings = data["embedding_model"]
    recommendation_engine.category = data["category"]

    logger.info(f"Collection name: {recommendation_engine.collection_name}")
    logger.info(f"Category: {recommendation_engine.category}")
    logger.info(f"Embedding Model: {recommendation_engine.embeddings}")
    logger.info(f"Large Language Model: {recommendation_engine.llm}")

    if recommendation_engine.embeddings_available:
        logger.info("Embeddings already available")
    else:
        recommendation_engine.embedding_columns = data["embedding_fields"]
        dataset = data["dataset_file"]
        logger.debug(dataset)
        recommendation_engine.dataset_file_path = Path(f"datasets/{dataset.filename}")
        # with open(recommendation_engine.dataset_file_path, "w") as dataset_file:
        #     # dataset_file.write(dataset.file.)

    background_task.add_task(recommendation_engine.initialize_recommendation_pipeline())

    return "Initialization successful"
