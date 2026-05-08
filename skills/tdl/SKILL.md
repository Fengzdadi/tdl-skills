---
name: tdl
description: Use when a user wants to operate the tdl Telegram Downloader CLI, especially to download, archive, resume, or export Telegram media/messages from t.me links, channel/chat URLs, protected/private chats, Telegram Desktop JSON exports, or tdl export JSON. Covers safe routing to download workflows, login/auth checks, namespaces, proxy/network setup including SOCKS5, storage/runtime flags, version compatibility, progress reporting, and sensitive Telegram data handling.
---

# tdl

## Purpose

Use `tdl` as the execution engine for Telegram Downloader workflows. This skill is the top-level router: apply the global runtime and safety rules here, then load the specific reference for the user's task.

## Route

- Download, archive, resume, ranges, topics/replies, message links, channel URLs, JSON exports, filters, templates, progress, and download recovery: read `references/download.md`.
- Login, auth checks, namespaces, proxy, storage, installation, Docker, and runtime flags: read `references/auth-and-runtime.md`.
- Upload, forward, delete, join/leave, and other account-modifying workflows are not covered by this skill. Do not run them from this skill.

## Global Safety

- Treat Telegram sessions, private/protected chats, exported JSON, proxy URLs, and local storage paths as sensitive.
- Do not ask the user to paste Telegram login codes, 2FA passwords, desktop passcodes, session data, or API credentials into chat. Let `tdl login` collect interactive input directly.
- Do not paste export JSON contents into chat. Summarize counts, paths, and status instead.
- Redact proxy credentials in summaries. Do not repeat `protocol://user:pass@host:port` unless the user explicitly needs the exact command and already supplied it.
- For private/protected chats, summarize only counts, status, destination, and failures by default. Do not list private chat titles or filenames unless the user asks.
- Confirm before running commands that may download large amounts of data, use `--takeout`, access private/protected chats, write to shared/external/broad destinations, or use high parallelism.
- Never delete downloads, storage, sessions, or task state unless the user explicitly requests cleanup.

## Runtime Setup

When executing, start with local facts:

```bash
command -v tdl
tdl version
```

Use the local CLI as authority. If a flag is uncertain or the user may have an older version, inspect help before using it:

```bash
tdl dl --help
tdl chat export --help
tdl login --help
```

If a planned flag is not available locally, choose a compatible path or tell the user they need a newer `tdl`.

Check authentication only when execution is requested, because it accesses the user's Telegram chat list:

```bash
tdl chat ls
```

If auth is missing, guide the user to an interactive login method. See `references/auth-and-runtime.md`.

## Network And Accounts

- If the user is in mainland China, says Telegram is unreachable, mentions VPN/proxy, or reports timeouts/no response, ask for a proxy address.
- Prefer SOCKS5 when supplied: `--proxy socks5://127.0.0.1:1080` or `--proxy socks5://localhost:1080`.
- Proxy is not persisted by tdl; include it in every network command in that workflow, including `login`, `chat ls`, `chat export`, and `dl`.
- Use `-n NAME` when the user mentions multiple Telegram accounts or namespaces.
- Use stable `--storage` for long-running or resumable archive work.
- Do not run multiple `tdl` network commands concurrently against the same namespace/storage; tdl can fail with "Current database is used by another process".

## Execute

Before execution, make sure the command is specific enough:

- Source is clear: message link, chat/channel URL plus selection criteria, JSON file, or export plan.
- Destination is explicit or an acceptable local `downloads` default for small low-risk work.
- Any private/protected/large/shared/external/high-parallelism risk has been confirmed.
- Any required proxy/namespace/storage choice has been carried through all commands.

While commands run, report useful progress without flooding:

- Export phase: report scanning status, then matched message count and elapsed time when `tdl` prints `done`.
- Download phase: summarize visible percent, downloaded size, speed, and `~ETA`; note that ETA is live and can change.

## Final Report

For completed download workflows, prefer a compact fixed shape:

```text
Export: N messages, DURATION
Download: N files, SIZE, DURATION
Destination: PATH
Skipped/failed: SUMMARY
Resume: COMMAND, if useful
```

For private/protected chats, keep the report count-oriented unless the user asks for more detail.

## References

- `references/download.md`: detailed download workflow, clarification prompts, export-first cases, flags, examples, result reporting, and failure recovery.
- `references/auth-and-runtime.md`: install, login, namespace, proxy, storage, Docker, and runtime guidance.
