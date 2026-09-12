# LOC-IV 4 po — modèle OpenRocket simulable

- **Date :** 2026-09-12
- **Statut :** brouillon de simulation — dimensions, masses et conditions à valider.
- **Auteur :** Steve Prud’Homme, avec assistance Codex.
- **Source principale :** [configuration et budget niveau 1](../notes/loc-iv-configuration-budget-niveau-1.md).
- **Géométrie :** [plan OpenSCAD](loc-iv-4po.scad), révision 1.1; ailerons corrigés depuis le fichier LOC `[F]`, autres hypothèses `[A]` conservées. [Historique de comparaison](../notes/loc-iv-comparaison-modeles.md).

## Fichiers et utilisation

**Pour débuter :** suivre l'[aide à la tâche OpenRocket pour la LOC-IV complète](../aides-a-la-tache/debuter-openrocket-loc-iv.md). Elle couvre la reconstruction de tous les composants, les configurations moteur/récupération et l'analyse du vol entier.

- [loc-iv-4po.ork](loc-iv-4po.ork) : fichier natif à ouvrir directement dans **OpenRocket 24.12 ou ultérieur**.
- [loc-iv-4po.xml](loc-iv-4po.xml) : contenu XML lisible, identique à l'entrée `rocket.ork` de l'archive `.ork` lors de la livraison. Format OpenRocket **1.10**, longueurs en mètres, masses en kilogrammes.
- [Vérification](loc-iv-openrocket-verification.md) : chargement et essais réalisés avec le moteur officiel OpenRocket 24.12.

Dans OpenRocket, ouvrir le `.ork`, consulter les commentaires des composants puis l'onglet des simulations. Sélectionner un scénario et lancer la simulation. Les quatre scénarios sont enregistrés **sans résultats pré-calculés**, afin de les recalculer après les modifications. Aucun moteur externe à installer : les références proviennent de la base intégrée à OpenRocket 24.12. Si une autre version ne retrouve pas exactement une courbe, vérifier le moteur sélectionné avant de simuler.

Le `.xml` n'est pas un fichier moteur RockSim `.rse` ni un import de maillage STL. C'est un document OpenRocket complet : composants, matériaux, configurations moteur et conditions de simulation. Le lecteur officiel a également accepté le XML non compressé. Si le sélecteur de fichiers masque `.xml`, ouvrir le `.ork` ou copier le XML sous une extension `.ork`.

Pour modifier la géométrie, utiliser les composants dans OpenRocket ou éditer le XML. Après un enregistrement dans OpenRocket, actualiser la copie `.xml` en extrayant l'entrée `rocket.ork` de l'archive enregistrée. Inversement, après une édition XML, reconstruire le `.ork` comme archive ZIP contenant ce XML nommé `rocket.ork`. Les deux fichiers doivent rester synchronisés; le modèle ne relit pas automatiquement le SCAD.

## Conversion du plan

La structure est à un étage : ogive, payload et booster. Le coupleur, sa cloison, le support moteur, les trois anneaux, les ailerons à languette, les deux boutons de rail, le parachute et la sangle sont des composants OpenRocket. MR-1, protecteur, attaches et consommables sont représentés par des masses estimées, sans dessin détaillé de leur traînée. Le ProDAT reste au sol et est exclu de la masse de vol.

OpenSCAD place l'origine à l'arrière et pointe vers l'ogive; OpenRocket mesure depuis la pointe vers l'arrière. Pour un segment SCAD commençant à `z` et long de `l`, son début OpenRocket est `x = 1,1938 − (z + l)` en mètres, puis relatif au parent. Les ogive et tubes successifs sont positionnés automatiquement bout à bout.

