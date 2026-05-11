# tdl Extensions

Use this reference when the user wants to list, install, upgrade, remove, or run tdl extensions. Sources: https://docs.iyear.me/tdl/guide/extensions/ and local `tdl extension --help`.

Extensions are experimental and may change in future tdl versions. Installed extensions live under `~/.tdl/extensions` and become new `tdl` subcommands. Treat extensions as external code.

## Command Surface

Check local help before using flags:

```bash
tdl extension --help
tdl extension list --help
tdl extension install --help
tdl extension upgrade --help
tdl extension remove --help
```

Current command shapes:

```bash
tdl extension list
tdl extension install --dry-run iyear/tdl-whoami
tdl extension install iyear/tdl-whoami
tdl extension install /path/to/local-extension
tdl extension upgrade --dry-run EXTENSION
tdl extension upgrade EXTENSION
tdl extension remove --dry-run EXTENSION
tdl extension remove EXTENSION
```

## Clarify The Request

For extension management, clarify:

- Action: list, install, upgrade, remove, or run an installed extension.
- Extension source/name: GitHub `owner/repo`, local path, or installed command name.
- Trust: whether the user trusts this extension source.
- Network: whether GitHub/network/proxy is needed.
- Private repo: whether `GITHUB_TOKEN` is already available in the shell environment.
- Scope: one extension or all installed extensions.

Do not ask the user to paste `GITHUB_TOKEN` into chat. If needed, ask them to set it in the shell environment before running the command.

## List Extensions

Listing installed extensions is read-only:

```bash
tdl extension list
```

Report extension names, authors, and versions if tdl prints them. Do not infer an extension's behavior from its name alone; inspect its help or README before running it.

## Install Extensions

Supported sources:

- GitHub repository: `owner/repo`
- Local extension directory: `/path/to/extension`

Always dry-run first:

```bash
tdl extension install --dry-run owner/repo
tdl extension install --dry-run /path/to/local-extension
```

Then show a plan and wait for confirmation:

```text
Extension install plan
- Source: owner/repo or local path
- Network: GitHub / local
- Private repo token: present in environment / not needed / missing
- Force: no / yes
- Risk: installs external code under ~/.tdl/extensions
```

Install after confirmation:

```bash
tdl extension install owner/repo
tdl extension install /path/to/local-extension
```

Use `--force` only when the user understands it will overwrite or replace an existing extension:

```bash
tdl extension install --force owner/repo
```

## Upgrade Extensions

Upgrade can affect installed command behavior. Dry-run first:

```bash
tdl extension upgrade --dry-run EXTENSION
tdl extension upgrade --dry-run
```

An empty extension list upgrades all installed extensions. Confirm explicitly before upgrading all.

After dry-run, show the planned target(s), whether network/private repo access is needed, and ask for confirmation:

```bash
tdl extension upgrade EXTENSION
tdl extension upgrade
```

## Remove Extensions

Remove changes local tdl extension state. Dry-run first:

```bash
tdl extension remove --dry-run EXTENSION
```

Confirm the exact extension name before removal:

```bash
tdl extension remove EXTENSION
```

Do not manually delete `~/.tdl/extensions` unless the user explicitly asks for low-level cleanup.

## Running Installed Extensions

After installing a repository named `tdl-foo`, the command is usually run as:

```bash
tdl foo
```

Global tdl flags must come before the extension command; extension-specific flags come after:

```bash
tdl -n NAME --proxy socks5://127.0.0.1:1080 foo --extension-flag
```

Before running an extension:

- Inspect `tdl foo --help` when available.
- Read the extension README if the behavior is unclear.
- Confirm before running commands that send Telegram messages, modify local files, call external services, or handle private data.
- Carry namespace, proxy, and storage flags as needed.

## Private GitHub Extensions

Private GitHub repositories require a `GITHUB_TOKEN` with read access. Do not ask the user to paste the token into chat.

Preferred flow:

```bash
tdl extension install --dry-run owner/private-repo
tdl extension install owner/private-repo
```

If authentication fails, tell the user to set `GITHUB_TOKEN` in their shell environment and retry. Do not print token values.

## Progress And Result Report

Final report:

```text
Extension action: list / install / upgrade / remove / run
Targets: EXTENSION(S)
Dry-run: completed / skipped with reason
Result: completed / failed summary
Network/proxy: none / GitHub / Telegram / redacted proxy
Next command: tdl EXTENSION-NAME --help, if useful
```

## Failure Recovery

For command failures, classify with `troubleshooting.md` before retrying.

Extension-specific defaults:

- Unknown extension command: run `tdl extension list` and inspect installed names.
- Install source invalid: ask for GitHub `owner/repo` or a valid local path.
- Private repo auth failure: ask the user to set `GITHUB_TOKEN`; do not request token text.
- Network/proxy failure: add or fix `--proxy` when GitHub or Telegram is unreachable.
- Existing extension conflict: use `--force` only after explaining the overwrite risk and getting confirmation.
- Upgrade all requested vaguely: dry-run first and confirm exact affected extensions.
- Extension behavior unclear: inspect `tdl EXTENSION --help` or the extension README before running it.
