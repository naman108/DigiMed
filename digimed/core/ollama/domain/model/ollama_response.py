"""This module contains the OllamaResponse class."""
from digitalpy.core.domain.node import Node

# TODO: fix this pylint error
class OllamaResponse(Node):  # pylint: disable=abstract-method
    """This class is used to represent the response from the Ollama api."""

    def __init__(self, model_configuration, model, oid=None, node_type="ollama_response") -> None:
        super().__init__(node_type, model_configuration=model_configuration, model=model, oid=oid)  # type: ignore
        self._text: str = ""

    @property
    def text(self) -> str:
        """get the text

        Returns:
            str: the text
        """
        return self._text

    @text.setter
    def text(self, text: str):
        """set the text

        Args:
            text (str): the text

        Raises:
            TypeError: if text is not a string
        """
        if not isinstance(text, str):
            raise TypeError("'text' must be a string")

        self._text = text

    def __str__(self) -> str:
        return f"OllamaResponse(text={self.text})"
