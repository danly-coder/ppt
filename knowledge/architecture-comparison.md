# 按设计问题理解四个项目

这是阅读侧重点，不是独占能力表、兼容性保证或性能排名。

| 项目 | 最值得追问的问题 | 核实到的机制 | 本案例怎样借用 | 边界 |
|---|---|---|---|---|
| Codex | 模型提议怎样变成受控行动？ | run_turn、ToolOrchestrator、线程事件 | 研究、写文件、执行构建 | 沙箱不能保证事实正确 |
| DSH | 怎样替换能力而不复制整个产品？ | Cordis Service / events、profile / bundle / patch | 替换检索或工具 provider | 接口、生命周期、策略要回归 |
| LangGraph | 哪些进度能保存并继续？ | typed state、checkpointer、Store | 保存待核结论与生成进度 | 持久后端要配置；外部副作用要另管 |
| OpenHands SDK | 软件 Agent 放在哪里执行？ | Agent / Conversation / Workspace / Agent Server | 本地原型与远程渲染环境 | 本地 workspace 不等于自动沙箱 |

它们可以组合，但不是拿来就必然兼容。例如 LangGraph 节点调用 Codex，需另行约定 thread 对应关系、超时、重复请求与状态所有权。

## 最小源码阅读路线

- Codex：S10 run_turn → S11 ToolOrchestrator。
- DSH：S04 architecture → S16 AgentLoop → S19 ReactLoopAgent → S21 guarded tools。
- LangGraph：S12 compile → S13 BaseCheckpointSaver ↔ S18 BaseStore。
- OpenHands：S17 Conversation.__new__ → S14 Agent._step。

固定 commit 和直链见 [research.md](research.md) 与 sources/verified_sources.json。
