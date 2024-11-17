from pydantic import BaseModel, Field
from typing import List, Dict, Optional


class LLMRequest(BaseModel):
    prompt: str = Field(
        ...,
        example="What is the weather like today?",
        description="The prompt to send to the LLM.",
    )
    context: Optional[Dict] = Field(
        None, description="Optional context to send with the prompt."
    )


class LLMResponse(BaseModel):
    status: str = Field(
        ..., example="success", description="The status of the LLM operation."
    )
    result: str = Field(
        ...,
        example="The weather is sunny today.",
        description="The result returned by the LLM.",
    )
    tokens_used: Optional[int] = Field(
        None, description="Number of tokens used in the operation."
    )


class NLPExtractionResult(BaseModel):
    entities: List[Dict] = Field(
        ..., description="Extracted entities with types and values."
    )
    confidence: float = Field(
        ..., example=0.95, description="Confidence score of the NLP extraction."
    )
