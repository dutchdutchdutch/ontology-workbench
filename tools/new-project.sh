#!/usr/bin/env bash
# Instantiate a project by copying _templates/project to projects/<name>.
# Usage, from the workspace root:  tools/new-project.sh <name>
set -euo pipefail
cd "$(dirname "$0")/.."

name="${1:-}"
if [ -z "$name" ]; then
  echo "usage: tools/new-project.sh <name>   (short, lowercase, hyphens: my-bistro)" >&2
  exit 2
fi
if ! [[ "$name" =~ ^[a-z0-9][a-z0-9-]*$ ]]; then
  echo "name must be lowercase letters, digits and hyphens: $name" >&2
  exit 2
fi
dest="projects/$name"
if [ -e "$dest" ]; then
  echo "$dest already exists. Refusing to overwrite." >&2
  exit 1
fi

cp -R _templates/project "$dest"
today="$(date +%F)"

perl -pi -e "s/^name: <name>.*/name: $name/; s/^started: <YYYY-MM-DD>/started: $today/" "$dest/project.yaml"
perl -pi -e "s/^# <Project name>/# $name/; s/^- Project: \`<name>\`/- Project: \`$name\`/; s/^- Started: \`<YYYY-MM-DD>\`/- Started: \`$today\`/" "$dest/README.md"
for f in "$dest"/*/README.md; do
  perl -pi -e "s/<project>/$name/g" "$f"
done

echo "Created $dest"
echo "Next: fill $dest/project.yaml, then open factory/steps/00-sources/CONTEXT.md"
