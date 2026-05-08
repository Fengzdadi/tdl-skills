# Auth and Runtime

Use this reference when installing tdl, checking login state, choosing namespaces, or configuring proxy/storage. Sources: https://docs.iyear.me/tdl/getting-started/installation/ and https://docs.iyear.me/tdl/more/cli/tdl_login/

## Availability

```bash
command -v tdl
tdl version
```

If missing, suggest one installation path based on platform:

```bash
brew install telegram-downloader
curl -sSL https://docs.iyear.me/tdl/install.sh | sudo bash
go install github.com/iyear/tdl@latest
```

Do not run installer commands without the user's approval.

## Authentication Check

```bash
tdl chat ls
tdl --proxy socks5://127.0.0.1:1080 chat ls
```

Use this as a practical session check before executing Telegram downloads. It accesses and prints the user's chat list, so avoid running it when the user only asked for a command draft.

If the command fails because no session is available, do not ask for credentials in chat. Tell the user to run one login command interactively.

## Login

Let `tdl` collect credentials interactively:

```bash
tdl login
tdl login -T qr
tdl login -T code
tdl login -T desktop
tdl --proxy socks5://127.0.0.1:1080 login -T qr
```

- default `tdl login`: desktop login mode; import from official Telegram Desktop where supported.
- `-T desktop`: explicit desktop login mode.
- `-T qr`: QR login.
- `-T code`: phone/code login.
- `-d, --desktop`: official desktop client path.
- `-p, --passcode`: desktop client passcode; do not ask the user to paste this into chat.

Selection guidance:

- Prefer default/desktop login when Telegram Desktop is installed and the user wants to reuse that session.
- Prefer QR login when the user has Telegram on a phone and wants the least typing.
- Prefer code login when QR or desktop import is unavailable.
- Add `--proxy` to login commands when Telegram is unreachable without a proxy.

## Namespaces

Use namespaces when the user has multiple Telegram accounts or wants isolated tdl sessions:

```bash
tdl login -n work -T qr
tdl dl -n work -u https://t.me/example/123 -d ./downloads
```

Default namespace is `default`.

## Proxy, Storage, and Timing

Global options can be added to download commands:

```bash
tdl --proxy socks5://127.0.0.1:1080 dl -u https://t.me/example/123
tdl --storage type=bolt,path=/path/to/tdl-data dl -u https://t.me/example/123
tdl --ntp pool.ntp.org dl -u https://t.me/example/123
```

- `--proxy`: proxy URL. Format: `protocol://username:password@host:port`.
- Common local proxy examples:
  - `socks5://127.0.0.1:1080`
  - `socks5://localhost:1080`
  - `http://127.0.0.1:8080`
  - `https://127.0.0.1:8081`
- `--storage`: persistent tdl state, useful for long-running archive jobs.
- `--ntp`: use when clock drift causes Telegram MTProto message ID errors.
- `--delay`: delay between tasks, useful to reduce pressure on account/network.
- `--reconnect-timeout`: Telegram client reconnection backoff timeout.

Global config flags are not persisted by tdl. If a proxy is required, include `--proxy` in every command in the workflow: `login`, `chat ls`, and `dl`.

When downloads fail with flood, rate-limit, or unstable network symptoms, retry with lower `-t` and `-l`, add `--delay` if appropriate, or use a proxy if the user already has one.

Do not run multiple `tdl` network commands concurrently against the same namespace/storage. If tdl reports "Current database is used by another process", wait for the other process to finish, or intentionally use a separate namespace/storage.

If a SOCKS proxy is configured but not reachable, tdl may report `socks connect ... connection refused`. Treat that as a local proxy availability or port issue and ask the user to verify the proxy app and port.

For Docker, mount both config and download directories so sessions and outputs persist. If the proxy runs on the host as `localhost`, Docker may need host networking so the container can reach it:

```bash
docker run --rm -it --network host iyear/tdl --proxy socks5://localhost:1080 version
```
