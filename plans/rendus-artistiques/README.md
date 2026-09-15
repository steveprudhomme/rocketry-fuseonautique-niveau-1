# Chasse Galerie 1 - Décollage à l'heure dorée

**Image artistique, 2026-09-14.** Scène construite et rendue dans **Blender 4.3 / Cycles**, avec le décor **Le sillage fleurdelisé**. Blender est le logiciel 3D utilisé ici; aucun rendu POV-Ray n'est revendiqué.

![Chasse Galerie 1 décolle au-dessus des chaumes de maïs dans la lumière du soir](chasse-galerie-1-golden-hour.png)

## Fichiers

- [Image finale PNG](chasse-galerie-1-golden-hour.png) : portrait de 1800 × 2400 pixels.
- [Scène Blender modifiable](chasse-galerie-1-golden-hour.blend) : textures intégrées au fichier, caméra et éclairage conservés.
- [Script de construction et de rendu](../outils/rendre-decollage-blender.py) : géométrie, paysage, matériaux et composition reproductibles.

## Composition

La fusée quitte sa rampe au-dessus d'un champ de maïs récolté : tiges coupées, feuilles sèches recourbées, sol irrégulier et lisière automnale. Un soleil bas éclaire la fusée et le panache en contre-jour; un léger éclairage d'appoint conserve la lisibilité du bleu, du drapeau et du nom. Le jet et la fumée sont des éléments visuels procéduraux.

La fusée reprend les cotes du [plan OpenSCAD](../loc-iv-4po.scad) : diamètre nominal 101,6 mm, tubes de 584,2 et 279,4 mm, ogive ellipsoïdale dérivée de 330,2 mm et profil des trois ailerons LOC. Les deux [textures du décalque](../decalques/sillage/README.md) sont appliquées avec un tour complet par section et le raccord à 60 degrés dans le repère du modèle. L'inclinaison et la hauteur de la fusée sont des choix de composition.

Le paysage est fictif. Ce rendu n'est ni une photographie de lancement, ni une simulation de trajectoire ou de panache moteur. Les cotes du kit et la masse du décor restent à confirmer dans le projet technique. Aucun paramètre des fichiers OpenRocket ou du plan SCAD de base n'est modifié pour cette image.

## Ouvrir ou refaire le rendu

1. Ouvrir le fichier `.blend` dans Blender 4.3 ou une version compatible.
2. Appuyer sur **pavé numérique 0** pour voir la composition depuis la caméra.
3. Appuyer sur **F12** pour rendre l'image avec Cycles; enregistrer le résultat depuis la fenêtre de rendu.
4. Si le GPU utilisé ici n'est pas disponible, choisir un appareil de calcul compatible ou le CPU dans les réglages Cycles.

Pour reconstruire la scène depuis la racine du dépôt, lancer Blender avec le script :

```text
blender --background --factory-startup --python plans/outils/rendre-decollage-blender.py
```

Ajouter `-- --preview` à la commande pour produire un aperçu à demi-résolution avec moins d'échantillons. La reconstruction lit le SCAD et les textures du dépôt. La scène `.blend`, elle, contient les textures nécessaires à son rendu.

## Vérification de la livraison

Image finale inspectée; scène rouverte dans Blender 4.3 : moteur Cycles, 1800 × 2400 pixels et deux textures intégrées confirmés. Les collections séparent la fusée, le champ, la lisière, la lumière/caméra et le panache/rampe. L’aperçu `apercu-decollage.png` conserve un essai antérieur; le fichier `chasse-galerie-1-golden-hour.png` est le rendu final.

## Provenance

- Géométrie : plan SCAD du projet, dont les ailerons issus de la référence LOC.
- Illustration du vinyle : [adaptation du Sillage fleurdelisé et prompt conservé](../decalques/sillage/prompt-adaptation.md); la texture provient de la création graphique précédente.
- Champ, feuilles, lisière, soleil, fumée et jet : objets et matériaux procéduraux construits pour cette scène. Aucun fond photographique ni bibliothèque 3D externe.
- Image finale : rendu Cycles, avec profondeur de champ et halo lumineux dans le compositeur Blender; aucune génération d'image utilisée pour remplacer le rendu 3D.
- Documentation du moteur : [Blender 4.3, rendu en ligne de commande](https://docs.blender.org/manual/en/4.3/advanced/command_line/index.html), [Cycles 4.3](https://developer.blender.org/docs/release_notes/4.3/cycles/).

[Plans](../README.md) · [Décalque retenu](../decalques/sillage/README.md) · [Accueil](../../README.md)
