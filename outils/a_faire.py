"""Écrit la liste JSON des fichiers de entree/ qui n'ont pas encore de texte dans sortie/."""
import json
from pathlib import Path

EXTENSIONS = {".mp3", ".m4a", ".wav", ".ogg", ".opus", ".flac", ".mp4", ".mov", ".webm"}

fichiers = [
    f.name for f in sorted(Path("entree").iterdir())
    if f.suffix.lower() in EXTENSIONS and not (Path("sortie") / f"{f.stem}.txt").exists()
]
print("fichiers=" + json.dumps(fichiers))
