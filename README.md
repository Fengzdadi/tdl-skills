# tdl Codex Skill

Codex skill for operating the [`tdl`](https://docs.iyear.me/tdl/) Telegram Downloader CLI.

- tdl repository: https://github.com/iyear/tdl
- tdl documentation: https://docs.iyear.me/tdl/

## Skill

- `skills/tdl`: top-level tdl router
- `skills/tdl/references/download.md`: download, archive, export-first, resume, filters, ranges, topics/replies, templates, progress, and failure recovery
- `skills/tdl/references/export.md`: export-only message/user workflows, filters, ranges, topics/replies, output safety, and result reporting
- `skills/tdl/references/chat-diagnostics.md`: read-only auth, proxy, namespace, chat list, and target chat diagnostics
- `skills/tdl/references/account-data.md`: backup, recover, migrate, storage selection, confirmations, and result reporting
- `skills/tdl/references/upload.md`: local file/directory uploads, destination confirmation, captions, topics, filters, deletion safety, and reporting
- `skills/tdl/references/forward.md`: message forwarding, dry runs, destination confirmation, direct/clone mode, edits, silence, grouped messages, and retry safety
- `skills/tdl/references/extensions.md`: extension list/install/upgrade/remove, dry-run first, private GitHub token handling, and running installed extensions
- `skills/tdl/references/auth-and-runtime.md`: install, login, namespaces, proxy, storage, Docker, and runtime guidance
- `skills/tdl/references/troubleshooting.md`: failure classification and recovery for auth, proxy, storage, IDs, protected content, empty results, rate limits, disk, and version issues
- `skills/tdl/scripts/summarize_tdl_result.py`: local-only summary tool for export JSON and download directories

## Installation

Install with the cross-agent `skills` CLI:

```bash
npx skills add Fengzdadi/tdl-skills
```

Or ask Codex directly:

```text
Install the Codex skill from:
https://github.com/Fengzdadi/tdl-skills/tree/main/skills/tdl
```

Restart your agent after installation so the new skill is loaded.

## Usage

After installing, ask your agent for a Telegram task, for example:

```text
Use tdl to download the latest 50 messages from https://t.me/example.
```

The skill is designed to route the request, check local `tdl` compatibility, handle proxy/auth/runtime concerns, and build safe `tdl` commands.

## Notes

- Local test output is ignored under `downloads/` and `exports/`.
- Telegram sessions, private/protected chats, exported JSON, and proxy credentials are treated as sensitive.
- Upload, forward, recover/migrate, extension installation, and destructive options require explicit confirmation.
