# 10 — Monter la musique et les bruitages à la main

**But :** refaire le montage sonore avec les pistes fournies, puis comprendre comment elles ont été inventées.

## Les ingrédients

Dans [audio v9](../plans/animations/son/README.md), tu trouveras la musique seule, les bruitages seuls, leur mixage et la bande sonore finale. Les pistes ont toutes 40,57 s, 48 000 échantillons par seconde et deux canaux. Un **échantillon** est un nombre qui décrit un tout petit morceau de l’onde sonore.

## Refaire le montage dans Blender

1. Crée un nouveau projet Blender, ouvre l’espace **Video Editing** et règle 30 fps, début 1, fin 1217.
2. Dans le Sequencer, utilise **Add → Movie** pour ajouter le MP4 v8 sans son. Place son début à l’image 1. Si l’import ajoute une piste audio inutile, supprime uniquement cette piste.
3. Utilise **Add → Sound** pour ajouter `bande-son.wav`, début image 1, sur un autre canal.
4. Lis autour des images 61, 369 et 977. Observe allumage, éjection et contact.
5. Pour une variante personnelle, supprime la bande-son de ce montage d’essai et importe à sa place **musique-originale.wav** et **bruitages.wav**, tous deux à l’image 1.
6. Sélectionne la piste musique. Dans le panneau des propriétés de la bande, trouve Volume. Compare 1,0 puis 0,5. Ne laisse pas en plus la bande-son complète : elle doublerait les sons.
7. Sur un champ Volume, clic droit → **Insert Keyframe** permet de faire varier le volume. Pose une clé avant un événement, une clé plus faible pendant, puis une clé de retour après.

**Je vérifie :** le grondement commence à **2,000 s**, cesse vers **3,730 s**, l’éjection survient à **12,267 s** et le contact à **32,533 s** du film. Ce ne sont pas tous les temps physiques de la simulation.

Les pistes séparées sont déjà dosées et la musique y est déjà atténuée pendant certains événements. Leur somme reproduit le mixage **avant** normalisation, pas nécessairement le volume du WAV final. Pour reproduire exactement la version publiée, utilise `bande-son.wav`.

## Comprendre « Sept sillages »

La musique est originale et synthétisée : pas un enregistrement d’un groupe. Elle utilise des accords saturés, une basse, des percussions et des arpèges.

À 120 battements/minute, un battement dure 0,5 s. Une croche dure 0,25 s. Une mesure à **7/8** contient sept croches, soit **1,75 s**. Tape doucement le motif **1-2 / 1-2 / 1-2-3**. L’autre motif fait trois coups pendant que le premier en fait deux : c’est une polyrythmie 3:2.

Pour composer une variante à la main dans un logiciel de musique de ton choix, règle 120 BPM, dessine des mesures de sept croches et marque les groupes 2+2+3. Cette opération reproduit la structure, **pas les timbres exacts** du synthétiseur Python. Les fréquences, enveloppes, décalages stéréo et bruits sont explicités dans `creer-son.py`.

## D’où viennent les bruitages ?

- Moteur : bruit grave et large bande, dont l’enveloppe suit la poussée.
- Air : bruit filtré dont le niveau suit la vitesse pendant la montée sans moteur.
- Éjection : une impulsion brève, suivie d’un froissement illustratif.
- Contact : un choc amorti, puis un frottement court.

Ils illustrent le vol; ce ne sont pas des mesures du son réel d’un H143. La normalisation finale vise −18 LUFS et −2 dBTP avant compression AAC; la mesure publiée après AAC est d’environ −18,41 LUFS et −1,79 dBTP. Les LUFS décrivent le niveau perçu; la crête décrit les pointes. Monter simplement le volume peut créer de la saturation.

**Dépannage :** aucun son ? Vérifie le muet de la bande, le volume du lecteur et la sortie audio Windows. Écho ? Cherche une piste complète ajoutée en double.

[Suite : ATH](11-ath.md) · [Sommaire](README.md)
