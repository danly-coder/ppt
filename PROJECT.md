# 从一份 PPT 看 Agent 与 Harness

本项目使用 `.agents/skills/ai-tech-talk/SKILL.md` 完成官方资料研究、知识整理、讲解设计和可编辑 PPT 生成。主稿 23 页，建议 43 分钟讲述、20 分钟讨论。不是正式课程，以这次资料到 PPT 的交付为贯穿案例。

## 从哪里开始

- `output/ai-agent-harness-talk.pptx`：23 页主稿，文本和图形可编辑，含逐页讲者备注与来源直链。
- `output/architecture-diagrams.pptx`：8 页可单独复用的架构图，均为 PowerPoint 原生对象。
- `output/preview/ai-agent-harness-talk.pdf`：阅读版；`output/montage.png`：全稿缩略图。
- `content/speaker_script.md`：逐页讲稿、过渡问题、证据定位。
- `content/discussion.md`：三组讨论题与时间建议。
- `knowledge/research.md`：官方来源、支持/不支持范围与未核实事项。
- `knowledge/claims.json`：18 条 fact / synthesis / hypothesis 记录。
- `knowledge/architecture-comparison.md`、`knowledge/concept-map.md`：对比与概念解释。
- `sources/verified_sources.json`：22 项来源清单；`sources/evidence/`：固定提交的带行号源码摘录。
- `output/QA.md`：实际运行的检查、视觉审阅和局限。

幻灯片左下角没有固定的“AI 交流会”标记；仅保留各页必要的证据说明与来源，右下角为页码。

## 重建

需要 Node.js；字体使用 Noto Sans CJK SC。

```sh
npm ci
npm run build
npm run check
npm run render
```

`render` 另需 `libreoffice` 或 `soffice`、Python 的 `pymupdf` 与 `Pillow`。没有这些程序时会明确失败，不会把渲染算作通过。

可直接编辑 `content/slide_plan.json` 后 build/check/render。`scripts/build_deck.js` 是保留的 JavaScript 生成源，绘图均用 PptxGenJS 原生 shapes / text。`scripts/check_pptx.py` 检查 XML、备注、可编辑对象和页面边界；渲染脚本生成 PDF、逐页 PNG、montage 和 render-check.json。边界检查不保证没有文字碰撞，仍需目检。

`scripts/prepare_content.py` 保留本次研究与内容的数据生成过程。它读取 `work/sources/` 下的五个源码浅克隆；克隆不包含在交付 ZIP。只重建 PPT 无需运行它。更新研究时需重新取得官方仓库、阅读文档并核实内容，不能盲目重用旧结论或自动把日期改成今天。

## 核实范围

2026-10-23 核查官方网页及五个仓库的局部代码。没有部署四个 Agent 项目、没有做同题性能对比、没有复现 DGM 基准。网页链接可能更新，源码直链固定到提交。具体边界见 research.md 与 QA.md。
