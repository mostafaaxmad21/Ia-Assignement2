# Erreurs et blocages rencontres

Ce fichier sert a noter les problemes rencontres pendant le developpement, separes du journal de tests.

## Blocage 001 - Evaluation amelioree moins performante que l'alignement naif

Version concernee :

`my_agent.py`

Contexte :

Une nouvelle fonction d'evaluation a ete ajoutee avec plusieurs idees :
- prise en compte des alignements ouverts ou bloques
- bonus sur les lignes et colonnes atteignables avec `Game.actions`
- evaluation par fenetres de 4 cases
- passe couleur + passe symbole

Probleme observe :

Cette "amelioration" a perdu contre `naive_global_alignment_agent.py`.

Resultat observe :

- `my_agent.py` en `p0` contre `naive_global_alignment_agent.py` en `p1` : 0 victoire, 10 defaites
- `my_agent.py` en `p1` contre `naive_global_alignment_agent.py` en `p0` : 0 victoire, 10 defaites

Conclusion provisoire :

L'evaluation actuelle etait mal calibree et attribuait mal certaines menaces, en particulier sur la partie fenetres / symbole / accessibilite.

Cause precise :

- La passe symbole par fenetres etait trop agressive et attribuait des menaces de facon instable.
- Les bonus ajoutes a l'evaluation naive etaient trop forts : ils remplaçaient pratiquement l'heuristique de base au lieu de simplement departager des coups proches.
- Le probleme restant venait ensuite surtout du departage entre plusieurs ouvertures de meme score. Certaines ouvertures equivalentes pour l'evaluation menaient a une victoire contre `naive_global_alignment_agent.py`, d'autres a une defaite.

Resolution retenue :

- Suppression de la passe symbole par fenetres dans la version actuelle de `my_agent.py`.
- Reutilisation du scoring naif global comme base principale.
- Utilisation du score par fenetres couleur comme critere secondaire de departage.
- Ajout d'une ouverture fixe simple pour `p0`, choisie parmi les ouvertures testees qui gagnent contre `naive_global_alignment_agent.py`.

Verification :

Apres ces corrections, `my_agent.py` gagne a nouveau contre `naive_global_alignment_agent.py` dans les deux sens.
