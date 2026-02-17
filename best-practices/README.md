# Best Practices Reference Library

> **🚨 REFERENCE ONLY - DO NOT MODIFY 🚨**
>
> This folder contains reference materials and examples. **NEVER save, edit, or modify files in this folder.**
>
> **To use these patterns:** Copy files to `workflows/[your-workflow-name]/` and customize there.

---

This folder contains reference materials documenting best practices for research workflows, validation checklists, templates, and agent configurations.

## 📁 Folder Structure

```
best-practices/
├── README.md                    # This file
├── REFERENCE-ONLY.md            # ⚠️ Usage guidelines - READ FIRST
├── checklists/                  # Validation checklists
│   ├── market-research-validation.md
│   ├── deep-prompt-validation.md
│   └── technical-research-validation.md
├── instructions/                # Workflow instruction sets
│   ├── research-router.md
│   ├── market-research.md
│   ├── technical-research.md
│   └── deep-research-prompt.md
├── templates/                   # Output templates
│   ├── market-research-report.md
│   ├── technical-research-report.md
│   └── deep-research-prompt.md
├── workflows/                   # Workflow configuration files
│   ├── research-workflow.yaml
│   └── injections.yaml
└── agents/                      # Agent persona definitions
    ├── analyst.md
    └── tech-writer.md
```

## 🎯 Purpose

This reference library provides:

1. **Validation Standards** - Comprehensive checklists for quality assurance
2. **Workflow Patterns** - Proven instruction patterns for research workflows
3. **Template Structures** - Well-structured output formats
4. **Configuration Examples** - YAML configurations for workflow systems
5. **Agent Personas** - Example agent definitions with activation patterns

## 📚 Contents by Category

### Checklists

Quality assurance checklists ensuring research integrity and preventing hallucinations:

- **[market-research-validation.md](checklists/market-research-validation.md)**
  - Source verification protocols
  - Anti-hallucination safeguards
  - Market sizing validation
  - Competitive analysis verification
  - Customer intelligence validation
  - References and citations audit

- **[deep-prompt-validation.md](checklists/deep-prompt-validation.md)**
  - Anti-hallucination instructions
  - Citation requirements for prompts
  - Multi-source verification requirements
  - Source quality guidance
  - Prompt completeness checks

- **[technical-research-validation.md](checklists/technical-research-validation.md)**
  - Version number verification
  - Technical claim source verification
  - Multi-source verification for technical claims
  - Documentation completeness
  - ADR (Architecture Decision Record) validation

### Instructions

Complete workflow instruction sets with step-by-step guidance:

- **[research-router.md](instructions/research-router.md)**
  - Router pattern for multi-type research
  - Workflow status management
  - Research type discovery
  - Dynamic instruction loading

- **[market-research.md](instructions/market-research.md)**
  - Collaborative market research workflow
  - TAM/SAM/SOM calculation methodology
  - Competitive analysis process
  - Customer segment research
  - Porter's Five Forces analysis
  - Source validation protocols

- **[technical-research.md](instructions/technical-research.md)**
  - Technology evaluation workflow
  - Requirements gathering
  - Comparative analysis frameworks
  - Trade-off analysis
  - ADR generation
  - Version verification protocols

- **[deep-research-prompt.md](instructions/deep-research-prompt.md)**
  - Research prompt generation workflow
  - Platform-specific optimization (ChatGPT, Gemini, Grok, Claude)
  - Scope definition
  - Anti-hallucination prompt engineering
  - Execution checklists

### Templates

Output templates with variable placeholders:

- **[market-research-report.md](templates/market-research-report.md)**
  - Executive summary structure
  - Market sizing sections
  - Competitive landscape analysis
  - Customer analysis frameworks
  - Strategic recommendations
  - References and sources section

- **[technical-research-report.md](templates/technical-research-report.md)**
  - Technology evaluation structure
  - Comparative analysis matrices
  - ADR template
  - Implementation roadmap
  - Source documentation

- **[deep-research-prompt.md](templates/deep-research-prompt.md)**
  - Research prompt packaging
  - Platform-specific tips
  - Execution checklist
  - Metadata tracking

### Workflows

YAML configuration files for workflow systems:

- **[research-workflow.yaml](workflows/research-workflow.yaml)**
  - Multi-type research configuration
  - Router pattern setup
  - Source tracking settings
  - Web research enablement
  - Template routing

- **[injections.yaml](workflows/injections.yaml)**
  - Subagent integration configuration
  - Content injection points
  - Claude Code enhancement settings
  - Parallel execution configuration

### Agents

Agent persona definitions with activation protocols:

- **[analyst.md](agents/analyst.md)**
  - Business Analyst persona (Mary)
  - Menu-driven activation pattern
  - Workflow handler configuration
  - Research and analysis specialization

- **[tech-writer.md](agents/tech-writer.md)**
  - Technical Writer persona (Paige)
  - Documentation standards loading
  - Menu-driven activation pattern
  - Diagram and documentation tools

## 🔑 Key Concepts

### Anti-Hallucination Protocol

All research workflows incorporate mandatory anti-hallucination safeguards:

- ✅ **EVERY** claim must have cited sources with URLs
- ✅ **CRITICAL** claims require 2+ independent sources
- ✅ Conflicting data is presented with ALL viewpoints
- ✅ Confidence levels are marked: `[Verified]`, `[Single source]`, `[Low confidence]`
- ✅ Clear distinction between **FACTS**, **ANALYSIS**, and **SPECULATION**
- ✅ Web research uses current year data (not outdated training data)
- ✅ Version numbers are verified from official sources

