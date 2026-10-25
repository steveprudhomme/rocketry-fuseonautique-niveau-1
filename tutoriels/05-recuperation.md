# 05 — Ouvrir le parachute et revenir au sol

![Récupération sous parachute](../plans/animations/ath/apercu-650.jpg)

**But :** distinguer la forme du tissu, la corde souple et le mouvement de la fusée. Travaille dans une copie de la scène 03.

## A. Examiner le gonflage

1. Place-toi à l’image 369, puis cherche `Parachute 36` dans l’Outliner.
2. Ouvre **Object Data Properties**, l’icône du triangle vert, puis **Shape Keys**.
3. Dans le fichier final, tu trouves `Initial`, puis `Image 1` à `Image 1217`. Ce sont des formes **absolues**, avec Relative désactivé : l’évaluation choisit où l’on se trouve dans cette suite de formes. Ne cherche pas un curseur de gonflage unique.
4. Avance dans la ligne de temps autour du déploiement. Observe le tissu. Une shape key est une forme faite avec les **mêmes sommets** que les autres.
5. La première construction v2 utilisait une clé relative nommée `Gonflage progressif 1.5 seconde`. Les passes suivantes ont enregistré les formes du montage final : le nom de la première recette n’est plus une commande disponible dans la scène finale.
6. Garde cette suite de formes intacte; utilise l’exercice ci-dessous pour apprendre à créer deux formes toi-même.

**Je vérifie :** le tissu change de forme. Nous n’agrandissons pas tout le groupe de récupération : cela ferait aussi grossir les cordes et déplacer les attaches. Le gonflage dure 1,5 seconde **physique**, pas nécessairement 45 images lorsque le montage accélère.

## B. Comprendre la corde comme un collier

Imagine 49 petites perles reliées par 48 ressorts. Les deux extrémités sont tenues; les autres bougent sous la gravité. C’est l’idée du solveur **Soft Body / corps souple**.

La simulation initiale a produit 601 échantillons à 60 images/s. Après adaptation au montage, la corde finale contient 1 218 formes absolues, comme le parachute : une forme initiale et une par image du film. Elle n’a donc pas besoin de recalculer la physique à chaque ouverture. L’absence d’un solveur actif sur cette corde finale n’est pas un oubli.

**Petit exercice de déformation :** dans un fichier neuf, ajoute une sphère. Dans Shape Keys, clique deux fois sur + : une base puis une deuxième forme. Sélectionne la deuxième forme, passe en Edit Mode, sélectionne les sommets et aplatis-les suivant Z. Reviens en Object Mode et déplace sa valeur entre 0 et 1. Tu viens de mélanger deux formes. C’est un exercice du mécanisme, pas la forme exacte de notre parachute.

Pour examiner les réglages originaux, ouvre le script [simuler-corde.py](../plans/animations/vol-complet/sources/simuler-corde.py) dans un éditeur de texte. Retrouve ces mots et nombres :

| Réglage | Valeur de référence | Image simple |
| --- | --- | --- |
| Longueur au repos | 4,572 m | Longueur du collier détendu |
| Groupe `Extremites fixees` | Poids 1 aux deux bouts, 0 ailleurs | Deux perles tenues |
| Pull / Push | 0,8 / 0,8 | Résistance à l’étirement et à l’écrasement |
| Damping / Bend | 0,5 / 0,5 | Frein du mouvement et résistance à la courbure |
| Goal Spring / Friction | 0,9 / 10 | Maintien des extrémités |
| Cadence / intervalle | 60 fps, images 1–601 | Échantillonnage de la simulation |

Ces réglages sont artistiques, pas des propriétés mesurées d’une sangle réelle. Pour reconstruire les mêmes 49 points sans inventer leur courbure, utilise les sources expliquées au [chapitre 13](13-reproduction-exacte.md).

## C. Faire un balancier à la main

Dans un fichier d’exercice, ajoute un cube et place trois clés de rotation Y : image 1 = −5°, image 16 = +5°, image 31 = −5°. Reprends la méthode de clic droit du chapitre 04, cette fois sur **Rotation**. Le mouvement de pendule est ce va-et-vient. Une petite rotation Z produit du **lacet**, comme une toupie qui tourne doucement.

Dans la copie du vol, cherche `Corps - pendule` et `Section avant separee`. Regarde leurs courbes sans remplacer celles du parent de trajectoire. Les mouvements locaux et le déplacement général sont deux animations différentes.

## D. Comprendre le contact

Visite les images 977, 1001, 1043 et 1142. Observe successivement contact, basculement, dégonflage et repos. Le corps ne traverse pas le sol et les cordes restent visibles au-dessus de l’appui.

Pour un exercice, anime un cube qui touche un plan, remonte légèrement puis bascule. Avec la vue de côté, vérifie chaque pose entre les clés : un coin peut traverser le plan même si le début et la fin semblent bons. Ce petit exercice n’est pas une simulation de résistance à l’impact.

**Dépannage :** le parachute se déplace avec une échelle étrange ? Vérifie que tu n’as pas mis à l’échelle le parent de toute la récupération. La corde saute ? Reviens au fichier sauvegardé; ne supprime pas ses centaines de formes pour « nettoyer » la scène.

[Suite : atmosphère](06-atmosphere.md) · [Sommaire](README.md)
