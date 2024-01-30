"""This module contains the HelloWorld class, which is a DefaultFacade that is used 
to say hello to the world."""
from typing import TYPE_CHECKING
from datetime import datetime as dt
import uuid
from digimed.core.ollama.configuration.ollama_permissions import OllamaPermissions
from digitalpy.core.component_management.impl.default_facade import DefaultFacade
from digitalpy.core.digipy_configuration.impl.inifile_configuration import InifileConfiguration
from digitalpy.core.zmanager.impl.async_action_mapper import AsyncActionMapper
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.IAM.configuration.iam_constants import AUTHENTICATED_USERS
from digitalpy.core.IAM.persistence.permissions import Permissions as IAMPermission
from digitalpy.core.IAM.persistence.system_group_permission import SystemGroupPermission
from .controller.ollama_request_controller import OllamaRequestController

from .configuration.ollama_constants import (
    ACTION_MAPPING_PATH,
    LOGGING_CONFIGURATION_PATH,
    INTERNAL_ACTION_MAPPING_PATH,
    MANIFEST_PATH,
    CONFIGURATION_PATH_TEMPLATE,
    LOG_FILE_PATH
)

from . import base

if TYPE_CHECKING:
    from digitalpy.core.iam.IAM_facade import IAM
    from digitalpy.core.IAM.persistence.system_group import SystemGroup


class Ollama(DefaultFacade):
    """HelloComponent is a DefaultFacade that is used to say hello to the world. 
    It is a simple example of a DefaultFacade.
    """

    def __init__(self, sync_action_mapper, request: Request,
                 response: Response, configuration,
                 action_mapper: AsyncActionMapper = None,  # type: ignore
                 tracing_provider_instance=None):  # type: ignore
        super().__init__(
            # the path to the external action mapping
            action_mapping_path=str(ACTION_MAPPING_PATH),
            # the path to the internal action mapping
            internal_action_mapping_path=str(INTERNAL_ACTION_MAPPING_PATH),
            # the path to the logger configuration
            logger_configuration=str(LOGGING_CONFIGURATION_PATH),
            # the package containing the base classes
            base=base,  # type: ignore
            # the general action mapper (passed by constructor)
            action_mapper=sync_action_mapper,
            # the request object (passed by constructor)
            request=request,
            # the response object (passed by constructor)
            response=response,
            # the configuration object (passed by constructor)
            configuration=configuration,
            # log file path
            log_file_path=LOG_FILE_PATH,
            # the tracing provider used
            tracing_provider_instance=tracing_provider_instance,
            # the template for the absolute path to the model object definitions
            configuration_path_template=CONFIGURATION_PATH_TEMPLATE,
            # the path to the manifest file
            manifest_path=str(MANIFEST_PATH),
        )
        self.ollama_request_controller = OllamaRequestController(
            request, response, action_mapper, configuration)

    def initialize(self, request, response):
        self.ollama_request_controller.initialize(request, response)
        return super().initialize(request, response)

    def register(self, config: InifileConfiguration, **kwargs):
        iam: IAM = ObjectFactory.get_instance("IAM")
        authed_users: 'SystemGroup' = iam.get_group_by_name(AUTHENTICATED_USERS)
        if authed_users is None:
            raise ValueError("Authenticated users group not found")
        for perm in authed_users.system_group_permissions:
            if perm.permissions.PermissionID == OllamaPermissions.PROMPT.value:
                return super().register(config, **kwargs)

        permission = IAMPermission(
            PermissionID=OllamaPermissions.PROMPT.value,
            PermissionName=OllamaPermissions.PROMPT.name,
            PermissionDescription="Permission to prompt the Ollama API",
            ResourceType="",
            CreateDate=str(dt.now()),
            LastModifiedDate=str(dt.now()),
            IsActive=True
        )

        system_group_permission = SystemGroupPermission(
            permissions=permission,
            system_groups=authed_users,
            uid=str(uuid.uuid4())
        )
        iam.create_group_permission(group_permission=system_group_permission)
        return super().register(config, **kwargs)

    def execute(self, method=None):
        try:
            if hasattr(self, method):  # type: ignore
                print("executing method "+str(method))  # type: ignore
                getattr(self, method)(**self.request.get_values())  # type: ignore
            else:
                self.request.set_value("logger", self.logger)
                self.request.set_value("config_loader", self.config_loader)
                self.request.set_value("tracer", self.tracer)
                response = self.execute_sub_action(self.request.get_action())
                self.response.set_values(response.get_values())
        except Exception as e:
            self.logger.fatal(str(e))

    @DefaultFacade.public
    def ollama_prompt(self, *args, **kwargs):
        """This method is used to receive messages sent by client.
        """
        self.ollama_request_controller.ollama_prompt(*args, **kwargs)
