# 12 — Garder, vérifier et partager son film

**But :** refaire un MP4 à la main et comprendre ce qu’un commit conserve.

## A. Exporter le montage final dans Blender

1. Ouvre une copie du dossier `ath`, avec son MP4, puis le `.blend`.
2. Choisis **06 — Vol avec ATH et son**. Cette scène possède déjà une bande vidéo et le son intégré.
3. Dans **Output Properties**, vérifie 1920 × 1080, 100 %, 30 fps, début 1, fin 1217.
4. Choisis un **nouveau chemin de sortie**, par exemple `resultats/mon-film.mp4`. Ne remplace jamais le MP4 utilisé comme entrée de la scène.
5. Choisis **FFmpeg Video**, conteneur **MPEG-4**, codec vidéo **H.264**, codec audio **AAC**.
6. Lance **Render → Render Animation**. Attends la fin puis ouvre le MP4 dans un lecteur externe.

**Je vérifie :** le début, l’éjection et la fin sont présents; le son suit les images; la durée est d’environ 40,57 s. Cet export Blender peut réencoder son et image : il n’est pas forcément identique octet par octet au MP4 publié, dont l’audio avait été copié sans réencodage.

## B. Refaire les images 3D

Pour modifier la fusée ou la caméra, choisis la scène 03. Pour un essai, règle seulement cinq images, par exemple 650–654, et choisis PNG dans un dossier vide. Lance Render Animation. Une fois l’essai correct, rétablis 1–1217.

Une suite d’images est pratique : si le calcul s’arrête, les images déjà terminées restent disponibles. On les assemble ensuite dans le Sequencer avec **Add → Image/Sequence**, à 30 fps, puis on ajoute le son. Attention : les images brutes de la scène 03 n’ont pas les panneaux ATH. Ceux-ci viennent du chapitre 11.

## C. Vérifier comme un détective

- Ouvre réellement le fichier exporté, pas seulement le projet.
- Compare une image de montée, de récupération et de contact.
- Vérifie les accents, les unités et les crédits.
- Écoute sans autre lecteur lancé; recherche les doubles pistes.
- Ferme puis rouvre le `.blend` depuis son nouveau dossier. La scène 06 doit retrouver son MP4 voisin.
- Garde une petite note avec le logiciel, la version, la durée et le changement effectué.

Les vérifications automatiques archivées décodent toutes les images et comparent certaines empreintes. Elles complètent le visionnage, sans remplacer ton appréciation du film.

## D. Préparer les Markdown avant le commit

Un **commit** est une photo datée de l’état du dossier de travail. Avant de la prendre, mets à jour README, ROADMAP, CHANGELOG et la notice de ce que tu modifies. Écris ce qui a réellement changé et ce que tu as vérifié. Ne coche pas une tâche seulement parce que tu as commencé.

Avec une application Git graphique, examine la liste des fichiers modifiés, puis leur différence. Sélectionne seulement ceux de ton étape, écris un résumé clair, crée le commit et publie-le avec **Push**. Les vidéos et scènes restent des fichiers volumineux; aucune pièce individuelle ne doit dépasser la limite acceptée par le dépôt.

Après l’envoi, ouvre GitHub, retrouve le commit et vérifie les liens du README. Un commit local n’est pas encore une publication. Un message d’erreur d’identifiants ne veut pas dire que ta vidéo est mauvaise.

**Ne force pas l’envoi pour contourner une erreur.** Si Git signale une propriété de dossier différente, utilise uniquement l’exception ciblée fournie pour ce dossier de confiance; ne désactive pas globalement les contrôles avec un joker. Un adulte peut aider pour le compte, l’authentification et le dépôt public.

[Suite : recettes exactes](13-reproduction-exacte.md) · [Sommaire](README.md)
