# Agent instructions for this repository

This repo produces research-backed, discussion-first technical talks in Chinese. The built-in project skill is `$ai-tech-talk` (see `.agents/skills/ai-tech-talk/SKILL.md`). Invoke it for all research-to-slides requests.

## Core rules
- Research from official documentation / official repositories / primary papers. Verify material time-sensitive claims at run time. Do not infer implementation details from a repo's marketing text.
- Evidence is required for nontrivial technical claims. Track evidence in `knowledge/claims.json` and add slide `sources` IDs. Distinguish **官方事实**, **架构归纳**, **推测 / 讨论题**.
- Agent ≠ Harness ≠ a framework. Explain naming conventions and variations between projects.
- Target audience: mixed AI users and developers. Show a practical scenario before abstractions. Use one idea per slide, not long bullet pages.
- Do not claim RSI is production-proven or autonomous unlimited self-improvement. Label research caveats.
- Use editable PowerPoint shapes for architecture diagrams, include notes, and keep project-generated JavaScript source.
- New versions of slides must be visually inspected after rendering; fix overflow before delivery. Don't say verified unless validation actually ran.
- No automatic publishing, GitHub pushing, third-party upload, or deletion. Ask approval for external changes.

## Typical commands
- `npm install`
- `npm run build` (generates `output/ai-agent-harness-talk.pptx`)
- `npm run check` (validates content and pptx structure)
- `npm run render` (requires `libreoffice` and Python package `pymupdf`)

## Deliverables
`knowledge/` research notes and claims, `content/slide_plan.json`, `content/speaker_script.md`, `content/discussion.md`, `output/*.pptx`, rendered preview if available, and `output/QA.md`.
