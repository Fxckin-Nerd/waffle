# WAFFLE

Interactive CLI tool for testing how web servers and WAFs handle alternate request styles, protocol flags, headers, and encoded path variants.

Use this only on systems you own or are explicitly authorized to test.

## What This Tool Is For

WAFFLE helps you run repeatable HTTP request variations against a target path (for example `/admin`) to validate:

- WAF normalization behavior
- Path parsing edge cases
- Header handling differences
- HTTP version and TLS behavior differences
- Request parsing tolerance (spacing, tab-separated raw requests, chunked slow-send style)

## Requirements

- Python 3.8+
- `curl` (used by several modes)
- `nc` / `netcat` (required for raw request mode)
- `openssl` (required for TLS mode when selecting OpenSSL)
- `wget` (required for wget mode)

## Run

```bash
python3 waffle.py
```

Or:

```bash
./waffle.py
```

To see full documentation:

```bash
python3 waffle.py --help
```

## Quick Flow

1. Enter base URL (example: `https://example.com`)
2. Enter directory/path segment to test (example: `admin`)
3. Select cURL HTTP mode
4. Select request type
5. Select directory handling/encoding mode
6. Choose verbose output and user agent
7. WAFFLE prints and runs the generated command
8. After command completion, WAFFLE returns to `Select cURL HTTP mode`

## Menu Options

### 1) cURL HTTP Mode

- `1. http` -> uses `curl -0` (HTTP/1.0 behavior)
- `2. http1.1` -> uses `curl --http1.1`
- `3. http2` -> uses `curl --http2`
- `4. no http (default)` -> no explicit HTTP version flag

### 2) Request Type

- `1. Standard (curl)`
  Sends `curl -I <target>` with selected HTTP mode, optional user-agent, and optional verbose output.

- `2. WebDAV method (curl -X)`
  Sends `curl -X <METHOD> <target>`. Methods menu includes:
  `PROPFIND`, `LOCK`, `UNLOCK`, `TRACK`, `TRACE`, `OPTIONS`, `GET`.

- `3. Raw request line format (echo | nc)`
  Builds a raw HTTP request and sends via netcat. Lets you vary request-line formatting and optionally send small chunks with delays.

- `4. TLS fingerprint modification (curl/openssl)`
  Uses a fixed TLS 1.2 cipher preference (`ECDHE-RSA-AES128-GCM-SHA256`) with either:
  - `curl --tls-max 1.2 --ciphers ...`
  - `openssl s_client ... -cipher ...`

- `5. Header test (curl -H)`
  Sends one or many custom headers via repeated `-H` flags.

- `6. wget mode`
  Runs wget-based probes:
  - `simple`: `wget --no-check-certificate --spider ...`
  - `headers`: adds one or many custom `--header="Key: Value"`

- `7. Back`
  Returns to cURL HTTP mode selection.

### 3) Raw Request Sub-Options

If you select `Raw request line format`:

- Enter destination port (example: `443`)
- Select request-line format:
  - `standard`: `GET /path HTTP/1.1`
  - `extra-spaces`: `GET  /path  HTTP/1.1`
  - `tab-separated`: `GET\t/path\tHTTP/1.1`
- Select slow-send mode:
  - `No`: sends one raw request via `nc`
  - `Yes`: splits request line into small chunks (2 chars each), sends each chunk with `timeout`, and optional sleep between chunks

When slow-send is enabled, WAFFLE prompts for:

- `timeout duration` (default: `2` seconds)
- `sleep duration` between chunks (default: `0` seconds)

### 4) Header Input Modes

- `Single header`: one `name/value` pair
- `Multi header`: repeated `name/value` pairs until `done`

These are used by:

- Header test request type
- wget headers mode

### 5) Directory Handling / Encoding Modes

These transform the directory text before building `<base>/<directory>`:

