# Coverage: bistro

From `projects/bistro/04-draft/v2/glossary.md`, by `tools/check-glossary.py`. A report, never a gate: see "Built version over version" in `factory/rules/entry-format.md`.

| Measure | Count |
|---|---|
| Entries | 27 |
| Entries with no valid type | 0 |
| Relation lines | 46 |
| Lines with a kind | 45 |
| Lines without a kind | 1 |
| Stand-alone entries (no relation either way) | 1 |
| Errors (rules broken) | 0 |
| Warnings (findings) | 1 |

## Entries by type

| Type | Entries |
|---|---|
| `action` | 2 |
| `document` | 3 |
| `entity` | 11 |
| `event` | 4 |
| `metric` | 2 |
| `role` | 4 |
| `state` | 1 |

## Stand-alone entries

Family meal

## Against the previous version

| Measure | v1 | v2 | Why it moved |
|---|---|---|---|
| Entries | 25 | 27 | Ruling 002 adds Cover; ruling 003 splits the Walk-in gap into two entries |
| Relation lines | 42 | 46 | Cover and the two walk-ins bring their lines |
| Lines without a kind | 1 | 1 | Comp's "reduces [[Check]]": no kind fits well yet |
| Stand-alone entries | 2 | 1 | The Walk-in gap is gone. Only Family meal is left; it is in the question pack |
| Warnings | 0 | 1 | Party now has one `is_a` child, Walk-in (party). Kept: a walk-in really is a party |
| Open question-pack items | 0 | 1 | Family meal `precedes` [[Service]] |
