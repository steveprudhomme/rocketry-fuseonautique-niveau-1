# Comparaison du modèle LOC-IV avec des références externes

Date : 2026-09-12. Modèle examiné : `loc-iv-4po.ork`, commit local `297424e`.

**Statut :** comparaison historique de la première version. Les tableaux et marges ci-dessous décrivent ce commit, pas la révision 1.1 corrigée. Voir la section de suivi en fin de note.

## Conclusion

Le modèle créé se charge et simule, mais sa géométrie approximative ne représente pas assez fidèlement la LOC-IV pour valider les performances. La priorité est de reprendre les ailerons à partir du fichier fabricant, puis de vérifier leur correspondance avec le kit reçu. Les résultats de simulation précédents restent des essais logiciels, pas des prévisions de vol validées.

## Références trouvées

1. **LOC Precision**, fichier `PK-48 Loc-IV.rkt`, distribué dans [l'archive RockSim liée depuis la fiche LOC-IV](https://cdn.shopify.com/s/files/1/0568/7489/3503/files/PK-48-Loc-IV-3.zip?v=1623759843). Il a été téléchargé et importé dans OpenRocket 24.12. Il reprend les sections de 23 et 11 pouces : c'est la référence externe la plus proche de la configuration des notes. La date de révision interne du modèle n'a pas été établie; un lien encore publié ne garantit pas que toutes ses cotes correspondent à la production actuelle. [Fiche fabricant](https://locprecision.com/products/loc-iv).
2. **Aero B**, [LOC IV Level 1 Certification Data Gathering](https://www.rocketryforum.com/threads/loc-iv-level-1-certification-data-gathering.47879/), 19 janvier 2013. L'auteur partage deux fichiers OpenRocket, dont une version proche du kit mais dotée d'un déflecteur, et une version allongée. Le téléchargement de la pièce jointe demande une connexion : ses fichiers n'ont pas été chargés ni validés ici.
3. **codysmith**, [LOC IV modifiée](https://www.rocketryforum.com/designs/loc-iv.1597/), 22 décembre 2013. La fiche publique décrit une fusée de 1695 mm : trop allongée pour être une référence directe de notre configuration. Les performances affichées sur cette page ne sont pas comparables à nos essais H143/H152.

Les fichiers de tiers ne sont pas redistribués dans ce rapport.

## Comparaison directe après import dans OpenRocket 24.12

| Caractéristique | Notre modèle | Fichier LOC importé |
| --- | ---: | ---: |
| Diamètre extérieur | 101,6 mm | 101,6 mm |
| Payload / booster | 279,4 / 584,2 mm | 279,4 / 584,2 mm |
| Ogive exposée | Ellipsoïde, 330,2 mm | Ogive, 325,12 mm |
| Pointe à arrière du tube | 1193,8 mm | 1188,72 mm |
| Paroi du corps | 1,6 mm | 1,27 mm |
| Support moteur, longueur | 300 mm | 279,4 mm |
| Coupleur, longueur | 140 mm | 203,2 mm |
| Ailerons | Trapèze, trois pièces | Profil libre à cinq sommets, trois pièces |
| Corde d'emplanture | 230 mm | 171,45 mm |
| Envergure extérieure d'un aileron | 125 mm | 107,95 mm |
| Épaisseur des ailerons | 3,175 mm | 3 mm |
| Surface extérieure d'un aileron, hors languette | 21 250 mm² | 14 012 mm² |
| Languette : longueur × profondeur | 230 × 30,1 mm | 117,475 × 29,972 mm |
| Bord avant de l'aileron depuis l'avant du booster | 334,2 mm | 412,75 mm |
| Extrémité la plus arrière des ailerons | 20 mm avant l'arrière du corps | 34,925 mm derrière l'arrière du corps |
| Parachute, diamètre / masse | 914,4 mm / 80 g estimés | 914,001 mm / 85 g imposés |
| Masse totale sans moteur calculée dans OpenRocket | 1,094 kg | 1,022 kg |

Les surfaces ont été calculées à partir des sommets des profils. Notre approximation augmente la surface extérieure d'un aileron de **51,65 %**. Le diamètre total et les longueurs des tubes proches ne suffisent donc pas à établir l'équivalence aérodynamique.

Le fichier fabricant utilise un profil libre : ses champs de corde et de flèche récapitulatifs ne doivent pas remplacer aveuglément ses sommets. Sa longueur totale, ailerons dépassants compris, atteint 1223,645 mm; elle n'est pas directement comparable à une longueur mesurée uniquement jusqu'au tube.

## Masse et stabilité : contrôles supplémentaires

Le calcul de masse du fichier LOC n'inclut pas le même inventaire que le nôtre, notamment les masses ajoutées de MR-1, protecteur, attaches et consommables. L'écart de masse totale n'est donc pas une simple erreur de densité. Les deux valeurs restent des calculs de modèles, pas des pesées de la fusée réelle.

Avec le même calculateur Barrowman d'OpenRocket 24.12, à Mach 0,3 et incidence nulle :

- Notre centre de pression calculé : 880,6 mm depuis la pointe.
- Celui du fichier fabricant importé : 906,8 mm depuis la pointe.
- Notre CG sans moteur : 756,1 mm; celui du fichier fabricant : 760,4 mm.

Avec les masses de lancement de notre modèle, la marge statique `(CP − CG) / diamètre` vaut environ **0,39 calibre pour H143** et **0,49 calibre pour H152** dans ce contrôle ponctuel. Ce ne sont pas des marges minimales sur toute la trajectoire. Les marges chargées du fichier fabricant n'ont pas été comparées, faute d'avoir configuré un essai moteur identique dans celui-ci.

Ces résultats montrent que l'absence d'avertissement dans les anciens essais à vent nul et déploiement idéal n'établit pas la validité du modèle pour le vol. Les altitudes précédemment calculées ne doivent pas être retenues comme prévisions de la fusée réelle.

## Limites de la référence fabricant

L'importateur signale que le trou central du parachute n'est pas pris en charge et l'ignore. Le fichier source décrit ce trou à 90 mm. Son inventaire et certaines épaisseurs diffèrent aussi de la fiche actuelle; il reste nécessaire de mesurer le kit reçu. Le fichier LOC constitue une meilleure base géométrique que nos approximations, pas une certification de la configuration réelle.

Empreinte SHA-256 du fichier `.rkt` examiné :

`202acb4295f957f51e70792fe9122a7cd76edd1068706454d303ccd6a7526d8d`

## Suite à donner

Reprendre le profil et la position des ailerons, la longueur du support et le coupleur dans une révision sourcée; conserver explicitement les différences entre le fichier LOC et la version du kit. Mettre ensuite à jour les masses et le CG à partir de mesures, puis refaire les essais de stabilité et de récupération avec les conditions prévues. Aucun fichier de géométrie existant n'a été modifié pendant cette comparaison.

## Suivi — révision 1.1 du 2026-09-12

Historique des essais du commit `297424e` : masse sans moteur estimée 1,094 kg, CG à 756 mm; apogées H143/H152 de 539/615 m, temps à l'apogée 9,76/10,07 s. Les essais d'éjection 13/15 s signalaient environ 25/22,1 m/s au déploiement. Ces chiffres sont remplacés, pour le modèle courant seulement, par ceux du rapport de révision 1.1; ils n'ont jamais été des mesures de vol.

À la demande de Steve, le profil des ailerons est maintenant repris dans les deux modèles depuis le fichier LOC identifié ci-dessus. Les coordonnées sont en mm, avec `x` depuis le bord avant de l'emplanture vers l'arrière, et `y` radial depuis la peau :

| Sommet | x | y |
| --- | ---: | ---: |
| 1 | 0 | 0 |
| 2 | 142,875 | 107,95 |
| 3 | 206,375 | 107,95 |
| 4 | 206,375 | 31,75 |
| 5 | 171,45 | 0 |

Le bord avant est à 412,75 mm depuis l'avant du booster. La languette mesure 117,475 × 29,972 mm, en retrait de 38,1 mm depuis ce bord. L'épaisseur de **3,175 mm** de la fiche/notice est conservée; le fichier LOC indique **3 mm**. Cet écart reste ouvert jusqu'à la mesure du kit.

Dans OpenSCAD, les coordonnées deviennent `(y, 171,45 − x)` dans le plan radial/axial; la racine arrière est à `z=0`. Les ailerons dépassent donc de 34,925 mm derrière le corps. La longueur pointe/arrière du corps reste 1193,8 mm; la longueur avec ailerons atteint 1228,725 mm. La différence d'ogive avec le fichier LOC n'a pas été arbitrée sans mesure.

Les fentes suivent la nouvelle languette (longueur nominale modélisée 117,475 mm, jeu graphique inchangé). L'anneau milieu dérivé est déplacé à `z=135,35 mm` dans OpenSCAD, soit un début à 442,5 mm depuis l'avant du booster dans OpenRocket. Cette position est encore une hypothèse, à 2 mm devant la languette. Le support actuel laisse un jeu radial calculé de **0,128 mm** avec sa profondeur : ce n'est pas une tolérance validée.

La longueur du support, le coupleur, l'ogive, les matériaux et les masses estimées ne sont pas automatiquement remplacés par ceux d'un fichier tiers. Leurs divergences sont enregistrées dans la [fiche de mesures](loc-iv-mesures-kit.md) et la [feuille de route](../ROADMAP.md). **Aucune cote, masse ni position de CG du kit réel n'a été confirmée.**

Les résultats actualisés sont dans le [rapport de vérification OpenRocket](../plans/loc-iv-openrocket-verification.md). L'ancien diagnostic est conservé ci-dessus pour expliquer la correction.

Synthèse de la révision 1.1 : masse sans moteur toujours estimée de **1,033 kg**, CG estimé à **747,8 mm** depuis la pointe; CP à Mach 0,3 et incidence nulle à **902,1 mm**. Les marges chargées ponctuelles deviennent **0,63 calibre (H143)** et **0,73 calibre (H152)**. Apogées d'essai : environ **594/677 m**, sans valeur de prévision validée. Les essais d'éjection signalent toujours un déploiement à grande vitesse, environ **26,7/25,2 m/s**. Ces calculs améliorent le diagnostic du modèle mais ne ferment aucune case de mesure physique.

[Retour aux notes](README.md)
