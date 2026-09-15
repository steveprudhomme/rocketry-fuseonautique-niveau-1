# Chasse Galerie 1 — Animation du vol complet

Animation Blender fondée sur le scénario **H143 — apogée IDÉALE [A]** du modèle OpenRocket 24.12, recalculé le 2026-09-15. Le décor et les textures reprennent la scène du décollage à l'heure dorée. Le rendu animé utilise EEVEE avec un ciel et des effets simplifiés pour accélérer le calcul.

[![Lire la vidéo du vol complet](apercu-video.jpg)](chasse-galerie-1-vol-complet.mp4)

## Livrables

- [Vidéo MP4](chasse-galerie-1-vol-complet.mp4) : 1920 × 1080, 30 images/s, environ 34,5 secondes, sans piste sonore.
- [Scène Blender modifiable](chasse-galerie-1-vol-complet.blend) : géométrie, textures intégrées, caméras et mouvements enregistrés.
- [Trajectoire exportée](vol-h143.csv) et [événements](evenements-h143.csv).

## Lecture de l'animation

Le vol simulé dure **106,843 s**. La vidéo couvre le départ, la propulsion, la montée balistique, l'apogée, la récupération et le premier contact au sol. La montée est montrée en temps réel, la partie centrale de la descente à **×6**, puis les trois dernières secondes de vol reviennent au temps réel. Des pauses encadrent le vol. Le temps simulé, l'altitude et la vitesse sont affichés à l'écran; les accélérations sont signalées.

L'export donne une apogée de **593,893 m**, une extinction moteur à **1,730 s**, un déclenchement de récupération à **10,246 s** et un contact au sol à **106,843 s**. Le marqueur d'apogée est enregistré à 10,245 s; le maximum d'altitude échantillonné survient légèrement avant, vers 10,205 s. Cette distinction vient des événements et pas de temps du moteur de simulation.

## Ce que représentent les images

- Les positions et l'altitude proviennent des échantillons OpenRocket, interpolés dans Blender. Un petit décalage de présentation de 8 cm place les ailerons au-dessus du sol au départ.
- Le vent est nul dans ce scénario. La caméra suit la fusée, ce qui réduit volontairement son déplacement apparent à l'écran.
- Le parachute s'ouvre idéalement à l'apogée : ce scénario n'est pas un réglage d'éjection moteur. L'événement d'éjection nominal à 14,73 s demeure dans l'export mais ne commande pas un second déploiement.
- Le parachute de 36 pouces, son gonflage, les sangles, la séparation de la section avant, la fumée et le paysage sont des représentations illustratives. La forme du parachute gonflé et les longueurs visibles de la récupération ne constituent pas un plan d'assemblage. L'attitude est simplifiée; la vidéo ne prétend pas restituer la rotation calculée ni simuler le choc au sol ou l'affaissement de la voilure.
- Les masses, cotes et conditions du modèle restent provisoires. Il s'agit d'une visualisation du scénario numérique, pas d'une prévision validée du lancement réel.

## Reproduction

Les sources sont dans `sources/` : exportateur Java, préparation Blender et génération des titres. Dépendances utilisées : OpenRocket 24.12, Java 21, Blender 4.3 et FFmpeg avec libass et libx264. Le script de titres utilise Python 3; le script Blender utilise le Python et NumPy livrés avec Blender.

1. Exécuter `ExporterVol.java` avec le JAR OpenRocket dans le classpath et trois arguments : fichier `.ork`, chemin CSV du vol, chemin CSV des événements.
2. Ouvrir en arrière-plan la scène source `plans/rendus-artistiques/chasse-galerie-1-golden-hour.blend` du dépôt et exécuter `animer-vol.py`, suivi de `--` et des quatre chemins : CSV du vol, CSV des événements, dossier final, dossier temporaire. Le script enregistre la scène animée et trois aperçus.
3. Ouvrir la scène animée; rendre les images 1 à 1035 à 30 images/s dans le dossier temporaire. Dans Blender, choisir un chemin PNG absolu avant le rendu si le dossier temporaire d'origine n'existe plus.
4. Générer les titres avec `titres-vol.py`, en lui donnant le dossier temporaire contenant `telemetrie.json`.
5. Assembler les PNG avec FFmpeg à 30 images/s, appliquer le filtre ASS `titres.ass`, encoder avec libx264 en yuv420p et activer `+faststart` pour la lecture web.

La scène `.blend` conserve les mouvements mais les titres sont ajoutés lors de l'encodage MP4. Ils ne sont pas intégrés au rendu brut Blender.

## Présentation dans le README

Le README utilise une image cliquable et un lien explicite vers le MP4 stocké dans le dépôt. Cela donne accès à la vidéo sans dépendre de la prise en charge d'une balise HTML vidéo dans le lecteur Markdown.

## Vérification de la livraison

Les 1 035 images du MP4 ont été décodées sans erreur : H.264, yuv420p, 1920 × 1080, 30 images/s, durée de 34,5 s. Départ, récupération, titres et contact au sol inspectés. Les positions animées reproduisent l’altitude exportée avec un écart numérique maximal inférieur à 0,1 mm; les deux textures sont intégrées à la scène. La dernière image fige les données au contact, dont la vitesse juste avant impact.
