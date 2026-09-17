# Chasse Galerie 1 — Descente et atterrissage v3

**Révision du 2026-09-17.** Ajout du balancement sous voilure, d’un léger lacet et d’une séquence d’atterrissage avec mise au repos.

[![Lire la vidéo](apercu-video.jpg)](chasse-galerie-1-vol-complet.mp4)

- [Vidéo complète](chasse-galerie-1-vol-complet.mp4) : MP4 H.264, 1080p, 30 images/s, **40,57 secondes**, sans son.
- [Extrait de l’atterrissage](extrait-atterrissage.mp4) : approche, contact, basculement et dégonflage.
- [Scène Blender modifiable](chasse-galerie-1-vol-complet.blend).
- [Contrôles de la scène](verification-atterrissage.json).
- [Données OpenRocket](vol-h143.csv) et [événements](evenements-h143.csv).

## Descente sous voilure

Après le gonflage de 1,5 seconde conservé de la v2, le corps effectue un mouvement de pendule autour de son attache supérieure. Les deux composantes du balancement ont des amplitudes maximales réglées à 7° et 4°, avec un amortissement partiel. Le lacet oscille doucement entre −6° et +6°. La section avant reçoit un mouvement secondaire plus faible.

Ces mouvements sont calculés en fonction du temps du vol : ils sont donc accélérés, comme le reste de la descente, dans le passage marqué ×6. Les derniers instants d’approche sont en temps réel. La trajectoire de référence OpenRocket reste conservée; le balancement est un déplacement visuel des pièces autour de leurs attaches.

## Contact et mise au repos

La vidéo comprend **huit secondes après le contact** :

1. Contact du corps et petit rebond amorti, plafonné par un paramètre de 3,5 cm.
2. Basculement du corps sur le côté en environ 1,9 seconde, suivi d’une petite oscillation amortie.
3. Descente et basculement de la section avant, légèrement décalés.
4. Affaissement de la voilure pendant environ 4,4 secondes; son tissu forme une surface plissée au sol.
5. Mise en mou des cordes et rapprochement de la caméra sur l’ensemble au repos.

Une surface de contact horizontale située à **32 mm** dans le repère de la scène évite que la géométrie pénètre le terrain, dont le relief maximal est d’environ 22,4 mm. Les deux sections reposent sur leurs parties basses; le corps est déplacé latéralement pendant son basculement pour se placer à côté du trépied. Les chaumes constituent un décor et ne sont pas des obstacles physiques calculés.

## Cordes et continuité avec la v2

Le gonflage progressif et les échantillons du solveur Soft Body natif sont conservés. La corde principale est adaptée aux points d’attache mobiles. Lors de l’atterrissage, des boucles de mou préservent sa longueur au lieu de la raccourcir à mesure que le parachute descend. La longueur contrôlée pendant cette phase reste entre **4,614 et 4,621 m**, en continuité avec le léger allongement de la corde de 4,572 m de la v2.

Les attaches et les suspentes suivent les pièces et le bord de la voilure. La corde et la déformation du tissu sont intégrées au fichier Blender; aucun cache de calcul extérieur n’est nécessaire pour lire l’animation.

## Portée des mouvements et des données

OpenRocket fournit le scénario **H143 — apogée idéale**, jusqu’au premier contact à 106,843 s, avec une altitude maximale de 593,893 m. Les données de la simulation restent inchangées. Le temps, l’altitude et la vitesse de vol s’affichent jusqu’au contact.

**Après le contact, les titres indiquent « animation visuelle » et le temps écoulé depuis l’impact.** Ils n’affichent pas de mesures de vol inventées. Le balancement, le rebond, le basculement et le dégonflage sont des animations géométriques, pas une simulation validée des charges, des dommages, du tissu ou de la dynamique de collision. Le traitement du sol est une contrainte géométrique, et les boucles de corde après contact sont illustratives. Le vent et la fumée volumétrique restent des tâches distinctes du ROADMAP.

## Vérifications

- Contrôle de la scène rouverte sur **317 images**, dont chaque image après le contact.
- Corps, section avant, voilure et corde au-dessus du relief maximal du terrain lors des contrôles.
- Écart maximal des attaches inférieur à **0,1 mm**.
- Trajectoire de référence conservée à moins de **0,1 mm** d’écart numérique sur l’altitude.
- Balancement et lacet présents pendant la descente; les deux sections sont horizontales à la fin.
- Voilure finale affaissée : environ **18 mm** de différence de hauteur dans son maillage.
- Six poses d’approche et d’atterrissage inspectées visuellement.
- MP4 complet (1 217 images) et extrait (332 images) décodés sans erreur.

## Reproduction et modification

Les sources des versions précédentes sont conservées dans `sources/`. La v3 ajoute `animer-atterrissage.py` et `verifier-atterrissage.py`.

1. Ouvrir la scène animée v2 en arrière-plan dans Blender 4.3.
2. Exécuter `animer-atterrissage.py` avec, après `--`, quatre chemins : télémétrie de la v2, JSON natif de corde, dossier final et dossier temporaire. Le script produit la scène v3, la nouvelle télémétrie d’affichage et six aperçus.
3. Rendre les images **1 à 1217**, à 30 images/s, dans un dossier temporaire avec un chemin absolu. Les 368 premières images de v2 ont été réutilisées dans cette livraison; la suite a été rendue avec la scène v3.
4. Exécuter `titres-vol.py` sur le dossier contenant la nouvelle `telemetrie.json`. Encoder les PNG avec FFmpeg, filtre ASS, H.264/yuv420p et `+faststart`.
5. Pour contrôler une scène rouverte, exécuter `verifier-atterrissage.py` avec deux chemins après `--` : rapport JSON de sortie et télémétrie v3.

Les titres sont ajoutés lors de l’encodage et ne sont pas incorporés au rendu brut Blender. Les paramètres de pendule, de rebond, de basculement et d’affaissement se trouvent dans le script de la v3.
