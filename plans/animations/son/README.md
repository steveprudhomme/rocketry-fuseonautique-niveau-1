# Chasse Galerie 1 — Son et musique v9

10 octobre 2026. Vol complet sonorisé, avec bruitages synthétisés et composition instrumentale originale **Sept sillages**. Livraison locale; publication GitHub à confirmer. La v8 est publiée, vérifiée le 10 octobre 2026.

[![Lire la vidéo sonorisée](apercu-video.jpg)](chasse-galerie-1-vol-sonorise.mp4)

- [Vidéo MP4 sonorisée](chasse-galerie-1-vol-sonorise.mp4) : 1080p, 30 images/s, 40,57 s, audio AAC stéréo.
- [Scène Blender avec son intégré](chasse-galerie-1-son.blend) : ouvrir la scène 03 pour lire l’animation avec sa bande sonore.
- [Bande sonore finale WAV](audio/bande-son.wav), [musique seule](audio/musique-originale.wav), [bruitages seuls](audio/bruitages.wav) et [mixage avant normalisation](audio/mixage.wav).

## Bruitages synchronisés

| Repère | Temps dans la vidéo | Traitement |
| --- | --- | --- |
| Attente | 0 à 2 s | Quatre impulsions discrètes pendant l’attente existante |
| Allumage | 2,000 s | Grondement grave et bruit large bande, enveloppe liée à la poussée |
| Extinction | 3,730 s | Fin du grondement; souffle aérodynamique variant avec la vitesse |
| Éjection | 12,267 s | Impulsion brève, puis froissement illustrant l’ouverture de la voilure |
| Contact au sol | 32,533 s | Choc amorti et frottement court |

Les sons suivent le **temps du montage**, qui condense une partie du vol simulé. Leur hauteur n’est pas multipliée par la vitesse de lecture. Il s’agit de bruitages procéduraux illustratifs : aucun enregistrement réel du moteur, aucune mesure acoustique ni propagation sonore avec distance ou effet Doppler. Les repères et la télémétrie sont archivés dans [son.json](donnees/son.json) et [telemetrie.json](donnees/telemetrie.json).

## Composition originale

**Sept sillages** est une courte composition instrumentale synthétisée, inspirée du métal progressif : accords de puissance saturés répartis en stéréo, basse, percussion et arpèges plus légers pendant la récupération. Tempo de 120 BPM, mesures à 7/8 regroupées en 2+2+3 et superposition rythmique de cymbales en 3 contre 2. L’introduction accompagne l’attente; l’entrée de la section forte coïncide avec l’allumage.

La musique baisse pendant le moteur et l’éjection pour laisser passer les bruitages. La fin se résout et s’atténue pendant la mise au repos. Tous les sons sont créés par synthèse déterministe (graine 14309), sans musique ni échantillon tiers. Les instruments restent des timbres synthétiques, et non une prestation enregistrée de guitare et de batterie. La préférence esthétique pourra être ajustée après écoute.

## Vérifications

Les deux canaux WAV contiennent exactement 1 947 200 échantillons à 48 kHz, soit la durée des 1 217 images. Le MP4 est entièrement décodé sans erreur et son flux vidéo est identique à celui de la v8. Normalisation en deux passes, cible de −18 LUFS et plafond de crête vraie de −2 dBTP; les valeurs mesurées après encodage AAC sont conservées dans le [rapport audiovisuel](verification-audiovisuelle.json). Les pistes séparées précèdent cette normalisation finale.

Le son est intégré dans le fichier Blender et les quatre événements sont repérés sur sa ligne de temps. Le compositeur et les mouvements 3D restent ceux de la v8. Le montage vidéo final est effectué sans nouveau rendu des images. Les contrôles portent sur les données, la synchronisation des repères et le décodage; ils ne constituent pas une validation acoustique d’un vol réel.

## Reproduction et droits

Depuis la structure locale du projet, exécuter `sources/creer-son.py` avec Python et NumPy, puis `sources/encoder-verifier.py` avec Python et FFmpeg. Le premier script accepte `--source` et `--output`; le second utilise les dossiers `outputs/cinematographie-v8`, `outputs/son-v9` et `work/son-v9`. Ouvrir ensuite la scène Blender v8 et exécuter `sources/integrer-blender.py`. La bande sonore normalisée doit être produite avant l’intégration. Les scripts conservent le rendu vidéo original.

Audio : composition et synthèse originales du projet Chasse Galerie 1, avec assistance Codex, sans échantillons externes. Images et textures héritées : orthophoto **© Région Centre-du-Québec 2025**, MRNF, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.fr); relief NASA/NGA, [SRTM GL1](https://doi.org/10.5067/MEaSUREs/SRTM/SRTMGL1.003), OpenTopography; origine du site © [contributeurs OpenStreetMap](https://www.openstreetmap.org/copyright), ODbL. La normalisation sonore ne modifie pas ces images ou leurs crédits.

Prochaine étape de la feuille de route : affichage tête haute et éléments didactiques.
