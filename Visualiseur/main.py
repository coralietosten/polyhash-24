import pygame
import os, sys
from os.path import dirname, join, abspath
#Permet l'import des fichiers présent dans dans la racine du projet
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from DAOFichier import * 
from Ballon import Ballon 
from Polyhash import *
from Vecteur3 import *
import pickle
import math
import time


GREY = (88,84,100)
GREEN = (8,188,100)
YELLOW = (255,244,204)
chemin_entree = ""
chemin_sauvegarde = ""
if len(sys.argv) - 1 > 2 :
        print("Attention : Il y a trop de paramètres !")
        print("""Construction de la commande : 
                py Visualiseur/main.py chemin/fichier_entree.txt chemin/fichier_Sauvegarde
              OU
                py Visualiseur/main.py chemin/fichier_entree.txt
              OU
                py Visualiseur/main.py 
              """)
else:
    if len(sys.argv) - 1 == 0 :
        print("Aucun paramètre n'a été précisé")
        for i,file_name in enumerate(os.listdir("data/")):
            print(f"{i} - {file_name}")
        a = input("Entrer le numéro du fichier de donnée que vous souhaitez utiliser :")
        try:
            a = int(a)
            file = os.listdir("data/")[a]
            chemin_entree = "data/"+file
            chemin_sauvegarde = "SauvegardeAleatoire/"+file.split(".in")[0]
            
        except:
            long = len(os.listdir("data/"))-1
            print(f"Attention, la réponse attendu est un nombre entier compris entre 0 et {long}")
    elif len(sys.argv) - 1 == 1:
        chemin_entree = sys.argv[1]
    else:  
        chemin_entree = sys.argv[1]
        chemin_sauvegarde = sys.argv[2]

DAO = DAOFichier
polyhash = DAO.donne_polyhash(chemin_entree)
pygame.font.init()
my_font = pygame.font.SysFont(pygame.font.get_default_font(), 20)

max_game = []
if os.path.exists(chemin_sauvegarde):
    with open(chemin_sauvegarde, 'rb') as f:
        max_game = pickle.load(f)
        max_game = max_game[1]

#Fonction qui permet d'afficher sur une surface 
#le quadrillage associé au nombre de lignes et de colonnes
def quadrillage(surface : pygame.Surface,nb_rows,nb_colons,zoom=1,offset=Vecteur2(0,0)):
    w=surface.get_width()
    h=surface.get_height()
    case_w = (w / nb_colons) * zoom
    case_h = (h / nb_rows) * zoom
    for i in range(0,nb_colons):
        line_w=1
        if i + offset.x == 0:
            line_w = 20
        pygame.draw.line(surface,'black',(i*case_w,0),(i*case_w,h),line_w)

    for i in range(0,nb_rows):
        line_w=1
        if i + offset.y == 0:
            line_w = 20
        pygame.draw.line(surface,'black',(0,i*case_h),(w,i*case_h),line_w)

#Fonction récupéré par un developpeur externe, qui affiche une flèche
def draw_arrow(
        surface: pygame.Surface,
        start: pygame.Vector2,
        end: pygame.Vector2,
        color: pygame.Color,
        body_width: int = 2,
        head_width: int = 4,
        head_height: int = 2,
    ):
    """Affiche une flèche entre start et end ayant la tête de la flêche comme fin.  

    Args:
        surface (pygame.Surface):  Surface qu'utilisera la fonction pour afficher les vents
        start (pygame.Vector2): Position de départ
        end (pygame.Vector2): Position d'arrivée
        color (pygame.Color): Couleur de la flèche
        body_width (int, optional): Épaisseur du trait
        head_width (int, optional): Épaisseur de la tête de la flêche
        head_height (float, optional): Taille de la flêche
    """
    body_width: int = 2
    head_width: int = 15
    head_height: int = 25
    arrow = start - end
    angle = arrow.angle_to(pygame.Vector2(0, -1))
    body_length = arrow.length() - head_height

    # Create the triangle head around the origin
    head_verts = [
        pygame.Vector2(0, head_height / 2),  # Center
        pygame.Vector2(head_width / 2, -head_height / 2),  # Bottomright
        pygame.Vector2(-head_width / 2, -head_height / 2),  # Bottomleft
    ]
    # Rotate and translate the head into place
    translation = pygame.Vector2(0, arrow.length() - (head_height / 2)).rotate(-angle)
    for i in range(len(head_verts)):
        head_verts[i].rotate_ip(-angle)
        head_verts[i] += translation
        head_verts[i] += start

    pygame.draw.polygon(surface, color, head_verts)

    # Stop weird shapes when the arrow is shorter than arrow head
    if arrow.length() >= head_height:
        # Calculate the body rect, rotate and translate into place
        body_verts = [
            pygame.Vector2(-body_width / 2, body_length / 2),  # Topleft
            pygame.Vector2(body_width / 2, body_length / 2),  # Topright
            pygame.Vector2(body_width / 2, -body_length / 2),  # Bottomright
            pygame.Vector2(-body_width / 2, -body_length / 2),  # Bottomleft
        ]
        translation = pygame.Vector2(0, body_length / 2).rotate(-angle)
        for i in range(len(body_verts)):
            body_verts[i].rotate_ip(-angle)
            body_verts[i] += translation
            body_verts[i] += start

        pygame.draw.polygon(surface, color, body_verts)