| Élément | Conversion ou différence explicite |
| --- | --- |
| Corps et ogive | Longueurs 330,2 + 279,4 + 584,2 = 1193,8 mm; diamètre nominal 101,6 mm |
| Ailerons | Profil libre LOC à cinq sommets; racine 171,45 mm, envergure 107,95 mm, début à 412,75 mm depuis l'avant du booster; sommets détaillés dans les notes |
| Languettes | 117,475 × 29,972 mm, retrait avant 38,1 mm [F]; épaisseur 3,175 mm [L,I] conservée, à comparer aux 3 mm de [F] |
| Support moteur | Début à 281,375 mm depuis l'avant du booster, longueur 300 mm; alésage 38,5 mm et diamètre extérieur 41,4 mm `[A]` |
| Moteur | Dépassement de 7,825 mm derrière le support, soit 5 mm derrière le corps; les dimensions de la base moteur sont conservées |
| Anneaux | Débuts à 571,850 / 442,500 / 287,725 mm depuis l'avant du booster; épaisseur 6,35 mm; anneau milieu dérivé de la nouvelle languette, encore à mesurer; alésage automatique sur le support |
| Coupleur et cloison | Coupleur de 140 mm dépassant de 70 mm derrière le payload; cloison à son extrémité arrière |
| Boutons | Deux composants, à 154,2 et 514,2 mm depuis l'avant du booster; dimensions `[A]` du SCAD |
| Textiles | Diamètre parachute 914,4 mm et longueur sangle 4572 mm; masse, rangement, suspentes et coefficient de traînée estimés |

Le profil extérieur de l'ogive reste ellipsoïdal approché. Le calcul de coque et de masse d'OpenRocket n'est pas une intégration du solide OpenSCAD. Les fentes du tube ne sont pas soustraites de sa masse; les congés ne sont pas dessinés, leur masse est incluse dans l'estimation des consommables. Les positions des masses d'attaches sont simplifiées. La descente considère un ensemble solidaire sous un parachute : pas une simulation détaillée des éléments séparés et de leur sangle.

Longueur pointe/arrière du corps : 1193,8 mm; avec les ailerons dépassants : 1228,725 mm. Le recouvrement graphique de 0,05 mm de l'assemblage OpenSCAD n'est pas appliqué au modèle aérodynamique. Le jeu languette/support nominal de 0,128 mm reste non validé.

## Hypothèses supplémentaires pour la simulation

**Aucune masse pesée ni position du centre de gravité réel n'a été fournie.** La masse structurelle est calculée à partir de la géométrie et des estimations ci-dessous. Elle n'est pas forcée à la masse commerciale du kit. Les valeurs ne sont pas des propriétés certifiées des pièces LOC.

| Élément | Hypothèse `[A]` |
| --- | --- |
| Carton : corps, support, coupleur | 680 kg/m³ |
| Contreplaqué : ailerons, anneaux, cloison | 600 kg/m³ |
| Polypropylène de l'ogive | 900 kg/m³ |
| Finition extérieure | Réglage OpenRocket `normal`, à adapter après finition réelle |
| Parachute avec suspentes | Masse totale imposée de 80 g; Cd constant 0,8; huit suspentes de 457,2 mm |
| Sangle nylon | Masse totale imposée de 50 g; sa longueur nominale reste 4572 mm |
| Protecteur proposé de 12 po | 30 g |
| MR-1 et visserie | 20 g |
| Attache avant / attache payload | 15 g / 10 g |
| Boutons et visserie | 3 g chacun, soit 6 g |
| Époxy et finition | 60 g distribués sur un volume long de 540 mm dans le booster |

Les masses imposées des textiles remplacent leur calcul par matériaux : pas de double comptage des suspentes. La masse des boutons est également imposée. Les densités textiles indicatives inscrites dans le XML n'ajoutent donc pas de masse à ces valeurs. Le moteur chargé, boîtier compris, vient exclusivement de la base moteur; aucune masse supplémentaire de boîtier ou de recharge n'est ajoutée.

## Moteurs et scénarios

Les courbes de poussée **ne sont pas inventées à partir de la poussée moyenne**. Le fichier référence les données intégrées à OpenRocket par leur empreinte :

