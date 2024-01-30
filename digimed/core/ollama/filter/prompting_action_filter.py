from typing import TYPE_CHECKING
from digitalpy.core.iam.IAM_action_filter_strategy import IAMActionFilterStrategy

from digimed.core.ollama.configuration.ollama_permissions import OllamaPermissions

if TYPE_CHECKING:
    from digitalpy.core.IAM.persistence.user import User
    from digitalpy.core.zmanager.request import Request


class PromptingFilter(IAMActionFilterStrategy):
    """This class is used to filter the requests for executing prompts."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def apply_filter(self, request: 'Request', user: 'User', action_key: 'str') -> bool:
        """This function is used to filter the request based on the identity of the user."""
        if action_key != "ollama_prompt":
            return True
        else:
            return self._user_has_permission(user, OllamaPermissions.PROMPT.value)
