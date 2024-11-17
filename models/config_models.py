from pydantic import BaseModel, Field
from typing import Dict, Optional


class ConfigSetRequest(BaseModel):
    key: str = Field(
        ..., example="prompt.template", description="The configuration key."
    )
    value: Dict = Field(
        ...,
        example={"template": "This is a template"},
        description="The configuration value.",
    )


class ConfigGetRequest(BaseModel):
    key: str = Field(
        ..., example="prompt.template", description="The configuration key to retrieve."
    )


class ConfigResponse(BaseModel):
    status: str = Field(
        ..., example="success", description="The status of the operation."
    )
    message: Optional[str] = Field(
        None, example="Configuration retrieved successfully."
    )
    data: Optional[Dict] = Field(None, description="Configuration data, if any.")
