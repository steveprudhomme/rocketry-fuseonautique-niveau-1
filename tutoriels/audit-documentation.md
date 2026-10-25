# Revue documentaire et couverture pédagogique

**Date : 24 octobre 2026. Périmètre : état publié jusqu’à la v10, puis ajout du présent manuel.**

La revue associe un recensement de tous les fichiers Markdown, une relecture ciblée des notices, guides et documents de suivi, une comparaison avec les scripts et paramètres archivés, et une inspection des données de la scène Blender finale. Elle ne constitue pas un essai intégral de chaque geste dans l’interface ni une validation pédagogique avec un enfant.

## Ce qui manquait et ce qui est ajouté

| Travail déjà réalisé | Point faible trouvé | Explication maintenant disponible |
| --- | --- | --- |
| Organisation et suivi | Pas de porte d’entrée simple pour un enfant | Chapitre 00, extension des fichiers et trois dossiers |
| Modèles SCAD / OpenRocket | Guides détaillés mais vocabulaire dense | Chapitre 01 et renvoi précis aux guides complets |
| Comparaison, achats et mesures | Risque de prendre une hypothèse ou un prix ancien pour une mesure actuelle | Chapitre 01, sources datées et fiche de mesures conservée ouverte |
| Décoration et propositions | Création d’image et génération de gabarits difficiles à distinguer | Chapitre 02 : source bitmap, raccord, impression et limites de reproduction |
| Plan A3, galerie et coupe | Rôle de la vue et de l’échelle peu expliqué; révision A encore citée dans le suivi | Chapitre 02 et correction vers la révision B livrée |
| Image artistique Blender | Peu d’aide pour comprendre les scènes et le rendu | Chapitre 03, premier PNG et distinction Cycles/Eevee |
| Vol et compression du temps | Recettes surtout sous forme de scripts | Chapitre 04, exercice de clés et tableau temps/image |
| Parachute et corde | Confusion possible entre calcul Soft Body et formes embarquées | Chapitre 05, paramètres de la corde, morphing et contrôles |
| Pendule et atterrissage | Animation visuelle facile à confondre avec une prédiction physique | Chapitre 05, gestes manuels et limites |
| Vent et volumes de fumée | Pas d’exercice élémentaire de matériau volumétrique | Chapitre 06, nuage puis émissions indépendantes |
| SRTM, orthophoto et terrain hybride | Import, reprojection et interpolation difficiles à séparer | Chapitre 07, couches et masque à construire |
| Ombres et soleil | Formules sans parcours de nœuds | Chapitre 08, connexions et valeurs de la correction |
| Caméra et optique | Paramètres décrits sans repérage des objets de contrôle | Chapitre 09, poignées, modificateurs, mise au point et scène 05 |
| Son et musique | Synthèse exacte et montage manuel mélangés | Chapitre 10, pistes séparées, mixage, rythme et limites |
| ATH et bilan | Panneaux incrustés pouvant être pris pour des objets texte Blender | Chapitre 11, maquette et fonctionnement de la composition |
| Export et publication | Différence rendu/projet/commit/publication peu enseignée | Chapitre 12 et contrôles avant partage |
| Reconstruction historique | Chemins `outputs/work` absents de l’arborescence GitHub | Chapitre 13, correspondance des dossiers et dépendances explicites |

## Corrections de suivi

- La progression personnelle ne décrit plus les plans et aides déjà livrés comme « à faire ».
- Le glossaire général pointe vers un vocabulaire simple effectivement rédigé.
- Les exercices ont maintenant un parcours et une fiche de séance.
- Le README et les index donnent accès au manuel; les notices d’animation renvoient à la leçon correspondante.
- Les documents historiques restent datés : on ne remplace pas leurs résultats par ceux d’une autre version.
- Les exigences officielles, les mesures du kit et les validations réelles restent ouvertes. Elles ne sont pas inventées pour remplir des tableaux.

## Vérifications réalisées

- Contrôle des liens relatifs Markdown vers les fichiers livrés.
- Concordance des objets cités avec la scène 03 : parachute, corps, section avant, parent de fusée, terrain et poignées de caméra.
- Présence des 1 218 formes absolues du parachute final, masque 24–36 m, scènes et séquence finale vérifiés par réouverture Blender. Le tutoriel distingue désormais ces formes de la clé relative utilisée dans la construction v2.
- Confrontation des valeurs de corde, caméra, lumière, musique et ATH aux scripts et JSON archivés.
- Conservation des versions de référence : Blender 4.3, OpenRocket 24.12, OpenSCAD 2021.01.

L’accès au manuel Blender en ligne a échoué pendant cette revue; aucune nouvelle consultation réussie de ces pages n’est revendiquée. Les explications s’appuient sur les fichiers et logiciels locaux, ainsi que sur les sources déjà citées dans les notices. Les intitulés des menus restent à confirmer si l’on utilise une autre version ou traduction.

## Ce qui n’est pas encore validé

1. **Parcours avec un enfant débutant :** chaque leçon doit être essayée pour repérer les mots et gestes qui restent difficiles. Utiliser la fiche de séance; ne pas marquer cet essai terminé avant de l’avoir fait.
2. **Historique depuis zéro :** l’enchaînement de tous les scripts anciens n’a pas été rejoué intégralement sur une installation neuve. Certaines scènes intermédiaires et tuiles complètes nécessitent l’historique ou un téléchargement. Les scènes publiées permettent de refaire les rendus sans reconstruire toute cette histoire.
3. **Identité d’un exercice manuel :** les trois poses, le nuage et le masque d’exercice enseignent le mécanisme. Ils ne sont pas présentés comme des copies exactes de tous les calculs finaux.
4. **Fabrication et vol réels :** kit, masses, dimensions et démarche de certification demandent toujours leurs vérifications propres.

Le manuel couvre tous les volets livrés, mais ces limites empêchent d’affirmer « un enfant peut déjà refaire seul chaque résultat exact depuis un fichier vide ». C’est le critère d’un prochain essai utilisateur, pas une vérification déjà effectuée.

[Inventaire des documents](inventaire-documents.md) · [Fiche de séance](fiche-seance.md) · [Sommaire](README.md)
