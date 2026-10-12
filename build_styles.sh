#!/usr/bin/env bash
set -euo pipefail

project_dir="$(cd "$(dirname "$0")" && pwd)"
tailwind_tmp="$(mktemp)"
trap 'rm -f "$tailwind_tmp"' EXIT

cd "$project_dir"
npx --yes tailwindcss@3.4.17 \
  --config tailwind.config.js \
  --input assets/tailwind.input.css \
  --output "$tailwind_tmp" \
  --minify

cat "$tailwind_tmp" \
  assets/chapter-practice.css \
  assets/engineering-practice.css \
  assets/engineering-chapters.css \
  assets/written-practice.css \
  assets/engineering-archive.css \
  > assets/site.css

cp assets/site.css public/assets/site.css
cp assets/site.css web/assets/site.css
