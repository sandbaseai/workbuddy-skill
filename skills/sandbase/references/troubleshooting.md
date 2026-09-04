# Troubleshooting

## Discovery returns no candidates

- Shorten the query to the core capability, such as `web search`, `ocr`, `video`, or `embedding`.
- Try one synonym or remove the vendor filter.
- Use the relevant type filter only when the desired class is known.

## Schema validation fails

Re-run `sandbase_inspect`, compare every supplied key with the current schema, remove unsupported keys, and retry once with corrected inputs.

## Authentication or balance error

Use `sandbase_account` when available to distinguish missing authorization from insufficient balance. Do not request that users paste credentials into chat. Explain the exact configuration or funding action needed.

## Rate limit or service error

Respect retry information returned by the service. Retry transient failures conservatively; do not retry permission, balance, or invalid-input errors unchanged.

## Tools are unavailable

State that the SandBase MCP service is not configured in the current WorkBuddy workspace. Give setup guidance, but do not claim that a capability was searched or executed.

