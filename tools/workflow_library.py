from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from library import catalog, export_workflow, read_part


class WorkflowLibraryTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        action = tool_parameters.get('action', 'list')
        workflow = tool_parameters.get('workflow', 'ES')
        if action == 'list':
            yield self.create_json_message({'workflows': catalog()})
            yield self.create_text_message(
                '\n'.join(f"{x['name']}: {x['description']}; {x['parts']} parts; {x['bytes']} bytes"
                          for x in catalog()))
        elif action == 'read':
            yield self.create_text_message(read_part(workflow, tool_parameters.get('part', 1)))
        elif action == 'export':
            filename, blob = export_workflow(workflow)
            yield self.create_blob_message(blob=blob, meta={'mime_type': 'application/x-yaml', 'filename': filename})
            yield self.create_text_message(f'Exported {filename}. This reference YAML is not executed by the plugin.')
        else:
            raise ValueError('Choose action list, read, or export.')
