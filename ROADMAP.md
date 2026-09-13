# Feuille de route — Chasse Galerie 1 et certification niveau 1

Mise à jour : 2026-09-13. Organisation du projet personnel; cette liste ne constitue pas les exigences officielles de certification. Une validation logicielle ne vaut pas validation du kit ni autorisation de lancement.

## Réalisé

- [x] Rédiger les notes des trois vidéos, une [aide au montage illustrée](aides-a-la-tache/montage-chasse-galerie-1.md) et les [compléments aux achats](notes/loc-iv-achats-complement-montage-videos.md), sans valider physiquement le kit.

- [x] Créer la structure du carnet et les gabarits.
- [x] Documenter la [configuration et le budget](notes/loc-iv-configuration-budget-niveau-1.md).
- [x] Créer les modèles OpenSCAD et OpenRocket, avec hypothèses explicites.
- [x] [Comparer le modèle aux références externes](notes/loc-iv-comparaison-modeles.md), dont le fichier LOC importé dans OpenRocket.
- [x] Archiver les limites de la première version : ailerons surdimensionnés, masses estimées et faibles marges statiques ponctuelles.
- [x] Remplacer le trapèze approximatif par le profil libre LOC, sa position et sa languette, dans les deux modèles (révision 1.1).
- [x] Adapter les fentes et la position dérivée de l'anneau milieu à cette languette.
- [x] Préparer la [fiche de mesures du kit](notes/loc-iv-mesures-kit.md).
- [x] Vérifier la révision 1.1 : rendus OpenSCAD des pièces affectées et de la coupe, chargement XML/ORK, quatre scénarios recalculés dans les deux formats et marges statiques ponctuelles documentées.

## Priorité 1 — Confirmer le kit réel avec Steve

**En attente de mesures, aucune valeur physique confirmée.** Les modèles ne suffisent pas à fermer cette étape.

- [ ] Identifier la version du kit reçu, sa date et son état d'assemblage.
- [ ] Relever le profil des trois ailerons, leur épaisseur, leurs languettes et leurs positions réelles.
- [ ] Mesurer diamètre/paroi des tubes, ogive et épaulement, support moteur et coupleur.
- [ ] Confirmer les positions des trois anneaux et les jeux; vérifier notamment le jeu radial de languette de 0,128 mm produit par les cotes mixtes actuelles.
- [ ] Faire l'inventaire de MR-1, boutons, attaches, sangle, parachute et protecteur.
- [ ] Peser les composants accessibles puis la fusée complète sans moteur, avec tout l'équipement de récupération prévu.
- [ ] Mesurer le centre de gravité depuis la pointe dans exactement le même état que la pesée; consigner l'incertitude et répéter la mesure.

**Critère de fin :** fiche datée remplie avec unités, inventaire pesé, méthode et provenance; aucun nombre calculé présenté comme une mesure.

## Priorité 2 — Réconcilier et vérifier les modèles

- [ ] Arbitrer les différences restantes entre le fichier LOC et le kit : ogive, parois, longueur du support et du coupleur, épaisseurs.
- [ ] Reporter les mesures dans OpenSCAD et OpenRocket, avec date et source.
- [ ] Ajuster masses et répartition pour reproduire la masse totale et le CG mesurés sans compter deux fois moteur ou accessoires.
- [ ] Vérifier toutes les interfaces, notamment ailerons/languettes/fentes/anneaux/support.
- [ ] Recalculer les résultats après les mesures, et remplacer les anciens tableaux d'essais sans effacer leur contexte historique.
- [ ] Vérifier de nouveau les exports OpenSCAD, la concordance XML/ORK et les simulations OpenRocket.

**Critère de fin :** écarts masse/CG et cotes documentés et acceptés sur la base de mesures réelles.

## Priorité 3 — Étudier la configuration de vol

- [ ] Confirmer H143 ou H152, le jeu de données moteur et le matériel réellement disponible.
- [ ] Remplacer les conditions fictives par celles du site, du rail et de la météo prévus.
- [ ] Étudier stabilité sur la trajectoire et dans du vent, vitesse en sortie de rail, altitude et récupération.
- [ ] Déterminer puis faire valider le délai; les essais 13/15 s antérieurs signalent un déploiement à grande vitesse.
- [ ] Confirmer parachute, protecteur et récupération avec la masse finale.
- [ ] Faire vérifier configuration et démarche de certification par l'équipe du lancement.

