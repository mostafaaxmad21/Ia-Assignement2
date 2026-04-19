# Journal de tests de l'agent OXOno

Ce fichier sert a consigner tous les tests realises pour le rapport.
J'ajouterai chaque nouvelle campagne de tests sous le format ci-dessous.

## Template

### Test XXX - Nom de la campagne

Version :

Modification :

Hypothese :

Adversaires testes :

#### Match A

p0 :

p1 :

Nombre de parties :

Resultats :
- victoires :
- defaites :
- nulles :
- longueur moyenne :
- temps moyen (si dispo) :

#### Match B

p0 :

p1 :

Nombre de parties :

Resultats :
- victoires :
- defaites :
- nulles :
- longueur moyenne :
- temps moyen (si dispo) :

Verdict :
- garde / rejete

Pourquoi :

## Tests realises

### Test 001 - Baseline Alpha-Beta vs Random

Version :

baseline_alpha_beta_agent.py

Modification :

Version de base Alpha-Beta copiee depuis `my_agent.py`, profondeur effective 2 plis depuis l'etat courant (le coup racine plus une reponse adverse), avec `depth_left = 1` dans l'appel recursif et evaluation terminale uniquement.

Hypothese :

L'agent Alpha-Beta de base bat `random_agent.py` de facon stable dans les deux couleurs. Si les resultats restent similaires entre pink et black, la couleur ne change pas significativement le comportement sur ce duel.

Adversaires testes :

random_agent.py

#### Match A

p0 :

baseline_alpha_beta_agent.py

p1 :

random_agent.py

Nombre de parties :

10

Resultats :
- victoires : 10
- defaites : 0
- nulles : 0
- longueur moyenne : 13.00 coups
- temps moyen (si dispo) : 0.000727 s par coup

#### Match B

p0 :

random_agent.py

p1 :

baseline_alpha_beta_agent.py

Nombre de parties :

10

Resultats :
- victoires : 10
- defaites : 0
- nulles : 0
- longueur moyenne : 11.60 coups
- temps moyen (si dispo) : 0.000535 s par coup

Verdict :
- garde

Pourquoi :

La profondeur 2 est retenue comme baseline car elle bat `random_agent.py` de facon stable dans les deux couleurs tout en restant la version la plus simple et la moins couteuse. Tant qu'il n'y a pas de fonction d'evaluation coherente, augmenter la profondeur n'apporte pas de gain interpretable.

### Test 002 - Profondeur 3 vs Baseline profondeur 2

Version :

baseline_alpha_beta_depth3_agent.py

Modification :

Baseline Alpha-Beta sans heuristique terminale uniquement, avec profondeur effective 3 plis depuis l'etat courant.

Hypothese :

Augmenter la profondeur de 2 a 3 plis doit ameliorer le niveau de jeu contre la baseline profondeur 2 dans les deux couleurs.

Adversaires testes :

baseline_alpha_beta_agent.py

#### Match A

p0 :

baseline_alpha_beta_depth3_agent.py

p1 :

baseline_alpha_beta_agent.py

Nombre de parties :

10

Resultats :
- victoires : 0
- defaites : 10
- nulles : 0
- longueur moyenne : 16.00 coups
- temps moyen (si dispo) : 0.008202 s par coup

#### Match B

p0 :

baseline_alpha_beta_agent.py

p1 :

baseline_alpha_beta_depth3_agent.py

Nombre de parties :

10

Resultats :
- victoires : 10
- defaites : 0
- nulles : 0
- longueur moyenne : 16.00 coups
- temps moyen (si dispo) : 0.007043 s par coup

Verdict :
- rejete

Pourquoi :

Cette version n'est pas gardee pour le moment. Les resultats changent completement selon l'ordre de jeu, ce qui suggere que la profondeur seule n'explique pas la performance. Sans fonction d'evaluation coherente, la profondeur 3 ajoute surtout de la complexite.

### Test 003 - Profondeur 4 vs Baseline profondeur 2

Version :

baseline_alpha_beta_depth4_agent.py

Modification :

Baseline Alpha-Beta sans heuristique terminale uniquement, avec profondeur effective 4 plis depuis l'etat courant.

Hypothese :

Augmenter la profondeur de 2 a 4 plis doit ameliorer le niveau de jeu contre la baseline profondeur 2 dans les deux couleurs.

Adversaires testes :

