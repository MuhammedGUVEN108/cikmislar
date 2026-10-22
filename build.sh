#!/bin/sh
set -eu
cd -- "$(dirname -- "$0")"

# Publish only the files used by the study site.
mkdir -p dist
cp index.html soru-arsivi.html dist/
for directory in css js assets; do
  mkdir -p "dist/$directory"
  cp -R "$directory/." "dist/$directory/"
done
printf '%s\n' 'Site files ready in dist/'
