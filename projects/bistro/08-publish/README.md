# 08 Publish: bistro

What goes here: what was staged to go out, and a log of every send. The copies at the destinations
are mirrors. The product stays `../05-glossary/glossary.md`.

| File | Required | How it gets here |
|---|---|---|
| `outbox/` | once staged | `tools/stage-publish.py bistro` copies the files named in `publish: files:` here, each with a "do not edit" note, plus a `README.md` with every file's hash. |
| `publish-log.md` | once staged | The same script adds one row per destination. An empty `sent` cell means staged, not out. `--sent` fills it after each send. |

Destinations, the file list and the contact live in the `publish:` block of `../project.yaml`.
Only a glossary at `stage: trial` or `adopted` is sent.

Contract: [../../../factory/steps/08-publish/CONTEXT.md](../../../factory/steps/08-publish/CONTEXT.md)
