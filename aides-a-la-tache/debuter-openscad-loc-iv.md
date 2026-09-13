# Aide à la tâche — Débuter avec OpenSCAD et coder le plan LOC-IV

**Projet et fusée : Chasse Galerie 1.** Base technique : kit LOC-IV 4 po. Les noms de fichiers `loc-iv-*` sont conservés pour maintenir les liens et la traçabilité des références.

- **Date :** 2026-09-12
- **Statut :** brouillon pédagogique; exemples vérifiés avec OpenSCAD 2021.01. Essai par une personne débutante à réaliser.
- **Auteur :** Steve Prud’Homme, avec assistance Codex.
- **Public :** amateur de fuséonautique de loisir, sans expérience de programmation ni de dessin par code.
- **Modèle de référence :** [LOC-IV 4 po, révision 1.1](../plans/loc-iv-4po.scad).

## Objectif et contexte

À la fin, vous saurez ouvrir la fusée, changer ses paramètres, comprendre comment ses pièces sont dessinées, créer vos premiers composants et enregistrer un résultat. Prévoyez une première séance de découverte, puis reprenez les exercices à votre rythme.

**OpenSCAD** est le logiciel; **`.scad`** est l’extension du fichier qui contient les instructions. On décrit des formes avec du texte : « créer un cylindre », « le creuser », « le déplacer ». Le logiciel transforme ces instructions en dessin 3D. Un **paramètre** est une valeur nommée, comme le diamètre du corps. Le plan est **paramétrique** parce que certaines dimensions se recalculent lorsqu’on change une valeur.

Ce travail concerne la représentation de la fusée. Le rendu ne vérifie ni sa résistance ni son aptitude au vol. Les mesures du kit restent à confirmer; les simulations se font dans le [modèle OpenRocket](../plans/loc-iv-openrocket.md).

## Références applicables

- [Configuration et budget LOC-IV](../notes/loc-iv-configuration-budget-niveau-1.md) : source principale du projet.
- [Documentation du modèle](../plans/README.md) : paramètres, pièces et limites.
- [Plan d’ensemble avec vue écorchée](../plans/ensemble/README.md) : pour reconnaître les pièces et leurs positions.
- [Galerie des pièces](../plans/images/README.md) : pour comparer ce qui apparaît à l’écran.
- [Comparaison avec le fichier LOC](../notes/loc-iv-comparaison-modeles.md) et [fiche de mesures](../notes/loc-iv-mesures-kit.md) : provenance des cotes et relevés à effectuer.

Les références OpenSCAD officielles utilisées sont regroupées à la fin de la fiche.

## Prérequis — Préparer son poste

