from ..llm.llm_processor import LLMProcessor
from ..backend.kv_store import KVStore
from ..backend.db_setup import get_session, get_engine, init_db
import os

def get_llm_processor() -> LLMProcessor:
    return LLMProcessor(api_type="gemini", api_key=os.environ.get("GEMINI_API_KEY"), model_name="models/gemini-1.5-flash")

def get_kv_store() -> KVStore:
    engine = get_engine()
    init_db(engine)
    session = get_session(engine)
    return KVStore(session)