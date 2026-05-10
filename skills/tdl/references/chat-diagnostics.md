# tdl Chat Diagnostics

Use this reference for read-only diagnostics: checking whether `tdl` is installed, authenticated, connected through the right proxy, using the right namespace, or able to see a target chat/channel.

## Safety

- `tdl chat ls` accesses the user's Telegram chat list. Run it only when the user asks for diagnostics, auth checking, or help finding a chat.
- Do not paste the full chat list into chat. Report status, counts, and only the specific chat details the user requested.
- Treat private chat names, IDs, and user lists as sensitive.
- Redact proxy credentials in summaries.

## Basic Checks

Check local binary and version:

```bash
command -v tdl
tdl version
```

Check supported flags before relying on them:

```bash
tdl chat ls --help
```

Check login/session health:

```bash
tdl chat ls
```

If this succeeds, auth is working for the selected namespace. If it fails, classify the error with `troubleshooting.md`.

## Namespace Checks

Use namespaces when the user has multiple accounts:

```bash
tdl -n work chat ls
```

Report which namespace was checked. Do not assume `default` when the user mentions work/personal/another account.

## Proxy Checks

When the user is in mainland China, Telegram is unreachable, or a proxy is required:

```bash
tdl --proxy socks5://127.0.0.1:1080 chat ls
tdl --proxy socks5://127.0.0.1:1080 --reconnect-timeout 10s chat ls
```

If a proxy is needed, include the same `--proxy` in `login`, `chat ls`, `chat export`, and `dl`. If `socks connect ... connection refused` appears, it is a local proxy host/port issue.

## Finding A Chat

Use output formats intentionally:

```bash
tdl chat ls -o table
tdl chat ls -o json
```

For programmatic filtering, prefer `-o json` and local parsing. For privacy, show only matching candidates, not the whole list.

Examples of safe summaries:

```text
Auth: OK
Namespace: default
Chats visible: 128
Matched: 1 channel for "example"
Proxy: not used
```

If multiple candidates match, ask the user to choose by title/domain/id. Avoid exposing unrelated chats.

## Filter Fields

`tdl chat ls -f` supports expressions, but available fields can vary by version. If a filter fails, rerun without the filter and parse JSON locally instead of guessing complex expressions.

Safer pattern:

```bash
tdl chat ls -o json
```

Then inspect locally for the requested title/domain/id without sharing the whole JSON. In current tdl versions, JSON entries commonly include `id`, `type`, `username`, and `visible_name`.

## Result Report

Use a compact diagnostic report:

```text
tdl: installed, VERSION
Auth: OK / failed
Namespace: default
Proxy: none / redacted proxy / failed
Chats visible: N
Target chat: found / not found / ambiguous
Next step: download/export/login/proxy fix
```

## Failure Recovery

Classify failures with `troubleshooting.md`:

- auth/session failure -> interactive login
- proxy refused/timeout -> verify proxy host and port
- storage lock -> wait for other tdl process
- permission under `~/.tdl` -> local filesystem/sandbox permission issue
- unknown flag -> inspect local `tdl chat ls --help` or update tdl