#Cette fonction nous fait apparaître des flèches pour informer de
#la direction des vents
def draw_wind(surface : pygame.Surface,polyhash,num_altitude=0,zoom=1,offset=Vecteur2(0,0)):
    """
    entrées : 
        - surface : Surface qu'utilisera la fonction pour afficher les vents
        - polyhash : Classe où sont stockées toutes les données du fichier d'entrée
        - num_altitude : Numéro de l'altitude à afficher
        - zoom : Facteur de zoom de la map
        - offset : Un Vecteur2 définissant le déplacement sur la map
    """
    nb_rows, nb_colons, map = (polyhash.lignes,polyhash.colonnes,polyhash.carte_vent)

    w=surface.get_width()
    h=surface.get_height()
    case_w = (w / nb_colons) * zoom
    case_h = (h / nb_rows) * zoom
    red_arrow = None
    for j in range(nb_rows-zoom):
        for i in range(nb_colons-zoom):
            row = j
            colon = i
            wind = map[num_altitude][row+offset.y][colon+offset.x]
            wind_x,wind_y = wind.x,wind.y
            #Si le vent est null on passe à la case suivante
            if wind_x == 0 and wind_y == 0:
                continue
            current_case = Vecteur2(colon,row)
            case_end= current_case + wind
            case_end.x = case_end.x % nb_colons

            color = 'grey'
            if (pygame.mouse.get_pos()[0] >= case_w*colon and pygame.mouse.get_pos()[0] < case_w*(colon+1)) and (pygame.mouse.get_pos()[1] >= case_h*row and pygame.mouse.get_pos()[1] < case_h*(row+1)) :
                red_arrow = (pygame.Vector2(case_w*colon+case_w/2,case_h*row+case_h/2),pygame.Vector2(case_w*case_end.x+case_w/2,case_h*case_end.y+case_h/2))
            if wind_y + row + offset.y < 0 or wind_y + row+ offset.y >= nb_rows:
                pygame.draw.rect(surface,pygame.Color(173,173,173,0),(colon*case_w,row*case_h,case_w,case_h))
            
            draw_arrow(surface,pygame.Vector2(case_w*colon+case_w/2,case_h*row+case_h/2),pygame.Vector2(case_w*(1/2+case_end.x),case_h*(1/2+case_end.y)),color,head_width=40,head_height=60)
    if red_arrow != None : 
        draw_arrow(surface,red_arrow[0],red_arrow[1],'red',head_width=40,head_height=60)

