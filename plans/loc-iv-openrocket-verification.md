# Vérification du modèle OpenRocket LOC-IV

- **Date :** 2026-09-12
- **Statut :** vérification logicielle réussie; configuration physique non validée.
- **Logiciel :** OpenRocket 24.12, paquet JAR officiel; JDK portable Temurin 21.
- **Entrées :** [XML](loc-iv-4po.xml) et [archive native](loc-iv-4po.ork).
- **Révision :** 1.1, ailerons LOC corrigés; chiffres de la version précédente conservés dans les [notes historiques](../notes/loc-iv-comparaison-modeles.md).

## Contrôles

Le XML a été généré par le sérialiseur officiel OpenRocket, puis rechargé avec `GeneralRocketLoader`. Le `.ork` a été rechargé indépendamment. **Aucun avertissement d'import** pour l'un ou l'autre; les quatre simulations ont été exécutées dans chacun, soit huit exécutions. Le XML stocké dans le `.ork` est identique à la copie lisible.

Les longueurs ogive/tubes totalisent 1,1938 m; ailerons compris, la fusée atteint 1,228725 m. La masse à vide **calculée à partir des hypothèses**, accessoires compris et moteur exclu, est d'environ **1,033 kg**, avec un CG à **747,8 mm depuis la pointe**. Il ne s'agit pas de mesures de la fusée réelle.

Les deux moteurs de la base utilisée font **38 × 185 mm**, alors que l'enveloppe nominale du catalogue et du SCAD est 38 × 186 mm. Leur diamètre et leur dépassement arrière sont conservés; l'écart de 1 mm ne sert pas à modifier leurs données de poussée. H143 chargé : 347 g; H152 : 298 g. Voir les empreintes et le choix explicite du jeu H143 dans la [notice](loc-iv-openrocket.md#moteurs-et-scénarios).

## Résultats des essais logiciels

**Valeurs exploratoires du modèle estimé, pas une prévision de vol validée.** Conditions fictives décrites dans la notice : notamment vent nul, rail vertical de 2,4 m et atmosphère ISA au niveau de la mer.

| Scénario | Apogée calculée, arrondie | Temps jusqu'à l'apogée | Avertissement de simulation |
| --- | ---: | ---: | --- |
| H143 — apogée idéale | 594 m | 10,20 s | Aucun dans cet essai idéal |
| H143 — éjection 13 s | 594 m | 10,20 s | Déploiement à grande vitesse, environ 26,7 m/s |
| H152 — apogée idéale | 677 m | 10,53 s | Aucun dans cet essai idéal |
| H152 — éjection 15 s | 677 m | 10,53 s | Déploiement à grande vitesse, environ 25,2 m/s |

L'absence d'avertissement dans les deux essais idéaux ne valide ni le délai, ni la stabilité dans du vent, ni la résistance de la récupération réelle. Les scénarios d'éjection sont conservés pour rendre visible l'effet des délais d'essai; ces délais ne sont pas recommandés pour le lancement.

Contrôle statique complémentaire à Mach 0,3 et incidence nulle : CP à 902,1 mm depuis la pointe; CG chargé H143 à 838,1 mm, H152 à 828,2 mm. Les marges `(CP-CG)/101,6 mm` sont respectivement **0,63 et 0,73 calibre**, contre 0,39 et 0,49 avant correction. Cette amélioration ne valide pas la stabilité réelle ou minimale sur la trajectoire. La [confirmation des mesures du kit](../notes/loc-iv-mesures-kit.md) reste ouverte.

Les résultats ne sont pas intégrés au fichier comme simulations déjà calculées. Dans OpenRocket, exécuter de nouveau les scénarios après les mesures et modifications.

## Reproduire le contrôle

Avec un JDK 21 et le [JAR officiel OpenRocket 24.12](https://github.com/openrocket/openrocket/releases/tag/release-24.12), depuis la racine du dépôt :

```sh
java -cp /chemin/OpenRocket-24.12.jar plans/outils/verifier-openrocket.java plans/loc-iv-4po.xml plans/loc-iv-4po.ork
```

Ce contrôle utilise le moteur OpenRocket sans interface graphique. Il vérifie le chargement, la longueur totale, la présence des quatre scénarios, puis exécute les simulations et affiche leurs avertissements. Le fichier n'a pas été inspecté dans l'interface graphique; les validations portent sur le lecteur et le moteur de simulation officiels. L'environnement de test Windows a également émis des messages d'accès aux préférences Java, distincts des avertissements d'import et de vol ci-dessus; les conditions de lancement sont explicitement enregistrées dans le document.

[Retour à la notice OpenRocket](loc-iv-openrocket.md)
