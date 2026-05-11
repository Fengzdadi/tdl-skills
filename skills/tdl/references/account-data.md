# tdl Account Data

Use this reference when the user wants to back up, recover, restore, migrate, or move local tdl account data, sessions, namespaces, or storage between machines. These commands operate on tdl's local account/storage data, not Telegram message exports.

## Command Surface

Check local help before using flags, especially on older tdl versions:

```bash
tdl backup --help
tdl recover --help
tdl migrate --help
```

Current command shapes:

```bash
tdl backup --dst /path/to/date.backup.tdl
tdl recover --file /path/to/date.backup.tdl
tdl migrate --to type=bolt,path=/path/to/new-tdl-data
```

Global options such as `-n NAME`, `--storage ...`, and `--proxy ...` still apply. `--proxy` is usually unnecessary for local backup/recover/migrate unless tdl performs a network check in the local version.

## Clarify The Request

For backup, clarify:

- Namespace: default or `-n NAME`?
- Source storage: default `~/.tdl/data` or an explicit `--storage`?
- Destination file path: where should the `.backup.tdl` be written?
- Privacy: is the destination shared, synced, or external?

For recover, clarify and confirm:

- Backup file path.
- Target namespace and target storage.
- Whether current target data should be overwritten or merged by tdl's behavior.
- Whether a fresh backup of the current target data should be made first.

For migrate, clarify and confirm:

- Source namespace/storage.
- Destination `--to` storage driver and path.
- Whether this is a same-machine storage move or a preparation for another machine.
- Whether a backup should be created before migration.

Do not run `recover` or `migrate` from a vague request like "restore my tdl" or "move tdl"; produce a plan and ask for explicit confirmation.

## Backup Workflow

Prefer explicit destination paths instead of relying on tdl's default filename:

```bash
tdl backup -n default --dst ./tdl-backups/default-2026-05-11.backup.tdl
```

With explicit storage:

```bash
tdl --storage type=bolt,path=/Users/me/.tdl/data backup \
  -n default \
  --dst /Volumes/Backup/tdl/default-2026-05-11.backup.tdl
```

Before running backup:

- Confirm if the destination is shared, synced, external, or inside a repository.
- Create only the needed parent directory if it does not exist.
- Do not print backup contents. Treat backup files as sensitive account data.

After backup, report:

```text
Backup: created
Namespace: NAME
Source storage: default or redacted explicit storage
Output: PATH
Size: SIZE
Sensitive: contains tdl account/session data; keep private
```

## Recover Workflow

Recover modifies local tdl state. Always make or offer a current-state backup first unless the target storage is new/empty:

```bash
tdl backup -n default --dst ./tdl-backups/before-recover-default.backup.tdl
tdl recover -n default --file ./tdl-backups/source.backup.tdl
```

With explicit target storage:

```bash
tdl --storage type=bolt,path=/Users/me/.tdl/data recover \
  -n default \
  --file /Volumes/Backup/tdl/source.backup.tdl
```

Before recover, show a compact plan and wait for confirmation:

```text
Recover plan
- Backup file: PATH
- Target namespace: NAME
- Target storage: default or explicit path
- Pre-recover backup: PATH or skipped because target is new/empty
- Risk: local tdl account/storage state will change
```

After recover, verify only with a safe command when appropriate:

```bash
tdl chat ls
```

Use `tdl chat ls` only if the user wants verification; it accesses and prints the Telegram chat list.

## Migrate Workflow

Use `migrate` when the user wants to move current tdl data to a different storage driver/path, such as from default storage to an external archive path:

```bash
tdl migrate \
  -n default \
  --to type=bolt,path=/Volumes/Archive/tdl-data
```

With explicit source storage:

```bash
tdl --storage type=bolt,path=/Users/me/.tdl/data migrate \
  -n default \
  --to type=bolt,path=/Volumes/Archive/tdl-data
```

Before migrate:

- Back up the source data first, unless the user explicitly declines.
- Confirm source and destination storage are different.
- Confirm the destination path is not a broad shared directory or repository path.
- Do not run concurrent tdl commands against the same namespace/storage.
- Expect tdl to show an overwrite confirmation prompt for the destination namespace. Run this in an interactive terminal and let the visible prompt collect confirmation; do not assume piped stdin will work.

After migrate, report:

```text
Migrate: completed
Namespace: NAME
Source storage: default or redacted explicit storage
Destination storage: DRIVER/PATH
Pre-migration backup: PATH or skipped
Verification: not run / chat ls ok / failed summary
```

## Moving To Another Machine

For another machine, prefer backup/recover over ad hoc copying:

1. On the old machine, run `tdl backup --dst PATH`.
2. Move the `.backup.tdl` file through a private channel such as encrypted external storage.
3. On the new machine, install tdl and run `tdl recover --file PATH`.
4. Verify with `tdl chat ls` only if the user wants confirmation.

Keep proxy and namespace choices explicit on both machines. Do not paste backup contents, session files, or proxy credentials into chat.

## Failure Recovery

For command failures, classify with `troubleshooting.md` before retrying.

Account-data-specific defaults:

- Backup path unwritable: stop and ask for a writable private destination; do not choose a shared folder automatically.
- Backup file missing for recover: stop and ask for the correct path.
- Target storage locked: wait for the other tdl process to exit; do not run concurrent commands against the same storage.
- Unknown storage driver or malformed `--to`: inspect `tdl migrate --help` and rebuild the storage string.
- Recover/migrate uncertain outcome: stop and report the exact status; do not run a second recover/migrate blindly.
- `write error: can't rename log file` under `~/.tdl/log`: treat as a local logging/sandbox warning if the command still exits successfully; report it briefly but do not retry solely for that warning.
