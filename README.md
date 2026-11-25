# Transcription audio

Dépôt temporaire. Sert à transcrire les débats
enregistrés par Rabbi (dossier Synology `Document/Religion`).

## Fonctionnement

1. Extraire le son de la vidéo puis le découper en morceaux de 5 minutes :

   ```
   ffmpeg -i video.mp4 -vn -ac 1 -ar 16000 -b:a 32k nom.mp3
   ffmpeg -i nom.mp3 -f segment -segment_time 300 -c copy entree/nom__%03d.mp3
   ```

2. Pousser sur `main`. GitHub Actions transcrit chaque morceau dans
   un job séparé, jusqu'à 20 en parallèle (Whisper `large-v3-turbo`, français), et pousse
   `sortie/nom__NNN.txt` et `sortie/nom__NNN.horo.txt`. Un débat d'1 h 30 prend environ
   5 à 6 minutes.

3. Recoller les morceaux :

   ```
   python outils/assembler.py nom
   ```

   Produit `sortie/nom.txt` (texte en paragraphes) et `sortie/nom.horo.txt` (minutage
   recalé sur la vidéo entière). Supprimer ensuite les morceaux de `entree/` et `sortie/`.

Relancer à la main (ou changer de modèle) : onglet Actions, « transcription », « Run workflow ».

