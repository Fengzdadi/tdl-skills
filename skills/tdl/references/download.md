# tdl Download Workflow

Use this reference for `tdl dl/download` and the export-first workflows that feed it. Sources: tdl Download, Export Messages, CLI help, and Template Guide.

## Clarify The Request

If the user says only "download this channel/chat", ask for the missing choices instead of guessing a huge job:

- Scope: recent N messages/media, all, date range, message ID range, topic, replies/comments, or a specific filter?
- Unit: download attached media/files, or also export text-only message records?
- Destination: where should files go?
- Network: do they need a proxy, especially SOCKS5?
- Account: default namespace or another `-n NAME`?

Low-risk requests with explicit message links and destination can proceed directly after runtime/auth checks.

## Source Selection

- Specific message links: pass each link with `-u`.
- Telegram Desktop `result.json` or tdl export JSON: pass each JSON with `-f`.
- Channel/chat URL plus count/range/filter/topic/replies: run `tdl chat export` first, then `tdl dl -f`.
- Protected/private chats: prefer export-first. Direct links may fail.
- Mixed link and JSON sources can be combined in one `tdl dl` command.

Basic forms:

```bash
tdl dl -u https://t.me/channel/123 -d ./downloads
tdl dl -f /path/to/result.json -d ./downloads
tdl dl -u https://t.me/channel/123 -f /path/to/result.json -d ./downloads
```

## Export-First Rules

Decide whether the user means messages or media:

- Recent N messages / all messages / conversation slice / text record: add `--all`; add `--with-content` when message text matters.
- Media/files/videos/images matching tag or text: do not add `--all` by default; `tdl chat export` already exports media messages, and `tdl dl` only downloads media.
- If ambiguous, state the interpretation: "I will download media from messages whose text contains #Tag."

Recent messages:

```bash
tdl chat export -c https://t.me/channel -T last -i 50 --all --with-content -o ./downloads/channel/tdl-export.json
tdl dl -f ./downloads/channel/tdl-export.json -d ./downloads/channel --skip-same
```

Media messages with a tag:

```bash
tdl chat export \
  -c https://t.me/channel \
  --with-content \
  -f "Message contains '#Tag'" \
  -o ./downloads/channel/tag/tdl-export.json

tdl dl -f ./downloads/channel/tag/tdl-export.json -d ./downloads/channel/tag --skip-same
```

Messages with a tag, including text-only messages:

```bash
tdl chat export \
  -c https://t.me/channel \
  --all \
  --with-content \
  -f "Message contains '#Tag'" \
  -o ./downloads/channel/tag/tdl-export.json
```

Only run `tdl dl -f` afterward if the user wants attached media downloaded.

## Ranges, Topics, Replies

Range exports:

```bash
tdl chat export -c https://t.me/channel -T time -i START_TS,END_TS -o ./downloads/channel/range.json
tdl chat export -c https://t.me/channel -T id -i START_ID,END_ID -o ./downloads/channel/range.json
tdl chat export -c https://t.me/channel -T last -i 100 -o ./downloads/channel/latest-media.json
```

- `-T time`: input is Unix timestamps. Convert user-facing dates in the user's timezone.
- `-T id`: input is Telegram message IDs.
- `-T last`: input is count of most recent matching messages; without `--all`, this means recent media messages.
- Timestamp ranges can match multiple messages with the same Telegram timestamp; do not assume a narrow time window means one message.

Forum topics and channel post replies:

```bash
tdl chat export -c https://t.me/channel --topic TOPIC_ID -o ./downloads/channel/topic.json
tdl chat export -c https://t.me/channel --reply POST_ID -o ./downloads/channel/replies.json
```

Use `--topic` for forum topics. Use `--reply` for replies/comments under a channel post.
If `--reply` fails with `MSG_ID_INVALID`, the post ID is not valid for that chat's replies/comments; ask for the exact post/comment link and retry with the correct chat and post ID.

## Filters

Inspect available export filter fields before inventing complex filters:

```bash
tdl chat export -c CHAT -f -
```

Common fields include `Message`, `Media.Name`, `Media.Size`, `Date`, `ID`, `Views`, and `Forwards`.

Download extension filters:

```bash
tdl dl -u https://t.me/channel/123 -i jpg,jpeg,png,webp
tdl dl -u https://t.me/channel/123 -e mp4,mkv,mov,avi,webm
```

- `-i/--include` and `-e/--exclude` match file extensions by filename, not MIME.
- Do not combine include and exclude in one command.
- Use `--rewrite-ext` only when MIME-based extension correction is desired; it can rename files like `.apk` to `.zip`.

