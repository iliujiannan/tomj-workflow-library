import unittest
from unittest.mock import MagicMock

from dify_plugin import DifyPluginEnv
from dify_plugin.core.plugin_registration import PluginRegistration
from dify_plugin.entities.tool import ToolRuntime

from library import export_workflow
from tools.workflow_library import WorkflowLibraryTool


class SdkTests(unittest.TestCase):
    def setUp(self):
        self.tool = WorkflowLibraryTool(
            runtime=ToolRuntime(credentials={}, user_id='local-test', session_id='local-test'),
            session=MagicMock(),
        )

    def test_manifest_provider_and_tool_load(self):
        self.assertEqual(len(PluginRegistration(DifyPluginEnv()).tools_configuration), 1)

    def test_list_read_export_messages(self):
        listed = list(self.tool._invoke({'action': 'list'}))
        self.assertEqual([m.type.value for m in listed], ['json', 'text'])
        for key in ['ES', 'CR', 'DC']:
            read = list(self.tool._invoke({'action': 'read', 'workflow': key, 'part': 1}))
            self.assertEqual(read[0].type.value, 'text')
            exported = list(self.tool._invoke({'action': 'export', 'workflow': key}))
            self.assertEqual(exported[0].type.value, 'blob')
            self.assertEqual(exported[0].meta['filename'], f'TomJ-{key}.yml')
            self.assertEqual(exported[0].message.blob, export_workflow(key)[1])

    def test_unknown_action_is_reported(self):
        with self.assertRaises(ValueError):
            list(self.tool._invoke({'action': 'unknown'}))
