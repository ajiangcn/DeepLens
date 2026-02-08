# Workflow Specification: Understand a Paper

> Created: 2026-02-08
> Status: Active

## Problem Statement

Researchers encounter unfamiliar papers but don't want to spend hours deciphering jargon.
They have a paper link (arXiv, DOI, conference URL, etc.) and want to quickly understand:
What does this paper actually say? Is it solving a real problem or just hype?

## Business Value

- Researchers can triage papers in minutes instead of hours
- Decision-makers get a clear, honest assessment of any paper from just a link
- No manual copy-pasting of abstracts — just drop the link

## User Workflow

### Step 1: Provide a Paper Link

**User does:** Pastes a paper URL (arXiv, Semantic Scholar, DOI, or any research paper link)
**System responds:** Fetches the paper title, abstract, and available content from the link
**Input:** URL string (e.g., `https://arxiv.org/abs/2301.00001`)
**Output:** Confirmation with paper title

### Step 2: Get Unified Paper Summary

**User does:** Waits / views results
**System responds:** Shows a single unified output containing:
  - Plain-language summary (what the paper says, stripped of jargon)
  - Buzzword glossary (every technical term explained)
  - Research stage (exploration / scaling / convergence)
  - Industry demand assessment (real pull vs. academic hype)
  - Fundamental problem (what's really being solved, beyond stated claims)
**Input:** (automatic from Step 1)
**Output:** Structured markdown with all sections above

## User Stories

### US-1: Quick Paper Triage (Priority: P1)

As a researcher, I paste an arXiv link and get a plain-language summary with all
jargon explained, so I can decide in 2 minutes if the paper is worth reading.

**Why this priority:** Most common use case — quick triage of papers.

**Acceptance Scenarios:**
1. Given an arXiv link, When I submit it, Then I see the paper title + full summary
2. Given a paper with 5+ technical terms, When processed, Then each term is identified and explained
3. Given a link the system can't fetch, Then I get a clear error asking me to paste the abstract instead

### US-2: Full Paper Assessment (Priority: P1)

As a research lead, I paste a paper link and get both translation AND research analysis
in a single output, so I can assess whether this direction is worth investing in.

**Why this priority:** Core value prop — combined translation + analysis from just a link.

**Acceptance Scenarios:**
1. Given a paper link, When submitted, Then I get summary + stage classification + demand assessment
2. Given a convergence-stage paper, Then the system flags diminishing returns

### US-3: Fallback — Paste Abstract (Priority: P2)

As a user, when the paper link can't be fetched, I can paste the abstract text directly
and still get the same unified analysis.

**Why this priority:** Fallback for paywalled or unfetchable papers.

**Acceptance Scenarios:**
1. Given pasted abstract text, When submitted, Then I get the same output format as link-based input

## Requirements

### Functional Requirements

- FR-001: System MUST accept a URL and attempt to fetch paper metadata (title, abstract, content)
- FR-002: System MUST also accept raw text as fallback input
- FR-003: System MUST produce a unified output (summary + analysis) — NOT separate tabs/agents
- FR-004: System MUST classify research stage (exploration / scaling / convergence)
- FR-005: System MUST assess real industry demand vs. academic interest
- FR-006: System MUST identify and explain all technical jargon in the paper

### Input/Output Contracts

| Step | Input | Output |
|------|-------|--------|
| Paper Link | URL (str) | { title, abstract, content } |
| Fallback | raw text (str) | same as above with title="User-provided text" |
| Summary | paper content | unified markdown with summary, glossary, stage, demand |

## Edge Cases

- Paper is behind a paywall → prompt user to paste abstract
- Link is not a paper (e.g., blog post) → still attempt analysis, note uncertainty
- Paper is not in English → note language limitation
- Very short abstract (< 50 words) → warn that analysis may be limited

## Success Criteria

- SC-001: User gets complete results from just a URL — no extra steps
- SC-002: Output is a single unified view, not per-agent tabs
- SC-003: Jargon glossary covers 80%+ of technical terms
- SC-004: Works with arXiv, Semantic Scholar, and DOI links at minimum

## Acceptance Criteria

1. User pastes a link and gets a unified result without selecting agents
2. All technical terms are identified and explained
3. Research stage and demand assessment are included automatically
4. Works identically in Web UI and CLI
5. Graceful fallback when link can't be fetched
