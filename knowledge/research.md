# 官方资料与源码研究

核查日期：2026-10-23（北京时间）。本次完成官方网页阅读、五个仓库的浅克隆与静态代码核对；未运行四个 Agent 项目，也未复现 DGM 实验。源码证据固定到实际提交，文档只记录核查日，不能保证此后页面不变。

## 研究范围与顺序

先用产品文档确认概念，再用源码定位职责。源码读的是局部实现，不由 README 营销语推断内部机制。场景设计与评测阈值属于本次归纳。

## 仓库快照

- openai/codex：`8531184b49bcb160175a84e140b659a83a426df7`
- deepseek-ai/deepseek-harness：`687f282e8625c6b8d11ff58211a90524be2e4317`
- langchain-ai/langgraph：`9d68e5b3eb1a63027b05e9f0152149ea0284dcdb`
- OpenHands/software-agent-sdk：`60192ed54db73ac658ac1a07462916126c32d3a0`
- jennyzzt/dgm：`a565fd2d1dca504ef5104a7cc0f3bdc4ab9b4fd2`

## 逐项证据

### S01｜Codex as a platform

- 官方链接：https://developers.openai.com/blog/codex-as-a-platform
- 核查：2026-10-23；版本：2026-08-19；定位：The reusable part is the agent loop
- 支持什么：开源 Harness 管理运行边界并可嵌入应用。
- 不支持什么：模型权重或托管服务随 Harness 开源。
- 本例：应用用 app-server 承接进度与审批。
- 置信范围：high for cited scope; no runtime capability test

### S02｜Unlocking the Codex harness

- 官方链接：https://openai.com/index/unlocking-the-codex-harness/
- 核查：2026-10-23；版本：2026-02-04；定位：Inside the Codex harness; conversation primitives
- 支持什么：Codex core 包含循环；App Server 暴露双向 JSON-RPC 与线程生命周期。
- 不支持什么：所有客户端与当前版本部署细节完全一致。
- 本例：审批请求可暂停 turn 等待客户端。
- 置信范围：high for cited scope; no runtime capability test

### S03｜DeepSeek Harness 官网

- 官方链接：https://deepseek.com/harness/
- 核查：2026-10-23；版本：unversioned web page；定位：预览版; 一切皆插件
- 支持什么：页面标注预览版，链接官方仓库；强调插件组合。
- 不支持什么：营销演示证明任意任务可靠或性能领先。
- 本例：官网的 PPT 任务仅作产品演示。
- 置信范围：high for cited scope; no runtime capability test

### S04｜DSH architecture

- 官方链接：https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/docs/architecture.md#L1
- 核查：2026-10-23；版本：687f282e8625c6b8d11ff58211a90524be2e4317；定位：[(1, 42), (74, 145)]
- 支持什么：Cordis 以服务、事件与可撤销 effects 组合插件；profile 叠加 bundle/patch。
- 不支持什么：每种插件组合均兼容或无需回归。
- 本例：更换工具执行 provider 仍须检查日志与策略。
- 置信范围：high: static code reading only

### S05｜LangGraph Persistence

- 官方链接：https://docs.langchain.com/oss/python/langgraph/persistence
- 核查：2026-10-23；版本：unversioned web page；定位：Checkpointer vs. store; MemorySaver does not persist between restarts
- 支持什么：checkpointer 面向 thread，Store 面向跨 thread；内存 saver 重启会丢失。
- 不支持什么：默认 InMemorySaver 可断电恢复，或自动撤回外部动作。
- 本例：PPT 任务恢复需配置持久后端。
- 置信范围：high for cited scope; no runtime capability test

### S06｜Effective context engineering

- 官方链接：https://www.anthropic.com/research/effective-context-engineering-for-ai-agents
- 核查：2026-10-23；版本：2025-09-29；定位：Context engineering vs. prompt engineering; Long-horizon tasks
- 支持什么：按任务维护有限上下文；压缩与外部笔记可支持长任务。
- 不支持什么：摘要无损或所有任务都应多 Agent。
- 本例：保留未解决问题与证据路径。
- 置信范围：high for cited scope; no runtime capability test

### S07｜OpenHands SDK architecture

- 官方链接：https://docs.openhands.dev/sdk/arch/overview
- 核查：2026-10-23；版本：unversioned web page；定位：Four-Package Architecture; Two Deployment Modes
- 支持什么：SDK、工具、workspace、agent-server 分包；支持本地与远程执行。
- 不支持什么：LocalWorkspace 默认隔离宿主机，或所有 tools 通过 workspace RPC 执行。
- 本例：切换 workspace 部署形态要同时检查隔离策略。
- 置信范围：high for cited scope; no runtime capability test

### S08｜Darwin Gödel Machine paper

- 官方链接：https://arxiv.org/abs/2505.22954v3
- 核查：2026-10-23；版本：v3, 2026-03-12; v1 2025-05-29；定位：Abstract; submission history
- 支持什么：论文以编码基准经验验证自修改，并保留候选 Agent 档案。
- 不支持什么：证明所有修改有益，或通用无限 RSI 已实现。
- 本例：只在已定义任务和评测范围解读改进。
- 置信范围：high for cited scope; no runtime capability test

