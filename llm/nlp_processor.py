import spacy
from typing import Dict, Optional


class NLPProcessor:
    """
    A class for processing natural language inputs to extract action, key, and value using NLP.
    """

    def __init__(self, model: str = "en_core_web_sm"):
        """
        Initialize the NLPProcessor with a spaCy model.
        """
        self.nlp = spacy.load(model)

    def extract_action_key_value(self, text: str) -> Dict[str, Optional[str]]:
        """
        Extract the action, key, and value from a given natural language input using spaCy NLP features.

        :param text: The input string to process.
        :return: A dictionary containing 'action', 'key', and 'value'.
        """
        doc = self.nlp(text)

        action = None
        key = None
        value = None

        # Identify the action (verb) in the sentence
        for token in doc:
            if token.pos_ == "VERB":  # Look for the main verb
                action = token.lemma_  # Use the lemma (base form)
                break

        # Extract potential key-value pairs based on dependency parsing
        for token in doc:
            # Look for "key" or synonyms in the text
            if token.text.lower() in {"key", "identifier", "field"}:
                if token.nbor(1).text:  # Check the token to the right
                    key = token.nbor(1).text.strip("'\"")  # Handle quoted strings

            # Look for "value" or synonyms in the text
            elif token.text.lower() in {"value", "data", "entry"}:
                if token.nbor(1).text:  # Check the token to the right
                    value = token.nbor(1).text.strip("'\"")  # Handle quoted strings

        # Fallback to entity recognition for additional hints
        if not key or not value:
            for ent in doc.ents:
                if key is None and ent.label_ in {"PRODUCT", "ORG"}:
                    key = ent.text
                elif value is None and ent.label_ in {"PERSON", "QUANTITY", "GPE"}:
                    value = ent.text

        return {"action": action, "key": key, "value": value}
