---
name: "aws-resource-query"
display_name: "AWS 资源只读查询"
display_name_en: "AWS Resource Query"
description: "Use when answering natural-language questions about AWS resources, inventory, configuration, ownership, tags, cost signals, networking, or identity with strictly read-only AWS CLI queries."
description_zh: "用于用严格只读的 AWS CLI 查询回答资源盘点、配置、归属、标签、成本信号、网络或身份相关的自然语言问题。"
description_en: "Translate intent into scoped, paginated, read-only AWS describe/list/get queries, confirm account and region, minimize output, and report unavailable permissions without mutating infrastructure."
category: "cloud"
version: "0.1.0"
author: "github/awesome-copilot; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with AWS CLI and an authorized read-only identity; account, region, service availability, and support access may limit results"
---

# AWS Resource Query

## Purpose and absolute safety contract

Answer questions about currently existing AWS resources by translating intent into bounded,
read-only AWS CLI commands. This Skill never creates, modifies, deletes, starts, stops, reboots,
terminates, attaches, detaches, publishes, invokes, sends, or executes AWS resources or data.
It is for discovery and evidence gathering; use a separate authorized workflow for changes.

Allowed command families are limited to `describe-*`, `list-*`, `get-*`, `sts get-caller-identity`,
`aws configure get`, `resourcegroupstaggingapi get-resources`, `ce get-*`, and explicitly approved
read-only support queries. If a request implies a write, explain the read-only boundary and offer
to show current state or produce a separate change plan without executing it.

Do not expose access keys, session tokens, secret values, private endpoints, customer data, or
full policy documents when a redacted summary answers the question. Treat command output as
sensitive until its data class and audience are known.

## Step 1: parse and constrain intent

Extract:

- target account/profile and region (or explicitly all regions);
- service, resource type, identifier, tags, state, owner, environment, and time range;
- requested detail, output audience, and whether counts, a table, or raw JSON is needed;
- authorization and data-sensitivity limits.

If account, region, resource scope, or requested detail is ambiguous, query the safest narrow
scope first or state the assumption. Never silently scan every account or region. Use exact IDs
when provided and filter by tags or state before retrieving details.

## Step 2: confirm identity and region

Before resource queries, run only the following read-only checks as authorized:

```bash
aws sts get-caller-identity --query '{Account:Account,Arn:Arn,UserId:UserId}' --output json
aws configure get region
```

Record account ID, principal class, effective region, profile/context (without credentials), and
timestamp. If the identity or region cannot be confirmed, mark the result as partial and do not
claim it represents the intended account. Append `--region <region>` whenever the user specifies
one. For multi-region work, enumerate an explicit allowlist and label missing regions.

## Step 3: select safe query families

Use the narrowest service query that answers the question. Common mappings include:

| Intent | Read-only query family |
|---|---|
| EC2 instances, states, types, addresses, ASGs | `ec2 describe-*`, `autoscaling describe-*` |
| Lambda inventory and configuration summary | `lambda list-functions`, `lambda get-function-configuration` |
| S3 buckets and region/ownership metadata | `s3api list-buckets`, `s3api get-bucket-*` |
| RDS databases and snapshots | `rds describe-*` |
| ECS services/tasks and EKS clusters | `ecs describe-*`, `ecs list-*`, `eks describe-*`, `eks list-*` |
| VPC, subnets, routes, security groups | `ec2 describe-vpcs`, `describe-subnets`, `describe-route-tables`, `describe-security-groups` |
| IAM roles/users/policies metadata | `iam list-*`, `iam get-*` with redacted policy summaries |
| Secrets Manager inventory only | `secretsmanager list-secrets`, never retrieve secret values |
| Queues, topics, and notifications metadata | service-specific `list-*`/`get-*` without publishing or sending |
| Tags and ownership | `resourcegroupstaggingapi get-resources` with service/tag filters |
| Cost and usage signals | approved `ce get-*` with bounded dates, granularity, and dimensions |

Use JMESPath `--query` and `--output table/json` to return only fields needed. Avoid broad
unfiltered dumps. For policies, secrets, user data, logs, or resource contents, return metadata,
ARNs, timestamps, sizes, and redacted findings unless the exact sensitive content is separately
authorized.

## Step 4: execute bounded queries

Apply explicit bounds:

- use service filters, tags, states, IDs, dates, and `--max-items` where supported;
- handle `NextToken`/pagination and report whether the result is complete;
- cap regions, resources, retries, output size, and runtime;
- use one service or region at a time when a failure could obscure scope;
- preserve the exact command shape and non-sensitive parameters for reproducibility;
- stop on access-denied or throttling and report the missing permission/rate limit rather than retrying indefinitely.

Never substitute a mutating command because a read-only command is unavailable. Do not use
`--no-sign-request` to bypass an identity boundary, and do not ask users to paste credentials.

## Step 5: reconcile and present evidence

For each result, report account, region, query timestamp, scope/filter, completeness, resource
count, and the fields shown. Distinguish:

- **observed:** directly returned by AWS;
- **derived:** calculated from returned values, such as counts or age;
- **inferred:** a tentative interpretation requiring confirmation;
- **unavailable:** blocked by permission, region, service, pagination, or stale metadata.

Cross-check identifiers and tags before joining resources. Flag duplicate names, missing tags,
cross-region gaps, stale states, and conflicting fields. A resource's existence does not prove it
is healthy, reachable, compliant, or unused; link to a health or audit workflow when those claims
are requested.

## Safe output templates

```text
Account/region: <redacted or confirmed identity and region>
Scope: <service, filters, IDs, date window>
Observed at: <UTC timestamp>
Completeness: complete | partial | unknown; pagination=<handled/not handled>
Count: <number>
Results: <minimal table or redacted JSON>
Derived findings: <calculation, formula, evidence>
Unavailable/permission gaps: <exact limitation>
Read-only confirmation: no mutation command was run
Next safe query: <narrow follow-up, if useful>
```

For cost queries, show the currency, time zone, granularity, aggregation, and whether values are
estimated or finalized. For identity queries, show principal type and account rather than tokens.

## WorkBuddy handoff

Return the interpreted intent, confirmed account/region, exact read-only query families, filters,
result completeness, redacted evidence, observed/derived/inferred labels, permission and rate-limit
gaps, timestamp, and a safe next query. If asked to mutate AWS, refuse execution under this Skill
and provide only a clearly labeled, non-executing change plan or current-state inspection.
