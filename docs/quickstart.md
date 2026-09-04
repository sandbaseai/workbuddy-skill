# SandBase for WorkBuddy: 5-minute quickstart

## 1. Download

Download `sandbase-workbuddy-skill.zip` from the [latest release](https://github.com/sandbaseai/workbuddy-skill/releases/latest). Do not unzip and repackage it: `SKILL.md` is already at the archive root, as required by WorkBuddy.

## 2. Import into WorkBuddy

Open **Experts · Skills · Connectors → Skills → Add Skill**, upload the ZIP, and finish the import. Make sure the SandBase MCP service is enabled for the workspace.

## 3. Verify discovery without spending credits

Send:

```text
Use SandBase to find a web extraction API. Compare candidates, required inputs, and pricing only. Do not run a paid call.
```

A correct run uses capability discovery first, inspects candidate schemas, and stops before execution. It should not invent a provider name or request arguments.

Hosts supporting the open Agent Skills convention can install the reviewed
workflow by exact path:

```bash
gh skill install sandbaseai/workbuddy-skill skills/oss-review --dir .workbuddy/skills
```

## 4. Run a small task

After reviewing the candidates and price, ask WorkBuddy to run the selected capability with a small public input. Avoid confidential data during initial testing.

For asynchronous image, audio, or video jobs, WorkBuddy should preserve the returned run ID and poll the same job until it completes or fails. It should not start duplicate paid jobs while waiting.

## Troubleshooting

- **No SandBase tools appear:** enable the SandBase MCP service in the current workspace and reload WorkBuddy.
- **No candidates:** retry with a shorter capability term such as `ocr`, `web search`, or `video`.
- **Schema error:** inspect the capability again and retry once using only current schema fields.
- **Authorization or balance error:** resolve the account status without pasting secrets into chat.
