---
name: "rag-evaluation"
display_name: "RAG 检索增强生成评估"
display_name_en: "RAG Evaluation"
description: "Use when designing, running, reviewing, or diagnosing evaluations for retrieval-augmented generation systems, including corpora, chunking, retrieval, reranking, context assembly, grounded answers, citations, refusals, latency, cost, and regressions."
description_zh: "设计、运行、审查和诊断检索增强生成系统的评估，覆盖语料、切分、检索、重排、上下文、答案忠实度、引用、拒答、延迟、成本与回归。"
description_en: "Design, run, review, and diagnose RAG evaluations across corpora, chunking, retrieval, reranking, context assembly, grounded answers, citations, refusals, latency, cost, and regressions."
category: "research"
version: "0.1.0"
author: "NVIDIA Corporation & affiliates; adapted for WorkBuddy by SandBase AI"
license: "Apache-2.0"
---

# RAG Evaluation

Use this skill to measure and improve retrieval-augmented generation systems independently of a particular vector store, framework, model vendor, or judge library. Inspect the corpus, access controls, ingestion and retrieval code, prompts, models, configuration, product task, existing traces, privacy constraints, latency target and cost model before selecting metrics.

Separate retrieval, context construction and answer generation. An end-to-end score alone cannot explain which stage failed, and a grounded answer can still be wrong when its sources are wrong.

## Define the evaluation contract

Record:

- target users, tasks, languages, domains and risk tiers;
- corpus snapshot, permissions, freshness and authoritative-source policy;
- retriever, filters, embedding, index, fusion, reranker and top-k configuration;
- generator, prompt, context budget, refusal and citation behavior;
- quality, latency, cost, privacy and safety objectives;
- baseline, candidate, decision thresholds, confidence requirements and owner.

Pin every reproducibility input: source document identifiers and revisions, parser and chunker versions, chunk text hashes, embedding model and dimensions, index build, query rewrite, retrieval parameters, reranker, prompt, generator, decoding, judge, code commit and run time. Do not compare runs whose hidden inputs differ without naming the confounder.

## Build a representative dataset

Define the sampling frame before collecting examples. Include common, high-value, rare and adversarial tasks; short and multi-hop questions; exact entities; temporal questions; tables or images when supported; ambiguous queries; unanswerable questions; permission boundaries; conflicting documents; stale facts; and noisy or malformed sources.

Separate development, validation and held-out test sets by source, user, tenant, time or topic when near-duplicates could leak. Detect duplicated questions, overlapping chunks and answer-derived synthetic examples. Never place private production queries or documents in external judges without authorization, minimization and an approved retention path.

For each case preserve the query, expected answerable state, relevant evidence at passage or document granularity, acceptable answer variants, required citations, forbidden claims, access scope, difficulty and provenance. Multiple assessors should adjudicate ambiguous relevance labels; absence from one labeler's set is not proof that another passage is irrelevant.

Synthetic data can expand coverage but must not be the only evidence. Generating questions from a passage biases retrieval toward that passage's language and can overstate performance. Keep synthetic and human or production-derived results separate.

## Evaluate retrieval independently

Measure at the unit the product consumes—document, passage, parent section or fact—and define relevance grades. Useful metrics include:

- recall@k for whether required evidence is retrieved;
- precision@k for context pollution;
- mean reciprocal rank for first-useful-result position;
- nDCG@k for graded relevance and ordering;
- success or coverage for all required facts in multi-hop tasks;
- filter and authorization correctness as hard constraints.

Report per-query results and distributions, not only averages. Slice by language, source type, freshness, query class, tenant, difficulty, answerability and head versus tail traffic. Include zero-result rate, duplicates, stale versions, inaccessible-result rate, reranker changes and per-stage latency.

Tune chunk size, overlap, metadata, query rewriting, hybrid fusion, candidate depth and reranking one controlled variable at a time or use a declared experimental design. Do not claim vector search, hybrid retrieval or reranking is superior without domain data and matched conditions.

## Evaluate context construction

