#!/bin/bash
# Assemble les débats dont tous les morceaux sont transcrits, et liste ceux qui viennent d'être assemblés.
cd "$(dirname "$0")/.."
git pull -q --rebase origin main
for nom in $(ls entree/*__*.mp3 2>/dev/null | sed -E 's#entree/(.*)__[0-9]{3}\.mp3#\1#' | sort -u); do
  [ -f "sortie/$nom.txt" ] && continue
  total=$(ls entree/${nom}__*.mp3 | wc -l)
  faits=$(ls sortie/${nom}__[0-9][0-9][0-9].txt 2>/dev/null | wc -l)
  if [ "$total" -eq "$faits" ]; then
    python3 outils/assembler.py "$nom" > /dev/null && echo "$nom"
  fi
done
