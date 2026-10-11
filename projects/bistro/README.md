# Linden Street Bistro

A worked example of every step, from raw sources to a published, rendered and sent glossary.
The bistro, its people (Theo, the floor manager; Rosa, the head chef; Priya, who builds the
booking and ordering app) and every source are made up. Everything project-specific is in
[project.yaml](project.yaml).

- Project: `bistro`
- Started: `2026-09-01`
- Current draft: `v2`
- Rulings: `4`

## Why a restaurant needs its own glossary

Restaurants run on everyday words that mean something else everywhere else. Staff learn them in
their first week. Software built for them, and any AI agent helping with it, gets them wrong.

| Word | In this restaurant | Everywhere else |
|---|---|---|
| cover | one guest who sat down, counted | a lid, an insurance policy, a song |
| ticket | the kitchen's printed copy of an order | an admission ticket, a support ticket |
| check | the bill | an inspection; in the app, a validation step |
| fire | start cooking a course now | burn something; dismiss someone |
| 86'd | sold out for the rest of the service | a number |
| server | the person looking after your table | a computer |
| walk-in | a party with no reservation, and also the cold room | a closet |
| table | where a party sits | a database table, in the app's code |
| turn | one party seated, served and gone | a change of direction |
| the pass | the counter where plates wait for the expo | a permit; a mountain road |

The sample shows the method catching these. The app said "customer", "booking" and
"kitchen_order"; the floor and the kitchen said "guest", "reservation" and "ticket". "Server
timeout" froze the floor on a Friday because staff read it as a person. Four rulings settled what
the evidence could not.

## Read it in this order

1. [00-sources/raw/](00-sources/raw/): three staff documents, seven app issues, seven pull requests.
2. [01-terms/](01-terms/): one inventory per source, every row with a verbatim quote, and the
   signed review.
3. [02-delta/delta-report.md](02-delta/delta-report.md): the sources against each other.
4. [03-merge/conflicts.md](03-merge/conflicts.md): the reading list of conflicts.
5. [04-draft/v1/verification-queue.md](04-draft/v1/verification-queue.md): four questions for the
   experts, then their answers in [decisions/](decisions/), then [04-draft/v2/](04-draft/v2/).
6. [05-glossary/glossary.md](05-glossary/glossary.md): the product. Start with
   [core-terms.md](05-glossary/core-terms.md).
7. [06-ontology/ontology.html](06-ontology/ontology.html),
   [07-streams/value-streams.html](07-streams/value-streams.html) and
   [07-streams/processes.html](07-streams/processes.html): open them in a browser.
8. [08-publish/](08-publish/): the staged outbox, the publish log, a sent copy and the review
   package.

The glossary is at `stage: trial` with one open row in
[05-glossary/feedback.md](05-glossary/feedback.md), so `tools/status.sh bistro` still has
something to say.

## Where things stand

Status is the filesystem. A step is done when its file exists. `tools/status.sh <name>` prints it.

| Step | Done when this exists | Contract |
|---|---|---|
| 00 Sources | `00-sources/manifest.md` | [../../factory/steps/00-sources/CONTEXT.md](../../factory/steps/00-sources/CONTEXT.md) |
| 01 Terms | `01-terms/inventory-*.md` and `review.md` | [../../factory/steps/01-terms/CONTEXT.md](../../factory/steps/01-terms/CONTEXT.md) |
| 02 Delta | `02-delta/delta-report.md`, or `skipped.md` | [../../factory/steps/02-delta/CONTEXT.md](../../factory/steps/02-delta/CONTEXT.md) |
| 03 Merge | `03-merge/inventory-merged.md`, or `skipped.md` | [../../factory/steps/03-merge/CONTEXT.md](../../factory/steps/03-merge/CONTEXT.md) |
| 04 Draft | `04-draft/v<n>/glossary.md` | [../../factory/steps/04-draft/CONTEXT.md](../../factory/steps/04-draft/CONTEXT.md) |
| 05 Glossary | `05-glossary/glossary.md` | [../../factory/steps/05-glossary/CONTEXT.md](../../factory/steps/05-glossary/CONTEXT.md) |
| 06 Ontology | `06-ontology/ontology.html`, or `skipped.md` | [../../factory/steps/06-ontology/CONTEXT.md](../../factory/steps/06-ontology/CONTEXT.md) |
| 07 Streams | `07-streams/value-streams.html` and a signed stream file, or `skipped.md`. Optional | [../../factory/steps/07-streams/CONTEXT.md](../../factory/steps/07-streams/CONTEXT.md) |
| 08 Publish | `08-publish/publish-log.md` with a `sent` date for every destination | [../../factory/steps/08-publish/CONTEXT.md](../../factory/steps/08-publish/CONTEXT.md) |
| decisions | one `NNN-<slug>.md` per ruling | [../../factory/steps/decisions/CONTEXT.md](../../factory/steps/decisions/CONTEXT.md) |

Files starting with `_` and ending in `.template.md` are blank scaffolds. Copy one, drop the
underscore and the `.template` part, and fill it in. A scaffold sitting untouched means the step
has not started.

Superseded files are never deleted. Move them to `_archive/` in this folder, named with the
version they came from: `glossary-v3.md`.

## Notes

- Step 00 is simulated. A real project pulls through the connected servers; here the files in
  `00-sources/raw/` were written by hand, and every link reads `EXAMPLE-not-a-real-link`.
- Step 08 sends to a local folder, `08-publish/sent-example/`, so the whole loop runs without an
  account anywhere. A real project names a shared drive or a repository.
- The review zip, `08-publish/bistro-review.zip`, is rebuilt by `tools/build-review.py` and is
  not committed.
