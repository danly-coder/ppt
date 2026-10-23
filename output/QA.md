# 交付检查报告

核查与交付日期：2026-10-23（北京时间）。

## 产物

- 主稿：23 页；逐页讲者备注 23 条，均有案例说明和过渡问题。
- 独立架构图：8 页；主稿 653 个 PowerPoint 原生图形/文本对象，架构图稿 268 个，均无栅格图片。
- 研究：22 项官方文档、官方源码或作者论文/源码来源；18 条 fact / synthesis / hypothesis；5 个仓库固定 commit；源码摘录含行号和 SHA256。
- 配套：讲稿、讨论问题、对比表、概念地图、PPT 生成 JavaScript、内容 JSON、package-lock、PDF、逐页 PNG、montage。

## 实际执行

| 命令 / 检查 | 实际结果 | 证明范围 |
|---|---|---|
| npm install --no-audit --no-fund | 通过，19 个包 | 依赖已安装；最终锁定 PptxGenJS 3.12.0 |
| python3 scripts/prepare_content.py | 通过 | 生成 22 来源 / 18 claims / 23 页内容与讲稿 |
| npm run build | 通过 | 生成主稿与独立架构图 PPTX |
| npm run check | 通过 | 来源 ID、claim 类型、证据文件、最少讲稿长度、逐页过渡、PPTX ZIP/XML、23/8 页与备注数、原生对象、画布边界 |
| npm run render | 通过 | LibreOffice → PDF → PyMuPDF 逐页 PNG 与 montage |
| PDF 文本核对 | 通过 | 23 页标题齐全；全部生成文本可提取；没有页外文本或 U+FFFD 替代字符 |
| 视觉目检 | 通过 | 全稿 montage 检查；第 6/10/15/21 页架构图放大检查；最终第 1/18 页复查 |
| 左下角固定标记 | 已移除 | 没有固定“AI 交流会 / AI 技术交流”页脚；只保留本页必要的来源、说明与日期 |

运行环境：Node.js v24.19.0；PptxGenJS 3.12.0；LibreOfficeDev 26.8.0.0.alpha0。字体为 Noto Sans CJK SC。

边界自动检查与 PDF 提取不能独立证明没有框内文字碰撞，因此另做视觉检查。当前渲染未见明显文字溢出、碰撞或缺字；来源脚注用于追溯，主讲内容无需逐字阅读脚注。

## 本次修复

1. starter 原稿以拆分文本模拟图形；改为专门布局的循环、Harness、插件树、Checkpoint、Workspace、Memory 与关系总图。
2. 补齐 OpenHands 独立页、四项目对比、Tool/MCP/Skill、记忆纠错与评测，扩展至 23 页。
3. 去掉左下角“AI 交流会”固定标记，封面下方也不再出现该固定备注。
4. Codex 旧路径 core/src/codex.rs 不存在；根据实际 clone 更新为 session/turn.rs，并固定提交链接。
5. “State=真相”改为“任务记录”；写清记录也可能有错。
6. 明确 InMemorySaver 不跨进程保留、Store 的搜索/TTL 依后端配置；Checkpoint 不撤销外部副作用。
7. DGM 改为多候选档案解释，没有写成每次只留冠军或无限 RSI 已被证明。
8. 调整小型架构框的副标题字号与可用高度，改善中文换行空间；增强结构与来源检查。

## 研究新鲜度与版本

官方网页在本次运行中读取；网页未固定版本，后续可能改变。源码浅克隆成功，内容固定到如下提交：

| 仓库 | 提交 |
|---|---|
| openai/codex | 8531184b49bcb160175a84e140b659a83a426df7 |
| deepseek-ai/deepseek-harness | 687f282e8625c6b8d11ff58211a90524be2e4317 |
| langchain-ai/langgraph | 9d68e5b3eb1a63027b05e9f0152149ea0284dcdb |
| OpenHands/software-agent-sdk | 60192ed54db73ac658ac1a07462916126c32d3a0 |
| jennyzzt/dgm | a565fd2d1dca504ef5104a7cc0f3bdc4ab9b4fd2 |

完整来源与支持范围见 sources/verified_sources.json、sources/evidence/ 和 knowledge/research.md；原 starter 种子另存用于审计，没有直接当作已核实证据。

## 未核实与实际限制

- 未运行或部署 Codex、DSH、LangGraph、OpenHands 的集成环境；源码阅读是局部静态核查，不代表全平台功能测试。
- 未复现 DGM 实验、未重新核实全部 benchmark 设置；论文采用 v3 摘要与作者代码支持的机制，不作成绩比较。
- 未进行四项目同题对比、单/多 Agent 对比或评测改动前后的 A/B 实验。
- 评测任务集、记忆写入与纠错策略、RSI 迁移讨论是本案例的归纳或假设，均已标注。
- 未在现场 PowerPoint / Keynote 上逐页验证；当前可视结果来自 LibreOffice。缺少同名字体时其他软件可能重新换行。
- 未请真实初学者试讲测理解度；43 分钟是内容规划，现场可按讨论热度调整。

## Rubric 自评（非外部验收）

听众适配 1/2（尚未试讲）；叙事 2/2；来源 2/2；架构图 2/2；准确性边界 2/2；备注 2/2；讨论 2/2；密度 2/2；QA 2/2；复用 1/2（新题材仍需人工复核来源）。合计 18/20。

## 交付目录限制

本线程指定的 `/codex/browser/projectless/.../output` 在当前执行环境不存在，创建时分别得到 read-only filesystem 与 permission denied；额外文件写权限也无法创建根目录下的 `/codex`。这不影响构建与检查。完整成果另存当前项目 `/workspace/-demo/ai-tech-talk/output`；可直接从项目文件中取出。没有上传第三方或推送 GitHub。