| Moteur | Empreinte du jeu de données sélectionné | Masse chargée de ce jeu |
| --- | --- | ---: |
| Cesaroni 247H143-13A | `f27036309584bed36c3a39481f356b5f` | 347 g |
| Cesaroni 276H152-15A | `ace3745f12a3b82a68514e71b1faedc0` | 298 g |

La base contient aussi un autre jeu H143 de 308,9 g : il n'a pas été retenu. Le jeu de 347 g concorde avec la masse publiée dans le catalogue CTI cité par le plan. Les données ne sont ni mélangées ni ajustées à la main. **Vérifier les dimensions moteur effectivement enregistrées dans le XML et le rapport de vérification** : le catalogue présente une enveloppe nominale 38 × 186 mm, tandis que certains jeux intégrés utilisent 185 mm. Ce léger écart est conservé, sans altérer la courbe ou la masse. Le moteur peut donc dépasser de la même distance à l'arrière tout en commençant 1 mm plus loin vers l'arrière.

| Scénario | Déclenchement du parachute | Usage |
| --- | --- | --- |
| H143 — apogée IDÉALE `[A]` | À l'apogée, sans délai de déploiement | Comparaison exploratoire; ne modélise pas l'éjection pyrotechnique du kit |
| H152 — apogée IDÉALE `[A]` | À l'apogée, sans délai de déploiement | Même limite |
| H143 — éjection 13 s ESSAI `[A]` | Éjection moteur, 13 s après combustion | Essai du délai nominal de la référence, pas un réglage recommandé |
| H152 — éjection 15 s ESSAI `[A]` | Éjection moteur, 15 s après combustion | Même limite |

Les essais d'éjection déclenchent un **avertissement de déploiement à grande vitesse** dans cette géométrie estimée. Les scénarios idéaux ne suffisent donc pas à valider le vol réel. Déterminer le délai seulement après correction du modèle avec les mesures et les conditions du lancement.

Conditions communes **fictives et reproductibles** : rail de 2,4 m, vertical; vent moyen et turbulence nuls; atmosphère ISA; altitude 0 m, latitude 45°, longitude 0° (aucun site réel désigné); pas de temps 0,02 s, durée maximale 300 s, graine aléatoire 20260912. La longueur utilisable de guidage dépend aussi de la position des boutons. Ce cas calme ne couvre pas les conditions du club.

## Avant d'utiliser les résultats pour un lancement

1. Mesurer le profil des ailerons, les diamètres, parois et positions encore marqués `[A]`.
2. Peser les composants, puis la fusée prête à voler sans moteur; mesurer son centre de gravité dans le même état. Mettre à jour les masses, puis contrôler le total et le CG dans OpenRocket.
3. Confirmer la courbe et le boîtier/recharge réellement utilisés; éviter tout double comptage du moteur.
4. Remplacer les conditions fictives par le rail, le site et la météo prévus; examiner stabilité, vitesse de sortie du rail, altitude, récupération et avertissements.
5. Valider le parachute, le délai et la configuration avec l'équipe de certification selon les notes.

## Sources du format et du logiciel

- [Documentation officielle du format OpenRocket](https://openrocket.readthedocs.io/en/latest/dev_guide/file_specification.html), consultée le 2026-09-12.
- [OpenRocket 24.12 — publication officielle](https://github.com/openrocket/openrocket/releases/tag/release-24.12), moteur de chargement, sauvegarde et simulation utilisé.
- [Code officiel des composants et de leur sérialisation, version 24.12](https://github.com/openrocket/openrocket/tree/release-24.12/core/src/main/java/info/openrocket/core/file/openrocket), référence technique du XML généré par le logiciel lui-même.
- [Sources physiques et limites du plan OpenSCAD](README.md#sources-complémentaires), en complément des notes principales.

[Retour aux plans](README.md)