## Livrable complémentaire — Plan d'ensemble avec vue écorchée

En complément du plan paramétrique, Steve souhaite un **plan technique d'ensemble avec vue écorchée** (*cutaway drawing*). Une version destinée à expliquer la construction et le fonctionnement pourra être présentée comme un **schéma technique écorché**. Une [première édition pédagogique A3, révision A](plans/ensemble/README.md), est produite depuis le modèle 1.1 non mesuré.

- [x] Préparer les trois **vues orthogonales : face, profil et dessus**, alignées, avec orientation et convention de projection clairement indiquées.
- [x] Ajouter une **perspective écorchée** ou une **coupe partielle** du corps pour montrer les composants internes réellement présents : support et enveloppe moteur, anneaux, languettes, coupleur, cloison, attaches et récupération.
- [x] Ajouter repères et nomenclature des composants, légendes, échelle, unités, cotes d'ensemble, cartouche, date et indice de révision; identifier les cotes encore approximatives.
- [x] Définir le niveau attendu : document pédagogique ou document technique soumis à des normes de dessin industriel. Choix révision A : document pédagogique, sans conformité industrielle déclarée. Dans le second cas, identifier les normes applicables et vérifier leur respect avant toute mention de conformité. Prévoir des **dessins de définition des pièces** séparés si des détails de fabrication sont nécessaires.
- [ ] Clarifier la mention d'une **forme octogonale** et d'éléments de capsule (réservoirs, sièges, panneaux solaires, bouclier thermique) : ces exemples ne décrivent pas la LOC-IV actuelle. Confirmer s'ils concernent un autre projet ou une variante avant de les intégrer à un dessin.
- [x] Produire une version lisible à l'écran et imprimable en PDF, conserver la source modifiable dans `plans`, puis vérifier l'alignement des vues, la lisibilité des cotes et la cohérence avec la révision 1.1 actuelle du modèle.
- [ ] Réviser le PDF et ses annotations après intégration des mesures physiques du kit.

**Critère de fin :** plan d'ensemble réunissant les trois vues et la vue écorchée, avec repérage des pièces et statut des cotes explicites. Aucune conformité industrielle ni aptitude à la fabrication déclarée sans vérification correspondante.

## Décoration — Design et fabrication du décalque

- [x] Consigner l'[orientation retenue pour l'habillage](notes/chasse-galerie-1-decalque.md) : vinyle blanc opaque imprimé, laminage satiné compatible, fabrication chez un spécialiste et un morceau par section démontable. Produit et pose restent à valider sur échantillon.