### S09｜Build skills

- 官方链接：https://learn.chatgpt.com/docs/build-skills
- 核查：2026-10-23；版本：unversioned web page；定位：How ChatGPT and Codex use skills; Where Codex loads local skills
- 支持什么：Skill 目录含 SKILL.md，可附脚本与资料，按需读取。
- 不支持什么：读取 Skill 即保证遵循或产物正确。
- 本例：本项目 ai-tech-talk 规定研究与构建流程。
- 置信范围：high for cited scope; no runtime capability test

### S10｜Codex run_turn

- 官方链接：https://github.com/openai/codex/blob/8531184b49bcb160175a84e140b659a83a426df7/codex-rs/core/src/session/turn.rs#L158
- 核查：2026-10-23；版本：8531184b49bcb160175a84e140b659a83a426df7；定位：[(158, 195), (570, 640), (730, 750)]
- 支持什么：run_turn 处理模型输出、工具反馈和是否继续，并考虑待处理输入。
- 不支持什么：只有一个无限 while 就涵盖完整 Codex；本次代码已运行。
- 本例：工具报错后下一轮可读取结果再行动。
- 置信范围：high: static code reading only

### S11｜Codex ToolOrchestrator

- 官方链接：https://github.com/openai/codex/blob/8531184b49bcb160175a84e140b659a83a426df7/codex-rs/core/src/tools/orchestrator.rs#L1
- 核查：2026-10-23；版本：8531184b49bcb160175a84e140b659a83a426df7；定位：[(1, 4), (130, 180), (280, 305)]
- 支持什么：工具编排协调审批、沙箱选择及拒绝后重试。
- 不支持什么：沙箱保证内容正确，或所有动作都会弹窗。
- 本例：文件可写权限与事实可信度是两种检查。
- 置信范围：high: static code reading only

### S12｜LangGraph StateGraph.compile

- 官方链接：https://github.com/langchain-ai/langgraph/blob/9d68e5b3eb1a63027b05e9f0152149ea0284dcdb/libs/langgraph/langgraph/graph/state.py#L131
- 核查：2026-10-23；版本：9d68e5b3eb1a63027b05e9f0152149ea0284dcdb；定位：[(131, 157), (1177, 1214), (1355, 1365)]
- 支持什么：图编译可独立接受 checkpointer 与 store。
- 不支持什么：LangGraph 本身等同具体编码 Agent 产品。
- 本例：研究→核查节点共享 typed state。
- 置信范围：high: static code reading only

### S13｜LangGraph BaseCheckpointSaver

- 官方链接：https://github.com/langchain-ai/langgraph/blob/9d68e5b3eb1a63027b05e9f0152149ea0284dcdb/libs/checkpoint/langgraph/checkpoint/base/__init__.py#L93
- 核查：2026-10-23；版本：9d68e5b3eb1a63027b05e9f0152149ea0284dcdb；定位：[(93, 130), (199, 230)]
- 支持什么：Checkpoint 保存通道值和版本；以 thread_id 检索线程状态。
- 不支持什么：checkpoint 是可执行进程内存快照，或恢复撤销外部副作用。
- 本例：记录已确认 claims 与待完成节点。
- 置信范围：high: static code reading only

### S14｜OpenHands Agent.step

- 官方链接：https://github.com/OpenHands/software-agent-sdk/blob/60192ed54db73ac658ac1a07462916126c32d3a0/openhands-sdk/openhands/sdk/agent/agent.py#L690
- 核查：2026-10-23；版本：60192ed54db73ac658ac1a07462916126c32d3a0；定位：[(690, 757)]
- 支持什么：step 先处理待确认行动，再从会话视图组装消息并处理 condensation。
- 不支持什么：Agent 对象本身保存所有状态，或压缩等同长期记忆。
- 本例：长任务先整理会话视图，再继续调用模型。
- 置信范围：high: static code reading only

### S15｜DGM authors README

- 官方链接：https://github.com/jennyzzt/dgm/blob/a565fd2d1dca504ef5104a7cc0f3bdc4ab9b4fd2/README.md#L20
- 核查：2026-10-23；版本：a565fd2d1dca504ef5104a7cc0f3bdc4ab9b4fd2；定位：[(20, 32), (75, 104)]
- 支持什么：作者将系统描述为代码自修改加编码基准验证。
- 不支持什么：已在本次环境复现论文结果。
- 本例：研究讨论保留设计而不复述成绩排名。
- 置信范围：high: static code reading only

### S16｜DSH AgentLoop service

- 官方链接：https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/core/agent-loop/src/index.ts#L338
- 核查：2026-10-23；版本：687f282e8625c6b8d11ff58211a90524be2e4317；定位：[(338, 365)]
- 支持什么：AgentLoop 是 Cordis Service，注入 agents/sessions/llm/tools/systemPrompt 等依赖。
- 不支持什么：一切皆插件就等于安全热替换已验证。
- 本例：组合不同工具或模型适配，不改业务 UI。
- 置信范围：high: static code reading only