1. Télécharger et installer OpenSCAD depuis la [page officielle](https://openscad.org/downloads.html), en choisissant la version stable adaptée à son ordinateur.
2. Depuis la page du dépôt GitHub, télécharger le dépôt avec **Code → Download ZIP**, puis extraire l’archive. Si vous avez déjà le dépôt sur votre ordinateur, utilisez ce dossier.
3. Repérer `plans/loc-iv-4po.scad` dans le dossier extrait. Ne pas ouvrir une page HTML enregistrée à la place du fichier.
4. Lancer OpenSCAD, choisir **Fichier → Ouvrir** et sélectionner ce fichier.
5. Faire **Fichier → Enregistrer sous** et créer une copie nommée `loc-iv-apprentissage.scad` dans un dossier personnel d’exercice. Garder le fichier de référence intact pendant l’apprentissage.

Aucune bibliothèque supplémentaire n’est nécessaire pour ce modèle. Les intitulés des menus peuvent être en anglais selon l’installation; les touches F5 et F6 servent de repères. Sur certains portables, il faut aussi maintenir `Fn`.

## 1. Voir la fusée avant de coder

Repérez les trois zones utiles : l’éditeur contenant le texte, la vue 3D et la console qui affiche les messages.

| Action | Résultat attendu |
| --- | --- |
| Appuyer sur **F5** — aperçu / Preview | La LOC-IV apparaît avec une partie de l’enveloppe retirée. C’est le réglage initial voulu. |
| Faire tourner la vue en faisant glisser la souris, puis utiliser la molette | Vous examinez l’intérieur et changez le grossissement. Cela ne change pas les dimensions. |
| Utiliser **Vue → Tout afficher / View All** si nécessaire | La fusée rentre dans la fenêtre. |
| Appuyer sur **F6** — rendu / Render | Le logiciel calcule la géométrie; attendre la fin et lire la console. |

F5 convient pour travailler rapidement. F6 sert à vérifier le calcul géométrique et à préparer un export 3D. Des couleurs ou artefacts d’aperçu peuvent changer au rendu. Un rendu réussi ne confirme pas les cotes physiques. Ces commandes sont décrites dans le [manuel officiel](https://files.openscad.org/documentation/manual/OpenSCAD_User_Manual.html).

**Contrôle :** vous voyez l’ogive, le corps, les ailerons et les composants internes. Le message `ECHO: "BROUILLON…"` est une information prévue par le fichier, pas une erreur.

## 2. Réussir sa première modification

Dans le haut de votre copie, trouvez cette ligne :

```scad
view = "cutaway";
```

**Remplacez cette ligne**, sans en ajouter une deuxième, par :

```scad
view = "assembled";
```

Appuyez sur F5. Le corps et l’ogive doivent maintenant être fermés. Revenez ensuite à `"cutaway"` pour observer l’intérieur.

Le panneau **Customizer**, s’il est visible, permet aussi de changer certains paramètres. Pour cette initiation au code, modifiez les lignes dans l’éditeur et gardez le Customizer sur ses valeurs par défaut. Un préréglage actif dans ce panneau peut modifier le résultat affiché.

Essayez ensuite **une seule modification à la fois** dans les lignes existantes :

| Ligne à modifier | Essai | Ce que vous devez voir |
| --- | --- | --- |
| `part = "assembly";` | `part = "fin";` | Un seul aileron complet, avec sa languette. |
| `part = "assembly";` | `part = "motor_mount";` | Le tube support moteur isolé. |
| `view = "cutaway";` | `view = "exploded";` | Payload et ogive espacés axialement; ce n’est pas l’éclatement de toutes les pièces. |
| `show_motor = true;` | `show_motor = false;` | Le moteur disparaît de l’assemblage. |
| `motor_preset = "H143";` | `motor_preset = "H152";` | Le moteur change d’identification et de couleur en aperçu; son enveloppe reste identique. |

Pour voir les effets des quatre dernières lignes, remettre `part = "assembly";`. Pour terminer cette étape, rétablir `view = "cutaway";` et `show_motor = true;`.

## 3. Lire les signes du code

À partir des lignes de notre fichier :

```scad
body_d = 101.6;           // Diamètre nominal du corps, en mm.
show_motor = true;       // true = oui; false = non.
part = "assembly";       // Un choix écrit entre guillemets droits.
body_id = body_d - 2*body_wall; // Diamètre intérieur calculé.
```

Ce bloc explique des lignes existantes : **ne pas le coller en supplément** dans le modèle.

| Signe ou mot | Comment le lire |
| --- | --- |
| `=` | Donne une valeur à un nom. Pour changer un réglage, modifier sa définition existante. |
| `;` | Termine une instruction simple. |
| `//` | Commence un commentaire que le logiciel ne dessine pas. |
| `()` | Contient les arguments d’une commande, par exemple son diamètre. |
| `[]` | Contient une liste, par exemple `[x,y,z]`. |
| `{}` | Regroupe plusieurs instructions. |
| `*` et `/` | Multiplication et division. |
| `module` | Définit une recette réutilisable pour créer une pièce. |
| `assert` | Vérifie une condition et arrête le calcul si elle est fausse. |

Écrire **`101.6` avec un point**, même si l’on écrit 101,6 mm en français. Respecter l’orthographe et les majuscules des noms. Éviter les guillemets typographiques `« »` dans le code.

Dans ce projet, une unité du dessin représente **1 mm**. OpenSCAD ne choisit pas une unité physique pour vous. `4` signifie donc ici 4 mm, pas 4 pouces; 4 pouces correspondent à 101,6 mm.

## 4. Se repérer dans la fusée

L’origine `[0,0,0]` est au centre de l’arrière du **corps**. Z augmente vers l’ogive; X et Y désignent les deux directions perpendiculaires à cet axe.

- `translate([0,0,100])` place une forme 100 mm plus haut sur Z.
- `translate([50,0,0])` la décale de 50 mm sur X.
- `rotate([0,0,120])` tourne une forme de 120 degrés autour de Z.

Dans le modèle actuel, la section payload commence à Z = 584,2 mm et l’ogive à Z = 863,6 mm. La pointe nominale est à Z = 1193,8 mm. Les ailerons descendent jusqu’à Z = −34,925 mm : l’origine n’est donc pas le point le plus bas de l’ensemble.

## 5. Coder un premier tube

**Ouvrir un nouveau fichier vide**, distinct de la copie LOC-IV. Coller le bloc complet ci-dessous, enregistrer sous `exercice-tube.scad`, puis appuyer sur F5.

```scad
// Exercice autonome : tube booster simplifié, sans fentes.
// Cotes reprises du modèle 1.1; paroi [A] non mesurée.
$fn = 64;              // Nombre de facettes autour d'un cercle.
diametre = 101.6;       // Nominal 4 po, traité comme diamètre extérieur.
longueur = 584.2;       // Longueur nominale du booster.
paroi = 1.6;            // [A] Approximation du modèle.
epsilon = 0.02;         // Petit dépassement pour la soustraction graphique.

difference() {
    cylinder(d=diametre, h=longueur);
    translate([0,0,-epsilon])
        cylinder(d=diametre-2*paroi, h=longueur+2*epsilon);
}
```

**Résultat attendu :** un tube ouvert aux deux extrémités. Incliner la vue pour regarder à l’intérieur.

`cylinder` crée un cylindre. Dans `difference()`, la première forme est conservée et les suivantes sont soustraites. Le second cylindre représente le vide intérieur. Il dépasse légèrement aux deux bouts pour éviter des faces exactement superposées; `epsilon` n’est pas une tolérance d’assemblage.

Le calcul `diametre-2*paroi` enlève une paroi de chaque côté : 101,6 − 3,2 = 98,4 mm. Le corps réel du dépôt ajoute ensuite les fentes destinées aux languettes des ailerons.

**Petit essai :** dans ce fichier d’exercice seulement, changer `longueur` à `200`, appuyer sur F5 et constater que le tube raccourcit. Remettre ensuite `584.2`. La valeur 200 est un essai d’apprentissage, pas une nouvelle cote LOC.

## 6. Réutiliser une recette pour le support et un anneau

Dans **un autre nouveau fichier vide**, coller ce bloc complet et enregistrer sous `exercice-support-anneau.scad`.

```scad
// Exercice autonome : support et anneau séparés pour la lecture.
// Diamètres et longueur du support : [A] valeurs du modèle à mesurer.
$fn = 64;
eps = 0.02;

module tube(od, id, h) {
    difference() {
        cylinder(d=od, h=h);
        translate([0,0,-eps]) cylinder(d=id, h=h+2*eps);
    }
}

tube(41.4, 38.5, 300);                 // Support moteur [A].
translate([120,0,0]) tube(98.4,41.4,6.35); // Anneau à côté pour l'exercice.
```

**Résultat attendu :** un long tube et un anneau plat à côté. Le déplacement de 120 mm sert uniquement à séparer les dessins.

`module tube(od, id, h)` définit la recette avec trois entrées : diamètre extérieur, diamètre intérieur et hauteur. La définition seule n’affiche rien : `tube(...)` appelle la recette avec des valeurs. Dans la fusée complète, `ring()` appelle cette même recette avec les dimensions de l’anneau et l’assemblage le place autour du support.

Le **moteur** et le **support moteur** sont deux pièces différentes : l’enveloppe moteur nominale fait 38 mm; le support est un tube dont l’alésage vaut provisoirement 38,5 mm dans le dessin.

## 7. Dessiner puis répéter les ailerons

Un aileron commence comme un contour plat. `polygon` relie ses sommets; `linear_extrude` lui donne une épaisseur. L’exemple suivant reprend le contour extérieur du fichier LOC utilisé dans notre modèle. Il **omet volontairement la languette** pour apprendre le principe; le module `fin()` du modèle complet la contient.

Dans **un nouveau fichier vide**, coller le bloc complet et enregistrer sous `exercice-ailerons.scad`.

```scad
// Exercice autonome : contour extérieur LOC [F], sans languette.
// Épaisseur nominale [L,I]; pas une mesure du kit reçu.
epaisseur = 3.175;
rayon_corps = 101.6/2;
trois_ailerons = false;

module aileron_exercice() {
    rotate([90,0,0])
        linear_extrude(height=epaisseur, center=true)
            polygon([
                [0,171.45],
                [107.95,28.575],
                [107.95,-34.925],
                [31.75,-34.925],
                [0,0]
            ]);
}

if (trois_ailerons) {
    for (angle=[0,120,240])
        rotate([0,0,angle])
            translate([rayon_corps,0,0]) aileron_exercice();
} else {
    aileron_exercice();
}
```

**Premier résultat :** un aileron seul. Après rotation, son contour se trouve dans le plan X/Z et son épaisseur suivant Y. Dans la liste de points, la première coordonnée indique la portée radiale et la seconde la position axiale dans ce repère local. Le bord arrière de la racine est à Z = 0.

**Deuxième résultat :** remplacer `trois_ailerons = false;` par `trois_ailerons = true;`, puis F5. Trois ailerons entourent maintenant un espace central vide : le corps n’est pas dessiné dans cet exercice.

Lire les opérations depuis la pièce vers l’extérieur : on crée l’aileron, on le décale jusqu’au rayon du corps, puis on tourne l’ensemble autour de Z. La boucle `for` recommence aux angles 0°, 120° et 240°. Inverser déplacement et rotation ne donne pas la même disposition.

Dans la LOC-IV complète, conserver les paramètres `fin_root`, `fin_span`, `fin_tab_length`, `fin_tab_depth` et les autres cotes du profil tant qu’aucune référence ou mesure ne justifie leur changement. La languette traverse la paroi vers le support; ce n’est pas une partie extérieure à supprimer.

## 8. Comprendre comment le fichier complet assemble la fusée

Revenir à `loc-iv-apprentissage.scad`. Lire le fichier dans cet ordre, sans chercher à tout modifier :

| Partie du fichier | Rôle et exemple |
| --- | --- |
| `Affichage` | Choisit la pièce, la vue et les options visibles. |
| `Dimensions documentées ou nominales` | Regroupe les valeurs issues des sources. |
| `Approximations à valider` | Regroupe notamment parois et positions encore estimées; certaines cotes d’aileron `[F]` y sont aussi commentées. |
| `Hidden` | Calcule les dimensions dépendantes; par exemple `nose_l = total_l - booster_l - payload_l`. |
| `assert(...)` | Signale certaines dimensions incompatibles. |
| `module tube`, `fin`, `nose`, etc. | Définit les recettes des composants. |
| `module assembly()` | Place, colore et réunit visuellement les composants. |
| Les dernières lignes `if(part == ...)` | Choisit quelle recette afficher. `==` compare deux valeurs. |

Dans `assembly()`, repérer par exemple cet **extrait de lecture**, à ne pas exécuter seul :

```scad
translate([0,0,payload_z]) {
    color("Ivory") shell_cut() payload();
}
```

La recette `payload()` construit le tube à son origine locale. `shell_cut()` applique éventuellement la coupe. `color` choisit une couleur d’aperçu et `translate` place le résultat à la hauteur calculée `payload_z`.

Les autres pièces utilisent les mêmes idées :

- **Ogive :** `nose()` étire une sphère, enlève l’intérieur et la moitié inférieure, puis ajoute un épaulement. Le profil ellipsoïdal reste une approximation.
- **Moteur :** `motor()` dessine son enveloppe externe cylindrique; aucun composant propulsif interne n’est modélisé.
- **MR-1 :** `retainer()` assemble des formes simples représentant deux clips en Z et leurs fixations.
- **Récupération :** `parachute()`, `protector()` et `cord()` représentent les textiles de façon schématique, rangés ou déployés.
- **Coupe :** `shell_cut()` retire un volume des enveloppes lorsque `view` vaut `"cutaway"`. Le nom évoque une coupe graphique, pas une opération à pratiquer sur le kit.

## 9. Reporter une mesure sans perdre sa provenance

Avant de modifier une cote, la noter dans la [fiche de mesures](../notes/loc-iv-mesures-kit.md) avec l’unité, la date et la méthode. Rechercher ensuite son nom dans la copie du code et modifier sa définition existante.

Conserver un commentaire indiquant la source du nouveau nombre. Ne pas remplacer une approximation par une autre valeur non documentée. `[F]` signifie « fichier de référence LOC », pas « mesuré sur notre kit ». Les autres références `[N,L,I,C,R]` sont expliquées au début du `.scad`; `[A]` signale une approximation.

Après chaque changement : enregistrer, F5, examiner la pièce isolée puis l’assemblage en coupe, et F6. Si une assertion échoue, lire sa condition et revoir les valeurs concernées; ne pas supprimer l’assertion pour faire disparaître le message.

Exemple de dépendance à comprendre : changer `body_wall` modifie `body_id`, donc les anneaux et le coupleur. Cela peut rendre les languettes incompatibles avec le support. La longueur `total_l` est la distance pointe/arrière du corps; elle n’inclut pas le dépassement des ailerons.

## 10. Enregistrer, exporter et actualiser les plans

1. **Garder le `.scad` :** enregistrer la copie contenant les instructions. C’est ce fichier qui permet de reprendre les paramètres.
2. **Créer une image :** choisir la vue et cadrer avec F5, puis utiliser **Fichier → Exporter → Exporter comme image / Export as Image**. Le PNG sert à montrer le résultat.
3. **Créer une géométrie 3D :** choisir une pièce, par exemple `part = "fin";`, lancer F6, puis **Fichier → Exporter → STL**. Donner un nom explicite, comme `aileron-reference.stl`. Le STL ne conserve ni les paramètres ni les couleurs.
4. **Contrôler :** rouvrir le fichier enregistré; vérifier la bonne pièce et l’absence de message d’erreur. Un export ne constitue pas une autorisation de fabriquer une pièce de vol.

Le PDF d’ensemble, les images et le modèle OpenRocket **ne se mettent pas à jour automatiquement** quand on change le `.scad`. Pour remplacer les documents du dépôt, suivre les instructions du [générateur de plan d’ensemble](../plans/ensemble/README.md) et de la [galerie](../plans/images/README.md), puis réconcilier séparément OpenRocket. Cette étape peut être faite avec l’aide d’une personne plus expérimentée.

## Dépannage rapide

| Symptôme | Action à essayer |
| --- | --- |
| `Parser error` | Regarder la ligne indiquée et celle qui précède : point-virgule, parenthèse, accolade ou guillemet manquant. |
| `Unknown variable` ou valeur `undef` | Vérifier le nom, les majuscules et la définition; un extrait non autonome a peut-être été collé seul. |
| `Assertion failed` | Lire le message et remettre le dernier paramètre modifié à sa valeur précédente pour identifier la cause. |
| Rien n’apparaît après avoir écrit un module | Ajouter son appel, par exemple `aileron_exercice();`, comme dans l’exercice. |
| La fusée paraît vide ou très éloignée | F5, puis Tout afficher; vérifier `part` et les réglages de visibilité. |
| Le fichier reste écorché | Modifier la ligne `view` existante; vérifier qu’un préréglage du Customizer ne la remplace pas. |
| Une pièce isolée reste entière malgré `view="cutaway"` | C’est prévu : la coupe concerne les enveloppes dans l’assemblage. |
| L’export de rétention est vide | Vérifier que `retention = "MR-1";`, et non `"none"`. |
| L’aperçu clignote sur certaines faces | Vérifier avec F6; des surfaces proches peuvent produire un artefact d’aperçu. Ne pas modifier une cote physique au hasard. |
| Le calcul prend du temps | Attendre la fin de F6; utiliser F5 pendant les modifications. `quality = 32;` accélère la découverte; revenir à 64 pour comparer au modèle de référence. |

## Liste de vérification de fin de séance

- [ ] J’ai conservé le modèle de référence et enregistré ma copie `.scad`.
- [ ] Je sais passer de la vue assemblée à la coupe et isoler un aileron.
- [ ] Je sais expliquer comment deux cylindres donnent un tube.
- [ ] Je sais reconnaître un module, un déplacement et la répétition des trois ailerons.
- [ ] Je distingue une cote nominale, une référence LOC et une mesure de mon kit.
- [ ] J’ai effectué F5 puis F6 et traité les messages d’erreur éventuels.
- [ ] J’ai noté mes changements et identifié les documents dérivés à actualiser.

## Points à confirmer

La géométrie réelle du kit, les positions, les jeux, la masse et le centre de gravité restent à mesurer. Faire essayer cette fiche par une personne n’ayant jamais utilisé OpenSCAD et noter les étapes qui nécessitent une explication supplémentaire. Les détails de fabrication et la validation de vol sortent du périmètre de cette initiation.

## Validation et date

Le 2026-09-12 : vérification des noms et comportements contre le fichier `plans/loc-iv-4po.scad` v1.1; compilation des trois exercices autonomes et de la variante à trois ailerons avec OpenSCAD 2021.01. Cette vérification porte sur le code des exercices, pas sur un essai utilisateur débutant ni sur le kit physique.

## Pour approfondir

Documentation officielle consultée le 2026-09-12 :

- [Télécharger OpenSCAD](https://openscad.org/downloads.html).
- [Documentation et tutoriels](https://openscad.org/documentation.html).
- [Aide-mémoire du langage, version 2021.01](https://openscad.org/cheatsheet/) : retrouver les commandes rencontrées dans cette fiche.
- [Manuel OpenSCAD](https://files.openscad.org/documentation/manual/OpenSCAD_User_Manual.html) : aperçu, rendu et export.

[Retour aux aides à la tâche](README.md) · [Retour aux plans](../plans/README.md)
