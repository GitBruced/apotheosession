## Commands

```bash
uv run apotheosession --flatten
uv run pytest
```

## Non-obvious

- **No external dependencies** — stdlib only by design
- **Session ID** is derived from Codex UUID (`ses_codex_<uuid>`), not random — deterministic across runs
- **`projectID` = "global"** — `opencode import` always overrides this to the current project, so there's no point computing it
- **`opencode import` always uses CWD** for project assignment, ignores `directory` field in JSON — this is an OpenCode CLI limitation

## Known Technical Debt

- `CodexEvent`/`SessionMeta`/`TurnContext` dataclasses exist but converter works with raw dicts (dead models)
- No `--import` flag to auto-run `opencode import` after conversion
- Reasoning content is encrypted server-side (OpenAI AES-256-GCM), cannot be decrypted locally — placeholder only

## Boundaries

- Don't add external dependencies without explicit request
- Don't remove or rename the deterministic `ses_codex_` session ID prefix
