import pygame
import os, sys
from os.path import dirname, join, abspath
#Permet l'import des fichiers présent dans dans la racine du projet
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from DAOFichier import * 


DAO = DAOFichier
polyshash = DAO.donne_polyhash('data/a_example.in')#sys.argv[1])



#Fonction qui permet d'afficher sur une surface 
#le cadrillage associé au nombre de lignes et de colonnes
def cadrillage(surface : pygame.Surface,nb_rows,nb_colons):
    w=surface.get_width()
    h=surface.get_height()
    case_w = w/nb_colons
    case_h = h/nb_rows
    for i in range(1,nb_colons):
        pygame.draw.line(surface,'black',(i*case_w,0),(i*case_w,h))

    for i in range(1,nb_rows):
        pygame.draw.line(surface,'black',(0,i*case_h),(w,i*case_h))

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
    """Draw an arrow between start and end with the arrow head at the end.

    Args:
        surface (pygame.Surface): The surface to draw on
        start (pygame.Vector2): Start position
        end (pygame.Vector2): End position
        color (pygame.Color): Color of the arrow
        body_width (int, optional): Defaults to 2.
        head_width (int, optional): Defaults to 4.
        head_height (float, optional): Defaults to 2.
    """
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



#Cette fonction nous fait apparaître des flêches pour informer de
#la direction des vents
def draw_wind(surface : pygame.Surface,map,nb_rows,nb_colons,num_altitude=0):
    w=surface.get_width()
    h=surface.get_height()
    case_w = w/nb_colons
    case_h = h/nb_rows
    red_arrow = None
    for row in range(nb_rows):
        for colon in range(nb_colons):
            wind = map[num_altitude][row][colon]
            wind_x,wind_y = wind.x,wind.y
            if wind_x == 0 and wind_y == 0:
                continue
            current_case = Vecteur2(colon,row)
            case_end= current_case + wind
            case_end.x = case_end.x % nb_colons

            color = 'grey'
            if (pygame.mouse.get_pos()[0] >= case_w*colon and pygame.mouse.get_pos()[0] < case_w*(colon+1)) and (pygame.mouse.get_pos()[1] >= case_h*row and pygame.mouse.get_pos()[1] < case_h*(row+1)) :
                red_arrow = (pygame.Vector2(case_w*colon+case_w/2,case_h*row+case_h/2),pygame.Vector2(case_w*case_end.x+case_w/2,case_h*case_end.y+case_h/2))
            if wind_x + colon <= 0:
                draw_arrow(surface,pygame.Vector2(case_w*colon+case_w/2,case_h*row+case_h/2),pygame.Vector2(case_w*case_end.x+case_w/2,case_end.y*case_h+case_h/2),color,head_width=40,head_height=60)
                    
            if wind_x+colon >= nb_colons :
                # case_end = (wind_x + colon)%nb_colons
                draw_arrow(surface,pygame.Vector2(case_w/2,case_h*row+case_h/2),pygame.Vector2(case_w*(case_end.x-1/2),case_end.y*case_h),color,head_width=40,head_height=60)
            draw_arrow(surface,pygame.Vector2(case_w*colon+case_w/2,case_h*row+case_h/2),pygame.Vector2(case_w*(1/2+case_end.x),case_h*(1/2+case_end.y)),color,head_width=40,head_height=60)
    if red_arrow != None : 
        draw_arrow(surface,red_arrow[0],red_arrow[1],'red',head_width=40,head_height=60)



nb_rows, nb_colons, nb_altitudes, map = (polyshash.lignes,polyshash.colonnes,polyshash.altitudes,polyshash.carte_vent)

# pygame setup
pygame.init()
screen_w,screen_h = 1280, 720
screen = pygame.display.set_mode((screen_w, screen_h))
clock = pygame.time.Clock()
running = True
etage = 0

while running:
    # Permet de gérer la fermeture de la fenêtre et l'appuie des différentes touches
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                etage = (etage + 1) % nb_altitudes
            if event.key == pygame.K_RIGHT:
                etage = (etage - 1) % nb_altitudes

    screen.fill("light blue")

    # Rendu de l'affichage
    cadrillage(screen,nb_rows,nb_colons)
    draw_wind(screen,map,nb_rows,nb_colons,etage)

    #Actualise l'affichage
    pygame.display.flip()

    clock.tick(60)  # Limite à 60 images par secondes
pygame.quit()