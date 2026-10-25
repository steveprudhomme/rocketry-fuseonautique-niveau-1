# 13 — Comprendre et reprendre les recettes exactes

**Pour Steve et un adulte accompagnateur.** Les gestes des autres leçons expliquent les principes. Ce chapitre relie les fichiers pour reprendre les calculs d’origine sans dépendre du dossier personnel de l’assistant.

## 1. Pourquoi les chemins diffèrent

Dans GitHub, les livrables sont rangés dans `plans/animations`. Pendant leur fabrication, les scripts utilisaient des dossiers `outputs` et `work`. Le **dossier courant** est le dossier depuis lequel une commande cherche ses chemins relatifs. Copier un script n’en change pas automatiquement les chemins.

Dans ton atelier, crée `outputs` et `work`. Avec l’Explorateur, copie chaque dossier de gauche vers le nom de droite, **avec tout son contenu** :

| Dossier du dépôt | Dossier attendu dans l’atelier |
| --- | --- |
| `plans/animations/vol-complet` | `outputs/vol-complet-v4` |
| `plans/animations/topographie` | `outputs/topographie-v5` |
| `plans/animations/terrain-hybride` | `outputs/terrain-hybride-v6` |
| `plans/animations/eclairage` | `outputs/eclairage-v7` |
| `plans/animations/cinematographie` | `outputs/cinematographie-v8` |
| `plans/animations/son` | `outputs/son-v9` |
| `plans/animations/ath` | `outputs/ath-v10` |

Pour simplement ouvrir une scène et la rendre, ces copies supplémentaires ne sont pas nécessaires. Elles servent à reconstruire avec les scripts historiques.

## 2. Lire un script sans l’exécuter

Ouvre un `.py` dans un éditeur de texte, ou dans **Text Editor → Open** de Blender. Cherche successivement :

1. `Path`, `out`, `work` : où il lit et écrit.
2. `read_text`, `load`, `open` : ses ingrédients.
3. `for` : les actions répétées, par exemple une fois par image.
4. `keyframe_insert` : les positions ou valeurs animées.
5. `save_as_mainfile`, `write_text`, `render` : ses résultats.
6. `assert` : ce qu’il vérifie avant d’accepter le résultat.

Une valeur comme `.18` signifie 0,18. Les points sont les séparateurs décimaux du code. Une valeur de rotation interne peut être en radians même si l’interface affiche des degrés. Un nom qui finit par `_m` est en mètres, `_s` en secondes.

Le script est une suite de gestes et de calculs, pas un fichier à lancer à l’aveugle. Pour chaque recette, écris sur papier : **entrée → transformation → sortie → contrôle**.

## 3. Carte de fabrication

| Travail | Entrée | Recette et rôle | Contrôle manuel |
| --- | --- | --- | --- |
| Modèles | Cotes et hypothèses datées | Fiches OpenSCAD/OpenRocket; sources dans `plans/outils` | Arbre des pièces, unités, masse et CG calculés |
| Décalque | Illustration source + configuration + dimensions | `generer-sillage.py` : patron, textures et mosaïque | Barre de 100 mm et raccord des bords |
| Plan A3 et galerie | Modèle SCAD | `generer-plan-ensemble.py --render` et outils d’images | Trois vues, légendes, révision B |
| Rendu artistique | SCAD + textures | `rendre-decollage-blender.py` | Image portrait et textures intégrées |
| Vol initial | Trajectoire et modèle | `animer-vol.py` | Images clés et étapes de vol |
| Récupération v2 | Simulation locale de corde + vol | `simuler-corde.py`, puis `ameliorer-recuperation.py` | Attaches et gonflage, sans mise à l’échelle du groupe |
| Atterrissage v3 | Vol avec récupération | `animer-atterrissage.py` | Contact, basculement, corde et tissu au-dessus du sol |
| Atmosphère v4 | CSV vent archivé + scène précédente | `animer-atmosphere.py` puis les passes ci-dessous | Pas de fumée avant allumage; disparition et dérive |
| Topographie v5 | GeoTIFF et coordonnées + scène v4 | Préparation du module et du terrain, `integrer-topographie.py` | Repère, origine, 57 200 sommets natifs |
| Terrain v6 | Scène v5 + données préparées | `creer-hybride.py`, `finaliser-rendu.py`, `metadonnees-et-masque.py` | Masque 24–36 m et contacts |
| Éclairage v7 | Image v6 + scène v6 | `corriger-orthophoto.py`, `appliquer-eclairage.py` | Comparaison tonale et direction solaire |
| Caméra v8 | Scène v7 + CSV et télémétrie v4 | `creer-camera.py`, `finaliser-optique.py`, `corriger-disque.py` | Cadrage, mise au point, pas d’ombre du disque solaire |
| Son v9 | MP4 v8 + télémétrie | `creer-son.py`, `encoder-verifier.py`, `integrer-blender.py` | Son à l’image 61, 369, 977; pas de doublon |
| ATH v10 | Images v8 sans titres + son v9 | Export des projections, `creer-ath.py`, encodage et intégration | Jauges, texte, phase, bilan et lien MP4 relatif |

