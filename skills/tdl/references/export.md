# tdl Export Workflow

Use this reference when the user wants to export Telegram data without necessarily downloading media: message JSON, text records, selected ranges, topic/reply records, or channel/group user lists.

## Clarify The Request

If the user asks to "export this chat/channel", clarify:

- Data type: messages, media-message metadata, text-only message records, raw MTProto messages, or users?
- Scope: recent N, all, date range, message ID range, topic, replies/comments, or filter?
- Content: include message text with `--with-content`, include text-only messages with `--all`, or only media messages?
- Output path: where should the JSON file be written?
- Sensitivity: is this a private/protected chat or user list?

Do not default to full-history `--all` exports for vague requests. Ask for scope first.

## Message Exports

Basic media-message export:

```bash
tdl chat export -c https://t.me/channel -o ./exports/channel/tdl-export.json
```

Recent message record export:

```bash
tdl chat export \
  -c https://t.me/channel \
  -T last \
  -i 50 \
  --all \
  --with-content \
  -o ./exports/channel/latest-50.json
```

Tag/text record export:

```bash
tdl chat export \
  -c https://t.me/channel \
  --all \
  --with-content \
  -f "Message contains '#Tag'" \
  -o ./exports/channel/tag.json
```

Use `--all` only when text-only messages should be included. Without `--all`, `tdl chat export` focuses on media messages, which is usually better for later `tdl dl -f`.

## Ranges, Topics, Replies

Date/time range:

```bash
tdl chat export -c https://t.me/channel -T time -i START_TS,END_TS --with-content -o ./exports/channel/range.json
```

Message ID range:

```bash
tdl chat export -c https://t.me/channel -T id -i START_ID,END_ID --with-content -o ./exports/channel/id-range.json
```

Forum topic or channel post replies:

```bash
tdl chat export -c https://t.me/group --topic TOPIC_ID --with-content -o ./exports/group/topic.json
tdl chat export -c https://t.me/channel --reply POST_ID --with-content -o ./exports/channel/replies.json
```

Notes:

- Convert user-facing date ranges to Unix timestamps in the user's timezone.
- Timestamp ranges can match multiple messages with the same timestamp.
- If `--reply` fails with `MSG_ID_INVALID`, ask for the exact post/comment link and retry with the correct chat and post ID.

## Filters

Inspect available fields before complex filters:

```bash
tdl chat export -c CHAT -f -
```

Common fields include `Message`, `Media.Name`, `Media.Size`, `Date`, `ID`, `Views`, and `Forwards`.

Examples:

```bash
tdl chat export -c CHAT --with-content -f "Message contains '#Null'" -o ./exports/null-media.json
tdl chat export -c CHAT --with-content -f "Media.Name contains '.pdf'" -o ./exports/pdfs.json
tdl chat export -c CHAT --with-content -f "Views > 10000" -o ./exports/popular.json
```

Keep filters simple unless the user explicitly asks for complex criteria.

## User Exports

Export users from a channel or supergroup:

```bash
tdl chat users -c https://t.me/channel -o ./exports/channel/users.json
```

Use user exports carefully:

- Treat user lists as sensitive.
- Confirm before exporting private/protected groups or large communities.
- Summarize counts and output path; do not paste user JSON into chat.
- Use `--raw` only for debugging when the user explicitly needs raw Telegram structures.

## Output Safety

- Never paste exported JSON contents into chat by default.
- For private/protected chats or user lists, report counts and paths only unless the user asks for details.
- Prefer an `exports/` directory over `downloads/` when the goal is record keeping rather than media download.
- Use stable, descriptive filenames: `latest-50.json`, `2025-09.json`, `topic-123.json`, `users.json`.
- Export JSON may be suitable for `tdl dl -f`, but it is not a full backup unless tdl docs say so for that mode.

## Progress And Result Report

For long exports, report that scanning is still running. When done, use a compact report:

```text
Export: N messages/users, DURATION
Output: PATH
Scope: latest N / range / topic / replies / filter
Includes: media messages only / all messages / with content / raw
```

For tdl message export JSON, count messages with `.messages | length` when `jq` is available. For user export JSON, inspect the top-level structure before counting; do not assume it matches message export shape.

## Failure Recovery

- Auth/session failure: use `references/auth-and-runtime.md`; do not collect credentials in chat.
- Empty message export: suggest checking the chat URL, range, topic/reply ID, or filter expression.
- `MSG_ID_INVALID` with replies: ask for the exact channel post/comment link.
- Proxy timeout/no response: verify proxy and include `--proxy` on every command.
- Storage lock: wait for the other `tdl` process or intentionally use a separate namespace/storage.
- Permission/private chat errors: ask the user to confirm they can access the chat in Telegram and are using the right namespace.
