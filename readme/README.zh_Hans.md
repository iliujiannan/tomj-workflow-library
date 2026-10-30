# TomJ 工作流资料库

内置三份 Dify YAML 参考文件：TomJ-ES 节能编排、TomJ-CR 客诉分流、TomJ-DC 五表清洗。

## 安装和使用

1. 从 Dify Marketplace 安装审核通过的插件；上架前可在允许安装本地包的 Dify 工作区验证 `.difypkg`。
2. 在工作流或 Agent 中添加 **Workflow Reference / 工作流参考文件** 工具，无需 API Key 或其他凭据。
3. `action=list` 查看目录；`action=read` 选择 ES/CR/DC 和片号；`action=export` 返回完整 YML 文件。
4. read 输出以 PART_END 标记结束。按顺序拼接 BEGIN_ORIGINAL 与 END_ORIGINAL 之间的正文可精确还原源文件。
5. 若需运行导出的流程，需要单独导入 YML、安装其中声明的插件并配置模型账号。

## 范围和隐私

插件只读取固定内置资源，不执行工作流或其中的 Python 代码，不接收任意文件路径、不联网、不收集个人数据。工具输出会进入调用它的 Dify 对话或工作流，后续如何交给模型由该工作区决定。

本插件不会直接连接网页版 DeepSeek，也不会自动把资料变成其永久记忆。插件是否允许安装或导出，取决于工作区策略；市场上架也不改变使用场景的资料访问规则。

原工作流说明和代码以中文为主。插件本身及主 README 使用英文，并提供中文翻译。参考文件结构针对所附样例流程，不是任意 CSV 的通用处理器。
