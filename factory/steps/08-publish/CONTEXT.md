# Step 08: Publish

Send the glossary, and the pictures drawn from it, to the places where people work: the root of
the shared drive, the code repository, a shared folder. Keep a log of what was staged, what was
sent, where, and in what exact form. Everyone then reads one definition set, and anyone can tell
which version they hold.

Folders 05 to 07 are the workbench. This step is the shop window. Nobody outside the workspace
reads from 05, 06 or 07 directly: during `review` the wording changes in place, and a reader of
the workbench would see edits nobody signed.

This is the second step that touches the network. Step 00 brings words in; step 08 sends them out.
No script does either: Claude sends through the connected servers or git, and the script only
builds and records.

## Precondition

- `05-glossary/glossary.md` is at `stage: trial` or `stage: adopted`. A glossary at `review` is
  read in place by its reviewers and is not sent.
- `project.yaml` has a `publish:` block with at least one destination.
- Every picture listed in `publish: files:` is newer than what it was drawn from: `ontology.html`
  newer than `glossary.md`, `value-streams.html` newer than the step 06 data and every stream file.
- Every stream file is signed (`reviewed:` holds a date), when `streams` is listed.

`tools/stage-publish.py` checks all four and stages nothing if one fails.

## Inputs

- `projects/<p>/project.yaml`, the `publish:` block:

  ```yaml
  publish:
    folder: <folder name>       # the folder at every destination. Each project picks its own
    contact: <name>             # who receives corrections; printed in every copy
    files: [glossary, core-terms, about-core-terms, taxonomy, ontology]
    destinations:               # one per line: <kind> <where>
      - drive <shared drive or folder id>
      - repo <owner>/<repo>
      - folder <path>           # a synced or shared folder
  ```

  `files` names come from the script: `glossary`, `core-terms`, `about-core-terms`, `taxonomy`,
  `backlog`, `ontology`, `ontology-machine`, `streams`, `processes`. Leave it out and the four step 05 reading
  files are sent. `ontology-machine` sends `06-ontology/ontology-machine.json`, the file an agent
  outside the workspace reads; nobody outside reads step 06 directly, so this is its only way
  out.
- The files themselves, in `05-glossary/`, `06-ontology/` and `07-streams/`.
- `tools/stage-publish.py`.

## Process

1. **Stage.** Run `tools/stage-publish.py <p>`. It checks the precondition, empties
   `08-publish/outbox/`, copies each listed file into it with a one-line note ("published copy,
   do not edit, send changes to <contact>"), writes `outbox/README.md` with every file's hash, and
   adds one row per destination to `08-publish/publish-log.md` with an empty `sent` cell. A newer
   staging marks the older unsent rows `superseded`.
2. **Checkpoint.** The lead reads the staged rows and the outbox README: right version, right files,
   right places. Nothing leaves before this.
3. **Send.** Claude copies the whole outbox into `<folder>` at each destination, replacing what is
   there.
   - `repo`: a branch and a pull request in that repository, so its owners approve the change in
     their usual way. The receipt is the pull request link.
   - `drive`: through the Drive connector, into `<folder>` at the root of the shared drive. The
     receipt is the folder link.
   - `folder`: a plain copy. The receipt is the path.
   A destination that cannot be reached stays staged, with the reason in the receipt cell, the
   same way step 00 records a source it could not pull.
4. **Record.** For each destination reached, run
   `tools/stage-publish.py <p> --sent <kind>:<where> "<receipt>"`. It fills `sent` with today's date.
5. **Check, on a schedule.** Download or clone each destination's folder and run
   `tools/stage-publish.py <p> --verify <kind>:<where> <local folder>`. It compares the copy with the
   fingerprint of the last send, and names any file edited, added or missing there. An edit found
   there is a finding: copy what it says into `05-glossary/feedback.md`, then re-send. Never edit
   the glossary to match a copy.

Rules:

- A published copy is never an input to any step. It is a mirror with a note on top. The one
  product is still `05-glossary/glossary.md`.
- Send the whole outbox or nothing. A destination never holds files from two versions.
- Never edit a file in the outbox or at a destination. Change the source, re-run the step that
  makes it, and stage again.
- Re-publishing step 05 returns the glossary to `review`, so a new send waits for `trial` again.
  The copies already out stay as they are until then, and the log says which version they hold.

## Before trial: a review package

A glossary at `review` is not sent through this step, but its readers still need something to
open. `tools/build-review.py <p>` builds one: `08-publish/review/`, a folder with an `index.html`
and four pages (the key terms, the ontology, the value streams, the processes), each next to its
data, plus `08-publish/<p>-review.zip` to send. It opens with no tools and no network beyond fonts.

- **Key terms only.** The package holds the core set, the same terms the ontology draws. It is for
  leadership and first readers; area specialists review the full glossary separately, in its file.
- **No stage gate, no log row.** It goes to people, not to a destination, and nothing it holds is
  final. Unsigned streams and processes are included and marked "draft" on the index.
- **One gate: freshness.** The script stops if a picture is older than what it was drawn from.
- **Rebuilt, never edited.** The folder is replaced on every build. The copied data files gain
  one line, `const reviewHome`, which the pages read to show a link back to the index.
- **Same pages, same panel.** The pages carry the closed Machine detail section, as in step 06.
  The key-terms page shows each term's status and is-a parent.

Corrections that come back go where every correction goes: `feedback.md` once at `trial`, a ruling
in `decisions/` before that.

## Outputs

In `projects/<p>/08-publish/`:

| File | Required | What it is |
|---|---|---|
| `outbox/` | yes | The exact files staged for the last send, with `README.md` listing each one's hash. Replaced on every staging; git keeps the history. |
| `review/`, `<p>-review.zip` | before trial, on request | The review package: `index.html` and the four pages. Replaced on every build. |
| `publish-log.md` | yes | One row per destination per send: `#`, `staged`, `sent`, `from`, `stage`, `destination`, `fingerprint`, `receipt`. An empty `sent` is staged and not yet out. Rows are never removed. |

## Human checkpoint

The lead approves the staged rows before anything is sent (process step 2), and confirms each receipt
afterwards. For a `repo` destination, the repository's owners approve the pull request as well.

## Status signal

Step 08 is done when every destination's latest row has a date in `sent`, and its `from` matches
the `published_from:` of `05-glossary/glossary.md`. An empty `sent` means staged, not out. A `from`
older than the glossary means the copies out there are behind.

## Back to

[../../../CLAUDE.md](../../../CLAUDE.md)
