# 逐页讲者备注

建议讲述约 43 分钟，另留 20 分钟讨论。每页正文约一分钟，余下时间用于看图、互动与停顿。

本场案例是本项目资料到 PPT 的制作；四个开源项目没有做同题性能实测。

## 01｜让 AI 交付成果，需要一整套系统

结论：从这份 PPT，聊 Agent、Harness 与持续改进

今天不从名词考试开始。我们把准备这场交流会的过程摆到台面上：AI 要查官方资料、读源码、解释概念、制作幻灯片，最后还要证明自己确实检查过。大家可以带着一个问题听：如果把你工作中的一项任务交给它，你最不放心哪一步？我会把能从官方材料核实的机制，与个人的架构归纳和研究设想分开说。先用这份 PPT 本身做案例，再看四个项目各自提供了什么。

过渡问题：一份能看的回答，离一份能交付的 PPT 还有多远？

证据类型：交流地图；claims：演讲组织 / 本场案例。

## 02｜交付一份 PPT，至少要走完六步

结论：同一个目标，需要多次行动、落盘和核验

假设委托只有一句话：帮我准备校友 AI 交流会。如果模型只返回一篇大纲，回答已经结束，工作却刚开始。资料要能追溯，讲解要适合初学者，PPT 要能编辑，最后还要打开看看。我们把它拆成六段，后面每个概念都回到其中一个具体环节。特别留意“检查”这一步：文件存在、能打开、事实有证据，是不同条件。这个任务由当前 Codex 会话完成，其他项目用于官方架构对照。

过渡问题：哪些步骤适合固定下来，哪些步骤需要模型临场判断？

证据类型：贯穿案例；claims：演讲组织 / 本场案例。

## 03｜固定流程与动态决策可以一起用

结论：LLM 生成内容；Workflow 固定路径；Agent 根据反馈选下一步

把三者看成可组合的做法。单次模型调用可以解释 Harness；固定脚本可以把 JSON 生成 PPT；Agent 则在发现文档链接失效后决定换到官方仓库。这里的差异是“下一步由谁选择”，不是谁听起来更高级。现实系统常把开放的研究步骤交给 Agent，把构建和校验交给确定性程序。如果步骤已经清楚，固定流程往往更容易观察和复现。

过渡问题：当模型开始调用工具后，循环是怎样闭合的？