### S17｜OpenHands Conversation factory

- 官方链接：https://github.com/OpenHands/software-agent-sdk/blob/60192ed54db73ac658ac1a07462916126c32d3a0/openhands-sdk/openhands/sdk/conversation/conversation.py#L34
- 核查：2026-10-23；版本：60192ed54db73ac658ac1a07462916126c32d3a0；定位：[(34, 58), (153, 165), (190, 235)]
- 支持什么：Conversation 按 workspace 类型返回本地或远程会话。
- 不支持什么：远程工具经本地 workspace 代理；本地自动沙箱。
- 本例：在服务器容器内执行渲染工具。
- 置信范围：high: static code reading only

### S18｜LangGraph BaseStore

- 官方链接：https://github.com/langchain-ai/langgraph/blob/9d68e5b3eb1a63027b05e9f0152149ea0284dcdb/libs/checkpoint/langgraph/store/base/__init__.py#L1
- 核查：2026-10-23；版本：9d68e5b3eb1a63027b05e9f0152149ea0284dcdb；定位：[(1, 12), (708, 736)]
- 支持什么：跨线程 key-value Store 使用 namespace；语义搜索与 TTL 依实现和配置。
- 不支持什么：Store 自动选择值得记住的信息、自动纠错或默认有向量搜索。
- 本例：namespace=(alumni,style)，保留演讲偏好。
- 置信范围：high: static code reading only

### S19｜DSH ReactLoopAgent

- 官方链接：https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/core/agent-loop/src/agent.ts#L260
- 核查：2026-10-23；版本：687f282e8625c6b8d11ff58211a90524be2e4317；定位：[(260, 313), (675, 703)]
- 支持什么：预步骤扩展点与 session 日志投影参与循环。
- 不支持什么：日志有记录就证明推理或事实正确。
- 本例：审查模型可见历史来自哪些事件。
- 置信范围：high: static code reading only

### S20｜DGM outer loop

- 官方链接：https://github.com/jennyzzt/dgm/blob/a565fd2d1dca504ef5104a7cc0f3bdc4ab9b4fd2/DGM_outer.py#L146
- 核查：2026-10-23；版本：a565fd2d1dca504ef5104a7cc0f3bdc4ab9b4fd2；定位：[(146, 190), (270, 300), (315, 332)]
- 支持什么：选择父 Agent、产生自修改尝试并更新档案；默认可 keep_all。
- 不支持什么：只保留本代分数最高者或每一步必须严格变好。
- 本例：失败或中等候选也可能成为后续探索起点。
- 置信范围：high: static code reading only

### S21｜DSH guarded tools

- 官方链接：https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/core/tools/src/index.ts#L725
- 核查：2026-10-23；版本：687f282e8625c6b8d11ff58211a90524be2e4317；定位：[(725, 739), (1500, 1537)]
- 支持什么：扩展 pre-execute 流水线后还有执行 guard。
- 不支持什么：随便挂插件就应绕过权限边界。
- 本例：新增网页检索工具同时测试政策和记录。
- 置信范围：high: static code reading only

### S22｜Building effective agents

- 官方链接：https://www.anthropic.com/research/building-effective-agents
- 核查：2026-10-23；版本：2024-12-19; page notes tooling has evolved；定位：What are agents?
- 支持什么：以预定代码路径与模型动态决策区分 workflow/agent；术语存在差异。
- 不支持什么：这是所有项目统一采用的定义。
- 本例：固定构建脚本嵌在 Agent 流程中。
- 置信范围：high for cited scope; no runtime capability test

## 已纠正的 starter 问题

1. 来源种子不视为已核实；原清单保留为 sources/starter_seed_sources.json。
2. Codex 旧的 core/src/codex.rs 路径未找到；当前源码循环位于 core/src/session/turn.rs。
3. 官网 DSH 状态仅采用页面“预览版”，不虚构稳定版承诺。
4. State 改称“任务记录”，避免把数据库内容误说成必然为真。
5. 明确 InMemorySaver 重启会丢失；Store 的语义搜索和 TTL 不是默认自动能力。
6. DGM 的候选档案不是只留冠军；没有复现基准或引用排名。

## 未核实与限制

- 不保证本次静态阅读覆盖所有功能分支、平台与版本。没有运行 Codex/DSH/LangGraph/OpenHands 的集成测试。
- 未复现 DGM 实验，未核实所有论文章节及 benchmark 配置；只采用摘要和作者代码能支持的机制。
- 网页可能随时间更新；版本化结论以固定 commit 源码为准。
- 本案例中的候选评测任务与阈值是设计建议，不是已完成的 A/B 研究。
- 未做现场 PowerPoint / Keynote 的跨软件目检；LibreOffice 渲染只覆盖当前环境。
