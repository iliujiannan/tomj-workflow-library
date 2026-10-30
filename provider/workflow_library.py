from typing import Any
from dify_plugin import ToolProvider


class WorkflowLibraryProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        """This plugin reads bundled files and requires no credentials."""
