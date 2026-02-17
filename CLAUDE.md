# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## What This Is

This is a **Claude Workspace Template** — a structured environment designed for working with Claude Code as a powerful agent assistant across sessions. The user will spin up fresh Claude Code sessions repeatedly, using `/prime` at the start of each to load essential context without bloat.

**This file (CLAUDE.md) is the foundation.** It is automatically loaded at the start of every session. Keep it current — it is the single source of truth for how Claude should understand and operate within this workspace.

---

## The Claude-User Relationship

Claude operates as an **agent assistant** with access to the workspace folders, context files, commands, and outputs. The relationship is:

- **User**: Defines goals, provides context about their role/function, and directs work through commands
- **Claude**: Reads context, understands the user's objectives, executes commands, produces outputs, and maintains workspace consistency

Claude should always orient itself through `/prime` at session start, then act with full awareness of who the user is, what they're trying to achieve, and how this workspace supports that.

---

## Workspace Structure

```
.
├── CLAUDE.md                # This file — core context, always loaded
├── .claudeignore            # Filters visibility (best-practices/, reference/, workflow outputs)
├── .claude/
│   └── commands/            # Slash commands Claude can execute
│       ├── prime.md         # /prime — session initialization
│       └── implement.md     # /implement — execute plans
├── context/                 # Background context about the user and project
├── workflows/               # Parent directory for all automated workflows
│   └── <workflow-name>/     # Each workflow is an isolated subfolder
│       ├── instructions/    # workflow.yml, instructions.md, template.html
│       ├── working/         # Drafts, raw data, intermediate steps
│       └── output/          # Finalized, production-ready deliverables
├── best-practices/          # Hidden vault — reference only (via .claudeignore)
├── plans/                   # Implementation plans
├── outputs/                 # General work products and deliverables
├── reference/               # Research data and competitive intelligence (via .claudeignore)
└── scripts/                 # Automation scripts
```

**Key directories:**

| Directory         | Purpose                                                                        |
| ----------------- | ------------------------------------------------------------------------------ |
| `context/`        | Who the user is, their role, current priorities, strategies. Read by `/prime`. |
| `workflows/`      | Parent for all automated workflows. Each gets its own isolated subfolder.      |
| `best-practices/` | Hidden reference vault. Only access when explicitly asked.                     |
| `plans/`          | Detailed implementation plans, executed by `/implement`.                       |
| `outputs/`        | General deliverables, analyses, reports.                                       |
| `reference/`      | Research data and competitive intelligence (hidden via `.claudeignore`).       |
| `scripts/`        | Automation and tooling scripts.                                                |

---

## Workflow Directory Architecture

All automated tasks and content generation processes must be housed within the `workflows/` parent directory.

- **Isolation Rule:** Each specific workflow **must** have its own unique subfolder (e.g., `workflows/research/`, `workflows/invoice-gen/`).
- **Standardized Sub-structure:** Every workflow subfolder must contain:
    - `instructions/`: Contains `workflow.yml`, `instructions.md`, and `template.html`.
    - `working/`: Reserved for drafting, raw data, and intermediate processing steps.
    - `output/`: Reserved strictly for finalized, production-ready deliverables.
- **Context Handling:** When navigating a workflow, Claude must restrict its focus to that specific subfolder to maintain a hermetic environment.
- **Portability:** Each `workflow.yml` must include `root_path: ./` so the workflow folder can be relocated without breaking references.

---

## Workflow & Automation Standards

All project workflows follow the **Hermetic Source of Truth** strategy:

- **Source of Truth Hierarchy:**
    1. `workflow.yml` — The primary logic and mapping authority (defining data-to-HTML routing).
    2. `instructions.md` — Defines nuances like tone of voice, style constraints, and brand guidelines.
    3. `template.html` — The mandatory semantic HTML5 skeleton (strict table/block structures).
