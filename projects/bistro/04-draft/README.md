# 04 Draft: bistro

What goes here: one folder per draft version. `v1` is the first draft; every run after a round
of rulings writes the next `v<n>`. Older versions are never edited.

| File, in `v<n>/` | Required | How it gets here |
|---|---|---|
| `glossary.md` | yes | Step 04 writes it. Header lists the rulings applied. |
| `conflict-report.md` | yes | Step 04 writes it. |
| `verification-queue.md` | yes | Step 04 writes it. The questions for the experts; each answer becomes a file in `../decisions/`. |
| `blocked-by-rulings.md` | only on stop | Step 04 writes this instead when a draft would contradict a ruling. |
| `core-terms.md` | optional | When a review round is about the core set. |
| `contested-term-probes.md` | optional | Deep probes of a few terms. |

The entry shape lives once, in
[../../../factory/rules/entry-format.md](../../../factory/rules/entry-format.md).

Contract: [../../../factory/steps/04-draft/CONTEXT.md](../../../factory/steps/04-draft/CONTEXT.md)
