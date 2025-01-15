# PolyHash-24

Ce dépôt correspond au projet informatique de première années de 4 étudiants de Polytech Nantes.

# EQUIPE B : BLACK HAT

## Étudiants : 
- Augustin BERNARD
- Bryan LEVY
- Coralie TOSTEN
- Roudy HAJO

## descriptif général du projet ;

A Partir d'une carte des vents tridimensionnel, d'une liste de balise à couvrir et d'une liste de ballons a disposition, nos stratégies doivent fournir une liste d'action a donner aux ballons (se déployer, aller en haut, en bas, ou ne rien faire) afin qu'ils puisse être portés par le vent (chaque case de la carte vent contient un vecteur de déplacement deux dimensionnel) et couvrir le plus de balise pendant un maximum de temps.

## Assignation des taches :
- **Augustin** : Gestion du groupe, travail théorique sur la résolution du problème (carte ID balises, décalage des ballons, système de clustering, stratégie aléatoire variée), trouver des idées, régler les problèmes d'optimisation. Réalisation d'une première version prototype de A star + clustering. Travail en binôme avec Roudy sur le clustering. Implémentation de la stratégie ligne pour la solution d

- **Bryan** : Création de la stratégie aléatoire, aide pour la stratégie A star + clustering. Amélioration de la stratégie aléatoire en stratégie aléatoire évolutive, puis évolutive variée.

- **Roudy** : Fonction pour créer le DOT a partir du fichier d'entrée. Travail en binôme avec Augustin sur le clustering. Parralélisation de la stratégie Aléatoire évolutive variée.

- **Coralie** : Création de la stratégie proche. Travail avec Bryan sur la stratégie Aléatoire.

## procédure d'installation ;

## procédure d'exécution ;
Deux Objets utiles utilisés sur certaines stratégies :

**Carte ID balises :** Carte créée au tout début de l'éxecution sur laquelle chaque case contient une liste des balises dont le rayon de couverture est dans la case (utile pour calculer le score ou les clusters).

**Interval entre les ballons :** On ne déploie le ballon uniquement si son id multiplié par un interval de déploiement est inferieur au tour actuel.

## Stratégies utilisées :

### - A star + clustering
Regroupement des balises en clusters a l'aide d'une carte contenant les ID des balises dans chaque cases du rayon de couverture de celles-ci. Selection des meilleurs clusters en fonction du nombre de balises a l'interieur. Affectation des clusters dans l'ordre croissant des scores a chaque ballon. Recherche des clusters pour chaque ballon. Puis utilisation de la stratégie A star pour que ces ballons se dirigent vers leur balise associé et y restent.

Efficacité :

Complexité :

### - Stratégie Aléatoire
Stratégie par force brute dans laquelle chaque ballon décide de prendre une direction aléatoire et on ne garde que le meilleur score.

Efficacité : Assez efficace sur le long terme, peu efficace si on doit souvent changer de carte.

Complexité : Extremement long pour trouver un bon score (270 000 sur la solution d en quelques heures)

### - Stratégie Proche
### - Stratégie Aléatoire évolutive variée
Même principe que pour la stratégie aléatoire mais pour éviter les redondances entre les solutions,on prend en compte la liste des ordres donnés aux ballons et on la modifie légèrement (avec une probabilité pour chaque ordre, qu'il change). Evolutive car on ne garde que la meilleure des listes d'ordres. Variée car on commence par des générations differentes afin d'avoir moins de chance de commencer par une liste d'ordre qui n'amène a rien.


Efficacité : Efficace sur le long terme, peu efficace si on doit souvent changer de carte. (**300 000 en moins d'une minute**, 400 000 en quelques heures, sur la solution d)

Complexité : Beaucoup plus rapide que la stratégie aléatoire car on évite les redondances.

### - Stratégie Ligne
Stratégie assez basique qui prend en arguments le numéro d'une ligne ainsi qu'un interval de déploiement entre les ballons. Cette stratégie a été pensée pour la solution d (car les ballons vont vers l'Est en permanance et les balises de la carte d sont surtout regroupées vers le Nord).

Efficacité : Efficace sur le long terme, peu efficace si on doit souvent changer de carte. (**277 000** sur la solution d à la ligne 15 et avec un interval de 80)

Complexité : Très rapide (5 secondes)


