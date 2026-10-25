# 00 — Préparer son atelier numérique

**But :** retrouver son travail et ne pas abîmer l’original. Aucun logiciel 3D n’est nécessaire pour cette séance.

## Fais trois boîtes

1. Dans l’Explorateur Windows, ouvre Documents.
2. Crée un dossier `Mon-atelier-fusee`.
3. Dedans, crée `reference`, `essais` et `resultats`.
4. Télécharge le dépôt avec le bouton **Code → Download ZIP** de GitHub, puis choisis **Extraire tout**. Mets le dossier extrait dans `reference`. Un fichier encore dans le ZIP n’est pas prêt à travailler.
5. Dans **Affichage**, active l’affichage des extensions de fichiers si elles sont cachées.

`reference` est le livre de recettes que tu gardes intact. `essais` est ton brouillon. `resultats` contient ce que tu souhaites montrer.

## Reconnais les fichiers

| Fin du nom | C’est quoi ? | Avec quoi l’ouvrir ? |
| --- | --- | --- |
| `.md` | Un texte de documentation | GitHub, un éditeur de texte ou Markdown |
| `.scad` | Une recette de formes | OpenSCAD |
| `.ork` | Une fusée à étudier | OpenRocket |
| `.blend` | Un atelier 3D enregistré | Blender |
| `.csv` | Un tableau de nombres | Éditeur de texte; un tableur peut aussi le lire |
| `.json` | Des données nommées, entre accolades | Éditeur de texte |
| `.png` / `.jpg` | Une image | Visionneuse d’images |
| `.wav` | Du son | Lecteur audio ou Blender |
| `.mp4` | Une vidéo | Lecteur vidéo |

## Choisis la bonne version

Les dossiers d’animation se trouvent dans `plans/animations`. Les versions sont des étapes, pas des fichiers à mélanger au hasard : vol-complet = v4, topographie = v5, terrain-hybride = v6, eclairage = v7, cinematographie = v8, son = v9, ath = v10.

Pour voir le film final, ouvre `plans/animations/ath/chasse-galerie-1-ath.mp4`. Pour ouvrir son projet Blender, copie **tout le dossier `ath`**, pas seulement le `.blend` : il utilise le MP4 voisin. Les images sont déjà assemblées dans la scène 06; la scène 03 contient encore l’animation 3D.

## Sauvegarde ton expérience

Avant de modifier un fichier, utilise **Enregistrer sous / Save As** et un nom comme `mon-essai-01.blend`. Enregistre dans `essais`. Après un essai réussi, exporte son image ou sa vidéo dans `resultats`.

Dans une note, écris : date, fichier ouvert, changement, résultat. Exemple : « J’ai réduit le tremblement. La fusée bouge moins dans le cadre. »

**Je vérifie :** je retrouve une référence intacte, une copie d’essai et un résultat. Si le fichier est introuvable, je cherche son extension et je vérifie qu’il a été extrait du ZIP.

**Petit défi :** explique la différence entre un `.blend` et un `.mp4` : le premier conserve l’atelier, le second montre le film.

[Suite : modèles](01-modeles.md) · [Sommaire](README.md)