#Cette fonction nous affiche les différentes cibles de la carte
def draw_goals(surface,polyhash,zoom=1,offset=Vecteur2(0,0)):
    """
    entrées : 
        - surface : Surface qu'utilisera la fonction pour afficher les balises
        - polyhash : Classe où sont stockées toutes les données du fichier d'entrée
        - zoom : Facteur de zoom de la map
        - offset : Un Vecteur2 définissant le déplacement sur la map
    """
    w=surface.get_width()
    h=surface.get_height()
    case_w = (w / nb_colons) * zoom
    case_h = (h / nb_rows) * zoom
    for goal in polyhash.cibles:
        x,y =((int(goal.coord.x)-offset.x)%nb_colons+0.5,(int(goal.coord.y)-offset.y)%nb_rows+0.5 )        
        pygame.draw.polygon(screen, GREEN, (((x-0.3)*case_w, ((y+0.3)*case_h)),(x*case_w, (y-0.3)*case_h),((x+0.3)*case_w,(y+0.3)*case_h)))

#Cette fonction nous affiche les différents ballons présent sur la carte
def draw_balloon(surface,polyhash,zoom=1,offset=Vecteur2(0,0),ballons=[]):
    """
    entrées : 
        - surface : Surface qu'utilisera la fonction pour afficher les ballons
        - polyhash : Classe où sont stockées toutes les données du fichier d'entrée
        - zoom : Facteur de zoom de la map
        - offset : Un Vecteur2 définissant le déplacement sur la map
        - ballons : Liste des différentes instances des ballons
    """
    w=surface.get_width()
    h=surface.get_height()
    case_w = (w / nb_colons) * zoom
    case_h = (h / nb_rows) * zoom
    i = 0
    for balloon in ballons:
        if not balloon.estSortie:
            x,y =((int(balloon.coord.x)-offset.x)%nb_colons+0.5,(int(balloon.coord.y)-offset.y)%nb_rows+0.5 )
            pygame.draw.ellipse(screen, GREY, ((x-0.5)*case_w, (y-0.5)*case_h, case_w, case_h))
            text_surface = my_font.render(f'B{i}', True, (0, 0, 0))
            screen.blit(text_surface, dest=(x*case_w,(y-1)*case_h))
        i+=1

#Met à jour la position de chaque ballon dans la simulation
def updateBalloon(polyhash : Polyhash,tour=0,ballons=[],game=[]):
    """
    entrées : 
        - polyhash : Classe où sont stockées toutes les données du fichier d'entrée
        - tour : Le numéro du tour actuel
        - ballons : Liste des différentes instances des ballons
        - game = Liste des actions effectué
    """
    i=0
    if len(game)>1:
        for b in ballons:
            b.coord.z += game[tour][i]
            if b.coord.z >= 0 and b.coord.z < polyhash.altitudes and not b.estSortie:
                vent = polyhash.carte_vent[b.coord.z][b.coord.y][b.coord.x]
                b.coord += Vecteur3(vent.x,vent.y,0)
                b.coord.x %= polyhash.colonnes
                if b.coord.y < 0 or b.coord.y >= polyhash.lignes : 
                    b.estSortie = True
            i+=1

#Calcul d'un cercle de rayon V
def coocercle(v:int) -> list[(int,int)] :
        """
        entrée: le rayon v 
        sortie: la liste des coordonnées proche de (0,0) à une distance de v
        """
        liste_touche =[]
        for x in range(-v,v+1):
            for y in range(-v,v+1):
                if (x**2 + y**2) <= v**2:
                    liste_touche.append((x,y))
        return liste_touche

#Affiche la zone de couvrage sur chaque ballon
def draw_radius_balloon(surface,polyhash:Polyhash,ballons,zoom,offset):
    """
    entrées : 
        - surface : Surface qu'utilisera la fonction pour afficher les rayons des ballons
        - polyhash : Classe où sont stockées toutes les données du fichier d'entrée
        - ballons : Liste des différentes instances des ballons
        - zoom : Facteur de zoom de la map
        - offset : Un Vecteur2 définissant le déplacement sur la map
    """
    w=surface.get_width()
    h=surface.get_height()
    case_w = (w / nb_colons) * zoom
    case_h = (h / nb_rows) * zoom
    coords = coocercle(polyhash.rayon_couverture)
    for ballon in ballons:
        for coord in coords:
            coord = Vecteur2(coord[0],coord[1])
            coord += ballon.coord
            pygame.draw.rect(surface,YELLOW,pygame.rect.Rect(((int(coord.x)-offset.x)%nb_colons)*case_w,((int(coord.y)-offset.y))*case_h,case_w,case_h))

