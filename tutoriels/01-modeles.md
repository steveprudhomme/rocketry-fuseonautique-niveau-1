# 01 — Une fusée dessinée et une fusée calculée

**But :** comprendre pourquoi nous utilisons deux logiciels. OpenSCAD dessine les pièces; OpenRocket calcule un vol à partir de leur description.

## A. Examiner le dessin

1. Ouvre OpenSCAD et choisis **File → Open**.
2. Ouvre [loc-iv-4po.scad](../plans/loc-iv-4po.scad), puis enregistre une copie dans `essais`.
3. Appuie sur **F5** : c’est l’aperçu rapide.
4. Retrouve les réglages `part` et `view` au début du fichier. Ne crée pas une deuxième ligne du même nom.
5. Pour isoler l’aileron, utilise la valeur `"fin"` pour `part`, en conservant les guillemets et le point-virgule. Appuie sur F5.
6. Compare l’image avec la [galerie](../plans/images/README.md). La languette est la partie qui entre à l’intérieur du tube.
7. Remets la valeur d’origine pour revoir l’assemblage.

**Je vérifie :** je peux montrer un aileron seul puis la fusée. Si OpenSCAD annonce une erreur, annule la dernière modification et vérifie les guillemets.

Pour **construire les formes depuis zéro**, suis les exercices autonomes de la [fiche OpenSCAD](../aides-a-la-tache/debuter-openscad-loc-iv.md), sections 5 à 8 : cylindre creux, anneau, aileron et répétition. Un `module` est une petite recette; `translate` déplace et `rotate` tourne. Faire F6 puis exporter ne rend pas la pièce apte à voler.

## B. Examiner le calcul

1. Ouvre OpenRocket, puis [loc-iv-4po.ork](../plans/loc-iv-4po.ork).
2. Fais **Save As** dans `essais`.
3. Dans **Rocket Design**, clique sur le tube principal, puis sur le parachute. Observe leurs noms dans l’arbre des pièces.
4. Double-clique le parachute et relève le diamètre affiché, en lisant l’unité. La référence est 914,4 mm, soit 36 pouces.
5. Ferme sans changer ce nombre. Dans **Flight Simulations**, repère les quatre scénarios.
6. Sélectionne un scénario et lance **Run simulations**. Les résultats ne sont pas forcément présents à l’ouverture.
7. Ouvre ses courbes et choisis altitude en fonction du temps. Repère le sommet : c’est l’apogée.

**Je vérifie :** je distingue la forme de la fusée et la courbe de son vol. Je note le nom du scénario avec le résultat; je ne mélange pas deux scénarios.

La [fiche OpenRocket](../aides-a-la-tache/debuter-openrocket-loc-iv.md) donne les parents, positions, dimensions et masses des **19 entrées** du modèle. Pour le reconstruire à la main, avance par groupes : enveloppe, pièces internes, ailerons, récupération, masses, configurations. Compare l’arbre après chaque groupe.

## Les nombres ne sont pas tous des mesures

101,6 mm est un diamètre nominal du modèle. Environ 1 033 g est sa masse **calculée sans moteur**. Ces valeurs ne prouvent pas les dimensions ou la masse de notre kit.

Pour préparer les futures mesures, ouvre la [fiche du kit](../notes/loc-iv-mesures-kit.md). Inscris seulement une vraie observation dans la colonne « mesuré ». Garde « à relever » si tu n’as pas mesuré. Les prix du [budget](../notes/loc-iv-configuration-budget-niveau-1.md) sont aussi datés : ce ne sont pas des prix du jour.

**Défi :** dessine deux boîtes sur papier, « forme » et « vol », et place OpenSCAD et OpenRocket dans la bonne boîte.

[Suite : décoration et plans](02-decoration-plans.md) · [Sommaire](README.md)
