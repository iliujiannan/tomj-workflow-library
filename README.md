# TomJ Workflow Library

An offline Dify tool for inspecting and exporting three bundled YAML workflow references. It provides an indexed catalog, small lossless text parts for model context, and complete YAML file downloads without external hosting.

## Bundled references

| ID | File | Purpose |
|---|---|---|
| ES | TomJ-ES.yml | Base-station energy scheduling, risk checks, charts, and reporting |
| CR | TomJ-CR.yml | Complaint classification, routing recommendations, and reports |
| DC | TomJ-DC.yml | Five-table data cleaning and file export |

The reference workflows are domain-specific examples, not a parser for arbitrary CSV schemas. Their prompts, node names, and code comments are primarily in Simplified Chinese. The plugin interface and this README are in English; Chinese documentation is in `readme/README.zh_Hans.md`.

## Setup

1. Install the reviewed plugin from Dify Marketplace. Before publication, use a workspace that permits local plugin installation to test the `.difypkg` package.
2. Add **TomJ Workflow Library / Workflow Reference** to a Workflow or Agent.
3. No API key, account credential, external API, network connection, database, or user-uploaded file is required for the plugin itself.

Runtime: Python 3.12 and `dify-plugin==0.9.0`.

## Usage

| action | workflow | part | Output |
|---|---|---|---|
| list | ignored | ignored | JSON catalog and a short text summary |
| read | ES, CR, or DC | positive integer, starting at 1 | One small text part with a final PART_END marker |
| export | ES, CR, or DC | ignored | Complete `.yml` file in the tool's files output |

Use list to find the number of parts before reading. Concatenate only the content between BEGIN_ORIGINAL and END_ORIGINAL in numeric order to restore the exact YAML. A part may split a long line, code block, or node and cannot be imported on its own.

For file downloads from a Workflow, bind the tool's files output to an End-node output of type `array[file]`. To use a text part as model context, bind the tool's text output to a downstream LLM input. The plugin does not directly attach context to a separate chat website.

## Execution and security boundary

Only three fixed package-owned resources can be read. The plugin does not accept file paths or URLs, read arbitrary user/workspace files, write files at runtime, fetch external URLs, start subprocesses, run SQL, or execute Python/YAML supplied by users. It never executes or automatically imports the bundled workflows. The SDK returns file bytes to Dify; it does not upload them to a third-party service.

Executing an exported workflow after import is a separate operation. Those workflows declare model, chart, and Markdown-export dependencies; users must install those plugins and configure credentials separately. They are not bundled or invoked by this library. Workspace policies and permitted-use rules still apply.

## Privacy

No user data is collected, persisted, logged by plugin code, or sent to external services. Tool output is returned to the invoking Dify workspace; downstream model processing follows that workspace's settings. See [PRIVACY.md](PRIVACY.md).

## Source and support

Source repository: https://github.com/iliujiannan/tomj-workflow-library

Report issues: https://github.com/iliujiannan/tomj-workflow-library/issues

Contact: txy123yxt@protonmail.com

See CATALOG.json for the three resource hashes and CHANGELOG.md for version history. Local tests cover all three actions, package registration, invalid inputs, and lossless reconstruction. Actual Dify installation and interaction must be verified before submission; local unit tests do not replace that requirement.
