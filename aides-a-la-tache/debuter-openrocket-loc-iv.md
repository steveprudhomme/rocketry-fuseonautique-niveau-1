# Aide à la tâche — Construire et simuler la LOC-IV complète dans OpenRocket

**Projet et fusée : Chasse Galerie 1.** Base technique : kit LOC-IV 4 po. Les noms de fichiers `loc-iv-*` sont conservés pour maintenir les liens et la traçabilité des références.

- **Date :** 2026-09-12
- **Statut :** brouillon pédagogique; inventaire et réglages contrôlés contre le modèle du dépôt. Parcours dans l’interface à faire essayer par une personne débutante.
- **Auteur :** Steve Prud’Homme, avec assistance Codex.
- **Public :** amateur de fuséonautique de loisir n’ayant jamais utilisé OpenRocket.
- **Référence :** LOC-IV révision 1.1, fichier créé avec OpenRocket 24.12.

## Objectif et contexte

Cette fiche couvre **la fusée entière et son étude de vol** : ogive, tubes, coupleur, cloison, support moteur, trois anneaux, trois ailerons avec languettes, boutons de rail, attaches, MR-1, récupération, finition, moteurs et quatre simulations. Elle permet de parcourir le fichier existant **ou de reconstruire le modèle complet dans un document vide**.

OpenRocket représente la fusée avec des composants et calcule son comportement en vol. Vous utilisez principalement des fenêtres de réglage; il n’est pas nécessaire d’écrire du code. Le XML est une représentation textuelle de ce même document, abordée à la fin.

Les valeurs ci-dessous reproduisent **notre modèle de travail**, pas un kit déjà mesuré. `[A]` indique une approximation, `[F]` une cote du fichier LOC, et « nominal » une valeur documentée. Le [plan OpenSCAD](../plans/README.md) explique les sources détaillées. La [fiche de mesures](../notes/loc-iv-mesures-kit.md) est encore à remplir.

## Références applicables

- [Configuration et budget LOC-IV](../notes/loc-iv-configuration-budget-niveau-1.md) : source principale.
- [Modèle OpenRocket natif](../plans/loc-iv-4po.ork), [XML complet](../plans/loc-iv-4po.xml) et [notice du modèle](../plans/loc-iv-openrocket.md).
- [Rapport des essais logiciels](../plans/loc-iv-openrocket-verification.md) : résultats exploratoires et limites.
- [Plan d’ensemble écorché](../plans/ensemble/README.md), [galerie des pièces](../plans/images/README.md) et [comparaison avec LOC](../notes/loc-iv-comparaison-modeles.md).

## Parcours conseillé

| Séance | Travail | Résultat à conserver |
| --- | --- | --- |
| Découvrir | Étapes 1 à 3 | Une copie ouverte et l’arborescence comprise. |
| Construire ou vérifier | Étapes 4 à 9 | La fusée complète, accessoires compris. |
| Préparer l’étude | Étapes 10 à 12 | Masse/CG documentés, configurations moteur et récupération cohérentes. |
| Simuler et partager | Étapes 13 à 16 | Résultats commentés et fichiers enregistrés. |

## 1. Installer et ouvrir le bon fichier

