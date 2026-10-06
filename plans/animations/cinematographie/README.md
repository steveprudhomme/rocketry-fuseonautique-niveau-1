# Chasse Galerie 1 — Cinématographie et optique v8

6 octobre 2026. Nouvelle caméra pour le vol complet, avec secousses à l’allumage, suivi amorti, profondeur de champ et effets optiques subtils. Livraison locale; publication distante à confirmer. Les versions v2 à v7 sont déjà publiées.

[![Lire le vol complet](apercu-video.jpg)](chasse-galerie-1-vol-complet.mp4)

- [Vol complet MP4](chasse-galerie-1-vol-complet.mp4) : 1920 × 1080, 30 images/s, 1 217 images, 40,57 s, sans son.
- [Contrôle optique face au soleil](extrait-optique.mp4) : 5 s, vue de démonstration distincte du vol.
- [Scène Blender 4.3](chasse-galerie-1-cinematographie.blend), textures intégrées. Scène 03 : vol; scène 05 : contrôle optique.

## Caméra et paramètres

| Effet | Réalisation |
| --- | --- |
| Secousse moteur | Modificateurs natifs Noise et Envelope sur trois axes; amplitude liée à l’accélération positive du scénario, maximale vers 0,8 s. Extinction après la combustion de 1,73 s. Rotation effectivement mesurée : 0,088° au maximum sur un axe. |
| Suivi amorti | Zone de tolérance de ±2,2 % de la largeur et ±2,5 % de la hauteur; constante d’amortissement de 0,18 s. Retard de suivi limité à 5 % du cadre. Le suivi tient compte de l’ensemble fusée et récupération. |
| Profondeur de champ | Objectif 45 mm, mise au point sur le centre de l’ensemble, ouverture de f/7,1 au sol à f/2,8 en altitude; au moins f/4 pendant la récupération. |
| Aberration chromatique | Dispersion de 0,0007 dans le compositeur, avec ajustement aux bords. |
| Reflets parasites | Mélange progressif plafonné à 10 %, dans un cône de 25° vers le soleil. Disque solaire projeté dans le compositeur, sans géométrie susceptible de créer une ombre. |

**La caméra du vol regarde à l’opposé du soleil : les reflets y restent donc désactivés.** La scène 05 et son extrait montrent leur réponse face à la source. La profondeur de champ est volontairement modérée : la fusée reste lisible; il ne s’agit pas d’un flou uniforme ajouté à l’image.

## Vérifications et limites

Les 1 217 cadrages conservent les éléments contrôlés dans l’image, avec une marge minimale de 14,1 %. Les secousses sont nulles hors combustion. L’estimation optique donne moins de 0,4 pixel de flou sur le sujet et de 0,7 à 5,6 pixels pour un arrière-plan à l’infini; ces valeurs issues du modèle de lentille mince ne sont pas des mesures du rendu.

La trajectoire, le vent, les mouvements de récupération, le terrain hybride et l’éclairage v7 sont conservés. L’écart maximal de trajectoire dans le repère visuel est inférieur à 0,1 mm; les 241 poses après contact conservent au moins 32 mm de garde pour les éléments contrôlés. Le raccord vertical au relief et les appuis locaux restent illustratifs. Aucune nouvelle simulation physique n’est revendiquée.

Rapports : [caméra](verification-camera.json), [vol et terrain](verification-vol-terrain.json), [décodage des vidéos](verification-video.json). Paramètres : [cinématographie](donnees/cinematographie.json) et [caméra par image](donnees/camera-par-image.json).

La conception sonore et musicale, ainsi que le nouvel affichage tête haute, restent à réaliser.

## Sources et reproduction

Orthophoto : **© Région Centre-du-Québec, 2025**, distribuée par le MRNF / Gouvernement du Québec sous [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.fr). Mosaïque RGB à 2 m/pixel et correction tonale conservées de la v7. Relief : NASA/NGA, SRTM GL1 v3, [DOI](https://doi.org/10.5067/MEaSUREs/SRTM/SRTMGL1.003), hébergement OpenTopography. Origine du site : © [contributeurs OpenStreetMap](https://www.openstreetmap.org/copyright), ODbL. Animation et habillage du projet, avec assistance Codex.

Le fichier Blender autonome se rend directement. Les scripts de construction, vérification et encodage sont dans `sources/`. Ils utilisent la structure locale `outputs/eclairage-v7`, `outputs/vol-complet-v4`, `outputs/cinematographie-v8` et `work/cinematographie-v8`. Pour reconstruire : ouvrir la scène v7 avec `creer-camera.py`, puis la scène produite avec `finaliser-optique.py`; exécuter les vérifications et encoder les images avec `encoder-videos.py`. Le contrôle corrigé utilise `corriger-disque.py -- --animation` avant encodage. Les données de vol d’origine et les titres sont repris sans changer le rythme de lecture.

Pour préparer les entrées depuis le dépôt, exécuter `sources/preparer-reconstruction.py` depuis un répertoire de construction vide. Il copie les données archivées et la scène v7 dans la structure attendue.
