import json
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .llm_connector import LLMConnector
from .prompt_manager import PromptManager


class LLMProcessor:
    """
    Combines the LLMConnector and PromptManager to process and query prompts.
    Includes an option to force JSON formatting in the LLM output.
    """

    def __init__(
        self, api_type: str, api_key: str, model_name: str = "text-davinci-003"
    ):
        """
        Initialize the LLMProcessor.

        :param api_type: "openai" or "gemini" for the respective API.
        :param api_key: The API key for the chosen LLM.
        :param model_name: The model name (default: "text-davinci-003").
        """
        self.connector = LLMConnector(api_type, api_key, model_name)
        self.prompt_manager = PromptManager()

        # Prompt for re-asking LLM to return JSON format
        self.json_prompt_template = PromptTemplate(
            template="Ensure the following response is in JSON format:\n\n{response}"
        )
        self.output_parser = StrOutputParser()

    def process_prompt(
        self, template_name: str, raw_prompt: str, context: dict = None
    ) -> str:
        """
        Process a prompt with a selected template.

        :param template_name: The name of the template to use.
        :param raw_prompt: The raw user input.
        :param context: Optional context dictionary.
        :return: The formatted prompt.
        """
        return self.prompt_manager.format_prompt(template_name, raw_prompt, context)

    def _extract_json_substring(self, text: str) -> str:
        """
        Extract the text between the first '{' and the last '}' if the whole text is not valid JSON.

        :param text: The input text containing potential JSON content.
        :return: The extracted JSON substring or the original text if '{' and '}' are not found.
        """
        start_index = text.find("[")
        end_index = text.rfind("]")
        if start_index != -1 and end_index != -1:
            return text[start_index : end_index + 1]
        return text

    def _is_valid_json(self, text: str) -> bool:
        """
        Check if a given text is valid JSON.

        :param text: The text to validate.
        :return: True if the text is valid JSON, otherwise False.
        """
        try:
            json.loads(text)
            return True
        except json.JSONDecodeError:
            return False

    def _force_json_response(self, initial_response: str) -> str:
        """
        Re-prompt the LLM to force a JSON response.

        :param initial_response: The initial response from the LLM.
        :return: A JSON-formatted response as a string.
        """
        # Format the re-prompt with the JSON directive
        formatted_prompt = self.json_prompt_template.format(response=initial_response)

        # Pass the re-prompted query to the LLM
        llm = self.connector.llm  # Get the underlying LangChain LLM
        re_prompted_response = llm.invoke(formatted_prompt)

        return re_prompted_response

    def generate_response(
        self,
        template_name: str,
        raw_prompt: str,
        context: dict = None,
        force_json: bool = False,
        **kwargs
    ) -> dict:
        """
        Generate a response from the LLM based on the processed prompt.

        :param template_name: Template to use for formatting the prompt.
        :param raw_prompt: The raw user input.
        :param context: Optional context dictionary.
        :param force_json: If True, ensures the response is JSON formatted.
        :param kwargs: Additional parameters for the LLM.
        :return: A dictionary containing the status and response data.
        """
        # Format the prompt
        formatted_prompt = self.process_prompt(template_name, raw_prompt, context)

        # Query the LLM for the response
        response = self.connector.query(formatted_prompt, **kwargs)
        if response["status"] != "success":
            return response

        output = response["data"]

        # If force_json is enabled, validate the JSON response
        if force_json:
            content = (
                output.content.strip()
            )  # Ensure the content is stripped of any leading/trailing spaces
            if not self._is_valid_json(content):
                # Try extracting a valid JSON substring
                json_candidate = self._extract_json_substring(content)
                if self._is_valid_json(json_candidate):
                    return {"status": "success", "data": json.loads(json_candidate)}

                # Re-prompt to force JSON response
                forced_output = self._force_json_response(content)
                if self._is_valid_json(forced_output.content):
                    return {"status": "success", "data": json.loads(forced_output.content)}
                else:
                    return {
                        "status": "error",
                        "message": "Failed to produce valid JSON after re-prompting.",
                    }
            else:
                return {"status": "success", "data": json.loads(content)}

        # Return the raw response if JSON forcing is not required
        return {"status": "success", "data": output}
