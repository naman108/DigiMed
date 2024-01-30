"""This file contains the HelloController class. This class is used to say hello to the world.
It performs simple operations based on input data and sends a response back to the service."""
from typing import TYPE_CHECKING

import requests
from digimed.core.ollama.domain.builder.ollama_response_builder import OllamaResponseBuilder
from digitalpy.core.main.controller import Controller

if TYPE_CHECKING:
    from digitalpy.core.digipy_configuration.configuration import Configuration
    from digitalpy.core.zmanager.impl.default_action_mapper import DefaultActionMapper
    from digitalpy.core.zmanager.request import Request
    from digitalpy.core.zmanager.response import Response
    from digitalpy.core.domain.domain.network_client import NetworkClient


class OllamaRequestController(Controller):
    """LLMRequest is a DigitalPyController that is used to make requests. 
    By adding logic to the hello service"""

    def __init__(self, request: 'Request',
                 response: 'Response',
                 sync_action_mapper: 'DefaultActionMapper',
                 configuration: 'Configuration'):
        super().__init__(request, response, sync_action_mapper, configuration)
        self.ollama_response_builder = OllamaResponseBuilder(request, response, sync_action_mapper, configuration)

    def initialize(self, request: 'Request', response: 'Response'):
        """This function is used to initialize the controller. 
        It is intiated by the service manager."""
        self.ollama_response_builder.initialize(request, response)
        return super().initialize(request, response)

    def ollama_prompt(self, client: 'NetworkClient', data: bytes, model: str, config_loader, *args, **kwargs):  # pylint: disable=unused-argument
        """this function will send the prompt to the Ollama api and return the response."""

        # submit the request to the Ollama api
        """
        response = requests.post(
            self.configuration.get_value("OllamaApiUrl", "Ollama")+"/api/generate",
            json={"prompt": str(data), "model": model, "stream": False, "format": "json"},
            headers={"Content-Type": "text/plain"},
        )
        response_data = response.json()
        """
        response_data = {"text": "Hello World!"}

        self.ollama_response_builder.build_empty_object(config_loader)
        self.ollama_response_builder.add_object_data(response_data)
        ollama_response = self.ollama_response_builder.get_result()

        # list type as only lists are supported for this parameter
        self.response.set_value("message", [ollama_response])
        self.response.set_value("recipients", [str(client.get_oid())])
        self.response.set_action("publish")
