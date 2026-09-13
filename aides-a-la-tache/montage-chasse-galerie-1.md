# Aide à la tâche — Montage de Chasse Galerie 1

- **Date :** 2026-09-13
- **Statut :** fiche de préparation et de suivi, à confronter à la notice livrée et au kit réel avant les collages irréversibles. Montage physique non réalisé ni validé dans cette tâche.
- **Auteur :** Steve Prud’Homme, avec assistance Codex.
- **Public :** amateur de fuséonautique préparant l’assemblage de sa LOC-IV 4 po.
- **Périmètre :** structure, récupération, guidage, finition et relevés finaux. Aucune préparation de moteur, charge d’éjection ou opération de lancement.

## Objectif et références

Organiser le montage complet et savoir **quoi vérifier avant de rendre une zone inaccessible**. La fiche reformule les enseignements des vidéos pour notre projet; elle ne reproduit pas leur déroulé mot à mot.

- **Référence de montage :** [notice LOC PK-48 actuelle, sept pages](https://cdn.shopify.com/s/files/1/0568/7489/3503/files/Loc_IV_Instructions-final.pdf?v=1747083020), consultée le 2026-09-13; comparer à celle livrée avec le kit.
- **Explications vidéo :** [partie 1](../notes/2026-09-13-video-montage-loc-iv-partie-1.md), [partie 2](../notes/2026-09-13-video-montage-loc-iv-partie-2.md), [partie 3](../notes/2026-09-13-video-montage-loc-iv-partie-3.md), avec liens temporels.
- **Projet :** [configuration](../notes/loc-iv-configuration-budget-niveau-1.md), [achats complémentaires](../notes/loc-iv-achats-complement-montage-videos.md), [fiche de mesures](../notes/loc-iv-mesures-kit.md) et [plan d’ensemble](../plans/ensemble/README.md).

**Illustrations :** les images ci-dessous sont des rendus de notre fichier OpenSCAD, pas des photographies des vidéos. Elles servent à reconnaître les pièces. Les dimensions `[A]`, la visserie, les congés et les textiles sont simplifiés; ne pas mesurer une image ni reproduire sa quincaillerie comme un détail de fabrication.

## Préparer la séance

Sortir la notice, les pièces, le nécessaire de mesure et les fournitures du scénario d’achat retenu. Réserver une surface stable où les pièces pourront durcir sans bouger. Lire dosage, temps de travail, durcissement et consignes de protection des produits effectivement choisis; le temps « 5/15/30 min » évoqué dans les vidéos ne remplace pas leur fiche technique. Prévoir gants et protection des yeux adaptés aux produits et aux opérations.

Ne pas reprendre l’alcool sur la peau évoqué en partie 1. Les méthodes de nettoyage et de lissage doivent être compatibles avec le produit; ne pas ajouter de solvant à la résine sur la base d’un geste vidéo.

**Avant le premier collage, consigner :** version du kit, architecture payload retenue, système MR-1, séquence de montage et interfaces de récupération. La voie de base suit la notice du kit. La variante vidéo laisse provisoirement l’anneau arrière ouvert pour les joints internes : ce choix doit être fait dès le départ, pas après avoir collé l’anneau.

## 1 — Inventorier et mesurer

Référence vidéo : partie 1, 02:24. Identifier booster à fentes, payload, ogive, coupleur, cloison, support moteur, trois anneaux, trois ailerons, attaches, retenue, boutons, sangle et parachute. Contrôler les petites pièces dans les sachets et à l’intérieur des tubes.

- [ ] Inventaire comparé à la notice; pièces manquantes ou endommagées notées.
- [ ] Diamètres, parois, longueurs, languettes et quincaillerie relevés dans la fiche de mesures.
- [ ] Pièces accessibles pesées avant assemblage; photos personnelles datées des interfaces.
- [ ] Présence et adaptation du maillon rapide vérifiées : vidéo et notice actuelle diffèrent sur sa fourniture.

**Ne pas transposer le coupleur vidéo à notre hypothèse de 140 mm.** Ses repères de quatre pouces au milieu suggèrent une autre longueur. Les positions d’anneaux et de boutons du SCAD restent également à confirmer.

## 2 — Préparer les surfaces et repérer les orientations

Références : partie 1, 05:46 et 14:44; partie 2, 00:10. Marquer discrètement les pièces et leur avant/arrière. Faire les ajustements par petites reprises, puis dépoussiérer selon le produit et le matériau.

Pour les ailerons, distinguer **contour extérieur**, **racine** et **languette intérieure**. Réserver les zones de liaison; un bouche-pores destiné à la finition ne doit pas empêcher leur collage. L’ogive demande une préparation compatible avec son plastique, différente du bois.

![Aileron avec sa languette — rendu SCAD](../plans/images/aileron.png)

- [ ] Les trois ailerons entrent sans forçage excessif et sans jeu inexpliqué.
- [ ] Les surfaces à coller sont identifiées et propres.
- [ ] Les racines et languettes conservent leur géométrie utile; finition extérieure distinguée de l’ajustement structurel.

## 3 — Vérifier support, anneaux et retenue à blanc

Références : partie 1, 22:19; partie 2, 05:30. « À blanc » signifie sans collage définitif. Présenter les anneaux sur le support, puis l’ensemble dans le booster avec les ailerons. Contrôler simultanément fentes, languettes et retenue, pas seulement une pièce isolée.

![Tube support moteur — rendu SCAD](../plans/images/tube-support-moteur.png)

La vue du tube seul ne montre ni les anneaux ni le montage final. Le [plan écorché](../plans/ensemble/README.md) situe ces composants ensemble.

- [ ] Les languettes rejoignent les surfaces prévues, sans rencontrer un anneau ou un congé prématuré.
- [ ] Les anneaux n’obstruent pas les fentes et restent correctement orientés.
- [ ] L’implantation permet l’utilisation du MR-1 et l’accès à sa visserie.
- [ ] Orientation de l’écrou à griffes vérifiée sur le dessin constructeur; le possible montage inversé signalé sous la partie 2 n’est pas recopié.
- [ ] Tous les repères sont reportés sur les pièces réelles avant démontage.

Les dépassements du tube prescrits pour le MR-1 et pour un autre retainer ne sont pas interchangeables. Un contrôle d’encombrement peut utiliser du matériel inerte approprié; aucune recharge active n’est nécessaire sur l’établi de collage.

## 4 — Préparer les attaches et planifier l’accès intérieur

Références : partie 1, 12:34 et 17:04; partie 2, 10:29. Assembler les attaches et la retenue conformément à la notice du kit, en gardant utilisables filetages et passages. Identifier les zones qui seront inaccessibles après insertion du support.

**Voie notice :** suivre ses étapes de sous-assemblage et d’installation de la sangle avant fermeture. **Variante vidéo :** l’anneau arrière reste temporairement amovible; les renforts internes seront réalisés avant sa pose définitive. Cette variante demande un plan d’accès et une vérification de toutes les portées.

- [ ] Séquence choisie et notée; aucun collage ne ferme prématurément l’accès prévu.
- [ ] Quincaillerie complète, orientation et immobilisation contrôlées.
- [ ] Attache de sangle accessible, ou sangle installée et protégée suivant la séquence retenue.

## 5 — Installer le support et les ailerons

Références : partie 2, 12:24, 15:35 et 26:01. Répéter les gestes à sec avant de préparer la colle : présentation, insertion, alignement, retrait éventuel des pièces servant de contrôle. Choisir un temps de travail compatible avec ces opérations.

Installer le support selon les repères validés et la séquence retenue. Après durcissement requis, installer les ailerons avec contrôle de leur orientation. Les trois doivent rester répartis autour du corps sans inclinaison involontaire. Le pointage en cyanoacrylate gel montré en vidéo est une option de maintien, pas le collage structurel achevé.

- [ ] Fentes, intérieur du support moteur et portées arrière dégagés.
- [ ] Position du support inchangée après collage.
- [ ] Chaque languette est en contact avec les zones de liaison prévues.
- [ ] Alignement contrôlé avant immobilisation définitive, puis après durcissement.

## 6 — Contrôler les joints internes et fermer l’arrière

Référence : partie 2, 28:10–34:59. Dans la variante ouverte, inspecter les joints accessibles avant la fermeture arrière. Dans la voie notice, respecter les zones et la séquence de collage qu’elle prévoit. Un excès de résine peut empêcher la fermeture ou ajouter une masse inutile.

- [ ] Interfaces visibles contrôlées et photographiées avant fermeture.
- [ ] Aucun congé ne gêne les languettes, l’anneau arrière ou le passage moteur.
- [ ] Orientation finale de l’anneau et de la quincaillerie MR-1 revérifiée.
- [ ] Retenue accessible; aucun filetage rempli de colle.
- [ ] Temps de durcissement respecté avant nouvelle manipulation.

**Point de contrôle :** ne pas refermer une zone dont l’ajustement ou le collage reste douteux. Les images SCAD ne représentent pas les congés réels et ne permettent pas d’en valider la résistance.

## 7 — Assembler la section supérieure

Références : partie 1, 33:02 et 37:00; partie 3, 00:10. Préparer la cloison et son attache, puis le coupleur et le payload selon l’architecture retenue.

![Coupleur — rendu SCAD](../plans/images/coupleur.png)

![Cloison — rendu SCAD, sans sa quincaillerie](../plans/images/cloison.png)

Une liaison collée suit la notice. Une liaison payload démontable par rivets est une **variante distincte**, à définir sur les épaisseurs réelles. La retenue de l’ogive et la jonction payload/booster assurant la séparation ont des fonctions différentes.

- [ ] Cloison et attache orientées pour la récupération prévue.
- [ ] Profondeur d’engagement mesurée sur le coupleur réel.
- [ ] Ogive retenue sur la section qui doit rester solidaire pendant la récupération.
- [ ] Jonction prévue pour la séparation conservée fonctionnelle : aucune colle, vis ou rivet ne la bloque.
- [ ] Si rivets retenus : dimensions, appui, quantité, démontabilité et absence d’accrochage contrôlés; aucune cote de perçage copiée sans mesure.

## 8 — Finir les jonctions et poser le guidage

Références : partie 3, 12:45 et 17:10. Réaliser les congés extérieurs conformément au système de collage choisi. Repérer les boutons sur une même ligne entre les ailerons et déterminer leurs positions d’après les points d’ancrage et le coupleur réels.

![Bouton de rail — rendu SCAD simplifié](../plans/images/bouton-rail-1010.png)

- [ ] Fixation adaptée au support réel : anneau ou paroi avec quincaillerie appropriée.
- [ ] Aucun dépassement intérieur susceptible d’accrocher sangle ou suspentes.
- [ ] Aucun conflit avec l’engagement du coupleur.
- [ ] Guidage essayé sur un rail compatible; les boutons ne coincent pas.

La fixation avant par écrou à griffes et vis courte de la vidéo est une possibilité à vérifier, pas une obligation. La notice actuelle décrit une implantation différente : relever et documenter le choix effectué.

## 9 — Installer et examiner toute la récupération

Référence : partie 3, 25:55–36:31. Réunir sangle, attaches, parachute, protection et connecteurs retenus. Suivre un schéma de liaison cohérent avec la notice et les composants choisis. Les noms de nœuds mal reconnus dans les sous-titres ne constituent pas une instruction de nouage; apprendre et faire examiner la liaison réelle avec une personne compétente.

![Parachute — représentation SCAD déployée à plat, pas une voile gonflée](../plans/images/parachute-deploye.png)

- [ ] Tous les éléments qui doivent être récupérés restent reliés.
- [ ] Maillons fermés, ouverture compatible avec les œillets et caractéristiques mécaniques appropriées.
- [ ] Suspentes sans torsion ni accrochage; émerillon éventuel adapté.
- [ ] Protection de parachute et protection de sangle distinguées; textiles inspectables et remplaçables.
- [ ] Présentation et sortie manuelle à sec vérifiées, sans pyrotechnie; aucun blocage sur vis, bords ou coupleur.
- [ ] L’agencement ne favorise pas les collisions des parties suspendues.

Cet examen à sec ne valide ni l’éjection ni le vol. Le SCAD ne représente pas fidèlement le pliage, les nœuds, les maillons ou l’émerillon : il ne faut pas copier son tracé de sangle comme un montage réel.

## 10 — Finition et contrôle de fin de montage

Références : partie 2, préparation de l’ogive; partie 3, 36:33. La peinture finale n’est pas enseignée par la série : appliquer les instructions du système de finition retenu et préserver portées, filetages et zones de séparation. Après démontage pour peinture, remettre toute la quincaillerie nécessaire.

- [ ] MR-1 et boutons présents et vérifiés après finition.
- [ ] Jonctions fonctionnelles, surfaces et récupération inspectées.
- [ ] Produits et modifications consignés; aucun élément provisoire oublié.
- [ ] Fusée complète équipée, sans moteur, pesée; CG mesuré dans le même état depuis la pointe.
- [ ] Masses des connecteurs, rivets, protections et finition réconciliées sans double comptage dans OpenRocket.
- [ ] Cotes reportées dans les modèles, puis simulations recalculées avant étude du vol.

## Trace de montage à remplir

| Date / étape | Pièces et mesures | Produit / lot / dosage selon notice | Durcissement requis / atteint | Contrôle effectué et photo | Écart ou reprise nécessaire |
| --- | --- | --- | --- | --- | --- |
| À renseigner | À renseigner | À renseigner | À renseigner | À renseigner | À renseigner |

## Validation de cette fiche

Rédaction basée sur les trois ensembles de sous-titres et comparaison avec la notice LOC accessible le 2026-09-13. Liens locaux et illustrations contrôlés. Les vidéos ne sont pas une vérification de notre kit; aucun assemblage physique, essai de résistance ou essai d’éjection n’a été réalisé. Les points à mesurer restent ouverts dans la feuille de route.

[Achats par scénario](../notes/loc-iv-achats-complement-montage-videos.md) · [Aides à la tâche](README.md) · [Plans](../plans/README.md)