baseline_alpha_beta_agent.py

#### Match A

p0 :

baseline_alpha_beta_depth4_agent.py

p1 :

baseline_alpha_beta_agent.py

Nombre de parties :

10

Resultats :
- victoires : 0
- defaites : 10
- nulles : 0
- longueur moyenne : 24.00 coups
- temps moyen (si dispo) : 0.024080 s par coup

#### Match B

p0 :

baseline_alpha_beta_agent.py

p1 :

baseline_alpha_beta_depth4_agent.py

Nombre de parties :

10

Resultats :
- victoires : 10
- defaites : 0
- nulles : 0
- longueur moyenne : 16.00 coups
- temps moyen (si dispo) : 0.023204 s par coup

Verdict :
- rejete

Pourquoi :

Cette version n'est pas gardee pour le moment. Les resultats changent completement selon l'ordre de jeu, ce qui suggere que la profondeur seule n'explique pas la performance. Sans fonction d'evaluation coherente, la profondeur 4 ajoute de la complexite et du temps sans benefice clair.

### Test 004 - Alignement Naif Global vs Baseline

Version :

naive_global_alignment_agent.py

Modification :

Scoring d'alignement naif global : l'agent attribue un score selon le nombre de pions alignes horizontalement ou verticalement sur tout le plateau, pour la couleur et pour le symbole, sans verifier si les alignements sont bloques ou facilement jouables.

Hypothese :

Un scoring d'alignement naif global doit permettre a `naive_global_alignment_agent.py` de mieux jouer que la baseline Alpha-Beta terminale uniquement dans les deux couleurs.

Adversaires testes :

baseline_alpha_beta_agent.py

#### Match A

p0 :

naive_global_alignment_agent.py

p1 :

baseline_alpha_beta_agent.py

Nombre de parties :

10

Resultats :
- victoires : 10
- defaites : 0
- nulles : 0
- longueur moyenne : 23.00 coups
- temps moyen (si dispo) : 0.003023 s par coup

#### Match B

p0 :

baseline_alpha_beta_agent.py

p1 :

naive_global_alignment_agent.py

Nombre de parties :

10

Resultats :
- victoires : 10
- defaites : 0
- nulles : 0
- longueur moyenne : 16.00 coups
- temps moyen (si dispo) : 0.002766 s par coup

Verdict :
- garde

Pourquoi :
Lajout d'une heuristique lié au nombre de pions allignés par ligne et colonne montre bien que l'algorithme se guide mieux que si il n'y en a pas du tout malgré le fait que ce n'est pas encore parfait ( prend pas en compte si c accessible directement , si c'est possible etc )

### Test 005 - MyAgent ameliore vs Alignement Naif Global

Version :

my_agent.py

Modification :

Reprise du scoring naif global comme base principale, ajout d'un bonus secondaire par fenetres couleur, et ajout d'une ouverture fixe simple pour `p0`.

Hypothese :

Cette version de `my_agent.py` doit faire au moins aussi bien que `naive_global_alignment_agent.py`, et idealement le battre dans les deux couleurs.

Adversaires testes :

naive_global_alignment_agent.py

#### Match A

p0 :

my_agent.py

p1 :

naive_global_alignment_agent.py

Nombre de parties :

10

Resultats :
- victoires : 10
- defaites : 0
- nulles : 0
- longueur moyenne : 13.00 coups
- temps moyen (si dispo) : 0.008409 s par coup

#### Match B

p0 :

naive_global_alignment_agent.py

p1 :

my_agent.py

Nombre de parties :

10

Resultats :
- victoires : 10
- defaites : 0
- nulles : 0
- longueur moyenne : 24.00 coups
- temps moyen (si dispo) : 0.008367 s par coup

Verdict :
- garde

Pourquoi :
Cette amelioration est finalement conforme a ce qui etait attendu apres recalibrage. Les premiers essais avaient montre qu'ajouter trop de bonus (notamment autour des fenetres et du symbole) degradait l'evaluation au lieu de l'ameliorer. La version retenue garde une base solide avec le scoring naif global, puis ajoute seulement un bonus secondaire par fenetres couleur. Sur les tests, cette version bat `naive_global_alignment_agent.py` dans les deux sens (10/10 en `p0` et 10/10 en `p1`), ce qui montre que l'evaluation guide mieux la recherche tout en restant assez simple et stable.
