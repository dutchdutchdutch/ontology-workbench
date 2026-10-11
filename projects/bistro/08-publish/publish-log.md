# Publish log: bistro

One row per destination per send. Written by `tools/stage-publish.py`; Claude
fills `sent` and `receipt` after each send with `--sent`. A row with an empty `sent`
cell is staged and not yet out. `superseded` means a newer staging replaced it
before it was sent. Rows are never removed.

| # | staged | sent | from | stage | destination | fingerprint | receipt |
|---|---|---|---|---|---|---|---|
| 1 | 2026-10-10 | 2026-10-10 | v2 | trial | folder:08-publish/sent-example | 6fb559ef8b2e | copied to 08-publish/sent-example/Linden Street Bistro vocabulary/ on 2026-10-10 |
