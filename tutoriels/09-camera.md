# 09 — Une caméra qui accompagne le vol

**But :** comprendre le suivi, les petits tremblements, la netteté et les reflets. Utilise une copie du fichier v8 ou de la scène 03 finale.

## A. Suivre sans tout bloquer au centre

Dans l’Outliner, cherche `CAMÉRA — suivi amorti et zone de tolérance`. La caméra est enfant de plusieurs objets vides. Un **Empty** ne se voit pas au rendu; il sert de poignée pour déplacer d’autres objets.

La zone de tolérance autorise un petit mouvement du sujet : ±2,2 % de la largeur et ±2,5 % de la hauteur de l’image. Au-delà, la poignée rattrape doucement le sujet, avec une constante de 0,18 s.

Pour ton exercice manuel, anime un cube qui monte, ajoute une caméra et pose seulement trois clés de caméra : départ, milieu, fin. Fais-la rattraper le cube un peu après son déplacement. Observe le retard. **Ce n’est pas le calcul exact de la zone de tolérance** : le suivi final est enregistré image par image par le script, avec une limite de retard pour garder tout le parachute visible.

## B. Examiner le tremblement du moteur

1. Sélectionne `CAMÉRA — secousse moteur native`.
2. Change un éditeur en **Graph Editor** et affiche ses courbes de rotation.
3. Sélectionne une courbe; dans le panneau latéral des modificateurs, retrouve **Noise** puis **Envelope**.
4. Observe la restriction d’images du bruit : **61 à 113**.
5. Dans une copie, désactive temporairement le modificateur Noise avec son contrôle de visibilité et compare la lecture au décollage. Réactive-le ensuite.

Noise crée le tremblement; Envelope règle sa force au fil du temps. Les trois plafonds sont 0,22°, 0,16° et 0,12°, modulés par l’accélération. Les données internes de courbe utilisent des radians : **1° = environ 0,017453 radian**. Ne saisis pas « 0,22 » dans un champ en radians en pensant mettre 0,22 degré.

Le tremblement effectivement mesuré reste inférieur à 0,088° sur un axe. Il est nul hors combustion. Un simple Noise permanent ne reproduirait pas cette synchronisation.

## C. Faire la mise au point

1. Sélectionne la caméra active, puis son onglet de données, l’icône de caméra verte.
2. Repère la focale **45 mm** et **Depth of Field**.
3. Le Focus Object est `CAMÉRA — mise au point adaptative`. C’est le repère qui suit le centre de l’ensemble visible.
4. Sur une image fixée, dans ta copie, compare f/7,1 puis f/2,8. Fais deux rendus et reviens aux valeurs d’origine.

Un petit nombre f rend généralement la zone nette plus mince. Dans le film, l’ouverture varie avec l’altitude et reste au moins à f/4 pendant la récupération. Comme le champ est animé, changer d’image peut annuler une valeur d’essai non enregistrée.

## D. Observer les effets optiques

Dans Compositing, retrouve **Aberration chromatique subtile**, dispersion **0,0007**. Pour la comprendre, rends une image avant/après désactivation du nœud dans une copie; évite de pousser le réglage au point de rendre le texte illisible.

Les reflets ne sont actifs que si la caméra regarde vers le soleil, dans un cône de 25°, avec un mélange maximal de 10 %. Le vol principal regarde dans l’autre direction : **ne pas voir de reflets dans ce vol est normal**. Choisis la scène **05 — Contrôle optique face au soleil**, image 58, pour les observer.

Le disque solaire est une forme du compositeur; la sphère géométrique initiale est masquée. Ne la réactive pas : elle pourrait créer une ombre indésirable sur le terrain.

[Paramètres exacts](../plans/animations/cinematographie/donnees/cinematographie.json) · [Suite : son](10-son.md) · [Sommaire](README.md)
