from fastapi import FastAPI
from .routes import kv_router, llm_router
from .auth import auth_router
from .ws_manager import WebSocketManager

app = FastAPI(
    title="LLM and KV Store API",
    description="API for managing KV store and LLM queries with role-based access.",
    version="1.0.0",
)

# Register routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(kv_router, prefix="/kv", tags=["KV Store"])
app.include_router(llm_router, prefix="/llm", tags=["LLM"])

# WebSocket manager (global instance)
ws_manager = WebSocketManager()

@app.get("/status", tags=["Status"])
async def status():
    """
    API health check endpoint.
    """
    return {"status": "ok", "message": "API is running."}
