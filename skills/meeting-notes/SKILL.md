---
name: "meeting-notes"
display_name: "会议纪要"
display_name_en: "Meeting Notes"
description: "把會議逐字稿整理成結構化會議記錄（決議事項／待辦與負責人／未決問題三區）。使用者貼上逐字稿、說「整理會議」「幫我整理會議記錄」時使用；一般聊天、寫程式、整理非會議文件時不要用。"
description_zh: "将会议记录或逐字稿忠实整理为摘要、决议、行动项、负责人、风险和未决问题，不补造未出现的信息。"
description_en: "Turn meeting notes or transcripts into faithful summaries, decisions, action items, owners, risks, and open questions without inventing missing information."
category: "productivity"
version: "0.1.0"
author: "rainoff; adapted for WorkBuddy by SandBase AI"
---

# Meeting Notes

Convert meeting notes, chat logs, or transcripts into an accurate operational
record. Match the user's language and requested format. Do not apply this Skill
to unrelated articles or technical notes merely because they contain dialogue.

## Establish the source boundary

Identify the meeting purpose, date, participants, and source material only when
they are stated or supplied as metadata. Distinguish the transcript from later
comments, external facts, and your own interpretation.

If speaker attribution, wording, or chronology is unreliable, label the
uncertainty. Do not infer identity from voice, writing style, title, or context.

## Extract faithfully

1. Summarize the purpose and discussion themes without turning proposals into
   decisions.
2. Record a **decision** only when the source shows that participants accepted
   it. Capture the decision, rationale, constraints, and dissent when stated.
3. Record each **action item** with owner, due date, dependency, and expected
   outcome. Use `Unassigned` or `Not specified` rather than inventing missing
   owners or dates.
4. Put unresolved alternatives, deferred choices, and explicit disagreement in
   **Open questions**, not in decisions.
5. Capture blockers, risks, assumptions, approvals, and follow-up meetings only
   when supported by the source.
6. Merge duplicates carefully while preserving materially different scope,
   owners, deadlines, or conditions.

Never add dates, numbers, commitments, owners, consensus, or causal explanations
that were not present. Mark ambiguous content as `Unclear in source` and, when
useful, cite the timestamp, speaker label, message link, or line reference that
supports an important item.

## Default output

Use this structure unless the user supplies a template:

### Scope

- Meeting purpose, date, participants, and source coverage

### Summary

- A concise, neutral account of the discussion

### Decisions

| Decision | Rationale or constraint | Evidence |
|---|---|---|

### Action items

| Action | Owner | Due | Dependency or success condition | Evidence |
|---|---|---|---|---|

### Risks and blockers

- Confirmed risks, blockers, and assumptions

### Open questions

- Deferred decisions, disagreements, and missing information

Omit empty sections or write `None recorded`; do not fill them with guesses.

## Privacy and distribution

Meeting content may contain personal data, credentials, customer details,
health or financial information, legal advice, or confidential strategy. Do not
expose secrets in the output. Preserve essential meaning while redacting values
that are not needed for the intended audience. Do not publish, email, assign
tasks, or update an external system unless that side effect is within the user's
request and authorized scope.

## Verification

Compare every decision, owner, deadline, number, and action item against the
source. Keep completed, agreed, proposed, blocked, and unverified states
distinct. Finish with source limitations and any item that needs participant
confirmation. The result is a meeting record, not a substitute for legal advice
or proof that absent participants consented.