- **Execution Rule:** When performing a workflow, Claude must read the `.yml` and `.md` files **FIRST** before generating any content.
- **Output Rule:** Finalized files must be saved to the local `output/` sub-folder. **Never overwrite or modify files in the `instructions/` folder during execution.**
- **HTML Accuracy:** All tables must follow the `<thead>`/`<tbody>` structure and CSS classes defined in the local `template.html`.

---

## Global Governance

- **Best Practices Vault:** The `best-practices/` folder is a hidden vault for global templates (managed via `.claudeignore`). Only access or reference it when explicitly asked to "Pull from Global Best Practices."
- **Chain of Command:**
    1. **Global:** `.claudeignore` (Filters visibility)
    2. **System:** `CLAUDE.md` (Defines the strategy)
    3. **Local:** `workflow.yml` (Defines the specific task)

---

## Commands

### /prime

**Purpose:** Initialize a new session with full context awareness.

Run this at the start of every session. Claude will:

1. Read CLAUDE.md and context files
2. Summarize understanding of the user, workspace, and goals
3. Confirm readiness to assist

### /implement [plan-path]

**Purpose:** Execute a plan created by /create-plan.

Reads the plan, executes each step in order, validates the work, and updates the plan status.

Example: `/implement plans/2026-01-28-competitor-analysis-command.md`

### /scrape-venues

**Purpose:** Scrape venue websites from Airtable and write Markdown content back.

Reads venue URLs from Airtable, scrapes each using the Firecrawl API, cleans the Markdown content, and writes it to the `venue_url_scraped` field. Processes in batches of 5 with user confirmation between batches. Error states are marked with `MANUAL_CHECK` markers.

Workflow files: `workflows/scrape-venue-site/`

### /extract-brochures

**Purpose:** Extract text from brochure links in Airtable and write Markdown back.

Reads `brochure_link` URLs from Airtable (Google Drive files/folders, Google Docs, Calameo flipbooks, Canva designs, etc.), extracts text content, and writes consolidated Markdown to the `brochure_text` field. Processes in batches of 5 with user confirmation between batches. Handles multiple file types via MCP tools (Google Drive MCP for folder listing + doc reading, Firecrawl for web/PDF scraping). Error states are written as `[ERROR]: ...` markers.

Workflow files: `workflows/extract-brochures/`

---

## Critical Instruction: Maintain This File

**Whenever Claude makes changes to the workspace, Claude MUST consider whether CLAUDE.md needs updating.**

After any change — adding commands, scripts, workflows, or modifying structure — ask:

1. Does this change add new functionality users need to know about?
2. Does it modify the workspace structure documented above?
3. Should a new command be listed?
4. Does context/ need new files to capture this?

If yes to any, update the relevant sections. This file must always reflect the current state of the workspace so future sessions have accurate context.

**Examples of changes requiring CLAUDE.md updates:**

- Adding a new slash command → add to Commands section
- Creating a new output type → document in Workspace Structure or create a section
- Adding a script → document its purpose and usage
- Changing workflow patterns → update relevant documentation

---

## For Users Downloading This Template

To customize this workspace to your own needs, fill in your context documents in `context/` and modify as needed. Then use `/implement` to execute any structural changes. This ensures everything stays in sync — especially CLAUDE.md, which must always reflect the current state of the workspace.

---

## Session Workflow

1. **Start**: Run `/prime` to load context
2. **Work**: Use commands or direct Claude with tasks
3. **Execute**: Use `/implement` to execute plans
5. **Maintain**: Claude updates CLAUDE.md and context/ as the workspace evolves

---

## Notes

- Keep context minimal but sufficient — avoid bloat
- Plans live in `plans/` with dated filenames for history
- Outputs are organized by type/purpose in `outputs/`
- Reference materials go in `reference/` for reuse
- New workflows: copy structure from an existing workflow subfolder, never from `best-practices/` directly
- Workflow outputs are HTML — always use the local `template.html` for structure