## Destination And Storage

- Use the user's explicit destination when provided.
- If no destination is provided, a local `downloads` directory is acceptable only for small, low-risk work.
- Use absolute paths for large archives, external drives, or workflows that may be resumed later.
- Avoid writing Telegram media into a source repository unless explicitly requested.
- For likely large jobs, check free space when practical or warn that total size may only become clear during download.

For long-running archives:

```bash
tdl dl -f /path/to/result.json \
  -d /Volumes/Archive/telegram \
  --skip-same \
  --storage type=bolt,path=/Volumes/Archive/tdl-data \
  -t 4 \
  -l 2
```

## Options

- `--continue`: continue the last download directly.
- `--restart`: restart the last download directly; confirm before discarding task state.
- `--desc`: newest to oldest; use only when requested because order affects resume behavior.
- `--group`: detect grouped/album messages around message links.
- `--skip-same`: skip same files by name without extension and size.
- `--takeout`: prefer for large media exports to reduce flood-wait risk; confirm before use.
- `-t THREADS`: transfer threads per item.
- `-l LIMIT`: concurrent tasks.
- `--delay DURATION`: delay between tasks, useful under flood/rate pressure.
- `--serve --port PORT`: expose files to another downloader; use only when explicitly requested.

Keep tdl defaults unless the user asks for tuning or the job risk justifies conservative values.

## Naming Templates

Use `--template` when the user needs stable archive names, message IDs, dates, captions, or dedupe-friendly filenames.

Common variables:

- `DialogID`: Telegram dialog ID.
- `MessageID`: Telegram message ID.
- `MessageDate`: message timestamp.
- `FileName`: Telegram file name.
- `FileCaption`: file caption / message text.
- `FileSize`: human-readable file size.
- `DownloadDate`: download timestamp.

Examples:

```bash
tdl dl -f result.json -d ./downloads \
  --template "{{ .DialogID }}_{{ .MessageID }}_{{ filenamify .FileName }}"

tdl dl -f result.json -d ./downloads \
  --template "{{ formatDate .MessageDate \"2006-01-02\" }}_{{ .MessageID }}_{{ filenamify .FileName }}"
```

Prefer templates that include message IDs for archives. Caption-only names can collide or expose more text than intended.

## Download Plan

Show a plan before execution when confirmation is required or useful:

```text
Download plan
- Sources: links / JSON / export-first chat
- Selection: recent N / date range / IDs / tag / topic / replies
- Destination: PATH
- Namespace: default or NAME
- Proxy: none or redacted proxy
- Mode: normal / continue / restart
- Filters: export filter and/or extension filters
- Options: --skip-same, --takeout, storage, template, parallelism
- Risk notes: private/protected, large, full-history scan, external path, high parallelism
```

## Progress And Results

During export:

- Report that history scanning is still running for long jobs.
- When done, report matched message count and elapsed time.

During download:

- Summarize visible percent, downloaded size, speed, and `~ETA`.
- Tell the user ETA is live and can change with Telegram/network speed.

Final report format:

```text
Export: N messages, DURATION
Download: N files, SIZE, DURATION
Destination: PATH
Skipped/failed: SUMMARY
Resume: tdl dl ... --continue
```

For tdl export JSON, count messages with `.messages | length` when `jq` is available. Count downloaded files and destination size when practical.

## Empty Or Text-Only Results

- If export produces zero messages, stop before `tdl dl`; suggest checking the chat, range, topic/reply ID, or filter expression.
- If export includes only text-only messages and the user wanted downloads, explain that there is no attached media to download.
- Export message count, downloaded file count, and total size can differ significantly.

## Failure Recovery

For command failures, classify with `troubleshooting.md` before retrying.

Download-specific defaults:

- Interrupted download: rerun the same source and destination with `--continue`.
- Clean retry: use `--restart` only after confirming the user wants to discard task state.
- Protected link direct download failed: export the chat/messages first, then use `tdl dl -f`.
- No media found: explain whether the export matched no messages or only text-only messages; do not run download blindly.

## Example Prompts

- "Download the latest 50 messages from https://t.me/example."
- "Download media from messages containing #Null in this channel."
- "Download files from September 2025 in this channel."
- "Download media from message IDs 1000 to 2000."
- "Download attachments from this forum topic."
- "Download comments under channel post 12345."
- "Continue the previous download."
- "Archive this export with filenames containing dates and message IDs."
