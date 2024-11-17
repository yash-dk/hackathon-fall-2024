import os
from .llm.llm_processor import LLMProcessor
from .llm.nlp_processor import NLPProcessor
from .api.main import app

# Load environment variables or manually set API details
API_TYPE = "gemini"  # Specify "gemini" to use the Gemini API
API_KEY = os.getenv("GEMINI_API_KEY")
API_KEY = os.getenv("OPEN_AI_API_KEY")

def main():
    # Initialize the LLMProcessor with Gemini API details
    llm_processor = LLMProcessor(api_type=API_TYPE, api_key=API_KEY, model_name="models/gemini-1.5-flash")
    # llm_processor = LLMProcessor(api_type=API_TYPE, api_key=API_KEY, model_name="gpt-4o-mini")

    # Example prompt
    raw_prompt = "Please insert a key-value pair with the key 'name' and the value 'Alice' and update the key 'age' with the value '30'."

    # Optional context (can include user-specific or task-specific data)
    context = {
        "tone": "adventurous",
        "length": "short",
    }

    # Use the LLMProcessor to get a response from Gemini
    response = llm_processor.generate_response('default', raw_prompt, force_json=True)

    # Display the response
    if response["status"] == "success":
        print("LLM Response:")
        print(response["data"])
    else:
        print("Error:", response["message"])

if __name__ == "__main__":
    import uvicorn

if __name__ == "__main__":
    # Use `api.main:app` to reference the FastAPI instance in `api/main.py`
    import dotenv
    dotenv.load_dotenv()
    uvicorn.run(app, host="127.0.0.1", port=8000)

    # main()

# if __name__ == "__main__":
#     processor = NLPProcessor()

#     # Example input
#     text_input = "Please insert a key age and the value 40."

#     # Extract action, key, and value
#     result = processor.extract_action_key_value(text_input)

#     print("Extracted Information:")
#     print(f"Action: {result['action']}")
#     print(f"Key: {result['key']}")
#     print(f"Value: {result['value']}")