- `1. standard` -> unchanged
- `2. ascii encoded directory` -> percent-encodes each char (example `admin` -> `%61%64%6D%69%6E`)
- `3. ascii double encoded directory` -> percent-encodes the already encoded string
- `4. enclosed alphanumeric` -> enclosed Unicode-style letters
- `5. homoglyphs` -> lookalike letters from other scripts
- `6. invisible characters` -> inserts zero-width style chars
- `7. non-breaking characters` -> uses non-breaking spaces/chars
- `8. control characters` -> includes control-byte style variants
- `9. fullwidth characters` -> fullwidth character variants
- `10. variable spacing` -> uneven spacing variants
- `11. special symbols` -> symbol substitutions
- `12. pictograph characters` -> pictograph/symbol substitutions
- `13. whitespace variants` -> alternate Unicode whitespace
- `14. combining characters` -> combining-mark variants
- `15. path traversal` -> traversal style string (for example `../../../admin`)
- `16. Back` -> return to request-type menu

### 6) Output Menu

- Verbose prompt: `Do you want verbose output? (y/N)`
  - `y` enables `-v` / debug output where supported
  - `N` or Enter keeps normal output

### 7) User-Agent Menu

Options:

- Windows 10 Chrome
- Windows 11 Chrome
- Mac M1 Safari
- Mac M2 Safari
- Linux Firefox
- Random (from preset list)
- Custom (manual string)
- Default (no User-Agent override)

## Navigation Behavior

- `Back` options in submenus return to the previous menu
- After command execution, WAFFLE now loops back to `Select cURL HTTP mode`
- `Ctrl+C` exits gracefully

## Example Sessions

### Example 1: Standard HEAD Check

```text
$ python3 waffle.py
Enter website URL: https://example.com
Enter directory to test: admin

Select cURL HTTP mode: 2 (http1.1)
Select request type: 1 (Standard)
Select directory handling mode: 1 (standard)
Do you want verbose output? n
Select User Agent: 8 (Default)

Running command:
curl --http1.1 -I https://example.com/admin
```

### Example 2: Raw Request With Slow Send

```text
Enter website URL: https://example.com
Enter directory to test: admin

Select cURL HTTP mode: 2 (http1.1)
Select request type: 3 (Raw request line format)
Enter port number: 443
Select raw request format: 2 (Extra spaces)
Do you want to use slow send? 2 (Yes)
Enter timeout duration in seconds: 2
Enter sleep duration between requests in seconds: 0.5
Select directory handling mode: 1 (standard)
Do you want verbose output? n
Select User Agent: 6 (Random)

Running command:
[1/N] echo -e "..." | timeout 2 nc example.com 443
...
```

### Example 3: Header Test With Multiple Headers

```text
Enter website URL: https://example.com
Enter directory to test: admin

Select cURL HTTP mode: 3 (http2)
Select request type: 5 (Header test)
Select header test type: 2 (Multi header)
Header name: X-Forwarded-For
Header value: 127.0.0.1
Header name: X-Original-URL
Header value: /admin
Header name: done
Select directory handling mode: 2 (ascii encoded)
Do you want verbose output? y
Select User Agent: 2 (Windows 11 Chrome)

Running command:
curl --http2 -H X-Forwarded-For: 127.0.0.1 -H X-Original-URL: /admin -I -A "..." -v https://example.com/%61%64%6D%69%6E
```

## Notes

- WAFFLE prints the command before executing it, so you can see exactly what is being sent.
- If a required external tool is missing, WAFFLE prints a clear error message.
- URL building trims trailing slash from base URL and leading/trailing slash from directory before joining.

## Project Layout

```text
waffle/
|- waffle.py
|- menus/
|- utils/
|- encoders/
|- commands/
```

## Support

If you find WAFFLE useful and want to support development:

**Bitcoin (BTC):**
```
3DMmRsSRy2Tw81LP2WAGXxRUePaFU2hQR4
```

## License

MIT — see [LICENSE](LICENSE) file. Use freely in any project (commercial or otherwise), but please include the copyright notice.