nb_rows, nb_colons, nb_altitudes, map = (polyhash.lignes,polyhash.colonnes,polyhash.altitudes,polyhash.carte_vent)

# pygame setup
pygame.init()
screen_w,screen_h = 1280, 720
screen = pygame.display.set_mode((screen_w, screen_h))
clock = pygame.time.Clock()
running = True
etage = 0

display_quadrillage = False
display_actors = True
display_wind = False
balloonIsPlaying = False

#Initialisation
zoom = 1
offset = Vecteur2(0,0)
ballons = []
for i in range(polyhash.nombre_ballons):
    ballons.append(Ballon(Vecteur3(polyhash.depart.x,polyhash.depart.y,-1),i))
tour = 1

fps = 60
#Variable qui stock les positions des clicks souris
positions = []
while running:
    keys = pygame.key.get_pressed()

    # Permet de gérer la fermeture de la fenêtre et l'appuie des différentes touches
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            print("Positions des clicks souris : ",positions)
        if event.type ==  pygame.MOUSEBUTTONDOWN:
            w=screen.get_width()
            h=screen.get_height()
            case_w = (w / nb_colons) * zoom
            case_h = (h / nb_rows) * zoom
            a = pygame.mouse.get_pos()
            positions.append((a[0]//case_w,a[1]//case_h))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                etage = (etage - 1) % nb_altitudes
            if event.key == pygame.K_RIGHT:
                etage = (etage + 1) % nb_altitudes
            #DISPLAY
            if event.key == pygame.K_r:
                display_quadrillage = not display_quadrillage
            if event.key == pygame.K_t:
                display_actors = not display_actors
            if event.key == pygame.K_y:
                display_wind = not display_wind

            #Zoom map
            if event.key == pygame.K_KP_PLUS:
                if zoom + 1 < nb_colons and zoom + 1 < nb_rows:
                    zoom +=1
            if event.key == pygame.K_KP_MINUS:
                if zoom  > 1:
                    zoom -=1
                    offset.x,offset.y = (0,0)

            if event.key == pygame.K_p:
                balloonIsPlaying = not balloonIsPlaying
            if event.key == pygame.K_m:
                if fps>=10:
                    fps += 10
                else:
                    fps += 1
            if event.key == pygame.K_l:
                if fps>10:
                    fps -= 10
                else:
                    if fps >1:
                        fps-=1 


    #Se déplacer sur la carte zoomée
    if keys[pygame.K_z]:
        #UP
        if nb_rows//zoom +  offset.y>0 and offset.y>0:
            offset.y -=1

    if keys[pygame.K_s]:
        #DOWN
        if nb_rows//zoom +  offset.y<nb_rows:
            offset.y +=1

    if keys[pygame.K_q]:
        #LEFT
        if nb_colons-zoom + offset.x>0:
            offset.x -=1
    if keys[pygame.K_d]:
        #RIGHT
        if nb_colons-zoom + offset.x<nb_colons:
            offset.x +=1

            


    screen.fill((255,255,255))
    draw_radius_balloon(screen,polyhash,ballons,zoom,offset)
    

    if display_wind:
        draw_wind(screen,polyhash,etage,zoom,offset)
    if display_actors:
        draw_goals(screen,polyhash,zoom,offset)
    # Rendu de l'affichage
    if display_quadrillage:
        quadrillage(screen,nb_rows,nb_colons,zoom,offset)
    
    draw_balloon(screen, polyhash, zoom, offset,ballons)
    text_surface = my_font.render(f'Alt : {etage} Tour : {tour} FPS : {fps}', True, (0, 0, 0))
    screen.blit(text_surface, dest=(20,20))
    #Actualise l'affichage
    pygame.display.flip()

    #Anime les ballons
    if balloonIsPlaying:
        tour+=1
        if tour >= polyhash.nombre_tours : 
            ballons = []
            for i in range(polyhash.nombre_ballons):
                ballons.append(Ballon(Vecteur3(polyhash.depart.x,polyhash.depart.y,-1),i))
            tour = 1
        updateBalloon(polyhash,tour,ballons,max_game)

    clock.tick(fps)  # Limite à 60 images par secondes
    
pygame.quit()