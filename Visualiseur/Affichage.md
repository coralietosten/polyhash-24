# Visualiseur de map 

## Lancement du visualiseur

Il y a 3 façons de lancer le visualiseur : 
Si vous possédez seulement le fichier d'entrée contenant les informations du polyhash :
```shell
py Visualiseur/main.py chemin/fichier_entree.txt
```
Si vous vous possédez le fichier d'entrée et le fichier de sauvegarde des positions des ballons
```shell
py Visualiseur/main.py chemin/fichier_entree.txt chemin/fichier_Sauvegarde
```
Pour aller plus vite, il est possible de lancer le fichier sans paramètres et il vous sera demandé de choisir le fichier d'entrée sur lequel se baser :
```shell
py Visualiseur/main.py 
```
## Les touches 

`R` : Permet l'affichage du quadrillage de la carte
`T` : Permet l'affichage des cibles
`Y` : Permet l'affichage des vents de la carte
`P` : Permet de lancer/arrêter l'animation des ballons
`->` : La flèche de droite permet d'augmenter d'une altitude. (Met à jour les vents de la carte)
`<-` : La flèche de gauche permet de diminuer d'une altitude. (Met à jour les vents de la carte)
`M` : Pour augmenter le nombre de FPS (Image par secondes) / Augmente la vitesse de l'animation
`L` : Pour diminuer le nombre de FPS (Image par secondes) / Réduit la vitesse de l'animation

Il est aussi possible de zoomer la carte avec `+` et `-` et se déplacer avec les touches `zqsd`

Lors d'un clique gauche sur la carte, la position de la souris est enregistrée. Lorsque que vous quittez le visualiseur, la liste des cliques sera affichées dans la console.