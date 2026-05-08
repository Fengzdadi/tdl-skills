# tdl Codex Skill

Codex skill for operating the [`tdl`](https://docs.iyear.me/tdl/) Telegram Downloader CLI.

## Skill

- `skills/tdl`: top-level tdl router
- `skills/tdl/references/download.md`: download, archive, export-first, resume, filters, ranges, topics/replies, templates, progress, and failure recovery
- `skills/tdl/references/auth-and-runtime.md`: install, login, namespaces, proxy, storage, Docker, and runtime guidance

## Usage

Install or copy `skills/tdl` into your Codex skills directory, then ask Codex for a Telegram download task, for example:

```text
Use tdl to download the latest 50 messages from https://t.me/example.
```

The skill is designed to route the request, check local `tdl` compatibility, handle proxy/auth/runtime concerns, and build safe `tdl` commands.

## Notes

- Download test output is ignored under `downloads/`.
- Telegram sessions, private/protected chats, exported JSON, and proxy credentials are treated as sensitive.
