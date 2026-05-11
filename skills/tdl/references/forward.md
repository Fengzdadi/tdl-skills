# tdl Forward Workflow

Use this reference when the user wants to forward Telegram messages with `tdl forward` from message links or exported JSON files. Forwarding is externally visible when the destination is a chat, group, channel, or router target, so use dry-run first and require explicit confirmation before the real send.

## Command Surface

Check local help before using flags:

```bash
tdl forward --help
```

Current command shapes:

```bash
tdl forward --dry-run --from https://t.me/channel/123 --to DESTINATION
tdl forward --from https://t.me/channel/123 --to DESTINATION
tdl forward --dry-run --from ./exports/messages.json --to DESTINATION
tdl forward --from ./exports/messages.json --to DESTINATION --mode clone
```

Important flags:

- `--from`: source messages; can be links or exported JSON files.
- `--to`: destination peer or router expression.
- `--dry-run`: show how messages would be sent without actually sending.
- `--mode`: `direct` or `clone`; default is `direct`.
- `--edit`: edit message or caption with tdl's expression engine.
- `--silent`: send silently.
- `--single`: do not automatically detect and forward grouped messages.
- `--desc`: reverse message order for each input peer.

## Clarify The Request

If the user says only "forward this", clarify:

- Source: exact message link(s), exported JSON file(s), or an export-first selection.
- Destination: exact chat/channel/user/router target.
- Scope: one message, grouped album, recent N, date range, IDs, topic/replies, or filter.
- Mode: default `direct`, or `clone` if the user needs copied content behavior.
- Content changes: no edit, or a specific `--edit` expression.
- Notification: normal or `--silent`.
- Order: normal or `--desc`.
- Account/network: namespace and proxy, if needed.

Do not infer a public/group/channel destination. If the destination is missing, stop and ask.

## Source Selection

Specific message links:

```bash
tdl forward --dry-run \
  --from https://t.me/channel/123 \
  --to DESTINATION
```

Multiple links:

```bash
tdl forward --dry-run \
  --from https://t.me/channel/123 \
  --from https://t.me/channel/124 \
  --to DESTINATION
```

Export-first selection:

```bash
tdl chat export -c https://t.me/channel -T last -i 50 --with-content -o ./exports/forward/latest-50.json
tdl forward --dry-run --from ./exports/forward/latest-50.json --to DESTINATION
```

Use export-first when the user asks for recent N, date ranges, ID ranges, topics, replies/comments, or filters. Reuse `export.md` for export selection rules.

## Forward Plan

Show a plan before dry-run when the action is broad, private, or destination-sensitive:

```text
Forward plan
- Source: links / export JSON / export-first selection
- Scope: one message / N messages / range / topic / replies / filter
- Destination: DESTINATION or router summary
- Mode: direct / clone
- Grouped messages: auto-detect / single
- Edit: none / expression summary
- Silent: yes / no
- Order: normal / desc
- Namespace: default or NAME
- Proxy: none or redacted proxy
- First step: dry-run only
```

For private/protected sources or destinations, summarize counts and route shape. Do not paste exported JSON contents or sensitive chat titles into chat.

## Dry-Run Gate

Run dry-run first whenever practical:

```bash
tdl forward --dry-run --from SOURCE --to DESTINATION
```

Dry-run does not send messages, but it may still access local tdl session/storage, write logs, and contact Telegram to resolve sources or destinations. Carry proxy/namespace/storage flags into dry-run exactly as they would be used for the real command.

After dry-run:

- Summarize count, source shape, destination, mode, edits, silent/order flags, and any warnings.
- Do not run the real forward automatically after dry-run.
- Ask for explicit confirmation for the exact real command.

If `--dry-run` is unavailable in the local tdl version, inspect `tdl forward --help` and ask the user whether to proceed without it.

## Real Forward

After confirmation, run the same command without `--dry-run`:

```bash
tdl forward --from SOURCE --to DESTINATION
```

Examples:

```bash
tdl forward --from https://t.me/channel/123 --to https://t.me/target
tdl forward --from ./exports/forward/latest-50.json --to https://t.me/target --mode direct
tdl forward --from ./exports/forward/latest-50.json --to https://t.me/target --mode clone --silent
```

Use conservative defaults:

- Keep `--mode direct` unless the user asks for clone behavior or direct mode fails and clone is appropriate.
- Keep grouped-message auto detection unless the user wants only the exact single message.
- Use `--single` only when the user wants to avoid album/group expansion.
- Use `--edit` only with an explicit expression or a user-approved expression draft.
- Use `--silent` only when requested.
- Use `--desc` only when requested because order can matter.

## Edit Safety

`--edit` changes message text or captions through tdl's expression engine. Treat it as content mutation:

- Show the intended edit expression before dry-run.
- Avoid credentials, proxy URLs, session data, or private local paths.
- If editing many messages, prefer dry-run and a small sample explanation over pasting sensitive content.
- If the expression is complex or uncertain, ask the user to confirm the exact expression.

## Progress And Result Report

During large forwards, summarize visible progress without flooding. Report rate limits or waits if tdl prints them.

Final report:

```text
Forward: N messages, DURATION
Source: links / export JSON / selection summary
Destination: DESTINATION or private destination summary
Mode: direct / clone
Options: silent / desc / single / edit summary
Failed/skipped: SUMMARY
```

For private/protected chats, keep the report count-oriented unless the user asks for titles or message details.

## Failure Recovery

For command failures, classify with `troubleshooting.md` before retrying.

Forward-specific defaults:

- Dry-run fails: stop; do not run real forward.
- Dry-run hangs or loops on network/logging: stop it, report that dry-run is not offline, and retry only after fixing proxy/session/storage or narrowing the source/destination.
- Destination ambiguous or unauthorized: stop and ask for the exact destination or login/account namespace.
- Source link invalid: ask for the exact message link or export JSON.
- Export JSON missing or empty: stop and fix the export selection first.
- Direct mode fails: consider `--mode clone` only after explaining the behavior change and getting confirmation.
- Flood/rate pressure: reduce `-l`, add `--delay`, or retry later.
- Partial forward: do not blindly rerun; it may duplicate messages. Summarize what is known and ask whether to resume manually with a narrowed source.
