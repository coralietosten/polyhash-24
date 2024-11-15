import pygame
import os, sys
from os.path import dirname, join, abspath
#Permet l'import des fichiers présent dans dans la racine du projet
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from DAOFichier import * 
from Ballon import Ballon 


files = ["data/a_example.in","data/b_small.in","data/c_medium.in","data/d_final.in"]
DAO = DAOFichier
polyhash = DAO.donne_polyhash(files[0])


#Fonction qui permet d'afficher sur une surface 
#le cadrillage associé au nombre de lignes et de colonnes
def cadrillage(surface : pygame.Surface,nb_rows,nb_colons,zoom=0,offset=Vecteur2(0,0)):
    w=surface.get_width()
    h=surface.get_height()
    case_w = w/(nb_colons-zoom)
    case_h = h/(nb_rows-zoom)
    for i in range(0,nb_colons-zoom):
        line_w=1
        if i + offset.x == 0:
            line_w = 20
        pygame.draw.line(surface,'black',(i*case_w,0),(i*case_w,h),line_w)

    for i in range(0,nb_rows-zoom):
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



#Cette fonction nous fait apparaître des flêches pour informer de
#la direction des vents
def draw_wind(surface : pygame.Surface,polyhash,num_altitude=0,zoom=0,offset=Vecteur2(0,0)):
    nb_rows, nb_colons, map = (polyhash.lignes,polyhash.colonnes,polyhash.carte_vent)

    w=surface.get_width()
    h=surface.get_height()
    case_w = w/(nb_colons-zoom)
    case_h = h/(nb_rows-zoom)
    red_arrow = None
    for j in range(nb_rows-zoom):
        for i in range(nb_colons-zoom):
            row = j
            colon = i
            wind = map[num_altitude][row+offset.y][colon+offset.x]
            wind_x,wind_y = wind.x,wind.y
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
            
            # if wind_x + colon <= 0:--
                # draw_arrow(surface,pygame.Vector2(case_w*colon+case_w/2,case_h*row+case_h/2),pygame.Vector2(case_w*case_end.x+case_w/2,case_end.y*case_h+case_h/2),color,head_width=40,head_height=60)
                    
            # if wind_x+colon >= nb_colons :
                # case_end = (wind_x + colon)%nb_colons
                # draw_arrow(surface,pygame.Vector2(case_w/2,case_h*row+case_h/2),pygame.Vector2(case_w*(case_end.x-1/2),case_end.y*case_h),color,head_width=40,head_height=60)
            draw_arrow(surface,pygame.Vector2(case_w*colon+case_w/2,case_h*row+case_h/2),pygame.Vector2(case_w*(1/2+case_end.x),case_h*(1/2+case_end.y)),color,head_width=40,head_height=60)
    if red_arrow != None : 
        draw_arrow(surface,red_arrow[0],red_arrow[1],'red',head_width=40,head_height=60)

def draw_goals(surface,polyhash,zoom=0,offset=Vecteur2(0,0)):
    w=surface.get_width()
    h=surface.get_height()
    case_w = w/(nb_colons-zoom)
    case_h = h/(nb_rows-zoom)
    for goal in polyhash.cibles:
        x,y =((int(goal.coord.x)-offset.x)%nb_colons+0.5,(int(goal.coord.y)-offset.y)%nb_rows+0.5 )
        pygame.draw.polygon(screen, "orange", (((x-0.3)*case_w, ((y+0.3)*case_h)),(x*case_w, (y-0.3)*case_h),((x+0.3)*case_w,(y+0.3)*case_h)))

def draw_balloon(surface,polyhash,zoom=0,offset=Vecteur2(0,0)):
    w=surface.get_width()
    h=surface.get_height()
    case_w = w/(nb_colons-zoom)
    case_h = h/(nb_rows-zoom)
    balloon = Ballon(polyhash.depart)
    x,y =((int(balloon.coord.x)-offset.x)%nb_colons+0.5,(int(balloon.coord.y)-offset.y)%nb_rows+0.5 )
    pygame.draw.ellipse(screen, "red", ((x-0.12)*case_w, (y-0.2)*case_h, case_w/3, case_h/2))


nb_rows, nb_colons, nb_altitudes, map = (polyhash.lignes,polyhash.colonnes,polyhash.altitudes,polyhash.carte_vent)
print(map)
# pygame setup
pygame.init()
screen_w,screen_h = 1280, 720
screen = pygame.display.set_mode((screen_w, screen_h))
clock = pygame.time.Clock()
running = True
etage = 0

display_cadrillage = True
display_actors = True
display_wind = True

zoom = 0
offset = Vecteur2(0,0)
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
            #DISPLAY
            if event.key == pygame.K_r:
                display_cadrillage = not display_cadrillage
            if event.key == pygame.K_t:
                display_actors = not display_actors
            if event.key == pygame.K_y:
                display_wind = not display_wind

            #Zoom map
            if event.key == pygame.K_KP_PLUS:
                if zoom + 1 < nb_colons and zoom + 1 < nb_rows:
                    zoom +=1
            if event.key == pygame.K_KP_MINUS:
                if zoom  > 0:
                    zoom -=1
                    offset.x,offset.y = (0,0)
                    # offset.y %= nb_rows-zoom
                    # offset.x %= nb_colons-zoom

        if event.type == pygame.KEYDOWN:

            #Move into the zoomed map
            if event.key == pygame.K_z:
                #UP
                if nb_rows-zoom +  offset.y>0 and offset.y>0:
                    offset.y -=1

            if event.key == pygame.K_s:
                #DOWN
                if nb_rows-zoom +  offset.y<nb_rows:
                    offset.y +=1

            if event.key == pygame.K_q:
                #LEFT
                if nb_colons-zoom + offset.x>0:
                    offset.x -=1
            if event.key == pygame.K_d:
                #RIGHT
                if nb_colons-zoom + offset.x<nb_colons:
                    offset.x +=1

            if event.key == pygame.K_p:
                print(zoom)
                print(offset)

            
            

    screen.fill("light blue")

    if display_wind:
        draw_wind(screen,polyhash,etage,zoom,offset)
    if display_actors:
        draw_goals(screen,polyhash,zoom,offset)
    # Rendu de l'affichage
    if display_cadrillage:
        cadrillage(screen,nb_rows,nb_colons,zoom,offset)
    draw_balloon(screen, polyhash, zoom, offset)
    #Actualise l'affichage
    pygame.display.flip()

    clock.tick(60)  # Limite à 60 images par secondes
pygame.quit()