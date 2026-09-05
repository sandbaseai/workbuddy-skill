---
name: "confidence-gated-routing"
display_name: "证据门控的任务路由"
display_name_en: "Confidence-Gated Task Routing"
description: "Use before delegating work to multiple agents or model tiers; assign the cheapest verifiable tier, escalate only objective failure or disagreement residue, and preserve an auditable handoff."
description_zh: "用于多智能体或多模型分层委派前，按可验证性选择最低成本层级，仅因客观失败或分歧升级残余任务，并保留可审计交接。"
description_en: "Route delegated units with a model-agnostic rubric: start at the cheapest tier that can be verified, escalate only failed or uncertain residue, and avoid batch-wide retries or uncalibrated self-confidence."
category: "productivity"
version: "0.1.0"
author: "undercutsh/firstpass; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "Multi-agent or multi-model workflow with independent verification and explicit tier-to-model mapping"
---

# Confidence-Gated Task Routing

Use this skill before fan-out, swarm, parallel-agent, or model-tier dispatch. The goal is to run each unit at the cheapest tier that can pass independent verification. Do not route by asking a model for a numeric confidence score; self-reported confidence is a hint, not approval.

## Separate planning from execution

Choose a planning tier once, based on ambiguity and cross-cutting judgment. Choose an execution tier separately for each planned unit. Keep easy, mechanically verifiable work cheap even when the overall project is difficult. One hard unit must not raise the tier for the entire batch.

## Assign a base tier with six flags

For each unit, mark:

- `UNVERIFIABLE`: output cannot be checked by tests, schema, execution, or an independent sample;
- `AMBIGUOUS`: multiple defensible answers require judgment;
- `BLAST`: work is irreversible or touches money, authorization, production, deletion, or sensitive data;
- `CROSS-CUTTING`: reasoning spans many files, systems, or contracts;
- `NOVEL`: the task needs new design rather than an established pattern;
- `FORMAT-STRICT`: output must satisfy an exact schema or protocol.

Start with `cheap` for zero flags, `standard` for one or two, and `frontier` for three or more or any ownership/judgment call. Resolve these generic names through the host's explicit model map. `apex` is reserved for a sentence explaining why its marginal judgment value justifies the cost.

When output is mechanically verifiable, start at the lowest tier regardless of apparent difficulty. Format-strict work also starts cheap; let the verifier decide instead of paying for a speculative upgrade. Apply repository policy when blast radius or authorization requires a human gate.

## Escalate only objective residue

Escalate exactly one tier when any of these occurs:

1. two verification failures at the current tier;
2. disagreement between two cheap attempts on genuinely ambiguous work;
3. an explicit uncertainty marker identifying the missing fact or rule.

Pass only grounded results. The next tier receives failed/uncertain items, verification notes, and the single decision needed—not the entire successful batch. Never retry a model indefinitely or escalate every unit because one failed.

Use hysteresis: do not de-escalate mid-task, allow at most one retry per tier, and keep escalation per unit. Cap format-strict work at `standard` unless an explicit policy says otherwise. If residual items remain after the per-work cap, send one batched tie-break request rather than one expensive call per item.

## Require independent verification

Verify in this order when possible:

1. mechanical checks—tests, schema validation, compilation, diff, and grep;
2. execution against synthetic valid, empty, malformed, duplicate, retry, and boundary inputs;
3. independent re-derivation of a representative sample by a different lens;
4. a judge for genuinely unverifiable judgment output.

The generating agent must not be the sole verifier. Record tier, attempt count, verification method, pass/fail reason, and uncertainty. Use redacted context references and never place credentials in prompts, manifests, or escalation payloads.

## Use a structured handoff

Each escalated unit should carry a compact payload:

```json
{
  "item": "<id or path>",
  "attempted_tier": "cheap|standard",
  "attempts": [{"answer": "<redacted>", "verification": "failed|n/a", "notes": "<evidence>"}],
  "uncertainty_reason": "<missing fact or conflict>",
  "decision_needed": "<one question>",
  "context_refs": ["<bounded paths or evidence IDs>"]
}
```

Require every worker to return the declared schema, mark `grounded` or `uncertain`, and state one-line uncertainty rather than guessing. Higher tiers should resolve only the residue and return the same contract.

## Calibrate after each run

Record misses such as `over-tiered` (a cheap-verifiable unit sent to standard) and `escalated-late` (retries burned because a flag was missed). If a miss class repeats, update the routing rubric and keep the change evidence-backed. Report total units, tier distribution, verification denominator, escalations, failures, cost/latency observations, and unresolved residue.

Avoid asking for confidence numbers, dual-running mechanical work, verifying with the same agent, escalating a whole batch, starting at frontier “to be safe,” or claiming that a passing sample proves every unit. Stop when tier mapping, verification independence, authorization, or escalation ownership is undefined.
