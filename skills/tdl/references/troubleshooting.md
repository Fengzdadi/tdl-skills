# tdl Troubleshooting

Use this reference whenever a `tdl` command fails or behaves unexpectedly. First classify the error, then choose one recovery action. Do not blindly retry commands that failed because of auth, wrong IDs, protected content, proxy misconfiguration, disk space, or storage locks.

## Triage Steps

1. Capture the failed command shape, exit status, and the first meaningful error line.
2. Check whether the command touched Telegram network/session/storage.
3. Classify the error using the table below.
4. Preserve sensitive data: redact proxy credentials, do not paste sessions or export JSON contents.
5. Retry only after changing the cause: login, proxy, IDs, destination, flags, namespace/storage, or concurrency.

## Error Classes

| Symptom | Likely Cause | Recovery |
| --- | --- | --- |
| `not authorized`, auth/session failure | Missing or expired tdl session | Run interactive `tdl login`, `tdl login -T qr`, or `tdl login -T code`; do not ask for credentials in chat. |
| `operation not permitted` under `~/.tdl` | Sandbox or filesystem permission issue | Rerun with appropriate local permissions; do not change session files manually. |
| `Current database is used by another process` | Another tdl command is using the same namespace/storage | Wait for the other command to finish, or intentionally use another namespace/storage. Do not run concurrent network commands against the same storage. |
| `socks connect ... connection refused` | Local proxy app/port is unavailable | Ask the user to verify proxy app, host, and port; include `--proxy` on every network command once fixed. |
| timeout, no response, reconnect loops | Network/proxy/TG reachability problem | Ask whether a proxy is needed; verify `--proxy`; consider `--reconnect-timeout`; retry after connectivity is fixed. |
| `MSG_ID_INVALID` with `--reply` | Wrong post ID/chat pair, no valid comment thread, or unsuitable link | Ask for the exact channel post/comment link; retry with the correct chat and post ID. |
| invalid topic ID or empty topic export | Wrong forum topic ID | Ask for the exact topic link; inspect IDs if possible; retry with `--topic TOPIC_ID`. |
| protected link direct download fails | Protected/private content cannot be downloaded directly from link | Export messages first with `tdl chat export`, then use `tdl dl -f`. |
| zero message export | Filter/range/chat/topic selected no messages | Stop; report empty result and ask whether to adjust chat, range, topic/reply ID, or filter. |
| text-only export but user wanted downloads | Export matched messages without attached media | Explain no media is available to download; keep/export JSON only unless user changes scope. |
| flood wait, rate limit, slowdowns | Telegram account/network pressure | Reduce `-t`/`-l`, add `--delay`, consider `--takeout` for large exports, or retry later. |
| interrupted download | Previous task stopped before completion | Rerun same source/destination with `--continue`. |
| user wants clean retry | Prior task state should be discarded | Confirm, then use `--restart`. |
| disk full / write failure in destination | Destination filesystem lacks space or permission | Stop; report path and available space if known; ask for new destination or cleanup approval. Do not delete files unprompted. |
| unknown flag / flag missing | Local tdl version does not support planned flag | Inspect `tdl <subcommand> --help`; choose compatible flags or tell user to update tdl. |
| clock / MTProto message ID errors | Local clock drift | Consider `--ntp pool.ntp.org`. |

## Recovery Principles

- Auth failures are not proxy failures; proxy failures are not Telegram auth failures. Classify before retrying.
- Keep source and destination unchanged for `--continue`.
- Ask before `--restart`, `--takeout`, high parallelism, external/shared destinations, or private/protected data.
- For private/protected chats and user exports, report counts/status only unless the user asks for details.
- If a command failed during export, do not run downstream `tdl dl -f` unless a valid JSON was produced and contains matching media.
- If a command failed because of local sandbox/permissions, request appropriate permission instead of changing tdl configuration.

## Useful Checks

```bash
tdl version
tdl <subcommand> --help
tdl chat ls
jq '.messages | length' export.json
du -sh /path/to/downloads
df -h /path/to/destination
```

Use `tdl chat ls` only when execution/auth checking is appropriate because it accesses the user's chat list.