1. Installer OpenRocket depuis le [site officiel](https://openrocket.info/). Utiliser la distribution adaptée à votre système; le modèle du dépôt a été vérifié avec la version 24.12. Les intitulés peuvent différer dans une version plus récente.
2. Télécharger le dépôt GitHub avec **Code → Download ZIP**, puis extraire l’archive, ou utiliser votre dossier local existant.
3. Dans OpenRocket, choisir **File → Open / Fichier → Ouvrir**, puis `plans/loc-iv-4po.ork`.
4. Faire **Save As / Enregistrer sous** et créer `loc-iv-apprentissage.ork` dans un dossier personnel. Les manipulations suivantes se font dans cette copie.
5. Si vous souhaitez tout reconstruire, garder la référence ouverte, puis créer un **nouveau document** et l’enregistrer sous `loc-iv-reconstruction.ork`. Reprendre les étapes 3 à 12 dans ce document.

**Contrôle :** la copie de référence affiche un étage LOC-IV et quatre simulations. L’absence de résultats au premier chargement est normale : les scénarios sont enregistrés sans résultats pré-calculés.

## 2. Comprendre l’écran et les mots utiles

Les trois espaces de travail sont **Rocket Design** (conception), **Motors & Configuration** (moteurs et configurations) et **Flight Simulations** (simulations). Dans la conception, l’arborescence liste les composants; un double-clic ouvre les propriétés d’une pièce. Pour ajouter une pièce, sélectionner d’abord son **parent**, puis le type voulu. Un choix grisé peut indiquer que le parent n’est pas compatible. Voir la [présentation officielle de l’interface](https://wiki.openrocket.info/Getting_Started).

| Mot | Sens dans cette fiche |
| --- | --- |
| Parent / enfant | Un tube peut contenir un parachute : le tube est le parent. La position peut être mesurée depuis ce parent. |
| Configuration | Un choix de moteur et de réglages associés, notamment de récupération. |
| Simulation | Un calcul utilisant une configuration et des conditions de lancement. Plusieurs simulations peuvent partager une configuration. |
| CG | Centre de gravité : point d’équilibre associé à la répartition des masses. |
| CP | Centre de pression : position résultant du calcul aérodynamique. |
| Apogée | Point le plus haut de la trajectoire. |
| Cd | Coefficient de traînée; ici, notamment celui du parachute. |
| Override | Remplacement d’une masse ou d’un CG calculé par une valeur saisie. |

Choisir des unités familières dans les préférences ou les sélecteurs des champs : **mm**, **g**, **m/s**, **m** et **s**. Lire l’unité affichée avant chaque saisie. Les tableaux de cette fiche utilisent des **diamètres**, sauf mention contraire; le XML stocke souvent des **rayons**, en mètres.

## 3. Construire l’arborescence entière

Dans un document vide, nommer la fusée « LOC-IV — apprentissage » et conserver **un seul étage**. Ajouter l’ogive, puis les deux tubes extérieurs successifs. Ajouter ensuite les enfants sous le parent indiqué ci-dessous. Le regroupement payload désigne une section de la même fusée, pas un étage propulsif supplémentaire.

```text
LOC-IV
└── Étage unique
    ├── Ogive
    ├── Section payload
    │   ├── Coupleur
    │   │   └── Cloison payload
    │   └── Attache payload — masse
    └── Booster
        ├── Support moteur — tube interne déclaré support moteur
        ├── Anneau 1 arrière
        ├── Anneau 2 milieu
        ├── Anneau 3 avant
        ├── Bouton de rail avant
        ├── Bouton de rail arrière
        ├── Parachute
        ├── Sangle
        ├── Protecteur — masse
        ├── MR-1 et visserie — masse
        ├── SCM-3 avant — masse
        ├── Époxy et finition — masse
        └── Un jeu de 3 ailerons à profil libre, languettes incluses
```

**Le moteur se choisit ensuite dans les configurations.** Ne pas ajouter un cylindre ou une masse représentant le boîtier en supplément du moteur sélectionné. Le ProDAT-38 reste au sol : aucune masse de vol à ajouter pour cet outil.

**Contrôle :** 19 composants sous l’étage, en comptant chaque entrée de l’arbre ci-dessus une fois et le jeu de trois ailerons comme une seule entrée. La fusée et l’étage sont des conteneurs supplémentaires.

## 4. Définir l’ogive et les deux tubes extérieurs

Pour chaque composant : double-cliquer, saisir les dimensions, choisir le matériau, donner un nom lisible et noter les hypothèses dans **Comments / Commentaires**. Les commandes de création de composants et leurs propriétés sont présentées dans le [guide de conception officiel](https://wiki.openrocket.info/Basic_Rocket_Design).

| Composant / type | Dimensions à reproduire, en mm | Matériau du modèle |
| --- | --- | --- |
| Ogive / Nose cone | Forme ellipsoïdale `[A]`; longueur exposée 330,2 calculée; diamètre de base 101,6 nominal; paroi 2 `[A]` | Polypropylène personnalisé, 900 kg/m³ `[A]` |
| Épaulement de l’ogive | Longueur 70; diamètre extérieur 98,1; paroi 2; extrémité non bouchée, tous `[A]` | Même matériau que l’ogive |
| Payload / Body tube | Longueur 279,4 nominale; diamètre extérieur 101,6 nominal; paroi 1,6 `[A]`, donc intérieur 98,4 | Carton personnalisé, 680 kg/m³ `[A]` |
| Booster / Body tube | Longueur 584,2 nominale; mêmes diamètres et paroi que le payload | Même carton `[A]` |

Garder la finition extérieure correspondant à `normal` dans le XML de référence. Elle est estimée : ne pas choisir une surface polie uniquement pour augmenter l’altitude calculée. Pour reproduire les masses du brouillon, créer des matériaux personnalisés aux densités indiquées plutôt que de supposer que le matériau homonyme de la bibliothèque a la même densité.

Placer les trois éléments extérieurs **bout à bout**, dans l’ordre ogive, payload, booster. Ne pas ajouter les 70 mm de l’épaulement à la longueur exposée : il entre dans le tube.

**Contrôle :** 330,2 + 279,4 + 584,2 = **1193,8 mm**, pointe à arrière du corps. L’affichage de longueur totale peut inclure les ailerons dépassants ajoutés plus tard.

## 5. Placer le coupleur, la cloison et le support

OpenRocket mesure vers l’arrière à partir de la pointe, à l’inverse du Z du plan SCAD. Pour les composants ci-dessous, choisir une position **depuis l’avant du parent** (*Top of parent component* ou équivalent), puis saisir le début indiqué. Une position supérieure à la longueur du parent est possible si la pièce dépasse de celui-ci.

| Pièce / type | Parent | Début depuis l’avant du parent (mm) | Géométrie (mm) |
| --- | --- | ---: | --- |
| Coupleur / Tube coupler | Payload | 209,4 | Longueur 140; diamètre extérieur 98,1; paroi 1,6 `[A]` |
| Cloison / Bulkhead | Coupleur | 133,65 | Diamètre 94,9; épaisseur 6,35 `[A]` |
| Support / Inner tube | Booster | 281,375 | Longueur 300; diamètre extérieur 41,4; paroi 1,45; intérieur 38,5 `[A]` |

Le coupleur utilise le carton à 680 kg/m³; la cloison utilise le contreplaqué à 600 kg/m³; le support utilise le carton. Ces densités restent estimées.

Dans les propriétés du **support**, ouvrir la partie **Motor** et activer **This component is a motor mount**. Choisir un moteur unique, pas une grappe. Le dépassement moteur derrière le support (*motor overhang*) vaut **7,825 mm** dans le fichier, correspondant à 5 mm derrière le corps. Le [FAQ officiel](https://wiki.openrocket.info/FAQ) distingue bien la déclaration du support, la configuration du moteur et son affectation à une simulation.

**Contrôle :** le coupleur engage 70 mm dans le payload et dépasse de 70 mm vers le booster. Le support finit 2,825 mm avant l’arrière du corps. Ne pas ajouter une butée moteur non documentée pour compléter visuellement le tube.

## 6. Ajouter les trois anneaux et les deux boutons

Créer **trois anneaux distincts**, chacun sous le booster, car leurs espacements ne sont pas identiques. Type : **Centering ring**; nombre d’instances : 1 chacun.

| Anneau | Début depuis l’avant du booster (mm) | Diamètre extérieur / intérieur / épaisseur (mm) |
| --- | ---: | --- |
| 1, arrière | 571,850 | 98,4 / automatique autour du support / 6,35 |
| 2, milieu | 442,500 | mêmes réglages |
| 3, avant | 287,725 | mêmes réglages |

Utiliser le contreplaqué à 600 kg/m³ `[A]`. L’épaisseur 6,35 est nominale; les positions et interfaces sont à mesurer. Vérifier que le diamètre intérieur automatique donne **41,4 mm** avec ce support.

Ajouter **deux Rail buttons**, chacun avec une seule instance, sous le booster :

| Réglage | Avant | Arrière |
| --- | ---: | ---: |
| Début depuis l’avant du booster (mm) | 154,2 | 514,2 |
| Angle autour du corps | 60° | 60° |
| Diamètre extérieur / col (mm) | 12 / 7 | 12 / 7 |
| Hauteur totale / base / collerette (mm) | 9 / 3 / 3 | 9 / 3 / 3 |
| Hauteur de tête de vis modélisée (mm) | 0 | 0 |
| Masse imposée, visserie comprise (g) | 3 | 3 |

Les dimensions des boutons sont `[A]`; « 1010 » ne veut pas dire diamètre 10 mm. Le matériau indicatif vaut 1420 kg/m³, mais la masse imposée de 3 g remplace son calcul. L’angle des boutons est distinct de l’angle de lancement.

**Contrôle :** trois anneaux autour du support et deux boutons sur le même côté, espacés axialement de 360 mm. Ne pas créer deux jeux de deux boutons.

## 7. Reproduire les trois ailerons LOC, avec leurs languettes

Sous le booster, ajouter un **Freeform fin set / jeu d’ailerons à profil libre**. Si la version propose d’abord un jeu trapézoïdal, utiliser sa conversion en profil libre avant de modifier les points. Un simple trapèze ne reproduit pas le bord arrière LOC.

Dans l’éditeur du contour, saisir ces cinq sommets dans l’ordre. Les coordonnées sont en mm, X vers l’arrière depuis l’avant de la racine, Y vers l’extérieur :

| Sommet | X (mm) | Y (mm) |
| --- | ---: | ---: |
| 1 | 0 | 0 |
| 2 | 142,875 | 107,95 |
| 3 | 206,375 | 107,95 |
| 4 | 206,375 | 31,75 |
| 5 | 171,45 | 0 |

Ces points viennent du fichier LOC `[F]`. Dans l’éditeur, utiliser le format décimal accepté par votre installation et contrôler les valeurs affichées; dans le XML, le séparateur est un point et l’unité le mètre.

Compléter le jeu : **3 ailerons**, rotation autour du corps **0°**, angle d’inclinaison (*cant*) **0°**, épaisseur **3,175 mm** nominale, section **rectangulaire / square**, contreplaqué **600 kg/m³ `[A]`**. Début du jeu : **412,75 mm depuis l’avant du booster**. Rayon de congé modélisé : **0**; la masse de colle figure dans les consommables.

Dans les réglages des languettes, entrer **longueur 117,475 mm**, **hauteur/profondeur 29,972 mm** et **retrait 38,1 mm depuis l’avant de la racine**. Ne pas remplacer ces valeurs par un ajustement automatique sans contrôler le kit.

**Contrôle :** racine 171,45 mm, portée 107,95 mm, trois ailerons répartis à 120°. Ils dépassent le corps de **34,925 mm**, donnant **1228,725 mm hors tout**. L’épaisseur du fichier LOC tiers était 3 mm; notre référence conserve 3,175 mm selon les autres sources. L’écart reste à arbitrer sur le kit. Les languettes laissent actuellement un jeu radial nominal de 0,128 mm avec le support estimé; ce n’est pas une tolérance validée.

## 8. Ajouter toute la récupération

Ajouter **Parachute** et **Shock cord / sangle** sous le booster. Ils restent rangés dans le modèle de conception; le déploiement est un événement de simulation.

| Réglage | Parachute | Sangle |
| --- | --- | --- |
| Dimension nominale déployée | Diamètre 914,4 mm, soit 36 po | Longueur 4572 mm, soit 15 pi |
| Position depuis l’avant du booster | 136,375 mm `[A]` | 140,375 mm `[A]` |
| Encombrement rangé : longueur × diamètre | 100 × 65 mm `[A]` | 96 × 32 mm `[A]` |
| Masse totale imposée | 80 g `[A]`, suspentes incluses | 50 g `[A]` |
| Autres réglages | Cd manuel 0,8; 8 suspentes de 457,2 mm `[A]` | Largeur physique nominale 9,525 mm documentée dans les notes |

Le tissu indicatif du parachute vaut 67 g/m² et les suspentes 1,8 g/m; la sangle vaut environ 10,936 g/m. **Avec les masses imposées ci-dessus, ces matériaux n’ajoutent pas une seconde masse.** Le Cd, les suspentes et le pliage sont des hypothèses, pas des mesures.

Le protecteur est ajouté comme masse à l’étape suivante. Ce modèle ne calcule pas son ouverture ni les efforts détaillés dans les attaches. Il traite une récupération simplifiée de l’ensemble sous un parachute, sans double déploiement.

**Contrôle :** la récupération comprend bien parachute, suspentes incluses dans ses 80 g, sangle, protecteur et attaches. Les événements de sortie du parachute sont réglés à l’étape 12.

## 9. Ne pas oublier les masses sans forme aérodynamique détaillée

Ajouter les cinq **Mass components / composants de masse** ci-dessous. Leurs cylindres visibles servent à représenter leur encombrement et leur répartition estimée, pas la forme exacte des accessoires.

| Nom | Parent | Début depuis l’avant du parent (mm) | Longueur × diamètre représentés (mm) | Masse (g) |
| --- | --- | ---: | --- | ---: |
| Attache payload | Payload | 344 | 12 × 30 | 10 |
| Protecteur 12 po proposé | Booster | 136,375 | 100 × 30 | 30 |
| MR-1 clips et visserie | Booster | 576 | 6 × 30 | 20 |
| SCM-3 avant | Booster | 267 | 20 × 30 | 15 |
| Époxy et finition répartis | Booster | 20 | 540 × 30 | 60 |

Tout ce tableau est `[A]`. Garder ces masses centrées radialement pour reproduire le fichier. La position « 344 » de l’attache payload dépasse les 279,4 mm du tube parent : elle place l’attache vers l’arrière du coupleur. Ce dépassement est prévu, pas une faute d’unité.

Le protecteur carré de 304,8 mm (12 po) est proposé, pas imposé par les notes. Les clips MR-1 ne sont pas remplacés par un retainer fileté imaginaire. Ne pas ajouter une deuxième masse de colle via des congés si elle reste déjà incluse dans les 60 g.

**Contrôle :** aucune masse de boîtier, recharge ou ProDAT ajoutée dans ces cinq entrées. Toutes les pièces de la configuration modélisée sont maintenant représentées, soit par leur géométrie, soit par une masse explicitement simplifiée.

## 10. Vérifier la masse et le centre de gravité de l’ensemble

1. Choisir l’état **sans moteur** pour comparer la masse structurelle.
2. Examiner la masse calculée de chaque composant et ses remplacements (*Overrides*).
3. Quand une pièce a été pesée, saisir sa masse mesurée dans ses propriétés et commenter la date et la source. Pour le jeu d’ailerons, vérifier si le champ s’applique au jeu complet : contrôler la variation de masse totale pour éviter un facteur trois.
4. Comparer le total à la fusée complète équipée pour le vol **sans moteur**, pesée dans ce même état.
5. Comparer le CG affiché à la distance mesurée **depuis la pointe**, dans le même état que la pesée.

Le brouillon actuel donne environ **1033 g sans moteur** et un CG à **747,8 mm depuis la pointe**. Ces valeurs sont des repères de reproduction du fichier, jamais des mesures à recopier dans votre fiche de kit.

Un remplacement global à l’étage demande une attention particulière : vérifier si **Override mass and CG of all subcomponents** est activé. Selon ce choix, une valeur d’étage peut remplacer l’ensemble ou s’ajouter aux enfants. Pour un débutant, privilégier d’abord la correction des composants; faire vérifier un remplacement global et toujours contrôler ensuite le total sans moteur. Le [guide officiel des remplacements](https://wiki.openrocket.info/Common_Component_Characteristics) explique ce périmètre.

Ne pas déplacer des masses au hasard pour obtenir un indicateur de stabilité favorable. Une masse correcte avec un mauvais CG reste un modèle incorrect. Les remplacements globaux ne rendent pas exacte la répartition détaillée des masses.

## 11. Définir les moteurs et les quatre configurations

Dans **Motors & Configuration**, créer ou vérifier quatre configurations portant les noms de l’étape 12. Pour chacune, sélectionner le support moteur, puis **Select motor**. Filtrer sur Cesaroni et diamètre 38 mm; inspecter les détails du jeu de données, pas seulement le texte H143 ou H152.

| Référence retenue dans le dépôt | Masse chargée du jeu | Dimensions du jeu | Empreinte pour contrôle avancé |
| --- | ---: | --- | --- |
| Cesaroni 247H143-13A | 347 g | 38 × 185 mm | `f27036309584bed36c3a39481f356b5f` |
| Cesaroni 276H152-15A | 298 g | 38 × 185 mm | `ace3745f12a3b82a68514e71b1faedc0` |

La base comporte un autre jeu H143 à 308,9 g : ce n’est pas celui retenu ici. Ne pas mélanger la courbe d’un jeu et la masse d’un autre. La longueur de 185 mm dans la base diffère des 186 mm de l’enveloppe nominale SCAD; l’écart est documenté, sans retoucher les données moteur.

Conserver l’allumage automatique au lancement, sans retard d’allumage, pour cet étage unique. Le moteur chargé, boîtier compris, entre dans la masse via cette sélection. Vérifier que le total chargé augmente de 347 g ou de 298 g par rapport au même modèle sans moteur. Voir le [guide officiel des configurations et simulations](https://wiki.openrocket.info/Basic_Flight_Simulation).

**Contrôle :** un seul moteur dans un seul support, et le bon moteur dans chaque configuration. Les quatre configurations partagent la même géométrie; elles ne représentent pas quatre fusées à reconstruire.

## 12. Relier la configuration au déploiement du parachute

Dans les réglages de récupération du parachute ou la table des déploiements, sélectionner **la configuration concernée** puis son événement. Ne pas changer seulement le réglage par défaut en supposant qu’il s’applique à toutes les variantes.

| Configuration | Moteur / délai moteur enregistré | Événement du parachute | Délai supplémentaire de déploiement |
| --- | --- | --- | ---: |
| H143 — apogée IDÉALE `[A]` | H143 / 13 s | Apogée | 0 s |
| H143 — éjection 13 s ESSAI `[A]` | H143 / 13 s | Éjection moteur | 0 s |
| H152 — apogée IDÉALE `[A]` | H152 / 15 s | Apogée | 0 s |
| H152 — éjection 15 s ESSAI `[A]` | H152 / 15 s | Éjection moteur | 0 s |

Le **délai moteur** est compté après la fin de combustion. Le **délai supplémentaire du parachute** est ajouté à l’événement choisi. Saisir 13 s dans les deux champs retarderait encore le parachute : ce n’est pas le scénario du dépôt.

Les scénarios à l’apogée imposent une ouverture idéale; ils ne prouvent pas que le mécanisme réel pourra la produire. Une altitude de déploiement peut rester mémorisée dans un champ sans agir si l’événement choisi n’est pas un déclenchement à altitude donnée. **13 s et 15 s sont des essais, pas des réglages recommandés pour le vol.**

**Contrôle :** passer successivement par les quatre configurations et lire chaque événement. Copier une simulation seule ne crée pas forcément une configuration indépendante : pour comparer deux délais sans modifier l’essai d’origine, copier aussi la configuration et lui donner un nom distinct.

## 13. Créer ou vérifier les conditions de simulation

Dans **Flight Simulations**, créer une simulation par configuration avec **New simulation**, ou ouvrir les propriétés des quatre essais existants. Vérifier la configuration sélectionnée dans chaque simulation.

Pour reproduire le cas de référence, utiliser les conditions **fictives** suivantes :

| Champ | Valeur de référence |
| --- | --- |
| Longueur de rail | 2,4 m |
| Inclinaison par rapport à la verticale | 0° |
| Direction du rail | 0°; orientation automatique face au vent désactivée |
| Modèle de vent actif | Vent moyen / Average |
| Vitesse moyenne, direction, turbulence | 0 m/s, 0°, 0 |
| Altitude du site | 0 m |
| Latitude / longitude | 45° / 0°; aucun site réel désigné |
| Atmosphère | ISA, atmosphère standard |
| Méthode géodésique | Sphérique |
| Pas de temps / durée maximale | 0,02 s / 300 s |

Le XML contient aussi une couche de vent pour un autre mode, **inactif**. Pour reproduire ce cas calme, garder le mode **Average**; ne pas activer le profil multicouche par inadvertance. Aucun réglage de graine aléatoire n’est nécessaire pour cette initiation sans turbulence.

Pour une étude du lancement réel, **dupliquer** les essais et remplacer ces valeurs par les conditions documentées du site et du rail. La longueur effective de guidage dépend aussi des boutons. Étudier ensuite plusieurs conditions plausibles de vent et de masse, clairement nommées; ne pas supprimer le cas de référence.

**Contrôle :** chaque ligne de simulation montre la configuration voulue et possède ses propres conditions. Après toute modification, lancer de nouveau le calcul; les anciens résultats ne se mettent pas nécessairement à jour seuls.

## 14. Exécuter et lire les résultats du vol complet

Sélectionner une ou plusieurs simulations, puis **Run simulations**. Attendre la fin. Ouvrir les avertissements avant de comparer les altitudes. Le [guide de simulation](https://openrocket.readthedocs.io/en/latest/user_guide/basic_flight_simulation.html) décrit ce parcours.

Dans **Plot / Export**, choisir le temps comme axe horizontal, puis examiner les grandeurs disponibles dans votre version : altitude, vitesse, accélération, marge de stabilité et vitesse de descente. Afficher les événements : décollage, fin de combustion, apogée, éjection, déploiement et arrivée au sol. Les courbes doivent permettre de suivre tout le vol, pas seulement sa montée.

| Moment | Question à vérifier |
| --- | --- |
| Avant lancement | Le CG, le CP et la masse correspondent-ils à la configuration chargée sélectionnée ? |
| Sortie du rail | La vitesse et les avertissements signalent-ils un problème de guidage ? |
| Montée | Comment évoluent vitesse, accélération et stabilité ? |
| Apogée / ouverture | Le parachute sort-il au moment prévu et à quelle vitesse ? |
| Descente | La vitesse de descente et la dérive sont-elles compatibles avec l’étude du site et de la récupération ? |
| Fin du calcul | L’atterrissage est-il atteint ou la simulation est-elle simplement arrêtée à sa durée maximale ? |

La marge exprimée en **calibres** rapporte l’écart CP–CG au diamètre de référence. Avec les distances mesurées depuis la pointe, un CP plus loin vers l’arrière que le CG donne un écart positif. Cette valeur dépend des conditions de calcul; un nombre affiché dans la vue de conception ne remplace pas l’examen de la trajectoire. Cette fiche ne fixe pas de seuil universel d’acceptation.

Pour comparer au [rapport du dépôt](../plans/loc-iv-openrocket-verification.md), le brouillon 1.1 donnait environ 594 m avec H143 et 677 m avec H152 dans le cas calme. Les essais d’éjection 13/15 s signalaient une ouverture à grande vitesse. Un résultat différent doit conduire à comparer version, jeu moteur, géométrie, masses et conditions; ne pas ajuster les entrées pour atteindre artificiellement ces altitudes.

**Absence d’avertissement ne signifie pas validation du vol.** Les cas idéaux restent idéaux; la résistance, le fonctionnement réel des attaches et le pliage ne sont pas validés par ces calculs.

## 15. Faire un exercice complet et conserver une trace

Dans la copie d’apprentissage :

1. Vérifier les 19 composants avec les étapes 4 à 9 et sélectionner l’état sans moteur.
2. Noter la masse et le CG calculés, avec le statut « hypothèses du modèle ».
3. Passer à H143 puis H152 et constater le changement de masse chargée.
4. Lancer les quatre scénarios, lire les événements de déploiement et consigner chaque avertissement.
5. Dupliquer un essai, garder sa configuration et modifier **une condition fictive**, par exemple un vent moyen de 2 m/s; le nommer « apprentissage vent fictif ». Relancer et comparer la dérive. Ce cas n’est pas une météo réelle.
6. Enregistrer et rouvrir le `.ork`, puis vérifier composants, configurations et simulations.

Conserver dans les notes un tableau rempli, sans inventer les cases manquantes :

| Date / version du modèle | Configuration et jeu moteur | Masse sans moteur / CG et provenance | Rail / atmosphère / vent | Apogée / sortie de rail / ouverture / descente | Avertissements et prochaine action |
| --- | --- | --- | --- | --- | --- |
| À renseigner | À renseigner | Mesures ou hypothèses explicites | À renseigner | Valeurs avec unités | À renseigner |

Exporter les données utiles en **CSV** depuis les résultats pour les relire dans un tableur. Les documents imprimables et gabarits se trouvent dans **File → Print design info** selon la version. Un gabarit d’aileron doit être vérifié en échelle réelle et contre les mesures avant tout usage dimensionnel.

## 16. Conserver le projet complet et synchroniser le XML

Le `.ork` est le fichier de travail à conserver. Un PNG, un PDF ou un CSV ne remplace pas son arbre de composants et ses simulations.

Pour le format utilisé dans ce dépôt, le `.ork` est une archive ZIP contenant le document XML sous le nom **`rocket.ork`**. Le fichier voisin `loc-iv-4po.xml` en est la copie lisible. Après sauvegarde dans OpenRocket :

1. Garder une sauvegarde du `.ork` et travailler sur une copie pour l’extraction.
2. Ouvrir cette copie avec un outil d’archives ZIP; extraire l’entrée `rocket.ork`.
3. Copier son contenu dans `plans/loc-iv-4po.xml`, en conservant l’UTF-8.
4. Vérifier que ce contenu est identique à l’entrée de l’archive publiée et rouvrir le `.ork` dans OpenRocket. Git peut convertir les fins de ligne LF en CRLF sous Windows : cette différence de texte seule ne change pas les composants; comparer en normalisant les fins de ligne si nécessaire.

**Ne pas simplement renommer l’archive compressée en `.xml`.** Si le logiciel enregistre aussi d’autres ressources, conserver l’archive complète. Le [format officiel](https://openrocket.readthedocs.io/en/latest/dev_guide/file_specification.html) détaille cette structure.

L’édition XML manuelle est facultative et avancée : ses longueurs sont en mètres, ses masses en kilogrammes, certains diamètres sont stockés comme rayons, et les identifiants relient moteurs, récupération et simulations. Changer le nom visible d’un scénario ne change pas ces liens. Pour débuter, laisser l’interface écrire le XML.

OpenRocket **ne relit pas automatiquement le SCAD**. Après des mesures, reporter les corrections dans les deux modèles, régénérer les documents concernés et mettre à jour notes et historique. La démarche de contrôle reproductible figure dans le [rapport de vérification](../plans/loc-iv-openrocket-verification.md).

## Dépannage

| Problème | Vérification |
| --- | --- |
| Impossible d’ajouter une pièce | Sélectionner le parent compatible dans l’arbre. |
| Le moteur ne peut pas être sélectionné | Le tube interne est-il déclaré support moteur ? Existe-t-il une configuration ? |
| H143 présent, mais masse différente | Comparer le jeu de données sélectionné; deux jeux H143 existent dans la base utilisée. |
| Masse presque doublée | Chercher moteur ajouté comme masse, consommables dupliqués ou remplacement d’étage ajouté aux enfants. |
| La pièce est mal placée | Vérifier unité, parent et référence de position, surtout « avant du parent » contre « pointe ». |
| Le dessin est correct mais le CG est faux | Contrôler masses et positions des accessoires; un dessin seul ne détermine pas les masses réelles. |
| Modifier un délai change deux simulations | Elles partagent probablement une configuration; créer une copie indépendante de celle-ci. |
| Un parachute s’ouvre à un autre moment | Vérifier l’événement propre à la configuration, le délai moteur et le délai supplémentaire. |
| Résultats absents ou périmés | Sélectionner les scénarios et les recalculer après les changements. |
| Ouverture rapide ou autre avertissement | Documenter le problème et revoir les hypothèses; ne pas masquer l’avertissement pour présenter un résultat acceptable. |
| Le fichier XML semble illisible | Extraire le document de l’archive; ne pas ouvrir le ZIP comme s’il s’agissait de texte. |

## Liste de vérification finale

- [ ] J’ai une copie enregistrée et l’étage unique contient les 19 composants attendus.
- [ ] J’ai vérifié tous les diamètres, longueurs, parents, positions et languettes.
- [ ] J’ai inclus récupération, attaches, rétention, boutons et consommables sans compter deux fois leurs masses.
- [ ] Les masses et le CG sont identifiés comme mesurés ou estimés; les moteurs sont exclus de la pesée à vide.
- [ ] J’ai contrôlé le jeu moteur, le dépassement et la récupération des quatre configurations.
- [ ] Les conditions fictives sont distinguées des conditions du lancement réel.
- [ ] J’ai recalculé les essais et lu la montée, l’ouverture, la descente et les avertissements.
- [ ] J’ai enregistré le `.ork`, les résultats utiles et, pour le dépôt, la copie XML synchronisée.
- [ ] Les modifications à reporter dans OpenSCAD, les notes et les plans sont identifiées.

## Points à confirmer et validation

Le kit réel, ses cotes, ses masses et son CG restent à mesurer. Les choix de moteur, de délai et de récupération pour un lancement doivent être examinés avec l’équipe compétente dans les conditions prévues. Cette aide ne décrit pas la préparation physique d’un moteur.

Le 2026-09-12 : inventaire, parentés, cotes, masses, configurations et événements relus dans le XML du dépôt; contenu XML/ORK identique après normalisation des fins de ligne Windows CRLF en LF. Les huit exécutions de simulation de la révision 1.1 restent celles du rapport existant; cette rédaction ne constitue pas une nouvelle campagne de simulation. Les étapes d’interface s’appuient sur la documentation officielle, sans essai graphique de bout en bout ni validation par une personne débutante à ce stade.

[Retour aux aides à la tâche](README.md) · [Retour aux plans](../plans/README.md)
