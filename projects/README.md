# projects

One folder per project. Everything specific to that product lives here and nowhere else.
`factory/` holds the method; this folder holds the work.

## Start a new project

```bash
tools/new-project.sh <name>
```

Run it in a terminal, from the workspace root. Use a short lowercase name with hyphens:
`my-bistro`, not `Linden Street Bistro`. It copies [../_templates/project/](../_templates/project/)
to `projects/<name>/`, refuses if the folder exists, and puts the name and today's date into
`project.yaml` and `README.md`.

By hand, without the script: create the folder `projects/<name>/`, copy everything inside
`_templates/project/` into it, and write the name and today's date into `project.yaml` and
`README.md` where the angle-bracket placeholders are. The result is the same.

Then fill the rest of `projects/<name>/project.yaml` and start at
[../factory/steps/00-sources/CONTEXT.md](../factory/steps/00-sources/CONTEXT.md).

## The worked example

[bistro/](bistro/) is a fictional restaurant run through every step. Read it before your first
project: each step's output is there, at a size you can read in an hour.

## What a project folder looks like

```
projects/<name>/
  README.md            cover sheet
  project.yaml         sources, cutoffs, targets, people. The only home for product values
  00-sources/          manifest.md, raw/<source>/
  01-terms/            inventory-<source>.md, review.md
  02-delta/            delta-report.md or skipped.md; drift-report.md in drift mode
  03-merge/            inventory-merged.md, conflicts.md, or skipped.md
  04-draft/            v1/, v2/, ... each with glossary.md, conflict-report.md, verification-queue.md
  05-glossary/         glossary.md, core-terms.md, about-core-terms.md, taxonomy.md, backlog.md;
                       feedback.md from trial on
  06-ontology/         ontology-data.js, ontology.html, ontology-machine.json, or skipped.md
  07-streams/          <stream>.md, <process>.md, their generated pages, or skipped.md. Optional
  08-publish/          outbox/, publish-log.md
  decisions/           NNN-<slug>.md, one per ruling
  _archive/            superseded files, named with the version they came from
```

## Reading status

Status is the filesystem. A step is done when its output file exists. `tools/status.sh <name>`
prints the table; the table in each project's `README.md` says which file marks which step.

A `skipped.md` in a step folder means the step was considered and passed through, with the reason
inside. Files that start with `_` and end in `.template.md` are unfilled scaffolds. Neither is work.

## Superseded files

Never delete project work. Move it to `projects/<name>/_archive/` named with the version it came
from: `glossary-v3.md`. Nothing in an archive is an input to any step.

Back to [../CLAUDE.md](../CLAUDE.md).
