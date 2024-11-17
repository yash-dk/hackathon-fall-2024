from langchain.prompts import PromptTemplate
from typing import Dict
from .constants import DEFAULT_TEMPLATE

class PromptManager:
    """
    Manages and formats prompts using LangChain's PromptTemplate.
    """

    def __init__(self):
        """
        Initialize PromptManager with predefined templates.
        """
        self.templates = {
            "default": PromptTemplate.from_template(DEFAULT_TEMPLATE),
        }

    def format_prompt(
        self, template_name: str, prompt: str, context: Dict = None
    ) -> str:
        """
        Format a prompt using the selected template.

        :param template_name: The name of the template.
        :param prompt: The raw user input.
        :param context: Optional context dictionary.
        :return: A formatted string prompt.
        """
        if template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' not found.")
        template = self.templates[template_name]

        if context:
            return template.format(
                prompt=prompt,
                context="\n".join(f"{k}: {v}" for k, v in context.items()),
            )
        return template.format(prompt=prompt)

    def add_template(self, template_name: str, template: str):
        """
        Add a new prompt template.

        :param template_name: Name of the new template.
        :param template: Template string with placeholders.
        """
        self.templates[template_name] = PromptTemplate.from_template(template)