### Checkpoint Protocol

Workflows implement a checkpoint system:

1. Save content immediately after generation
2. Display checkpoint separator (`═══════════════════════`)
3. Show generated content to user
4. Present options: `[a]dvanced`, `[c]ontinue`, `[p]arty-mode`, `[y]OLO`
5. Wait for user response before proceeding

### Adaptive Facilitation

Workflows adjust communication style based on user skill level:

- **Expert**: Concise, technical, assumes knowledge
- **Intermediate**: Balanced explanation and guidance
- **Beginner**: Detailed explanations, educational tone

## 💡 Usage Examples

### Using Checklists

**Scenario**: You've completed market research and want to validate quality.

1. Open [market-research-validation.md](checklists/market-research-validation.md)
2. Go through each section systematically
3. Check off items as you verify them
4. Document issues in the "Issues Found" section
5. Ensure all critical items are addressed before distribution

### Implementing a Workflow

**Scenario**: You want to implement a research workflow in your system.

1. Study [research-router.md](instructions/research-router.md) for routing pattern
2. Review specific workflow instructions (e.g., [market-research.md](instructions/market-research.md))
3. Use [research-workflow.yaml](workflows/research-workflow.yaml) as configuration template
4. Adapt templates from `templates/` folder for your outputs
5. Reference checklists for quality standards

### Creating an Agent

**Scenario**: You want to create a custom agent persona.

1. Review [analyst.md](agents/analyst.md) or [tech-writer.md](agents/tech-writer.md)
2. Copy the XML structure and frontmatter
3. Customize persona characteristics
4. Define menu items and handlers
5. Configure activation protocol
6. Add specialized tools and workflows

## 🎓 Learning Path

**For Understanding Research Best Practices:**

1. Start with checklists to understand quality standards
2. Review instruction files to see how standards are enforced
3. Study templates to see output structure
4. Examine YAML configs for workflow orchestration

**For Implementing Workflows:**

1. Begin with simple router pattern
2. Implement checkpoint protocol
3. Add anti-hallucination safeguards
4. Integrate source validation
5. Add adaptive facilitation

**For Creating Agents:**

1. Define persona and communication style
2. Create menu structure
3. Implement activation protocol
4. Add workflow handlers
5. Configure context loading

## ⚠️ Critical Requirements

When implementing these patterns:

1. **Source Verification is MANDATORY**
   - Never present data without sources
   - Use WebSearch for current data
   - Cite URLs for all claims

2. **Checkpoints Cannot Be Skipped**
   - Save after each major step
   - Display content to user
   - Wait for confirmation

3. **Configuration Must Be Loaded**
   - Load config files at startup
   - Store variables for session
   - Fail gracefully if missing

4. **Maintain Document Structure**
   - Preserve comments in YAML
   - Keep template variables intact
   - Follow naming conventions

## 📊 Quality Metrics

Good research outputs should have:

- **Source Count**: 15-50+ sources cited
- **High Confidence Claims**: >70% with 2+ sources
- **Single Source Claims**: <20% (marked for verification)
- **Low Confidence/Speculative**: <10%
- **Source Recency**: Majority from current year
- **Source Credibility**: Mix of official docs, analyst reports, verified data

## 🔄 Maintenance

When updating these references:

1. **Version all changes** - Track what changed and why
2. **Test thoroughly** - Validate workflows end-to-end
3. **Update all related files** - Keep templates, checklists, and instructions in sync
4. **Document patterns** - Add new patterns to this README
5. **Preserve backwards compatibility** - Don't break existing implementations

## 📝 How to Use This Reference Library

**IMPORTANT: This folder is REFERENCE ONLY.**

### ✅ Correct Usage:

1. **Browse** - Read and study patterns, structures, and best practices
2. **Copy** - Copy files to `workflows/[your-workflow]/` folder
3. **Customize** - Modify the copied files for your specific needs
4. **Reference** - Refer back to examples when building new workflows

### ❌ Never Do This:

- ❌ Don't save new files to `best-practices/`
- ❌ Don't edit existing files in `best-practices/`
- ❌ Don't use `best-practices/` for active workflows
- ❌ Don't modify templates or instructions here

### Example: Creating a New Workflow

```bash
# 1. Copy structure from best-practices
Copy: best-practices/instructions/market-research.md
To:   workflows/my-workflow/instructions.md

Copy: best-practices/templates/market-research-report.md
To:   workflows/my-workflow/template.md

Copy: best-practices/workflows/research-workflow.yaml
To:   workflows/my-workflow/workflow.yaml

# 2. Customize the copied files in workflows/my-workflow/
# 3. Reference best-practices/ if you need pattern examples
```

## 🔗 Related Resources

- **BMad Method Documentation** - Core workflow engine
- **Claude Code Integration** - MCP servers and skills
- **Research Methodology** - Academic research standards
- **Prompt Engineering** - AI prompt optimization techniques

---

**Last Updated**: 2026-02-13
**Maintainer**: Reference Library
**Version**: 1.0.0

---

## 🚨 FINAL REMINDER: REFERENCE ONLY 🚨

**This folder is READ-ONLY reference material.**

- **Active workflows** belong in `workflows/[workflow-name]/`
- **Never modify** files in `best-practices/`
- **Copy to `workflows/`** then customize

See [REFERENCE-ONLY.md](REFERENCE-ONLY.md) for complete usage guidelines.
