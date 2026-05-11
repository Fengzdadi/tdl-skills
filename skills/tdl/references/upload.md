# tdl Upload Workflow

Use this reference when the user wants to upload local files or directories to Telegram with `tdl upload` / `tdl up`. Upload is externally visible when the destination is a chat, group, channel, or topic, so never run it without an explicit upload plan and confirmation.

## Command Surface

Check local help before using flags:

```bash
tdl upload --help
```

Current command shapes:

```bash
tdl upload --path /path/to/file --chat https://t.me/channel
tdl upload --path /path/to/dir --chat CHAT --topic TOPIC_ID
tdl upload --path /path/to/file --to CHAT_OR_ROUTER
tdl upload --path /path/to/image.jpg --chat CHAT --photo
```

Important defaults:

- Empty `--chat` means Saved Messages.
- `--chat` can be used with `--topic`.
- `--to` conflicts with `--chat` and `--topic`; use it only for advanced routing when the user asks for it.
- Default caption includes filename and MIME. Treat filenames as potentially sensitive.

## Clarify The Request

If the user says only "upload this", clarify:

- Files: exact files/directories to upload.
- Destination: Saved Messages, chat/channel URL, chat ID/domain, or forum topic.
- Caption: default caption, no caption, custom caption, or per-file caption strategy.
- Media mode: upload images as files or as photos with `--photo`.
- Filters: include or exclude extensions?
- Network/account: proxy and namespace, if needed.
- Deletion: whether uploaded local files should remain. Default is keep files.

Do not infer a public/group destination from context. If destination is missing, ask whether to use Saved Messages.

## Preflight

Before upload:

```bash
tdl upload --help
find /path/to/input -maxdepth 1 -type f
du -sh /path/to/input
```

Use local filesystem checks to verify paths exist and estimate size. Do not paste private filenames in chat unless needed; summarize counts and size for sensitive paths.

Avoid uploading from broad directories such as home, Desktop, Downloads, or repository roots unless the user has narrowed the file set with explicit paths or extension filters.

## Upload Plan

Show a plan and wait for confirmation before running:

```text
Upload plan
- Files: N files / PATHS
- Total size: SIZE if known
- Destination: Saved Messages / CHAT / CHAT topic TOPIC_ID / router
- Caption: default / none / custom summary
- Mode: file / photo
- Filters: include EXT / exclude EXT / none
- Namespace: default or NAME
- Proxy: none or redacted proxy
- Delete local files after upload: no unless explicitly requested
```

For private destinations, report only counts and destination type unless the user asks for names.

## Basic Uploads

Saved Messages:

```bash
tdl upload --path /path/to/file
```

Chat or channel:

```bash
tdl upload --path /path/to/file --chat https://t.me/channel
tdl upload --path /path/to/dir --chat CHAT_ID_OR_DOMAIN
```

Forum topic:

```bash
tdl upload --path /path/to/dir --chat https://t.me/group --topic 12345
```

Image as photo instead of file:

```bash
tdl upload --path /path/to/image.jpg --chat CHAT --photo
```

## Captions

Default tdl caption includes filename and MIME. If the user wants no caption, inspect local help/version and use the supported empty-caption form if available. If uncertain, ask the user whether the default caption is acceptable.

Custom caption:

```bash
tdl upload --path /path/to/file --chat CHAT --caption "caption text"
```

Caption safety:

- Avoid exposing local paths, private filenames, or sensitive project names in captions.
- Do not include credentials, proxy URLs, or session details in captions.
- For batch uploads, prefer a short generic caption unless the user wants filenames visible.

## Filters

Use include/exclude filters for directory uploads:

```bash
tdl upload --path /path/to/dir --chat CHAT --include pdf,zip
tdl upload --path /path/to/dir --chat CHAT --exclude tmp,log
```

- Do not combine `--include` and `--exclude` in one upload unless local help explicitly allows it and the behavior is clear.
- Extension filters match filenames; verify the selected file count before upload when practical.
- For mixed media, confirm whether images should be uploaded as photos or files.

## Deletion Safety

`--rm` removes uploaded local files after uploading. Default to never using it.

Only use `--rm` when all are true:

- The user explicitly asked to delete local files after successful upload.
- The upload file set is narrow and verified.
- The destination is confirmed.
- The final plan says `Delete local files after upload: yes`.

Never add `--rm` as a cleanup convenience.

## Progress And Result Report

During large uploads, summarize visible progress without flooding. Report speed/ETA only when tdl prints it.

Final report:

```text
Upload: N files, SIZE, DURATION
Destination: Saved Messages / CHAT / topic TOPIC_ID
Caption: default / custom / none
Filters: include/exclude/none
Deleted local files: no / yes, only if --rm was used
Failed/skipped: SUMMARY
```

For private chats or sensitive filenames, keep the report count-oriented unless the user asks for file names.

## Failure Recovery

For command failures, classify with `troubleshooting.md` before retrying.

Upload-specific defaults:

- Missing path or zero selected files: stop and ask for corrected paths or filters.
- Destination ambiguous: stop and ask for Saved Messages vs exact chat/topic.
- Auth/session failure: run interactive login; do not ask for credentials in chat.
- Proxy timeout: verify `--proxy` and carry it through retry.
- Flood/rate pressure: reduce `-t`/`-l`, add `--delay`, or retry later.
- Partial upload: report what is known from tdl output; do not rerun blindly if it may duplicate messages.
- `--rm` requested but upload partially failed: do not delete anything manually; report the risk and ask the user.
