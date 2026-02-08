# Workflow Specification: Evaluate a Researcher

> Created: 2026-02-08
> Status: Active

## Problem Statement

When considering collaborations, hiring, or reviewing grant proposals, users need to
understand a researcher's trajectory. They have a Google Scholar profile URL and want
to know: Is this person a trend follower, a deep specialist, or an abstraction upleveler?
Currently users must manually extract publication data and format it as JSON.

## Business Value

- Hiring managers can assess research depth from just a Google Scholar link
- PIs can identify potential collaborators with complementary strengths
- Grant reviewers can evaluate researcher commitment to a problem space

## User Workflow

### Step 1: Provide Google Scholar Link

**User does:** Pastes a Google Scholar profile URL (e.g., `https://scholar.google.com/citations?user=XXXXXX`)
**System responds:** Fetches the researcher's name and publication list from the profile
**Input:** Google Scholar profile URL
**Output:** Confirmation with researcher name + publication count

### Step 2: Get Researcher Evaluation

**User does:** Views evaluation results
**System responds:** Shows a unified evaluation containing:
  - Classification (trend follower / deep specialist / abstraction upleveler)
  - Evidence from specific publications
  - Career trajectory summary
  - Topic evolution over time
**Input:** (automatic from Step 1)
**Output:** Structured markdown with classification and evidence

## User Stories

### US-1: Quick Researcher Profile (Priority: P1)

As a hiring manager, I paste a Google Scholar link and get a clear profile
of the researcher's strategy, so I can assess fit for a deep-technical role.

**Why this priority:** Core use case — evaluate a researcher from just a link.

**Acceptance Scenarios:**
1. Given a Google Scholar URL, When submitted, Then I see researcher name + classification with evidence
2. Given a trend-follower profile, When evaluated, Then the system identifies topic-hopping pattern
3. Given a URL the system can't fetch, Then I get a clear error asking for manual publication input

### US-2: Fallback — Manual Publications (Priority: P2)

As a user, when Google Scholar can't be fetched, I can paste publication data
(JSON or plain text list) and still get the same researcher evaluation.

**Why this priority:** Fallback for profiles that can't be scraped.

**Acceptance Scenarios:**
1. Given pasted publication data, When submitted, Then I get the same evaluation format

## Requirements

### Functional Requirements

- FR-001: System MUST accept a Google Scholar profile URL and extract publications
- FR-002: System MUST also accept raw publication data as fallback (JSON or text)
- FR-003: System MUST classify researcher as trend follower, deep specialist, or abstraction upleveler
- FR-004: System MUST cite specific publications as evidence for the classification
- FR-005: System MUST handle researchers with as few as 3 publications

### Input/Output Contracts

| Step | Input | Output |
|------|-------|--------|
| Scholar Link | URL (str) | { name, publications: [{title, year, abstract}] } |
| Fallback | text or JSON | same format |
| Evaluation | publications | { classification, evidence, trajectory, topic_evolution } |

## Edge Cases

- Google Scholar profile is private or has CAPTCHA → prompt for manual input
- Researcher has < 3 publications → warn that evaluation may be limited
- Publications span only 1 year → note insufficient history for trajectory analysis
- Profile has co-authored papers only → note potential ambiguity

## Success Criteria

- SC-001: User gets evaluation from just a Google Scholar URL — no extra steps
- SC-002: Classification is clear and actionable (not vague)
- SC-003: Evidence cites specific publications by title/year
- SC-004: Works with profiles having 3-100+ publications

## Acceptance Criteria

1. User pastes a Google Scholar link and gets a unified evaluation
2. Classification includes specific evidence from the publication list
3. Works identically in Web UI and CLI
4. Graceful fallback when profile can't be fetched
5. Researcher name is auto-detected from the profile
