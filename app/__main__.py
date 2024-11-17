from .api.main import app
import uvicorn

if __name__ == "__main__":
    import dotenv
    dotenv.load_dotenv()
    uvicorn.run(app, host="127.0.0.1", port=8000)