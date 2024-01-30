"""This module contains the HelloMessageBuilder class for building hello messages instances"""
from digitalpy.core.domain.builder import Builder
from ...configuration.ollama_constants import OLLAMA_RESPONSE
from ..model.ollama_response import OllamaResponse


class OllamaResponseBuilder(Builder):
    """Builds a hello message object"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result: OllamaResponse = None  # type: ignore

    def build_empty_object(self, config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """Builds a HelloMessage object"""
        self.request.set_value("object_class_name", "OllamaResponse")

        configuration = config_loader.find_configuration(OLLAMA_RESPONSE)

        self.result = super()._create_model_object(
            configuration, extended_domain={"OllamaResponse": OllamaResponse})

    def add_object_data(self, mapped_object: dict):
        """adds the data from the mapped object to the HelloMessage object """
        self.result.text = mapped_object.get("text")

    def get_result(self):
        """gets the result of the builder"""
        return self.result
