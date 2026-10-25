# 03 — Entrer dans l’atelier Blender

**But :** obtenir une image sans reconstruire la fusée. Une scène est comme un plateau de cinéma : objets, caméra et lumière y sont réunis.

## Premier rendu

1. Copie tout le dossier `plans/animations/ath` dans ton dossier d’essai.
2. Ouvre `chasse-galerie-1-ath.blend` dans Blender 4.3.
3. Dans le sélecteur de scène en haut de la fenêtre, choisis **03 — Vol complet sur terrain hybride**. La scène **06 — Vol avec ATH et son** lit le film final; ce n’est pas celle où l’on modifie la fusée.
4. Dans la ligne de temps, saisis l’image **650**. Elle montre la descente.
5. Place le pointeur dans la vue 3D. Appuie sur **pavé numérique 0** pour voir par la caméra. Sans pavé numérique, utilise **View → Cameras → Active Camera**.
6. Appuie sur **F12**, attends le rendu, puis dans la fenêtre du résultat choisis **Image → Save As**. Enregistre `descente.png` dans `resultats`.
7. Ferme la fenêtre de rendu pour revenir à l’atelier. **Ctrl+S** enregistre le projet, pas l’image PNG.

**Je vérifie :** je vois la fusée et le parachute, sans les panneaux de l’ATH dans cette scène 03. Pour le film avec panneaux, choisis la scène 06 et rends la même image.

## Trouver un objet

L’**Outliner**, la liste des objets, est généralement en haut à droite. Son champ de recherche permet de saisir le début d’un nom. Cherche `Parachute 36`, `Corps - pendule`, `TERRAIN HYBRIDE` ou `CAMÉRA`.

1. Clique le nom dans la liste.
2. Dans la vue 3D, ouvre le panneau **N → Item** pour lire position, rotation et échelle.
3. Si le champ est coloré, une animation peut le contrôler. Changer l’image peut remettre la valeur animée.
4. Pour cadrer l’objet sélectionné, utilise **View → Frame Selected**. Reviens ensuite à la caméra avec le pavé numérique 0.

Ne confonds pas **tourner autour de l’objet pour le regarder** et **tourner l’objet lui-même**. Le premier change ton point de vue de travail; le second change la scène.

## Où sont les versions ?

| Scène | Utilité |
| --- | --- |
| 01 | Vol v4 conservé comme référence |
| 02 | Relief SRTM natif |
| 03 | Vol 3D sur terrain hybride, avec caméra et son des versions suivantes |
| 04 | Inspection du terrain |
| 05 | Test optique face au soleil |
| 06 | Film final avec ATH dans le séquenceur |

Pour refaire l’image artistique du décollage, ouvre plutôt le [projet de l’heure dorée](../plans/rendus-artistiques/README.md), puis F12. Il utilise Cycles; le vol utilise Eevee. Ce sont deux moteurs qui fabriquent l’image différemment.

## Apporter une pièce depuis OpenSCAD

Pour comprendre le passage entre les logiciels, isole un aileron dans ta copie SCAD, fais F6 puis exporte un STL. Dans un fichier Blender d’exercice, choisis **File → Import → STL** et sélectionne ce fichier. Le STL ne mémorise pas son unité : si les nombres SCAD étaient en millimètres et que tu travailles en mètres, réduis l’objet par **0,001**, puis contrôle ses dimensions dans N → Item. Une portée nominale de 107,95 mm doit devenir 0,10795 m, pas 107,95 m.

Tu peux ensuite nommer l’objet et lui affecter un matériau dans Material Properties. Cette voie manuelle transmet la géométrie, pas automatiquement les couleurs, les UV, les pièces parentes ou les animations. Le script du rendu artistique construit plusieurs formes directement à partir des cotes; un import STL n’est donc pas présenté comme une reproduction identique de son maillage.

## Si quelque chose manque

- **Film absent en scène 06 :** remets le MP4 à côté du `.blend`.
- **Tout paraît gris :** tu es peut-être en vue solide; F12 utilise les matériaux du rendu.
- **Objet introuvable :** efface le filtre de l’Outliner et vérifie la scène choisie.
- **Rendu lent :** pour un essai, réduis le pourcentage de résolution dans Output Properties; note ce changement et rétablis 100 % pour comparer le résultat final.

[Suite : mouvement](04-trajectoire.md) · [Sommaire](README.md)
