# Chasse Galerie 1 — Vol complet, récupération v2

**Révision du 2026-09-17.** Gonflage progressif du parachute et simulation native Blender de la corde de choc principale.

[![Lire la vidéo](apercu-video.jpg)](chasse-galerie-1-vol-complet.mp4)

- [Vidéo complète MP4](chasse-galerie-1-vol-complet.mp4) : 1920 × 1080, 30 images/s, 34,5 s, sans son.
- [Extrait de la récupération](extrait-recuperation.mp4) : six secondes centrées sur l’ouverture.
- [Scène Blender](chasse-galerie-1-vol-complet.blend) : textures et mouvements de corde intégrés.
- [Scène du solveur corps souple](sources/corde-solveur.blend) et [échantillons calculés](sources/corde-simulation.json).
- [Contrôles de la récupération](verification-recuperation.json).
- [Trajectoire OpenRocket](vol-h143.csv) et [événements](evenements-h143.csv).

## Changements visibles

La voilure passe d’une forme étroite plissée à un dôme gonflé sur **1,5 seconde de temps simulé**, avec une progression douce. Les suspentes suivent son bord; le système de récupération n’est plus agrandi uniformément. La caméra élargit le cadre avant le déclenchement pour conserver la voilure entière à l’image.

La corde principale utilise le véritable solveur **Soft Body de Blender 4.3** : 49 sommets reliés par 48 ressorts, deux extrémités fixées aux points d’attache animés, gravité et amortissement. Elle prend une courbure souple puis se tend. Les 601 états calculés à 60 Hz sur dix secondes sont intégrés au maillage de la scène finale; ensuite, son état stabilisé est conservé. La lecture utilise le temps physique de la télémétrie, y compris pendant la descente accélérée ×6.

## Contrôles réalisés

- Tous les échantillons de la corde sont finis, sans divergence numérique.
- Longueur au repos : **4,572 m**; longueur maximale calculée : **4,633 m**, soit **1,33 %** d’allongement.
- Écart maximal des attaches du solveur : inférieur à **0,001 mm**; écart des attaches après intégration au maillage : inférieur à **0,002 mm**.
- Gonflage progressif et monotone sur 1,5 seconde; cadrage de la voilure vérifié toutes les cinq images après déploiement.
- La trajectoire du corps reste celle de la première vidéo, avec un écart numérique inférieur à 0,1 mm par rapport aux altitudes exportées.
- Contrôle visuel de cinq états : début, 0,5 s, 1 s, 1,5 s et 3 s après le déclenchement.

## Portée de la simulation

Le scénario reste **H143 — apogée idéale**, avec un vol de 106,843 s et une altitude maximale de 593,893 m. La montée et le gonflage sont montrés en temps réel; la partie centrale de la descente est accélérée ×6. Le dernier plan fige l’état au premier contact au sol.

La corde est simulée dans un repère local attaché à la fusée : gravité, ressorts et ancrages imposés. Les coefficients de masse, rigidité et amortissement servent au rendu et ne sont pas des propriétés mesurées du nylon. Les collisions corde/fusée, les efforts aérodynamiques et le couplage des forces au vol OpenRocket ne sont pas calculés. La corde principale reprend une longueur nominale de 15 pieds, mais la répartition réelle des attaches et la branche secondaire restent à confirmer.

Le gonflage est une déformation animée de la voilure, pas une simulation aérodynamique du tissu. L’extraction depuis l’intérieur du tube et le lien secondaire vers la section avant restent illustratifs. Le modèle de vol conserve son déploiement idéal instantané : la durée visuelle du gonflage ne modifie pas sa traînée calculée. L’atterrissage dynamique, le dégonflage au sol, le vent et le balancement de la fusée restent des tâches distinctes du ROADMAP.

## Sources et reproduction

Les fichiers de base de la première édition restent dans `sources/` : `ExporterVol.java`, `animer-vol.py`, `titres-vol.py`, télémétrie et titres. Cette révision ajoute :

1. `simuler-corde.py` : lancer Blender 4.3 avec `--background --factory-startup --python`, puis `--` et un dossier temporaire absolu. Le script crée les données de corde et la scène du solveur. Il vérifie les attaches, les nombres finis et un allongement maximal inférieur à 3 %.
2. `ameliorer-recuperation.py` : ouvrir la scène animée de première édition en arrière-plan; exécuter le script avec quatre arguments après `--` : JSON de corde, JSON de télémétrie, dossier final et dossier temporaire. Il enregistre la scène révisée et cinq aperçus.
3. Rendre les images 1 à 1035 de la scène finale, à 30 images/s. Utiliser un chemin PNG absolu adapté au poste. Les images 1 à 332 de la première édition sont identiques et ont été réutilisées dans cette livraison.
4. Assembler les images avec FFmpeg, appliquer les titres ASS, encoder en H.264/yuv420p et activer `+faststart`. Les titres sont ajoutés au MP4 et ne font pas partie du rendu brut Blender.

Le fichier `.blend` final est autonome pour les textures et la déformation de corde. Pour modifier la physique, utiliser la scène du solveur ou le script, puis régénérer les échantillons et la scène finale.

Références : [forces extérieures et ancrages Soft Body](https://docs.blender.org/manual/en/4.3/physics/soft_body/forces/exterior.html), [ressorts des arêtes](https://docs.blender.org/manual/en/4.3/physics/soft_body/settings/edges.html).
