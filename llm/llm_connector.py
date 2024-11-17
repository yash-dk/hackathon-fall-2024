from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI


class LLMConnector:
    """
    A unified interface for interacting with Gemini and OpenAI LLMs via LangChain.
    """

    def __init__(self, api_type: str, api_key: str, model_name: str):
        """
        Initialize the LLM connector using LangChain.

        :param api_type: "openai" or "gemini" for the respective API.
        :param model_name: The model name to use (e.g., "gpt-4o-mini" or "gemini-1.5-flash").
        :param api_key: The API key for the respective API.
        """
        self.api_type = api_type.lower()
        self.model_name = model_name
        self.api_key = api_key

        if self.api_type == "openai":
            self.llm = self._initialize_openai_llm()
        elif self.api_type == "gemini":
            self.llm = self._initialize_gemini_llm()
        else:
            raise ValueError(f"Unsupported API type: {self.api_type}")

    def _initialize_openai_llm(self) -> ChatOpenAI:
        """
        Initialize the OpenAI LLM with the API key.
        """
        return ChatOpenAI(model=self.model_name, openai_api_key=self.api_key)

    def _initialize_gemini_llm(self) -> ChatGoogleGenerativeAI:
        """
        Initialize the Gemini LLM with the API key.
        """
        return ChatGoogleGenerativeAI(model=self.model_name, google_api_key=self.api_key)

    def query(self, prompt: str) -> Dict[str, Any]:
        """
        Query the LLM with a given prompt.

        :param prompt: The input prompt.
        :return: The LLM's response as a dictionary.
        """
        if not self.llm:
            raise ValueError("LLM is not initialized.")
        try:
            response = self.llm.invoke(prompt)
            return {"status": "success", "data": response}
        except Exception as e:
            return {"status": "error", "message": str(e)}
