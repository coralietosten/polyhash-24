# PolyHash-24 EQUIPE B : BLACK HAT

Ce dépôt correspond au projet informatique de troisième années de Polytech Nantes.

## Étudiants : 
- Augustin BERNARD
- Bryan LEVY
- Coralie TOSTEN
- Roudy HAJO

## descriptif général du projet ;

A partir d'une carte des vents tridimensionnel, d'une liste de balise à couvrir et d'une liste de ballons à disposition, nos stratégies doivent fournir une liste d'action à donner aux ballons (se déployer, aller en haut, en bas, ou ne rien faire) afin qu'ils puissent être portés par le vent (chaque case de la carte vent contient un vecteur de déplacement deux dimensionnel) et couvrir le plus de balise pendant un maximum de temps.

## Assignation des taches :
- **Augustin** : Gestion du groupe, travail théorique sur la résolution du problème (carte ID balises, décalage des ballons, système de clustering, stratégie aléatoire variée), trouver des idées, régler les problèmes d'optimisation. Réalisation d'une première version prototype de A star + clustering. Travail en binôme avec Roudy sur le clustering. Implémentation des stratégies ligne, double lignes et triple lignes pour la solution d a l'aide de la stratégie proche de Coralie et de la visualisation de carte de Bryan.

- **Bryan** : Création de la stratégie aléatoire, aide pour la stratégie A star + clustering. Amélioration de la stratégie aléatoire en stratégie aléatoire évolutive, puis évolutive variée. Création d'une visualisation d'une carte contenant l'emplacement des balises et le déplacement des ballons sur la carte.

- **Roudy** : Fonction pour créer le DAO (Data Access Object) à partir du fichier d'entrée. Travail en binôme avec Augustin sur le clustering. Parralélisation de la stratégie Aléatoire évolutive variée sur ordinateur. Tentative de bruteforce avec la stratégie arbre.

- **Coralie** : Création de fonction permettant de lancer la simulation. Création de la stratégie proche. Travail avec Bryan sur la stratégie Aléatoire. Calcul de la complexité spatiale et du temps d'exécution de chaque stratégie.

## procédure d'installation ;

Pour lancer le jeu : 
```shell
python3 polyhash.py data/a_example.in
```

## procédure d'exécution ;
Deux Objets utiles utilisés sur certaines stratégies :

**Carte ID balises :** Carte créée au tout début de l'éxecution sur laquelle chaque case contient une liste des balises dont le rayon de couverture est dans la case (utile pour calculer le score ou les clusters).

**Interval entre les ballons :** On ne déploie le ballon uniquement si son id multiplié par un interval de déploiement est inferieur au tour actuel.

## Stratégies utilisées :

### - A star + clustering
Regroupement des balises en clusters a l'aide d'une carte contenant les ID des balises dans chaque cases du rayon de couverture de celles-ci. Selection des meilleurs clusters en fonction du nombre de balises a l'interieur. Affectation des clusters dans l'ordre croissant des scores à chaque ballon. Recherche des clusters pour chaque ballon. Puis utilisation de la stratégie A star pour que ces ballons se dirigent vers leur balise associé et y restent.

Efficacité : Efficace sur les premieres solutions, assez peu efficace sur la solution_d étant donné de son aspect unidirectionnel

Complexité :

### - Stratégie Aléatoire
Stratégie par force brute dans laquelle chaque ballon décide de prendre une direction aléatoire et on ne garde que le meilleur score.

Efficacité : Assez efficace sur le long terme, peu efficace si on doit souvent changer de carte.

Complexité : Extremement long pour trouver un bon score (270 000 sur la solution d en quelques heures)

### - Stratégie Proche
Chaque ballon est assignée à une balise qui devient son objectifs, les balises sont choisis par distance : la cible du premier ballon est la balise la plus proche, celle du deuxième, la deuxième cible la plus proche. Tous les ballons ont donc des objectifs différents. A chaque tour le ballon se déplace en fonction de la distance entre lui et sa cible (il prend la plus proche). Enfin, si le ballon à atteint sa cible, elle est recalculée s'il est plus près d'une autre cible au prochain tour.

Efficacité : Asszez efficace sur les petites cartes mais pas sur la carte_d.

Conplexité : 

### - Stratégie Aléatoire Evolutive Variée
Même principe que pour la stratégie aléatoire mais pour éviter les redondances entre les solutions,on prend en compte la liste des ordres donnés aux ballons et on la modifie légèrement (avec une probabilité pour chaque ordre, qu'il change). Evolutive car on ne garde que la meilleure des listes d'ordres. Variée car on commence par des générations differentes afin d'avoir moins de chance de commencer par une liste d'ordre qui n'amène a rien.


Efficacité : Efficace sur le long terme, peu efficace si on doit souvent changer de carte. (**300 000 en moins d'une minute**, 400 000 en quelques heures, sur la carte_d)

Complexité : Beaucoup plus rapide que la stratégie aléatoire car on évite les redondances.

### - Stratégie Ligne
Stratégie assez basique reprenant le principe de la stratégie proche mais en ne visant qu'une coordonnée y précise, qui prend en arguments le numéro d'une ligne ainsi qu'un interval de déploiement entre les ballons. Cette stratégie a été pensée pour la carte_d (Les ballons vont vers l'Est en permanence et les balises de la carte d sont surtout regroupées vers le Nord).

Efficacité : Assez efficace pour une stratégie basique (**277 000** sur la carte_d à la ligne 15 et avec un interval de 80)

Complexité : Linéaire (5 secondes)

### - Stratégie Double Ligne
Même principe que la stratégie ligne mais on associe plusieurs lignes en fonction des ballons paires et impaires.

Efficacité : Très efficace sur la carte_d (**320 000** sur la carte_d à la ligne 10 et 30 et avec un interval de 40)

Complexité : Linéaire (5 secondes)

### - Stratégie Triple Ligne
Même principe que la double ligne mais 3 lignes, on coupe également les lignes en 3 pour chaque continent (Amérique, Afrique et Australie) ce qui donne 3 lignes à suivre par ballons en fonction de leur position en x et donc 9 lignes en tout.

Efficacité : Extremement efficace sur la carte_d (**432 000** sur la carte_d)

Complexité : Linéaire (5 secondes)

-> **Solution très efficace**, il ne reste plus qu'a adapter la fonction pour faire varier les paramètres et le nombre de lignes.

### - Stratégie Arbre

Cette stratégie consiste à créer un arbre où chaque nœud correspond à une action possible (-1 pour descendre, 0 pour rester, 1 pour monter). Chaque nœud possède un score cumulé depuis le début. La profondeur de l'arbre est déterminée par le nombre de tours.

Les nœuds feuilles sont triés en fonction de leur score, et la meilleure feuille est sélectionnée. Ensuite, le chemin des actions est construit en partant de cette feuille et en remontant l'arbre jusqu'à la racine.

Une fois qu'un chemin est sélectionné, les scores des nœuds de chaque niveau de l'arbre sont mis à jour pour prendre en compte les balises déjà couvertes par le chemin sélectionné à un tour donné.

Efficacité : Cette stratégie permet d'explorer différentes combinaisons d'actions et de trouver des chemins optimaux.

Complexité : La complexité de cette stratégie dépend de la profondeur de l'arbre et du nombre de nœuds générés. Plus l'arbre est profond, plus le temps de calcul et la mémoire nécessaire augmentent. Cette approche devient inefficace pour des fichiers de taille moyenne comme c_medium en raison de la croissance exponentielle du nombre de nœuds.