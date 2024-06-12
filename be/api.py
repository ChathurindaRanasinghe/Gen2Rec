import json

from fastapi import FastAPI, Request

from engine import RecommendationEngine
from schemas import DefualtConfig

app = FastAPI(title="Gen2Rec")
recommendation_engine = RecommendationEngine()


@app.get("/default-config")
async def get_default_config() -> DefualtConfig:
    return DefualtConfig(
        llms=recommendation_engine.available_llms,
        embedding_models=recommendation_engine.available_embedding_models,
    )


@app.get("/chat")
async def chat(query: str):
    output = recommendation_engine.run_recommendation_system(query=query)
    return output


@app.post("/config")
async def config(request: Request):
    data = await request.form()

    recommendation_engine.llm = data["large_language_model"]
    # TODO: Get evaluation
    # TODO: Process user details

    return "Config successfully updated"


@app.get("/recommendations")
async def recommendations(number: int):
    # TODO: Process user details
    return recommendation_engine.run_recommendation_system(
        query=f"Give me {number} {recommendation_engine.category} recommendations", recommendation_only=True,
    )


@app.post("/init")
async def init(request: Request):
    data = await request.form()

    recommendation_engine.document_content_description = data["document_content_description"]
    recommendation_engine.system_prompt = data["system_prompt"]
    recommendation_engine.metadata_field_info = json.loads(data["metadata_field_info"])
    recommendation_engine.embeddings = data["embedding_model"]
    recommendation_engine.category = data["category"]

    # TODO: Save dataset file
    # TODO: Add generating embeddings to a background task
