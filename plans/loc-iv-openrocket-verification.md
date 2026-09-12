# Vérification du modèle OpenRocket LOC-IV

- **Date :** 2026-09-12
- **Statut :** vérification logicielle réussie; configuration physique non validée.
- **Logiciel :** OpenRocket 24.12, paquet JAR officiel; JDK portable Temurin 21.
- **Entrées :** [XML](loc-iv-4po.xml) et [archive native](loc-iv-4po.ork).

## Contrôles

Le XML a été généré par le sérialiseur officiel OpenRocket, puis rechargé avec `GeneralRocketLoader`. Le `.ork` a été rechargé indépendamment. **Aucun avertissement d'import** pour l'un ou l'autre; les quatre simulations ont été exécutées dans chacun, soit huit exécutions. Le XML stocké dans le `.ork` est identique à la copie lisible.

Les longueurs exposées totalisent 1,1938 m. La masse à vide **calculée à partir des hypothèses**, accessoires compris et moteur exclu, est d'environ **1,094 kg**, avec un CG à **756 mm depuis la pointe**. Il ne s'agit pas de mesures de la fusée réelle.

Les deux moteurs de la base utilisée font **38 × 185 mm**, alors que l'enveloppe nominale du catalogue et du SCAD est 38 × 186 mm. Leur diamètre et leur dépassement arrière sont conservés; l'écart de 1 mm ne sert pas à modifier leurs données de poussée. H143 chargé : 347 g; H152 : 298 g. Voir les empreintes et le choix explicite du jeu H143 dans la [notice](loc-iv-openrocket.md#moteurs-et-scénarios).

## Résultats des essais logiciels

**Valeurs exploratoires du modèle estimé, pas une prévision de vol validée.** Conditions fictives décrites dans la notice : notamment vent nul, rail vertical de 2,4 m et atmosphère ISA au niveau de la mer.

| Scénario | Apogée calculée, arrondie | Temps jusqu'à l'apogée | Avertissement de simulation |
| --- | ---: | ---: | --- |
| H143 — apogée idéale | 539 m | 9,76 s | Aucun dans cet essai idéal |
| H143 — éjection 13 s | 539 m | 9,76 s | Déploiement à grande vitesse, environ 25 m/s |
| H152 — apogée idéale | 615 m | 10,07 s | Aucun dans cet essai idéal |
| H152 — éjection 15 s | 615 m | 10,07 s | Déploiement à grande vitesse, environ 22,1 m/s |

L'absence d'avertissement dans les deux essais idéaux ne valide ni le délai, ni la stabilité dans du vent, ni la résistance de la récupération réelle. Les scénarios d'éjection sont conservés pour rendre visible l'effet des délais d'essai; ces délais ne sont pas recommandés pour le lancement.

Les résultats ne sont pas intégrés au fichier comme simulations déjà calculées. Dans OpenRocket, exécuter de nouveau les scénarios après les mesures et modifications.

## Reproduire le contrôle

Avec un JDK 21 et le [JAR officiel OpenRocket 24.12](https://github.com/openrocket/openrocket/releases/tag/release-24.12), depuis la racine du dépôt :

```sh
java -cp /chemin/OpenRocket-24.12.jar plans/outils/verifier-openrocket.java plans/loc-iv-4po.xml plans/loc-iv-4po.ork
```

Ce contrôle utilise le moteur OpenRocket sans interface graphique. Il vérifie le chargement, la longueur totale, la présence des quatre scénarios, puis exécute les simulations et affiche leurs avertissements. Le fichier n'a pas été inspecté dans l'interface graphique; les validations portent sur le lecteur et le moteur de simulation officiels. L'environnement de test Windows a également émis des messages d'accès aux préférences Java, distincts des avertissements d'import et de vol ci-dessus; les conditions de lancement sont explicitement enregistrées dans le document.

[Retour à la notice OpenRocket](loc-iv-openrocket.md)
