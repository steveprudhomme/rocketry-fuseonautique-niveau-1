# 06 — Le vent pousse, la fumée se disperse

**But :** comprendre deux travaux différents : le vol avec du vent, puis son illustration par de la fumée.

## Le vent du calcul

Dans une copie du scénario OpenRocket, ouvre ses conditions de simulation. Retrouve les champs de vent. La référence v4 utilise **2 m/s**, une turbulence de **10 %** et une direction OpenRocket de **90°**. Lis la convention de direction dans le logiciel; ne suppose pas qu’un angle de vent se lit comme une rotation Blender.

Ne change qu’un paramètre dans une **copie** du scénario, relance le calcul et compare la dérive. Note le nom et les conditions des deux essais. La valeur d’environ 164 m appartient au CSV archivé du projet; elle n’est pas une promesse pour le terrain réel.

## Un nuage d’exercice dans Blender

1. Dans un fichier neuf, ajoute une sphère avec **Shift+A → Mesh → UV Sphere**. Enregistre ton exercice.
2. Passe dans l’espace **Shading**. Crée un matériau avec **New**.
3. Supprime le nœud Principled BSDF de ce matériau d’exercice.
4. Ajoute **Principled Volume**. Relie sa sortie **Volume** à l’entrée **Volume** de **Material Output**. Ne la branche pas sur Surface.
5. Mets une couleur grise et une densité de 0,1 pour commencer. Utilise la vue rendue ou F12 pour voir le volume.
6. À l’image 1, donne une petite échelle à la sphère et insère une clé d’échelle.
7. À l’image 61, agrandis-la; déplace-la un peu vers X négatif et vers le haut; insère des clés de position et d’échelle.
8. Sur le champ Density du nœud, insère une clé à 0,1 au début puis à 0 à l’image 91.

**Je vérifie :** le nuage se déplace, grossit puis disparaît. Si tu vois une boule solide, vérifie la connexion Volume et l’absence de matériau de surface opaque.

## Lui donner des irrégularités

Ajoute un nœud **Noise Texture** et un nœud **Math → Multiply**. Branche Fac du bruit sur une entrée de Multiply, mets 0,1 dans l’autre, puis branche le résultat sur Density. Le bruit fait des zones plus ou moins denses. À partir de là, anime le multiplicateur plutôt qu’une densité déjà pilotée par un fil.

Ce nuage simple peut avoir un bord trop visible. Dans le film, une atténuation supplémentaire vers le bord évite l’impression de coque. Les scripts règlent aussi les coordonnées du bruit, sa variation, l’expansion et la dilution : ce n’est pas un unique réglage Density.

## Ce que le film ajoute

La v4 contient **116 volumes**, émis seulement durant les **1,73 s** de combustion. Chacun naît à la position du moteur, puis reste indépendant de la fusée. Sa densité disparaît après environ 7 s. Si les nuages restaient enfants de la fusée en mouvement, ils la suivraient comme un paquet de ballons : ce serait faux visuellement.

Pour refaire une petite émission à la main, duplique ton nuage trois fois, décale ses clés dans le Dope Sheet et place chaque départ à l’endroit du moteur à cet instant. Refaire les 116 émissions exactement demande la recette archivée et ses passes de correction, listées au chapitre 13.

**Défi :** explique pourquoi le vent du calcul et le bruit d’une texture ne sont pas la même chose. Le premier change la trajectoire; le second dessine des variations dans la fumée.

[Notice et paramètres v4](../plans/animations/vol-complet/README.md) · [Suite : terrain](07-terrain.md) · [Sommaire](README.md)
