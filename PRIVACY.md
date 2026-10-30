# Privacy

This plugin reads three workflow YAML files bundled with its own package. It accepts only an action, a workflow ID and a part number. It makes no external network requests and does not collect, persist or send user files, credentials, personal data or analytics. Tool output is returned to the Dify workspace that invoked it; any downstream model processing follows that workspace's configuration.

The plugin does not execute the bundled workflows. Executing an exported workflow after import may invoke model or chart providers and is outside this plugin's runtime.