- [ ] Concevoir un décalque original pour **Chasse Galerie 1**, associant le thème de la chasse-galerie et celui du **drapeau du Québec**; préparer des propositions montrant le nom, les motifs et leur disposition sur la fusée.
- [ ] Mesurer les surfaces à décorer sur le kit et définir dimensions, emplacement, raccords et dégagements autour des ailerons, boutons de rail et jonctions démontables.
- [ ] Comparer les moyens de fabrication et de pose (par exemple vinyle adhésif découpé ou imprimé, décalcomanie à l'eau, fournisseur spécialisé) : équipement, compatibilité avec la peinture et le vernis, tenue, coût et disponibilité.
- [ ] Produire les sources modifiables, un fichier d'impression à l'échelle avec repère de contrôle et un aperçu sur la fusée; conserver les fichiers et leur notice dans `plans`.
- [ ] Rédiger un pas à pas de fabrication et de pose du décalque physique, puis tester un échantillon sur une surface représentative avant la pose finale.

**Critère de fin :** design retenu, dimensions vérifiées, méthode essayée et coût ajouté au budget.

## Décoration numérique — Textures et aides à la tâche

- [ ] Vérifier séparément la possibilité d'appliquer une texture de décalque dans **OpenSCAD**, dans un **autre logiciel 3D à choisir**, et dans **OpenRocket**. Consigner versions testées, formats acceptés, limites et solutions de remplacement dans une note comparative; ne pas supposer que les trois logiciels offrent les mêmes fonctions.
- [ ] Produire une texture issue du design retenu et les fichiers nécessaires à chaque logiciel compatible, en documentant résolution, transparence, échelle, orientation et raccord autour du tube.
- [ ] Créer une aide à la tâche pour débutant : **produire une texture de décalque**, depuis le dessin source jusqu'à l'export et au contrôle de ses dimensions.
- [ ] Créer un pas à pas illustré pour **appliquer la texture sur la fusée**, avec un parcours pour OpenSCAD, le logiciel 3D retenu et OpenRocket selon les possibilités vérifiées. Pour une fonction non disponible, expliquer la limite et donner un parcours de remplacement testé.
- [ ] Vérifier le résultat sur la fusée complète, les jonctions et les rendus/exportations; distinguer l'apparence visuelle des propriétés utilisées en simulation et reporter la masse réelle de la finition si nécessaire.

**Critère de fin :** fichiers de démonstration et guides reproductibles, avec capacités et limites vérifiées pour chaque logiciel.

## Comparaison complémentaire — Modèles SCAD et série de montage

Les [comparaisons existantes](notes/loc-iv-comparaison-modeles.md) et les notes des [parties 1](notes/2026-09-13-video-montage-loc-iv-partie-1.md), [2](notes/2026-09-13-video-montage-loc-iv-partie-2.md) et [3](notes/2026-09-13-video-montage-loc-iv-partie-3.md) constituent le point de départ; la comparaison systématique reste à faire.

- [ ] Identifier précisément le kit assemblé et les éventuels fichiers de modèle cités dans les trois vidéos, puis comparer l'ensemble aux versions SCAD du projet.
- [ ] Ajouter aux notes un tableau des ressemblances et différences : géométrie, ailerons, support moteur, anneaux, coupleur, retenue MR-1, boutons de rail, attaches, récupération et méthode de montage.
- [ ] Pour chaque différence, relever la version du fichier SCAD, la source vidéo et son repère temporel, la valeur documentée ou l'observation, l'incertitude et la mesure à effectuer sur le kit. Ne pas déduire une cote exacte d'une simple image.
- [ ] Illustrer les différences utiles avec des vues SCAD et relier les corrections proposées aux tâches de validation des modèles; conserver les différences de version sans les transformer automatiquement en corrections.

## Budget complet — Petit matériel et décoration

La [liste complémentaire issue des vidéos](notes/loc-iv-achats-complement-montage-videos.md) existe déjà. Il reste à la compléter, à vérifier les quantités et à chiffrer les scénarios avec le [budget principal](notes/loc-iv-configuration-budget-niveau-1.md).

- [ ] Inventorier l'atelier et compléter les listes de petit matériel, outils et consommables pour toutes les étapes du montage et de la finition; distinguer ce qui est fourni dans le kit, déjà possédé et à acheter.
- [ ] Ajouter les fournitures et prestations nécessaires au décalque selon la méthode retenue, y compris les essais, l'impression et la pose.
- [ ] Chiffrer les quantités et les conditionnements des scénarios S1/S2/S3 avec prix datés et sources, taxes et livraison; distinguer outils réutilisables et consommables.
- [ ] Réconcilier les lignes détaillées avec les enveloppes déjà prévues pour éviter les doubles comptes, puis présenter le **coût total de la fusée, kit compris**, le **reste à acheter** et les frais de vol/certification séparément.

## Identité documentaire — Petits drapeaux du Québec

- [ ] Recenser les principaux documents officiels du projet à décorer : accueil du dépôt, plans et cartouches, aides à la tâche et notes de référence.
- [ ] Préparer un petit visuel fidèle du drapeau du Québec, avec source et conditions de réutilisation documentées, puis définir une taille et un emplacement cohérents.
- [ ] Intégrer le drapeau aux documents retenus et à leurs sources de génération; vérifier sa lisibilité sur GitHub et dans les PDF, à l'écran et à l'impression.

## Dépôt et suivi

- [ ] Faire examiner la séquence de montage retenue et les interfaces de retenue/récupération sur le kit réel.

- [x] Publier les modèles OpenRocket, la révision 1.1 et la galerie des composants, puis les intégrer à `main` (commit `9aba35d`).
- [ ] Maintenir le budget à jour avec les achats réels après le chiffrage détaillé prévu dans « Budget complet ».
- [ ] Définir les objectifs personnels et un calendrier indicatif.
- [ ] Confirmer et dater les exigences officielles applicables.
- [ ] Alimenter les notes, exercices et glossaire.
- [ ] Préparer les aides à la tâche à faire vérifier.
- [ ] Consigner les activités et étapes de certification.
- [ ] Rédiger un bilan personnel.
