# Plans

Plans, schémas, fichiers sources et décisions. Préciser versions, unités, hypothèses et sources. Utiliser le [gabarit de plan](../modeles/plan.md).

## LOC-IV 4 po — plan paramétrique v1.0

- **Date :** 2026-09-12
- **Statut :** brouillon — représentation d'ensemble, dimensions à valider sur le kit reçu.
- **Auteur :** Steve Prud’Homme, avec assistance Codex.
- **Fichier :** [loc-iv-4po.scad](loc-iv-4po.scad), sans bibliothèque externe.
- **Source principale :** [configuration et budget niveau 1](../notes/loc-iv-configuration-budget-niveau-1.md).

![Aperçu en coupe du modèle LOC-IV](loc-iv-apercu.png)

Aperçu généré avec OpenSCAD à partir des paramètres par défaut; géométries approchées selon les limites ci-dessous.

Le modèle représente la configuration des notes : LOC-IV récente à support moteur 38 mm, Cesaroni Pro38 2G, H143 ou H152, MR-1, récupération et boutons 1010. Il comporte le booster à fentes, la section payload, un coupleur et sa cloison, une ogive creuse à épaulement, trois ailerons à languette, trois anneaux de centrage et les points d'attache schématiques. Le moteur est une enveloppe externe assemblée, pas un dessin du boîtier nu ni de ses composants internes. Le ProDAT-38 optionnel est un symbole séparé d'accessoire au sol.

Le fichier antérieur `LOC_IV_4in_v0.2.scad` n'a pas pu être récupéré depuis la conversation référencée (lecture indisponible). Cette version est une reconstruction; elle n'annonce pas une reprise ou une vérification de ce fichier.

### Unités, provenance et limites

Toutes les longueurs sont en **millimètres**, à l'échelle 1:1. L'origine est au bas du corps; l'axe Z pointe vers l'ogive. Les commentaires `[N]`, `[L]`, `[I]`, `[C]`, `[R]` renvoient aux sources ci-dessous. **`[A]` désigne une approximation à mesurer**, même si sa valeur comporte des décimales. Les couleurs sont indicatives.

| Paramètres | Base et statut |
| --- | --- |
| Corps 4 po, longueur totale 47 po; sections 23 et 11 po | Fiche LOC [L], nominal; diamètre extérieur réel à mesurer |
| Ogive exposée 330,2 mm | Différence des longueurs [L], pas une mesure directe; profil ellipsoïdal approché |
| Trois ailerons de 1/8 po, trois anneaux | Notice [I]; épaisseur des anneaux de 1/4 po : [L] |
| Moteur 38 × 186 mm | Enveloppe assemblée H152/H143 [C], pages PDF 15 et 16 |
| Parachute 36 po, sangle 15 pi | Notes [N], confirmées par LOC; largeur de sangle 3/8 po : [L] |
| MR-1 à deux clips en Z | [I,R]; largeur 3/4 po [R]; forme, visserie et implantation approchées |
| Dépassement du support derrière/devant les anneaux | 1/8 po pour MR-1 et 1/4 po à l'avant, notice [I], page 2 |
| Autres cotes | `[A]` : parois/alésages, longueur du support, profil des ailerons, coupleur, cloison, épaulement, fixations, positions, boutons, volumes textiles et ProDAT |

Le protecteur de **12 po est une proposition modifiable**, absente des notes. Le diamètre du bouton n'est pas déduit de « 1010 ». Les paramètres de jeux servent à la visualisation : ils ne constituent pas des tolérances de fabrication. La bague de poussée du moteur, les filetages, les congés d'époxy et les détails de couture sont omis. Aucune géométrie d'une rétention alternative n'est inventée : les options sont `MR-1` et `none`.

Ce modèle ne valide ni la résistance, ni l'ajustement réel, ni le centre de gravité, ni la stabilité, ni le volume de rangement. Les exports sont des maquettes de référence, pas des pièces de vol prêtes à fabriquer. Le choix de moteur et du délai reste à simuler avec la masse réelle, comme indiqué dans les notes.

### Paramètres et variantes

| Réglage | Valeurs / effet |
| --- | --- |
| `part` | `assembly` ou une pièce de la liste ci-dessous |
| `view` | `assembled`, `cutaway` (défaut : demi-enveloppes retirées côté Y négatif), `exploded` (sépare axialement payload et ogive) |
| `explosion_gap` | Espacement visuel en vue éclatée; ne modifie pas les pièces |
| `motor_preset` | `H143`, `H152`, `generic_2G`; couleur et identification seulement, même enveloppe |
| `retention` | `MR-1` ou `none`; ce dernier masque la retenue, sans valider un vol sans retenue |
| `recovery` | `packed` ou `deployed` : schéma explicatif à plat, pas une scène de descente calculée |
| `show_motor`, `show_recovery`, `show_protector`, `show_rail_buttons` | Visibilité dans l'assemblage |
| `show_prodat` | Affiche l'accessoire séparé; désactivé par défaut |
| `quality` | Résolution circulaire, 64 par défaut; minimum 12 |