证据类型：架构归纳；claims：C08。
- [S22 · Building effective agents](https://www.anthropic.com/research/building-effective-agents)；定位：What are agents?。
- [S10 · Codex run_turn](https://github.com/openai/codex/blob/8531184b49bcb160175a84e140b659a83a426df7/codex-rs/core/src/session/turn.rs#L158)；定位：[(158, 195), (570, 640), (730, 750)]。

## 04｜Agent Loop 把工具结果带回下一轮

结论：决策 → 行动 → 观察 → 再决策

我们请求查 DSH 的架构，模型提出读取文档，宿主执行读取，返回内容或报错。下一轮模型看到反馈，才决定是否继续读源码。这就是最小闭环。图里的“决策”是模型生成下一步建议；真正执行命令的是程序和工具，模型自己并没有文件系统权限。Codex 的 run_turn 明确处理工具反馈与继续条件；DSH 也有对应循环。停止条件同样重要：交付完成、预算耗尽或需要人工输入，都应该能退出。

过渡问题：既然能根据结果调整，为什么长任务仍会失败？

证据类型：源码事实 + 示意架构；claims：C01, C08。
- [S10 · Codex run_turn](https://github.com/openai/codex/blob/8531184b49bcb160175a84e140b659a83a426df7/codex-rs/core/src/session/turn.rs#L158)；定位：[(158, 195), (570, 640), (730, 750)]。
- [S19 · DSH ReactLoopAgent](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/core/agent-loop/src/agent.ts#L260)；定位：[(260, 313), (675, 703)]。

## 05｜能调用工具，还不足以可靠交付

结论：失败可能出在信息、执行、连续性和验收四处

想象四个小故障：搜索命中了过期教程，渲染工具没有安装，会话中断忘了哪条结论还没核实，最后构建成功但中文挤出文本框。这些都不是多写一句“请认真”就能完全解决的。需要分别补来源管理、执行环境、持久状态和验收机制。模型能力当然重要，但我们也能通过工程设计让失败更容易被发现和修复。今天我们实际遇到过缺少项目 Skill 与网络连接问题，这些属于环境前提，而不是事实真假。

过渡问题：这些补丁能不能组成一个可复用的运行底座？

证据类型：案例推演；claims：C13。

## 06｜Harness 承载循环，也管理运行边界

结论：模型提出行动；Harness 决定怎样执行和记录

可以把 Harness 理解为让智能体做事的运行底座。里面有循环，也有工具调用、权限、日志、上下文管理与状态；应用还可以在外面加验收与业务规则。这个词不是一个跨项目统一接口。我们只用它帮助定位责任：是模型建议错了，还是工具没有执行，还是结果没保存？图上把“事实核查”和“构建检查”放到应用验收层，是我们的设计建议，不能误称 Codex 会替所有任务自动做完。

过渡问题：在 Codex 里，哪些部分能找到具体代码？

证据类型：架构归纳；claims：C01, C08。
- [S02 · Unlocking the Codex harness](https://openai.com/index/unlocking-the-codex-harness/)；定位：Inside the Codex harness; conversation primitives。
- [S11 · Codex ToolOrchestrator](https://github.com/openai/codex/blob/8531184b49bcb160175a84e140b659a83a426df7/codex-rs/core/src/tools/orchestrator.rs#L1)；定位：[(1, 4), (130, 180), (280, 305)]。
- [S04 · DSH architecture](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/docs/architecture.md#L1)；定位：[(1, 42), (74, 145)]。

## 07｜Codex 把循环、工具策略和会话接在一起

结论：从 run_turn 到 ToolOrchestrator，再把反馈写回会话

对应到本次任务，模型决定读取文件，run_turn 驱动一次次请求，工具编排层处理执行政策，再把返回值送回后续上下文。源码的 run_turn 在当前提交已经移到 session/turn.rs，直接照搬旧路径会找不到。ToolOrchestrator 的职责注释写着审批、沙箱选择和拒绝后的重试。App Server 让客户端围绕 thread、turn 和 item 呈现工作进度。这里的持久会话不是长期知识库，也不代表所有外部动作都可回滚。

过渡问题：Skill、MCP 和 Tool 分别放在哪里？

证据类型：CODEX / 运行控制；claims：C01。
- [S10 · Codex run_turn](https://github.com/openai/codex/blob/8531184b49bcb160175a84e140b659a83a426df7/codex-rs/core/src/session/turn.rs#L158)；定位：[(158, 195), (570, 640), (730, 750)]。
- [S11 · Codex ToolOrchestrator](https://github.com/openai/codex/blob/8531184b49bcb160175a84e140b659a83a426df7/codex-rs/core/src/tools/orchestrator.rs#L1)；定位：[(1, 4), (130, 180), (280, 305)]。
- [S02 · Unlocking the Codex harness](https://openai.com/index/unlocking-the-codex-harness/)；定位：Inside the Codex harness; conversation primitives。

## 08｜Tool、MCP、Skill 各自补上不同的一环

结论：Tool 提供动作；MCP 连接能力；Skill 组织做事方法

举三个具体例子：读取一个文件是 Tool；通过 MCP 暴露的仓库连接，让 Agent 能访问外部能力；ai-tech-talk Skill 则告诉它先核来源、再写知识资料、再生成和检查 PPT。Skill 可以附脚本，但文字指令并不是硬性执行器；因此仍需检查代码和产物。MCP 服务不一定只提供工具，也可能提供资源等能力。三者不是竞争关系，一项任务可以同时用到它们。我们这次确实读取了项目 Skill，并在它的基础上重写内容和生成器。

过渡问题：如果要让模型、循环甚至会话都能替换，会怎样组织？

证据类型：架构归纳；claims：C06, C07。
- [S09 · Build skills](https://learn.chatgpt.com/docs/build-skills)；定位：How ChatGPT and Codex use skills; Where Codex loads local skills。
- [S02 · Unlocking the Codex harness](https://openai.com/index/unlocking-the-codex-harness/)；定位：Inside the Codex harness; conversation primitives。
- [S21 · DSH guarded tools](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/core/tools/src/index.ts#L725)；定位：[(725, 739), (1500, 1537)]。

## 09｜DSH 用 Cordis 把运行能力组合成插件树

结论：模型适配、工具、会话与 Agent Loop 都有替换接缝

DeepSeek Harness 不是 DeepSeek 模型的另一种称呼。官方架构把 Cordis 作为插件基础，插件贡献服务、事件与可撤销的注册效果。AgentLoop 在代码里也是 Service，依赖 sessions、llm、tools 等服务。profile 通过有顺序的 bundle 与 patch 组成运行树。对于 PPT 案例，可以想象替换资料检索或渲染能力，而不是复制一套界面。可替换带来灵活性，也需要接口、生命周期和权限回归；这里没有测量组合后的性能。

过渡问题：替换能力之外，任务中断时怎样接着做？

证据类型：DSH / 插件组合；claims：C02。
- [S03 · DeepSeek Harness 官网](https://deepseek.com/harness/)；定位：预览版; 一切皆插件。
- [S04 · DSH architecture](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/docs/architecture.md#L1)；定位：[(1, 42), (74, 145)]。
- [S16 · DSH AgentLoop service](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/core/agent-loop/src/index.ts#L338)；定位：[(338, 365)]。
- [S19 · DSH ReactLoopAgent](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/core/agent-loop/src/agent.ts#L260)；定位：[(260, 313), (675, 703)]。
- [S21 · DSH guarded tools](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/core/tools/src/index.ts#L725)；定位：[(725, 739), (1500, 1537)]。

## 10｜LangGraph 把恢复建立在线程状态之上

结论：Graph State → Checkpoint → 同一 thread 继续

假设核查已经完成，PPT 还没渲染。我们把已核结论、文件位置、待办和下一个节点放在图状态中，由 checkpointer 保存。恢复时用同一 thread_id 找回对应进度。Store 是另一条线，保存跨任务复用的信息，例如这类交流会喜欢先讲案例。源码 compile 同时接受两者。注意恢复的是保存的状态和执行进度，不是冻结整个操作系统；外部发邮件、重复计费或覆盖文件，仍需应用处理幂等和边界。

过渡问题：有了图状态，执行工具的工作区又在哪里？

证据类型：LANGGRAPH / 持久状态；claims：C03, C11。
- [S05 · LangGraph Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)；定位：Checkpointer vs. store; MemorySaver does not persist between restarts。
- [S12 · LangGraph StateGraph.compile](https://github.com/langchain-ai/langgraph/blob/9d68e5b3eb1a63027b05e9f0152149ea0284dcdb/libs/langgraph/langgraph/graph/state.py#L131)；定位：[(131, 157), (1177, 1214), (1355, 1365)]。
- [S13 · LangGraph BaseCheckpointSaver](https://github.com/langchain-ai/langgraph/blob/9d68e5b3eb1a63027b05e9f0152149ea0284dcdb/libs/checkpoint/langgraph/checkpoint/base/__init__.py#L93)；定位：[(93, 130), (199, 230)]。
- [S18 · LangGraph BaseStore](https://github.com/langchain-ai/langgraph/blob/9d68e5b3eb1a63027b05e9f0152149ea0284dcdb/libs/checkpoint/langgraph/store/base/__init__.py#L1)；定位：[(1, 12), (708, 736)]。

## 11｜OpenHands 把 Agent 行为与执行部署分开

结论：Conversation 选择本地或远程；工具在选定环境运行

OpenHands Software Agent SDK 有 Agent、Conversation、Tool 和 Workspace 等组件。Conversation 工厂检查 workspace 类型，返回本地或远程实现；Agent.step 从会话视图组装输入，也处理压缩事件。用在 PPT 案例里，本地原型可以直接调用渲染工具，而远程部署可以让 Agent Server 在容器工作区内执行同一类工作。不能把“用了 workspace”就等同有沙箱，也不要把 UI 产品和 SDK 当成同一个仓库。我们读了源码，但没有部署这个 SDK。

过渡问题：四个项目放在一起，究竟该比较什么？

证据类型：OPENHANDS / 执行部署；claims：C04, C05。
- [S07 · OpenHands SDK architecture](https://docs.openhands.dev/sdk/arch/overview)；定位：Four-Package Architecture; Two Deployment Modes。
- [S14 · OpenHands Agent.step](https://github.com/OpenHands/software-agent-sdk/blob/60192ed54db73ac658ac1a07462916126c32d3a0/openhands-sdk/openhands/sdk/agent/agent.py#L690)；定位：[(690, 757)]。
- [S17 · OpenHands Conversation factory](https://github.com/OpenHands/software-agent-sdk/blob/60192ed54db73ac658ac1a07462916126c32d3a0/openhands-sdk/openhands/sdk/conversation/conversation.py#L34)；定位：[(34, 58), (153, 165), (190, 235)]。

## 12｜四个项目提供的是不同的设计抓手

结论：先问自己缺什么，再选择要借用哪一层

如果已经在 Codex 里完成代码与文档任务，可以先利用它的工具执行和运行边界。如果在做可扩展产品，DSH 提供插件组合视角。如果任务的人工确认、分支和恢复很复杂，LangGraph 的状态模型值得研究。如果要把软件 Agent 放进远程工作区，OpenHands SDK 的部署分层很直观。这些都是观察重点，不是独占功能清单，更不是一个排序。也可以让 LangGraph 编排一个调用 Codex 的节点，前提是明确两边谁保存状态、谁处理失败。

过渡问题：选好底座以后，每次模型调用到底该看到什么？

证据类型：设计取舍；claims：C01, C02, C03, C04。
- [S10 · Codex run_turn](https://github.com/openai/codex/blob/8531184b49bcb160175a84e140b659a83a426df7/codex-rs/core/src/session/turn.rs#L158)；定位：[(158, 195), (570, 640), (730, 750)]。
- [S11 · Codex ToolOrchestrator](https://github.com/openai/codex/blob/8531184b49bcb160175a84e140b659a83a426df7/codex-rs/core/src/tools/orchestrator.rs#L1)；定位：[(1, 4), (130, 180), (280, 305)]。
- [S04 · DSH architecture](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/docs/architecture.md#L1)；定位：[(1, 42), (74, 145)]。
- [S12 · LangGraph StateGraph.compile](https://github.com/langchain-ai/langgraph/blob/9d68e5b3eb1a63027b05e9f0152149ea0284dcdb/libs/langgraph/langgraph/graph/state.py#L131)；定位：[(131, 157), (1177, 1214), (1355, 1365)]。
- [S13 · LangGraph BaseCheckpointSaver](https://github.com/langchain-ai/langgraph/blob/9d68e5b3eb1a63027b05e9f0152149ea0284dcdb/libs/checkpoint/langgraph/checkpoint/base/__init__.py#L93)；定位：[(93, 130), (199, 230)]。
- [S17 · OpenHands Conversation factory](https://github.com/OpenHands/software-agent-sdk/blob/60192ed54db73ac658ac1a07462916126c32d3a0/openhands-sdk/openhands/sdk/conversation/conversation.py#L34)；定位：[(34, 58), (153, 165), (190, 235)]。

## 13｜上下文工程决定这一轮模型拿到哪些信息

结论：把任务目标、相关证据和当前进度组装成有效输入

我们已经读了不少源码，但写某一页时不需要把五个仓库全部塞给模型。这一轮可能只需要一条结论、两段相关代码、来源路径以及还没解决的问题。上下文工程就是持续决定这些输入。压缩历史可以节省空间，但要保住约束、未核实项与可回查路径，不能把“没检查”压成“已确认”。OpenHands 的 step 与 DSH 的会话投影也说明，模型看到的是经过组装的视图，不是程序里所有数据。

过渡问题：这些原材料、进度和经验，是同一种“记忆”吗？

证据类型：架构归纳；claims：C09, C05。
- [S06 · Effective context engineering](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)；定位：Context engineering vs. prompt engineering; Long-horizon tasks。
- [S14 · OpenHands Agent.step](https://github.com/OpenHands/software-agent-sdk/blob/60192ed54db73ac658ac1a07462916126c32d3a0/openhands-sdk/openhands/sdk/agent/agent.py#L690)；定位：[(690, 757)]。
- [S19 · DSH ReactLoopAgent](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/core/agent-loop/src/agent.ts#L260)；定位：[(260, 313), (675, 703)]。

## 14｜Context、State、Memory 是三个观察视角

结论：本轮输入｜任务记录｜可复用保留信息

用同一份 PPT 看三个视角。模型正在读的源码片段属于 Context；程序保存“第十页待渲染、三条结论待复核”，属于 State；下次交流还适用的听众偏好，属于 Memory。State 可以包含记忆，取出的记忆也会进入 Context，所以它们不是三个互斥的桶。尤其不要把“State 是任务真相”理解成内容一定为真，它只是程序当前依赖的记录，仍然需要来源和校验。换一个窗口，也不等于把所有持久资料都清空。

过渡问题：记忆怎样写入和检索，才不会越用越错？

证据类型：架构归纳；claims：C10。
- [S13 · LangGraph BaseCheckpointSaver](https://github.com/langchain-ai/langgraph/blob/9d68e5b3eb1a63027b05e9f0152149ea0284dcdb/libs/checkpoint/langgraph/checkpoint/base/__init__.py#L93)；定位：[(93, 130), (199, 230)]。
- [S18 · LangGraph BaseStore](https://github.com/langchain-ai/langgraph/blob/9d68e5b3eb1a63027b05e9f0152149ea0284dcdb/libs/checkpoint/langgraph/store/base/__init__.py#L1)；定位：[(1, 12), (708, 736)]。
- [S14 · OpenHands Agent.step](https://github.com/OpenHands/software-agent-sdk/blob/60192ed54db73ac658ac1a07462916126c32d3a0/openhands-sdk/openhands/sdk/agent/agent.py#L690)；定位：[(690, 757)]。

## 15｜记忆要经过写入筛选，也要能失效纠错

结论：候选信息 → 验证与定界 → 保存 → 检索 → 更新

我们可以把短期进度放 checkpoint，把经核实的知识和偏好放应用自己的 Store。写入时至少问：来自哪里、适用谁、什么时候核实、何时复核？检索时也不只是相似度高就全拿来，要按当前任务和范围筛选。语义知识、情景经历、程序性经验是有用的分类，但不必为每一类建一个数据库。源码 BaseStore 提供存取接口和 namespace，是否启用向量搜索、TTL 及如何纠错，需要另外设计。

过渡问题：如果一条错误知识已经被保存，会造成什么？

证据类型：设计建议；claims：C10, C11, C12。
- [S18 · LangGraph BaseStore](https://github.com/langchain-ai/langgraph/blob/9d68e5b3eb1a63027b05e9f0152149ea0284dcdb/libs/checkpoint/langgraph/store/base/__init__.py#L1)；定位：[(1, 12), (708, 736)]。
- [S13 · LangGraph BaseCheckpointSaver](https://github.com/langchain-ai/langgraph/blob/9d68e5b3eb1a63027b05e9f0152149ea0284dcdb/libs/checkpoint/langgraph/checkpoint/base/__init__.py#L93)；定位：[(93, 130), (199, 230)]。

## 16｜把错误写成长期事实，会放大后续失误

结论：例：把“内存 saver”误记为“重启可恢复”

这里做一个小型故障演练。旧笔记写着“启用 checkpoint 后，断电也不丢”。下次做项目时照着用 InMemorySaver，就可能在重启后发现状态没了。正确的处理不只是改当前回答，还应找到这条笔记的来源，标记失效，写明只适用于当前进程，并为重启恢复配置持久后端。新的上下文应该检索到修正后的记录。这个例子提醒我们，记忆系统也需要回归问题集，而不是只统计写进去了多少条。

过渡问题：怎样证明这些改动让系统真的更可靠？

证据类型：案例推演；claims：C11, C12。
- [S05 · LangGraph Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)；定位：Checkpointer vs. store; MemorySaver does not persist between restarts。
- [S18 · LangGraph BaseStore](https://github.com/langchain-ai/langgraph/blob/9d68e5b3eb1a63027b05e9f0152149ea0284dcdb/libs/checkpoint/langgraph/store/base/__init__.py#L1)；定位：[(1, 12), (708, 736)]。

## 17｜评测先对齐交付标准，再比较改动

结论：用固定任务与独立验收，观察结果、成本和人工介入

如果比较两个版本的 Skill，先固定一批任务：正常资料、失效链接、缺少渲染器、中断恢复、故意放入错误来源。不要只用这一次演讲做训练题又当考试题。结构检查可以自动化，事实是否被证据支持需要逐条审阅，讲得是否清楚还要初学者反馈。我们可以记录成功率、耗时、费用与人工介入次数，再决定改动是否值得保留。今天只实际验收这份交付，不把一次 build 通过说成系统成功率提高。

过渡问题：哪些检查机器能做，哪些必须另外审查？

证据类型：设计建议；claims：C13, C14。
- [S20 · DGM outer loop](https://github.com/jennyzzt/dgm/blob/a565fd2d1dca504ef5104a7cc0f3bdc4ab9b4fd2/DGM_outer.py#L146)；定位：[(146, 190), (270, 300), (315, 332)]。

## 18｜构建检查、事实审阅和视觉检查各有盲区

结论：通过一项验收，不能替代另外两项

把这次交付的三条证据线展示出来。build 证明生成器能产出文件；check 检查引用 ID、备注和 PPTX 的结构；render 才能暴露字体与布局问题。它们都不能独立证明某条技术陈述被官方支持，所以我们另外保存 claim 到 source 的映射和固定提交的代码片段。目前这三条检查线都已完成；QA 保存实际命令和范围。大家也可以问：如果模型负责生成又负责检查，会不会重复自己的盲点？这也是保留独立验收标准的原因。

过渡问题：当系统发现自己的失败后，改的究竟是哪一层？

证据类型：实际案例 / 验收路径；claims：C13。

## 19｜重试、记忆积累与自修改不是同一种进步

结论：先分清改了任务结果、保留信息，还是 Agent 程序

模型发现一页挤不下，重新排版，这是任务内修正。把“标题应更短”的偏好留给下次，是记忆更新。改写工具或生成脚本，再用任务集验证，则开始触及系统自修改。RSI 更关心：改动能否进一步提升它产生后续改进的能力。几层之间没有一句提示词就能跨过去的保证。自修改也不一定修改模型权重，可能只是工具、上下文策略或 Agent 代码。我们本次修生成器是在人工目标约束下完成任务，不能据此声称复现了 RSI。

过渡问题：有没有研究系统真正尝试修改自己的 Agent 代码？

证据类型：架构归纳 + 研究讨论；claims：C16, C17。
- [S10 · Codex run_turn](https://github.com/openai/codex/blob/8531184b49bcb160175a84e140b659a83a426df7/codex-rs/core/src/session/turn.rs#L158)；定位：[(158, 195), (570, 640), (730, 750)]。
- [S18 · LangGraph BaseStore](https://github.com/langchain-ai/langgraph/blob/9d68e5b3eb1a63027b05e9f0152149ea0284dcdb/libs/checkpoint/langgraph/store/base/__init__.py#L1)；定位：[(1, 12), (708, 736)]。
- [S20 · DGM outer loop](https://github.com/jennyzzt/dgm/blob/a565fd2d1dca504ef5104a7cc0f3bdc4ab9b4fd2/DGM_outer.py#L146)；定位：[(146, 190), (270, 300), (315, 332)]。

## 20｜DGM 用编码评测筛查自修改的 Agent

结论：从候选档案选父代 → 修改代码 → 评测 → 更新档案

Darwin Gödel Machine 给出一个具体研究例子。它维护不同 Agent 的档案，选择父候选，让基础模型生成修改，再通过编码任务评测。源码不是简单的“只留本代冠军”，档案更新可以保留多个可运行候选，从而探索不同分支。论文讨论的是受限编码实验中的经验结果，不是任意环境都可靠的证明。这里还有评测适配、搜索成本、结果泛化和人工监督等问题。我们只读取论文摘要和作者代码，没有重新运行那些实验，也不引用分数作横向排名。

过渡问题：回到这份 PPT：这些机制怎样接成一条改进链？

证据类型：研究事实 + 边界；claims：C15。
- [S08 · Darwin Gödel Machine paper](https://arxiv.org/abs/2505.22954v3)；定位：Abstract; submission history。
- [S15 · DGM authors README](https://github.com/jennyzzt/dgm/blob/a565fd2d1dca504ef5104a7cc0f3bdc4ab9b4fd2/README.md#L20)；定位：[(20, 32), (75, 104)]。
- [S20 · DGM outer loop](https://github.com/jennyzzt/dgm/blob/a565fd2d1dca504ef5104a7cc0f3bdc4ab9b4fd2/DGM_outer.py#L146)；定位：[(146, 190), (270, 300), (315, 332)]。

## 21｜可靠改进来自多个闭环彼此连接

结论：Agent 做事；Harness 承载；Context / Memory 供给；Eval 检验

现在把地图接起来。Agent 在 Harness 中行动，工具改变环境，反馈回到下一轮。State 保存当前任务，Memory 留下可复用信息；上下文工程决定哪些内容进入模型。Eval 在另一条线上判断产物和系统改动是否值得接受。只有改动进一步提升后续自改进能力并获得证据，才有资格讨论 RSI。各环节不能相互替代：长记忆不能代替核事实，强沙箱不能代替好评测，多 Agent 也不能代替清楚的交付标准。

过渡问题：如果只带走一个实践动作，你会从哪个闭环开始？

证据类型：关系总图；claims：C08, C10, C13, C16。
- [S10 · Codex run_turn](https://github.com/openai/codex/blob/8531184b49bcb160175a84e140b659a83a426df7/codex-rs/core/src/session/turn.rs#L158)；定位：[(158, 195), (570, 640), (730, 750)]。
- [S11 · Codex ToolOrchestrator](https://github.com/openai/codex/blob/8531184b49bcb160175a84e140b659a83a426df7/codex-rs/core/src/tools/orchestrator.rs#L1)；定位：[(1, 4), (130, 180), (280, 305)]。
- [S13 · LangGraph BaseCheckpointSaver](https://github.com/langchain-ai/langgraph/blob/9d68e5b3eb1a63027b05e9f0152149ea0284dcdb/libs/checkpoint/langgraph/checkpoint/base/__init__.py#L93)；定位：[(93, 130), (199, 230)]。
- [S18 · LangGraph BaseStore](https://github.com/langchain-ai/langgraph/blob/9d68e5b3eb1a63027b05e9f0152149ea0284dcdb/libs/checkpoint/langgraph/store/base/__init__.py#L1)；定位：[(1, 12), (708, 736)]。
- [S20 · DGM outer loop](https://github.com/jennyzzt/dgm/blob/a565fd2d1dca504ef5104a7cc0f3bdc4ab9b4fd2/DGM_outer.py#L146)；定位：[(146, 190), (270, 300), (315, 332)]。

## 22｜从设计问题进入源码，比从项目名入手更容易

结论：每个问题都有一条可复查的阅读路径

给想继续研究的校友留一条轻量路线。想看循环，读 Codex run_turn，再读工具编排。想看插件，读 DSH architecture 和 AgentLoop 的依赖。想看恢复，先对照 BaseCheckpointSaver 与 BaseStore。想看部署，读 OpenHands Conversation 的工厂分支。最后再看 DGM 的外层选择与评测循环。资料包不是链接堆，每个重要结论都有定位和不适用范围。代码会演进，链接固定到本次实际读取的提交，官网状态另记核查日期。

过渡问题：带着自己的任务，我们可以争论哪三个选择？

证据类型：继续阅读；claims：C01, C02, C03, C04, C15。
- [S10 · Codex run_turn](https://github.com/openai/codex/blob/8531184b49bcb160175a84e140b659a83a426df7/codex-rs/core/src/session/turn.rs#L158)；定位：[(158, 195), (570, 640), (730, 750)]。
- [S11 · Codex ToolOrchestrator](https://github.com/openai/codex/blob/8531184b49bcb160175a84e140b659a83a426df7/codex-rs/core/src/tools/orchestrator.rs#L1)；定位：[(1, 4), (130, 180), (280, 305)]。
- [S16 · DSH AgentLoop service](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/core/agent-loop/src/index.ts#L338)；定位：[(338, 365)]。
- [S13 · LangGraph BaseCheckpointSaver](https://github.com/langchain-ai/langgraph/blob/9d68e5b3eb1a63027b05e9f0152149ea0284dcdb/libs/checkpoint/langgraph/checkpoint/base/__init__.py#L93)；定位：[(93, 130), (199, 230)]。
- [S18 · LangGraph BaseStore](https://github.com/langchain-ai/langgraph/blob/9d68e5b3eb1a63027b05e9f0152149ea0284dcdb/libs/checkpoint/langgraph/store/base/__init__.py#L1)；定位：[(1, 12), (708, 736)]。
- [S17 · OpenHands Conversation factory](https://github.com/OpenHands/software-agent-sdk/blob/60192ed54db73ac658ac1a07462916126c32d3a0/openhands-sdk/openhands/sdk/conversation/conversation.py#L34)；定位：[(34, 58), (153, 165), (190, 235)]。
- [S20 · DGM outer loop](https://github.com/jennyzzt/dgm/blob/a565fd2d1dca504ef5104a7cc0f3bdc4ab9b4fd2/DGM_outer.py#L146)；定位：[(146, 190), (270, 300), (315, 332)]。

## 23｜用三个真实取舍，交换各自的实践

结论：自主到哪一步？记住哪些东西？怎样证明改得更好？

最后把时间留给大家。第一题，请挑自己工作里的一项任务，说出哪一步可以自动做、哪一步你希望自己确认。第二题，请举一条应该长期保留的信息，以及一条必须过期的信息。第三题，假设 AI 改了自己的工具，你会拿哪组没见过的任务验收？不必追求统一答案。我们可以比较各自的约束：有人在乎速度，有人在乎可追溯，也有人必须处理复杂权限。今天这份资料的价值是让这些讨论有共同的案例和边界。

过渡问题：请选择一个问题，从你的实际经历开始。

证据类型：开放讨论 / 20 MIN；claims：C17, C18。