Inspect what the generator actually receives after deduplication, parent expansion, filtering, truncation and ordering. Measure required-evidence coverage, irrelevant-token fraction, duplicate-token fraction, contradiction presence, source diversity, lost evidence from context limits and ordering sensitivity.

Verify that access control is re-derived from the authenticated principal and cannot be bypassed by query rewrite, metadata omission, cache reuse, parent expansion or a forged cursor. Cross-tenant retrieval is a release blocker even if aggregate relevance improves.

Test prompt injection and instruction-like text embedded in documents. Retrieved content is untrusted evidence, not system instruction. Evaluate whether the pipeline preserves source boundaries and refuses requests that require disallowed data or actions.

## Evaluate answers and citations

Score dimensions separately:

- correctness against authoritative evidence or an adjudicated reference;
- faithfulness or groundedness: each externally verifiable claim is supported by supplied context;
- completeness: required facts and constraints are covered;
- relevance and directness to the query;
- citation correctness: cited source supports the associated claim;
- citation completeness: support-needing claims are cited;
- refusal correctness for insufficient, conflicting or unauthorized evidence;
- style and format only where they affect product requirements.

A faithfulness score is not truth probability. If retrieved material is false or obsolete, a fully grounded answer can be factually wrong. Audit source correctness and freshness separately.

Use deterministic checks for schemas, identifiers, citation targets, permission rules and exact invariants. Use human review for nuanced correctness and high-risk decisions. LLM judges require pinned prompts and models, position and verbosity bias checks, calibration against human labels, repeated trials where stochastic, and uncertainty reporting. Do not let a judge grade its own answer without disclosing the dependency.

## Include operational quality

Measure end-to-end and per-stage latency distributions, throughput, failure and timeout rates, retrieved and generated token counts, embedding and reranking work, model calls, cache state and monetary or resource cost. Use production-like corpus size, concurrency and cold/warm conditions.

Quality and performance runs may need different harnesses, but they must share the same versioned candidate configuration. A quality improvement that violates latency, cost, privacy or availability targets is not automatically shippable.

## Run controlled comparisons

Start with the current production or accepted baseline. Reuse identical cases and corpus snapshots, randomize or balance order when judges can drift, isolate caches, and record failures rather than silently dropping them. Treat missing outputs and judge errors as explicit outcomes.

For paired results report absolute and relative deltas, win/loss/tie counts, confidence intervals or bootstrap intervals, and slice regressions. Define hard gates for authorization, leakage, citation integrity and critical tasks; avoid averaging severe failures away with easy cases.

Choose thresholds before observing the final held-out set. Correct for repeated tuning on the same benchmark. Keep the full result artifact, per-case evidence, logs with sensitive data removed, configuration and code revision so another reviewer can reproduce the conclusion.

## Diagnose failures

Trace a failed case through corpus eligibility, parsing, chunking, metadata, embedding, index, filters, query rewrite, candidate retrieval, fusion, reranking, context packing, prompt, generation, citation mapping and judge. Compare retrieved evidence against labels and the actual generator context; do not infer retrieval failure solely from a bad answer.

Classify failures such as missing source, stale ingestion, bad parsing, fragmented evidence, incomplete key or filter, vocabulary mismatch, semantic confusion, hot-cluster approximation, reranker demotion, truncation, prompt noncompliance, unsupported synthesis, citation mismatch, refusal error or faulty label. Preserve counterexamples when fixing the system so they become regression tests.

## Validate and hand off

Run schema and provenance checks on the dataset; verify no train/test or tenant leakage; reproduce a sample of relevance labels; test judge calibration; and rerun a deterministic subset. Exercise answerable, unanswerable, conflicting, stale, injected and unauthorized cases. Confirm cited identifiers resolve to the exact evaluated document revision.

Return the evaluation contract, dataset card and splits, corpus and pipeline fingerprints, metrics with definitions and uncertainty, slice results, hard-gate outcomes, representative failures, latency and cost evidence, comparison decision, limitations, reproducible commands or harness entry points, stored result locations, and recommended next experiments. Do not report a single composite score without the stage-level evidence needed to act on it.
