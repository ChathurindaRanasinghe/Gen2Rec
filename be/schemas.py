from typing import List, Optional

from pydantic import BaseModel


class DefualtConfig(BaseModel):
    llms: List[str]
    embedding_models: List[str]
    system_prompt: Optional[str] = None
