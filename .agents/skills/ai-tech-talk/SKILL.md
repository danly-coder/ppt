---
name: ai-tech-talk
description: Research official AI/Agent/Harness sources, build a traceable Chinese knowledge pack, design a discussion-first talk and create a cited editable PowerPoint with diagrams, speaker notes and QA. Use when preparing AI technical meetups, presentations, Codex/DSH/LangGraph/OpenHands research or research-to-slides.
---

# AI Tech Talk: research → knowledge → talk → editable slides

The user wants to enable conversation, not deliver a formal course. Follow the 6 gated stages below. Use project configuration in `event.json` as defaults. If the user's new instruction conflicts with defaults, follow the user. Work within this repository only.

## Stage 0. Define the teaching story
1. Read `event.json`, `content/slide_plan.json`, this skill, and `AGENTS.md`.
2. Pick one concrete recurring scenario: "让 AI 自己搜资料、整理知识、制作 PPT、验证并交付".
3. Make the listener ask questions in this order: "为什么聊天不够？→ 为什么 Agent 仍会失败？→ Harness 如何让执行可控？→ Context/Memory 如何让长期任务持续？→ 怎样评测改进？".
4. Aim for 14–18 slides and about 35–45 minutes unless overridden. Reserve a separate Q&A block. Avoid a jargon-first taxonomy.

## Stage 1. Research (current, primary, falsifiable)
1. Use `sources/seed_sources.json` only as **starting URLs**, never proof of currentness. Revisit official docs, official repos, changelogs and primary papers; record checked-on dates, versions / commits when available, and direct links to precise pages.
2. For every source collect "what it says", "what it does NOT claim", one concrete example, and a confidence level. Build/update `knowledge/research.md`.
3. Pay particular attention to: Codex core loop/tool/sandbox/session; DeepSeek Harness/Cordis plugin architecture; LangGraph graph/thread Checkpointer vs cross-thread Store; optional OpenHands Agent SDK; Anthropic context engineering; DGM/RSI limitations.
4. Never conflate a discussion hypothesis with product-supported architecture. Avoid unsupported superlatives such as "most advanced".
5. If network access is blocked, keep verified seed claims but mark current version/status "unverified at run time"; do not fabricate citations.

## Stage 2. Knowledge pack / fact check
1. Update `knowledge/claims.json` with claim, kind (`fact`, `synthesis`, `hypothesis`), source IDs and confidence. Research claims should be evidence-backed.
2. Rewrite `knowledge/architecture-comparison.md` and `knowledge/concept-map.md` in ordinary Chinese, with intuitive examples and source links.
3. Define: LLM, Workflow, Agent, Agent Loop, Harness, Tool/MCP/Skill, Context, State, Memory, Checkpoint, Eval, RSI. Show where terms overlap and where project-specific meanings differ.
4. Leave open questions in `content/discussion.md` rather than presenting as facts.

## Stage 3. Narrative design
1. Produce `content/slide_plan.json` using the structure in this project. For every slide, write one **conclusion as the slide headline**, not a loose topic name.
2. Each slide must have: kind, title, one concise main idea, named source IDs when evidence is presented, and speaker notes explaining an example plus one transition question.
3. Compare Codex, DSH, LangGraph by **design problem** (agent runtime / extensibility / durable state), not invented benchmark standings.
4. Teach memory with a single task example, separating `Context = model sees now`, `State = workflow's current truth`, `Memory = reusable retained info`.
5. At least 3 visual slides: Agent Loop, Harness boundary, State/Memory pipeline. End with 3 genuine discussion questions.

## Stage 4. Generate artifacts
1. Prefer the installed `slides` Skill when available for rich slide layout and automatic render / overflow diagnostics. Otherwise use this project's `scripts/build_deck.js` (PptxGenJS, editable shapes, no external image APIs).
2. Build with `npm install && npm run build`. Keep slide plan + JS source and output PPTX. Do not convert architecture text into a non-editable screenshot by default.
3. Also maintain `content/speaker_script.md` (each slide: 1-minute verbal explanation + transition), `content/discussion.md`, and `knowledge/research.md`.

## Stage 5. Validate, preview and fix
1. Run `npm run check`. Check source IDs, slide count, minimal notes, generated pptx existence.
2. If LibreOffice+PyMuPDF are installed, run `npm run render`. Inspect `output/preview/slide-*.png` and `output/montage.png` (especially high-density diagrams and the citations slide). Check text overflow, collisions, low contrast, huge text blocks.
3. Update `output/QA.md`: actual commands run, pass/fail, remaining uncertainty, and research freshness. Never report an unrun test as complete.
4. Fix failures, rebuild and rerun checks. The final report lists source materials, study notes, deck and discussion prompts.

## Stage 6. Adapt / reuse
To prepare another talk, update `event.json`, research source seeds and `content/slide_plan.json`; run the same workflow. Do not blindly reuse citations or today's project statuses.

## Presentation notes
- Speaker notes: tell the story rather than reading bullets. In each section distinguish explanation, example, question.
- Accuracy: labels like "示意架构" are mandatory where the diagram is a conceptual synthesis, not a direct official reproduction.
- Style: clean 16:9, dark navy, high contrast; emphasis via diagrams and whitespace rather than many animations. Optional build animations only if simple and testable.
