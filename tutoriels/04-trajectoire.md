# 04 — Faire un petit film avec des positions

**But :** comprendre une image clé, puis relier le film aux nombres OpenRocket.

Une **image clé** est un rendez-vous : « à cette image, cet objet doit être ici ». Blender calcule les positions entre deux rendez-vous.

## Exercice à la souris, dans un nouveau fichier

1. Choisis **File → New → General**. Ce fichier d’exercice n’est pas la fusée de référence.
2. Garde le cube sélectionné et renomme-le `fusée-exercice` dans l’Outliner.
3. Dans **Output Properties**, règle la cadence à **30 fps**. Règle la fin à **61**.
4. À l’image 1, dans **N → Item → Location**, entre X=0, Y=0, Z=0. Fais un clic droit sur Location, puis **Insert Keyframe**.
5. À l’image 31, entre Z=2 et insère une nouvelle clé de Location.
6. À l’image 61, entre X=1 et Z=0, puis insère la troisième clé.
7. Lance la lecture avec Espace, puis arrête avec Espace.
8. Dans un éditeur **Dope Sheet**, sélectionne les clés et choisis **Key → Interpolation Mode → Linear** pour comparer avec une interpolation douce.

**Je vérifie :** le cube monte puis revient en se décalant. L’intervalle entre les images 1 et 31 dure 1 seconde. Une séquence de 61 images contient 61 images affichées, même si l’écart entre sa première et sa dernière position est de 2 secondes.

## Retrouver les mêmes idées dans notre vol

Ouvre la copie Blender de la scène 03. Dans l’Outliner, cherche le nom commençant par `CHASSE GALERIE`. C’est le parent de l’ensemble. Ne déplace pas toutes ses pièces une à une.

| Image du film | Ce qui se passe | Temps physique approximatif |
| --- | --- | --- |
| 1 | Attente | 0 s |
| 61 | Allumage | 0 s |
| 85 | Accélération | 0,80 s |
| 113 | Fin de combustion | 1,73 s |
| 369 | Début de récupération | 10,22 s |
| 650 | Descente | 56,47 s |
| 977 | Contact | 106,68 s |
| 1217 | Fin de l’animation après contact | Temps physique figé; 8 s visuelles ajoutées |

Le film dure 40,57 s, pas 106,68 s. C’est comme accélérer une partie d’une promenade dans une vidéo. Le facteur de lecture apparaît sur l’ATH.

## Lire une ligne de données

1. Ouvre [vol-h143.csv](../plans/animations/vol-complet/vol-h143.csv) dans un éditeur de texte.
2. Lis la première ligne : elle donne les noms des colonnes.
3. `time_s` est le temps en secondes; `x_m` et `y_m` sont les positions horizontales; `altitude_m` est l’altitude relative au départ; `speed_m_s` est la vitesse; `thrust_N` est la poussée calculée à cet instant.
4. Compare avec [telemetrie.json](../plans/animations/ath/donnees/telemetrie.json), qui associe une ligne à chaque **image du film**.
5. Sur papier, écris trois couples image/altitude du tableau ci-dessus, puis observe ces images dans Blender.

La reconstruction exacte utilise le CSV archivé. Relancer OpenRocket avec le même vent peut donner une petite variation; la notice v4 l’explique. Avec le terrain, les positions sont aussi déplacées vers le site et raccordées visuellement en hauteur. Copier le Z du CSV directement dans la scène géographique ignorerait ce raccord.

**Dépannage :** l’objet revient à sa place ? Une clé le commande. Rien ne bouge ? Vérifie que tu as créé une clé à deux images différentes. Un déplacement de 1 000 fois trop grand ? Tu as probablement confondu mètres et millimètres.

[Suite : récupération](05-recuperation.md) · [Sommaire](README.md)
