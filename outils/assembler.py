"""Recolle les morceaux nom__000, nom__001... d'un débat en un seul texte.

Usage : python outils/assembler.py <nom> [durée d'un morceau en secondes, 300 par défaut]
Écrit sortie/<nom>.txt et sortie/<nom>.horo.txt (minutages recalés sur la vidéo entière).
"""
import re
import sys
from pathlib import Path

SORTIE = Path("sortie")


def minutage(s: int) -> str:
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return f"{h:d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def secondes(t: str) -> int:
    parts = [int(x) for x in t.split(":")]
    total = 0
    for p in parts:
        total = total * 60 + p
    return total


def main() -> None:
    nom = sys.argv[1]
    duree = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    textes, horos = [], []
    morceaux = sorted(SORTIE.glob(f"{nom}__[0-9][0-9][0-9].txt"))
    for f in morceaux:
        n = int(f.stem.rsplit("__", 1)[1])
        textes.append(f.read_text(encoding="utf-8").strip())
        for ligne in (SORTIE / f"{f.stem}.horo.txt").read_text(encoding="utf-8").splitlines():
            m = re.match(r"\[([\d:]+)\] (.*)", ligne)
            if m:
                horos.append(f"[{minutage(secondes(m.group(1)) + n * duree)}] {m.group(2)}")
    (SORTIE / f"{nom}.txt").write_text("\n\n".join(textes) + "\n", encoding="utf-8")
    (SORTIE / f"{nom}.horo.txt").write_text("\n".join(horos) + "\n", encoding="utf-8")
    print(f"{len(morceaux)} morceaux assemblés, {len(horos)} segments")


if __name__ == "__main__":
    main()
