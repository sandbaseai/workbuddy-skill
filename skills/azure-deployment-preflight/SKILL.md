---
name: "azure-deployment-preflight"
display_name: "Azure 部署前置验证"
display_name_en: "Azure Deployment Preflight"
description: "Use before deploying Azure Bicep infrastructure or when validating azd/az deployment plans with syntax checks, what-if previews, parameter review, and permission-aware evidence."
description_zh: "用于 Azure Bicep 基础设施部署前，或验证 azd/az 部署计划时，执行语法检查、what-if 预览、参数审查和权限感知的证据记录。"
description_en: "Detect the deployment shape, validate Bicep and parameters, run the narrowest authorized what-if preview, classify changes, and report blockers without applying infrastructure mutations."
category: "development"
version: "0.1.0"
author: "github/awesome-copilot; adapted for WorkBuddy by SandBase AI"
license: "MIT"
compatibility: "WorkBuddy with read access to Bicep/azd files and Azure CLI tooling; Azure identity, subscription, resource-group, location, and any write deployment require authorization"
---

# Azure Deployment Preflight

## Purpose and boundary

Validate an Azure deployment plan before it changes infrastructure. The default output is a
read-only preflight report covering Bicep syntax, parameters, target scope, identity, permissions,
what-if changes, warnings, and rollback considerations. Never run `az deployment ... create`,
`azd up`, `azd provision`, resource mutation commands, or destructive recovery under this Skill.

Use synthetic or redacted parameter values when possible. Do not print client secrets, access
tokens, connection strings, private network data, or full sensitive parameter contents. If a
required target or authorization is missing, report a blocked/partial preflight instead of
guessing or asking the tool to create the missing resource group.

## Step 1: detect project and target

Read repository instructions, then locate `azure.yaml`, `infra/`, `deploy/`, `.bicep`,
`.bicepparam`, and `*.parameters.json` files. For each candidate, map:

- azd versus direct Azure CLI workflow;
- Bicep entry point and module graph;
- matching parameter file and environment overlays;
- `targetScope`: resource group, subscription, management group, or tenant;
- subscription, resource group, location, environment, and deployment name;
- referenced modules, providers, existing resources, identities, and sensitive parameters.

Prefer an explicitly named file and environment. If multiple entry points or parameter sets
exist, validate each only when its scope is clear and list omitted candidates. Record repository
revision and tool versions. Missing resource group, subscription, location, or environment is an
evidence gap, not permission to invent a default.

## Step 2: validate syntax and parameters

Check tool availability without installing or upgrading tools automatically:

```bash
az --version
azd version
bicep --version
```

For every selected entry point, run the narrowest syntax check:

```bash
bicep build <file.bicep> --stdout
```

Capture errors with file/line/column, warnings, module resolution status, parameter type and
required-value errors, and exit status. Inspect parameter files for undeclared keys, missing
required values, insecure literals, environment mismatch, and accidental secret material. Do not
echo parameter values into the report; show names, types, redacted fingerprints, and source paths.

Continue reviewing other independent files after one fails, but do not call syntax failure a
deployment failure unless the Azure-side validation also proves it.

## Step 3: confirm identity and permission boundary

Before Azure validation, confirm the intended context using read-only commands if authorized:

```bash
az account show --query '{subscription:id,tenant:tenantId,user:user.name}' --output json
az account list --query '[].{name:name,id:id,state:state,tenant:tenantId}' --output table
```

Redact identities as needed and verify subscription, tenant, resource group, location, and
deployment scope. Use the strongest authorized validation level available. If RBAC validation
fails, a `ProviderNoRbac` what-if may establish provider/template evidence, but it does not prove
that deployment permission exists; label this limitation explicitly. Never bypass login or RBAC
with arbitrary credentials or a broader account.

## Step 4: run a read-only what-if preview

For an azd project, use the documented preview mode only:

```bash
azd provision --preview --environment <environment>
```

For direct Bicep, choose the command matching `targetScope`:

```bash
az deployment group what-if --resource-group <rg> --template-file <file> --parameters <params> --validation-level Provider
az deployment sub what-if --location <location> --template-file <file> --parameters <params> --validation-level Provider
az deployment mg what-if --location <location> --management-group-id <id> --template-file <file> --parameters <params> --validation-level Provider
az deployment tenant what-if --location <location> --template-file <file> --parameters <params> --validation-level Provider
```

Use explicit names and bounds; do not pass secret values through shell history. If Provider-level
validation is denied, retry only with the least-privilege `ProviderNoRbac` mode when supported,
recording the weaker evidence. Do not treat a what-if preview as an approval or execute its
suggested changes.

## Step 5: classify changes and risks

Parse what-if results into:

| Symbol | Classification | Review focus |
|---|---|---|
| `+` | Create | quota, naming, identity, cost, network exposure |
| `~` | Modify | replacement risk, downtime, data migration, immutable properties |
| `-` | Delete | data loss, dependency impact, explicit approval and rollback |
| `=` | No change | confirm expected stability |
| `*`/`!` | Incomplete/unknown | missing provider analysis or deployment evidence |

For each create/modify/delete, record resource type, logical or redacted identifier, affected
properties, dependency order, blast radius, and confidence. Escalate deletes, replacements,
public exposure, identity changes, encryption changes, data-plane changes, quota changes, and
unbounded modules for human review. Compare the preview with the intended change and flag drift,
unexpected resources, missing tags, or environment crossover.

## Preflight report and handoff

Write a report only to an authorized path, using:

```text
Preflight: <name and revision>
Target: <subscription/tenant/resource group/location/environment, redacted as needed>
Status: pass | pass-with-warnings | blocked | partial
Files/tools: <entry points, versions, commands and exit status>
Syntax/parameters: <errors, warnings, redacted gaps>
Identity/RBAC: <confirmed scope, validation level, limitations>
What-if: <counts and create/modify/delete details>
Risks/approvals: <blast radius, data/security/cost concerns>
Rollback: <known reversible path, backup/restore evidence, unknowns>
Next action: <authorized approval, correction, or safe re-run>
```

A preflight passes only when syntax, parameters, target, and preview evidence are sufficient for
the requested scope and no unapproved high-impact change remains. State unavailable tools,
permissions, provider limitations, unresolved warnings, and the fact that no mutation command ran.
