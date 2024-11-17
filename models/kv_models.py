from pydantic import BaseModel, Field
from typing import Optional, Dict


class KVInsertRequest(BaseModel):
    key: str = Field(
        ..., example="example.key", description="The key to insert into the KV store."
    )
    value: Dict = Field(
        ...,
        example={"example": "value"},
        description="The value associated with the key.",
    )


class KVUpdateRequest(BaseModel):
    key: str = Field(
        ..., example="example.key", description="The key to update in the KV store."
    )
    value: Dict = Field(
        ...,
        example={"example": "updated value"},
        description="The updated value for the key.",
    )


class KVResponse(BaseModel):
    status: str = Field(
        ..., example="success", description="The status of the operation."
    )
    message: Optional[str] = Field(None, example="Operation completed successfully.")
    data: Optional[Dict] = Field(
        None, description="Data returned from the operation, if any."
    )
