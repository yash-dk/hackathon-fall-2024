from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, Field
from typing import Optional
from .auth import get_current_user
import json
from .dependencies import get_llm_processor, get_kv_store
from ..backend.kv_store import KVStore

kv_router = APIRouter()
llm_router = APIRouter()


class KVRequest(BaseModel):
    key: str
    value: Optional[str] = None


@kv_router.post("/insert")
def insert_kv(data: KVRequest, user=Depends(get_current_user)):
    if not user["is_admin"]:
        raise HTTPException(status_code=403, detail="Admin access required")
    # Insert logic here
    return {"message": f"Key {data.key} inserted with value {data.value}"}


@kv_router.put("/update")
def update_kv(data: KVRequest, user=Depends(get_current_user)):
    if not user["is_admin"]:
        raise HTTPException(status_code=403, detail="Admin access required")
    # Update logic here
    return {"message": f"Key {data.key} updated to value {data.value}"}


@kv_router.delete("/delete")
def delete_kv(key: str, user=Depends(get_current_user)):
    if not user["is_admin"]:
        raise HTTPException(status_code=403, detail="Admin access required")
    # Delete logic here
    return {"message": f"Key {key} deleted"}


@kv_router.get("/get")
def get_kv(key: str):
    # Fetch logic here
    return {"key": key, "value": "mock_value"}


@llm_router.post("/raw/query")
def raw_query(prompt: str, user=Depends(get_current_user)):
    if not user["is_admin"]:
        raise HTTPException(status_code=403, detail="Admin access required")
    # LLM query logic here
    return {"message": "LLM queried successfully"}

@llm_router.post("/control-kv")
async def control_kv(
    request: dict,
    llm_processor=Depends(get_llm_processor),
    kv_store: KVStore = Depends(get_kv_store),  # Inject KVStore instance
):
    """
    HTTP endpoint for controlling the KV store through LLM.
    """
    # Validate the input data
    if "prompt" not in request:
        raise HTTPException(
            status_code=400, detail="Request must contain a 'prompt' field"
        )

    user_prompt = request["prompt"]

    # Process the prompt with LLM
    llm_response = llm_processor.generate_response(
        template_name="default",  # Use a pre-defined template for LLM queries
        raw_prompt=user_prompt,
        context=None,
        force_json=True,
    )

    if llm_response["status"] != "success":
        raise HTTPException(
            status_code=500, detail="Failed to process the prompt via LLM"
        )

    # Extract actions from the LLM response
    actions = llm_response["data"]
    if not actions:
        raise HTTPException(
            status_code=400, detail="No actions found in the LLM response"
        )

    # Perform actions on KV store
    results = []
    for action in actions:
        action_type = action.get("action")
        key = action.get("key")
        value = action.get("value")

        if action_type == "insert":
            result = kv_store.insert(key, value)
            results.append(result)
        elif action_type == "update":
            result = kv_store.update(key, value)
            results.append(result)
        elif action_type == "delete":
            result = kv_store.delete(key)
            results.append(result)
        elif action_type == "get":
            result = kv_store.get(key)
            results.append(result)
        elif action_type == "get_revisions":
            result = kv_store.get_revisions(key)
            results.append(result)
        else:
            results.append(
                {
                    "status": "error",
                    "message": f"Unsupported action type '{action_type}'",
                }
            )

    # Return the result summary
    return {"status": "completed", "results": results}