**Passes v4 à conserver :** après la construction, appliquer `fix-vol.py`, `renforcer-fumee.py`, `diluer-fumee.py` puis `attente-sans-fumee.py`. La notice v4 décrit leur effet. Les titres ASS sont ajoutés ensuite à l’encodage; ne les incruste pas avant l’ATH v10, sinon deux interfaces se superposeraient.

## 4. Une reconstruction raisonnable : repartir d’une scène publiée

La manière recommandée de reproduire exactement un rendu est d’ouvrir son `.blend` publié. Les scènes v4 à v10 et les données préparées sont les points de départ conservés. Pour reconstruire **toute l’histoire depuis un fichier vide**, certains scripts attendent des scènes intermédiaires v1–v3 ou des tuiles complètes qui ne sont pas toutes dans le dernier dossier : elles doivent être reprises dans l’historique ou téléchargées selon les métadonnées. Ce parcours historique complet n’a pas été validé d’une seule traite sur une machine neuve.

Ne renomme pas une scène finale « v3 » pour satisfaire un chemin : elle contient déjà des effets qui seraient ajoutés deux fois. On conserve cette limite dans l’audit au lieu de promettre un résultat identique depuis n’importe quel point de départ.

Pour la caméra v8, le script `sources/preparer-reconstruction.py` sait préparer ses entrées depuis l’arborescence du dépôt. Lance-le depuis un **dossier de construction vide**, puis lis son message. Il copie les données; il ne remplace pas les étapes de rendu.

## 5. Reprendre la v10 sans recalculer la physique

1. Prépare les copies `outputs/cinematographie-v8`, `outputs/son-v9`, `outputs/ath-v10` et `work/ath-v10/frames`.
2. Dans Blender, ouvre la scène v8, scène 03. Rends les images 1–1217 en JPEG qualité 95 dans `work/cinematographie-v8/frames`, avec le préfixe `vol-`. Elles doivent se nommer `vol-0001.jpg` à `vol-1217.jpg`. Vérifie les premières images avant de tout lancer.
3. Le fichier `projections.json` est déjà livré. Pour le recalculer après un changement de caméra, exécute `exporter-projections.py` dans Blender sur la bonne scène, depuis l’atelier comme dossier courant.
4. Depuis un terminal ouvert dans l’atelier, avec Python, NumPy et Pillow installés, lance un aperçu :

```powershell
python outputs/ath-v10/sources/creer-ath.py --preview
```

5. Examine les huit aperçus. S’ils conviennent, relance sans `--preview` pour les 1 217 images.
6. Le script `encoder-verifier.py` assemble ces images et copie la piste AAC du MP4 v9. Il contient un chemin FFmpeg Windows à adapter si ton installation diffère.
7. `integrer-blender.py`, lancé sur la scène v9, ajoute la scène 06. Conserve son nouveau MP4 à côté du `.blend`.

Pour lancer un script Blender depuis un terminal, le principe est :

```powershell
# Exemple : adapter le chemin vers Blender installé, garder les guillemets.
& "C:/Program Files/Blender Foundation/Blender 4.3/blender.exe" -b "outputs/son-v9/chasse-galerie-1-son.blend" --python "outputs/ath-v10/sources/exporter-projections.py"
```

`-b` signifie sans fenêtre; `--python` indique la recette à exécuter. Ce n’est pas la même chose que lancer le script avec Python ordinaire : il a besoin du module `bpy` de Blender.

## 6. Ce qui doit rester identique, et ce qui peut varier

- **Données :** conserve les CSV/JSON archivés pour refaire la même trajectoire.
- **Images sources :** garde l’orthophoto et l’illustration; une nouvelle génération artistique ne sera pas identique.
- **Versions :** relève la version des logiciels et des dépendances. Une différence de GPU ou de version peut modifier légèrement les pixels.
- **Son :** conserve la graine 14309 et les paramètres pour reproduire la synthèse; garde le WAV final pour refaire le montage simplement.
- **Résultat :** même contenu visuel ne signifie pas même empreinte de fichier, car l’encodeur et les métadonnées peuvent changer.

Les [sources et limites](../references/sources.md), les notices de chaque version et les fichiers `verification-*.json` complètent ce parcours. Les scripts ne remplacent ni les mesures du kit ni une validation de lancement.

[Sommaire](README.md) · [Audit de couverture](audit-documentation.md)
