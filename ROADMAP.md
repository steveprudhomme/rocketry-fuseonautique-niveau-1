# Feuille de route — LOC-IV et certification niveau 1

Mise à jour : 2026-09-12. Organisation du projet personnel; cette liste ne constitue pas les exigences officielles de certification. Une validation logicielle ne vaut pas validation du kit ni autorisation de lancement.

## Réalisé

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

## Dépôt et suivi

- [ ] Publier les commits OpenRocket et la révision courante après autorisation de publication applicable, puis les intégrer à `main`.
- [ ] Actualiser le budget à partir des achats réels, taxes et frais compris.
- [ ] Définir les objectifs personnels et un calendrier indicatif.
- [ ] Confirmer et dater les exigences officielles applicables.
- [ ] Alimenter les notes, exercices et glossaire.
- [ ] Préparer les aides à la tâche à faire vérifier.
- [ ] Consigner les activités et étapes de certification.
- [ ] Rédiger un bilan personnel.