Exports individuels avec `part` : `booster`, `payload`, `nose`, `coupler`, `bulkhead`, `fin`, `motor_mount`, `ring`, `motor`, `retainer`, `parachute`, `protector`, `cord`, `rail_button`, `prodat`. Les pièces isolées sont dans leur repère local et complètes, indépendamment de `view`; `recovery` commande la forme des textiles. `retainer` avec `retention="none"` est volontairement vide. Les boutons de visibilité ne masquent pas les exports individuels.

La sangle rangée est un ruban schématique : le tracé ne développe pas les 4572 mm conservés dans `cord_l`. En mode déployé, les segments montrent les relations entre corps, payload et parachute; leurs longueurs ne sont pas celles de la sangle. La voile est un disque au diamètre nominal, avec des suspentes approximatives. Le protecteur rangé est une enveloppe indicative sans conservation de surface. Le modèle ne représente pas le double déploiement optionnel.

### Ouvrir, rendre et exporter

Ouvrir le fichier dans OpenSCAD, modifier les paramètres en tête ou dans le Customizer, puis utiliser **F5** pour l'aperçu et **F6** pour le rendu. Les couleurs sont visibles en aperçu; le STL ne les conserve pas. La vue éclatée sépare deux sous-ensembles, pas toutes les pièces; utiliser la coupe ou les exports individuels pour examiner l'intérieur.

Depuis la racine du dépôt, avec OpenSCAD dans le PATH :

```sh
openscad -o loc-iv-coupe.stl plans/loc-iv-4po.scad
openscad -o loc-iv-assemblee.stl -D 'view="assembled"' plans/loc-iv-4po.scad
openscad -o loc-iv-eclatee.stl -D 'view="exploded"' -D 'motor_preset="H152"' plans/loc-iv-4po.scad
openscad -o aileron.stl -D 'part="fin"' plans/loc-iv-4po.scad
openscad -o parachute.stl -D 'part="parachute"' -D 'recovery="deployed"' plans/loc-iv-4po.scad
```

Sous Windows PowerShell, remplacer `openscad` par `& 'C:/Program Files/OpenSCAD/openscad.com'` si nécessaire. Les STL sont des sorties générées; conserver le `.scad` comme source versionnée. L'assemblage contient plusieurs volumes : ce n'est pas un solide monobloc.

### Vérification effectuée

Le 2026-09-12, avec **OpenSCAD 2021.01 sous Windows** : 21 rendus STL terminés sans erreur ni avertissement — assemblage en coupe par défaut, les 15 pièces isolées, assemblages complet et éclaté avec H152/récupération déployée/ProDAT, assemblage sans moteur/récupération/boutons/retenue, et les deux textiles déployés isolés. Les vues en coupe et éclatée ont aussi été inspectées visuellement. Les liens locaux et `git diff --check` passent. Ces contrôles vérifient le modèle numérique, pas ses cotes physiques.

### Points à vérifier sur le kit

1. Confirmer la version à sections 23/11 po et l'inventaire décrit dans les notes.
2. Mesurer diamètres/parois, support moteur, ailerons et languettes, coupleur, cloison et ogive.
3. Relever les positions des anneaux, points d'attache, clips et boutons, et leurs interfaces réelles.
4. Mesurer les textiles rangés et choisir le protecteur; remplacer les valeurs `[A]` avec provenance datée.
5. Vérifier les jeux et la géométrie après toute modification; les assertions ne contrôlent que quelques incohérences, pas toutes les collisions.

### Sources complémentaires

Consultées le 2026-09-12; elles complètent les notes sans modifier leur statut de brouillon.

- **[N]** [Notes de configuration et budget](../notes/loc-iv-configuration-budget-niveau-1.md).
- **[L]** [LOC Precision — LOC-IV](https://locprecision.com/products/loc-iv).
- **[I]** [Notice LOC-IV PK-48](https://cdn.shopify.com/s/files/1/0568/7489/3503/files/Loc_IV_Instructions-final.pdf?v=1747083020), nomenclature page 1, support et MR-1 page 2.
- **[C]** [Catalogue Cesaroni Pro38](https://pro38.com/wp-content/uploads/2024/11/Pro38Catalog.pdf), document interne « 2010 Catalog v1.0 » malgré le chemin daté 2024; pages PDF 15–16 pour les enveloppes H152/H143.
- **[R]** [LOC Precision — MR-1 Z Clip](https://locprecision.com/products/z-clip-style-motor-retainer-set/).

[Retour à l’accueil](../README.md)
