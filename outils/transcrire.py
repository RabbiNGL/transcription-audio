"""Transcrit chaque fichier audio de entree/ qui n'a pas encore de texte dans sortie/.

Produit pour chaque fichier :
  sortie/<nom>.txt      le texte seul, en paragraphes
  sortie/<nom>.horo.txt le texte avec les minutages [mm:ss]
"""
import os
import sys
from pathlib import Path

from faster_whisper import WhisperModel

ENTREE = Path("entree")
SORTIE = Path("sortie")
EXTENSIONS = {".mp3", ".m4a", ".wav", ".ogg", ".opus", ".flac", ".mp4", ".mov", ".webm"}
MODELE = os.environ.get("MODELE", "large-v3-turbo")
LANGUE = os.environ.get("LANGUE", "fr") or None


def minutage(secondes: float) -> str:
    m, s = divmod(int(secondes), 60)
    h, m = divmod(m, 60)
    return f"{h:d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def main() -> int:
    SORTIE.mkdir(exist_ok=True)
    seul = os.environ.get("FICHIER")
    a_faire = [
        f for f in sorted(ENTREE.iterdir())
        if f.suffix.lower() in EXTENSIONS and not (SORTIE / f"{f.stem}.txt").exists()
        and (not seul or f.name == seul)
    ]
    if not a_faire:
        print("Rien à transcrire.")
        return 0

    print(f"Modèle : {MODELE}, langue : {LANGUE or 'auto'}")
    modele = WhisperModel(MODELE, device="cpu", compute_type="int8")

    for fichier in a_faire:
        print(f"Transcription de {fichier.name} ...", flush=True)
        segments, info = modele.transcribe(
            str(fichier), language=LANGUE, vad_filter=True, beam_size=5,
        )
        lignes, paragraphe, texte = [], [], []
        dernier = 0.0
        for seg in segments:
            t = seg.text.strip()
            if not t:
                continue
            lignes.append(f"[{minutage(seg.start)}] {t}")
            # Nouveau paragraphe après un silence de plus de 2 secondes
            if paragraphe and seg.start - dernier > 2:
                texte.append(" ".join(paragraphe))
                paragraphe = []
            paragraphe.append(t)
            dernier = seg.end
        if paragraphe:
            texte.append(" ".join(paragraphe))

        (SORTIE / f"{fichier.stem}.txt").write_text("\n\n".join(texte) + "\n", encoding="utf-8")
        (SORTIE / f"{fichier.stem}.horo.txt").write_text("\n".join(lignes) + "\n", encoding="utf-8")
        print(f"  ok, durée {minutage(info.duration)}, {len(lignes)} segments")
    return 0


if __name__ == "__main__":
    sys.exit(main())
