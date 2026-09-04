---
name: "dense-writing"
display_name: "高密度写作"
display_name_en: "Dense Writing"
description: "Use when a response or document is verbose relative to its actual information content, with unnecessary introductions, emphasis, repetition, summaries, qualifiers, or decorative phrasing."
description_zh: "在不丢失事实、逻辑、引用或重要限定的前提下，删去重复、铺垫和装饰性表达。"
description_en: "Remove repetition, filler, and decorative phrasing without losing facts, logic, citations, uncertainty, or material qualifications."
category: "content"
version: "0.1.0"
author: "Bogyie; adapted for WorkBuddy by SandBase AI"
---

# dense-writing

Preserve the information content while increasing expression density.

Use this Skill for drafting or revising chat responses, emails, reports,
documentation, briefs, and other prose. Match the user's requested language,
tone, audience, and format. Do not make terse output the objective.

## WorkBuddy editing pass

1. Identify the document's purpose, audience, decisions, evidence, and required
   constraints before deleting anything.
2. Remove repeated claims, throat-clearing, generic praise, redundant summaries,
   and formatting that adds no structure.
3. Combine adjacent sentences only when their logical relationship remains
   explicit. Prefer concrete verbs and established technical terms.
4. Preserve every source link, citation, number, date, owner, action item,
   requirement, exception, and unresolved question unless the user asks to
   remove it.
5. Compare the revision with the source and confirm that no material meaning,
   instruction, or evidence was lost.

Before producing the final answer, edit it using these rules:

- Remove introductions, praise, emotional framing, and scene-setting that do not carry information.
- Do not explain the same point twice.
- Do not add a closing summary if the conclusion is already clear.
- Use emphasis only when it distinguishes real logical importance.
- Remove adjectives and qualifiers that only make the writing sound more polished.
- Prefer established technical terms when they are more precise and shorter.
- If deleting a sentence does not reduce information or logical structure, delete it.

## Do not compress away

- uncertainty, confidence levels, assumptions, or conflicting evidence
- safety warnings, legal or policy qualifications, consent, and permission boundaries
- accessibility text, citations, provenance, or attribution
- distinctions between completed, pending, failed, and unverified work
- examples the user explicitly requested

When editing another person's text, do not silently change their position or
voice. If a requested length limit cannot preserve essential meaning, produce
the densest faithful version and state the constraint briefly.

The goal is not to make the answer short. The goal is to remove unnecessary language without losing substance.
