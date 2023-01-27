try:
    import pygame_sdl2
    pygame_sdl2.import_as_pygame() 
except ImportError: 
        pass 
    
import pygame
  
noir = (0,0,0)
blanc = (255,255,255)
blue = (0,0,255)
vert = (0,255,0)
rouge = (255,0,0)
violet = (255,0,255)
jaune = ( 255, 255,0)

Iicon = pygame.image.load('pacmanicon.png')
pygame.display.set_icon(Iicon)

# Ajout de musique

pygame.mixer.init()
pygame.mixer.music.load('pacman.mp3')
pygame.mixer.music.play(-1, 0.0)

# Cette classe représente la barre en bas que le joueur contrôle

class Wall(pygame.sprite.Sprite):
    # Fonction Constructeur
    
    def __init__(self,x,y,width,height, color):
        # Apelle le constructeur du parent
        
        pygame.sprite.Sprite.__init__(self)
   
        # Fait un mur bleu, de la taille spécifiée dans les paramètres
        
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
  
        # Fait de notre coin supérieur gauche l'emplacement de passage.
        
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x

# Cela crée tous les murs de la pièce 1

def setupRoomOne(all_sprites_list):
    # Fait les murs. (x_pos, y_pos, width, height)
    
    wall_list=pygame.sprite.RenderPlain()
     
    # Ceci est une liste de murs. Chacun est sous la forme [x, y, width, height]
    
    walls = [ [0,0,6,600],
              [0,0,600,6],
              [0,600,606,6],
              [600,0,6,606],
              [300,0,6,66],
              [60,60,186,6],
              [360,60,186,6],
              [60,120,66,6],
              [60,120,6,126],
              [180,120,246,6],
              [300,120,6,66],
              [480,120,66,6],
              [540,120,6,126],
              [120,180,126,6],
              [120,180,6,126],
              [360,180,126,6],
              [480,180,6,126],
              [180,240,6,126],
              [180,360,246,6],
              [420,240,6,126],
              [240,240,42,6],
              [324,240,42,6],
              [240,240,6,66],
              [240,300,126,6],
              [360,240,6,66],
              [0,300,66,6],
              [540,300,66,6],
              [60,360,66,6],
              [60,360,6,186],
              [480,360,66,6],
              [540,360,6,186],
              [120,420,366,6],
              [120,420,6,66],
              [480,420,6,66],
              [180,480,246,6],
              [300,480,6,66],
              [120,540,126,6],
              [360,540,126,6]
            ]
     
    # Fait une boucle dans la liste. Créer le mur, l'ajoute à la liste
    
    for item in walls:
        wall=Wall(item[0],item[1],item[2],item[3],blue)
        wall_list.add(wall)
        all_sprites_list.add(wall)
         
    # retourne notre nouvelle liste
    
    return wall_list
 
def setupGate(all_sprites_list):
      gate = pygame.sprite.RenderPlain()
      gate.add(Wall(282,242,42,2,blanc))
      all_sprites_list.add(gate)
      return gate

# Cette classe représente la boule  
      
# Elle dérive de la classe "Sprite" de Pygame

class Block(pygame.sprite.Sprite):
     
    # Constructeur. Passe dans la couleur du bloc,
    # et sa position x et y
    
    def __init__(self, color, width, height):
        # Appele le constructeur de la classe parent (Sprite)
        
        pygame.sprite.Sprite.__init__(self) 
 
        # Créer une image du bloc et la remplie d'une couleur.
        # Il peut également s'agir d'une image chargée à partir du disque.
        
        self.image = pygame.Surface([width, height])
        self.image.fill(blanc)
        self.image.set_colorkey(blanc)
        pygame.draw.ellipse(self.image,color,[0,0,width,height])
 
        # Récupére l'objet rectangle qui a les dimensions de l'image
        # image.
        # Met à jour la position de cet objet en définissant les valeurs
        # de rect.x et rect.y
        
        self.rect = self.image.get_rect() 

# Cette classe représente la barre en bas que le joueur contrôle

class Joueur(pygame.sprite.Sprite):
  
    # Définit le vecteur de vitesse
    
    change_x=0
    change_y=0
  
    # Fonction constructeur
    
    def __init__(self,x,y, filename):
        # Appele le constructeur du parent
        
        pygame.sprite.Sprite.__init__(self)
   
        # Set height, width
        self.image = pygame.image.load(filename).convert()
  
        # Fait de notre coin supérieur gauche l'emplacement de passage.
        
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.prev_x = x
        self.prev_y = y

    # Efface la vitesse du joueur
    
    def prevdirection(self):
        self.prev_x = self.change_x
        self.prev_y = self.change_y

    # Change la vitesse du joueur
    
    def changespeed(self,x,y):
        self.change_x+=x
        self.change_y+=y
          
    # Trouve une nouvelle position pour le joueur
    
    def update(self,walls,gate):
        # Obtien l'ancienne position, au cas où nous aurions besoin d'y revenir
        
        old_x=self.rect.left
        new_x=old_x+self.change_x
        prev_x=old_x+self.prev_x
        self.rect.left = new_x
        
        old_y=self.rect.top
        new_y=old_y+self.change_y
        prev_y=old_y+self.prev_y

        x_collide = pygame.sprite.spritecollide(self, walls, False)
        if x_collide:
            # Oups, je heurte un mur. Revenir à l'ancienne position
            self.rect.left=old_x
            # self.rect.top=prev_y
            # y_collide = pygame.sprite.spritecollide(self, walls, False)
            # if y_collide:
            #     # Oups, je heurte un mur. Revenir à l'ancienne position
            #     self.rect.top=old_y
            #     print('a')
        else:

            self.rect.top = new_y

            
            y_collide = pygame.sprite.spritecollide(self, walls, False)
            if y_collide:
                # Oups, je heurte un mur. Revenir à l'ancienne position
                self.rect.top=old_y
                # self.rect.left=prev_x
                # x_collide = pygame.sprite.spritecollide(self, walls, False)
                # if x_collide:
                #     # Oups, je heurte un mur. Revenir à l'ancienne position
                #     self.rect.left=old_x
                #     print('b')

        if gate != False:
          gate_hit = pygame.sprite.spritecollide(self, gate, False)
          if gate_hit:
            self.rect.left=old_x
            self.rect.top=old_y


class fantome(Joueur):
    # Change la vitesse des fantomes
    
    def changespeed(self,list,ghost,turn,steps,l):
      try:
        z=list[turn][2]
        if steps < z:
          self.change_x=list[turn][0]
          self.change_y=list[turn][1]
          steps+=1
        else:
          if turn < l:
            turn+=1
          elif ghost == "clyde":
            turn = 2
          else:
            turn = 0
          self.change_x=list[turn][0]
          self.change_y=list[turn][1]
          steps = 0
        return [turn,steps]
      except IndexError:
         return [0,0]

Pinky_directions = [
[0,-30,4],
[15,0,9],
[0,15,11],
[-15,0,23],
[0,15,7],
[15,0,3],
[0,-15,3],
[15,0,19],
[0,15,3],
[15,0,3],
[0,15,3],
[15,0,3],
[0,-15,15],
[-15,0,7],
[0,15,3],
[-15,0,19],
[0,-15,11],
[15,0,9]
]

Blinky_directions = [
[0,-15,4],
[15,0,9],
[0,15,11],
[15,0,3],
[0,15,7],
[-15,0,11],
[0,15,3],
[15,0,15],
[0,-15,15],
[15,0,3],
[0,-15,11],
[-15,0,3],
[0,-15,11],
[-15,0,3],
[0,-15,3],
[-15,0,7],
[0,-15,3],
[15,0,15],
[0,15,15],
[-15,0,3],
[0,15,3],
[-15,0,3],
[0,-15,7],
[-15,0,3],
[0,15,7],
[-15,0,11],
[0,-15,7],
[15,0,5]
]

Inky_directions = [
[30,0,2],
[0,-15,4],
[15,0,10],
[0,15,7],
[15,0,3],
[0,-15,3],
[15,0,3],
[0,-15,15],
[-15,0,15],
[0,15,3],
[15,0,15],
[0,15,11],
[-15,0,3],
[0,-15,7],
[-15,0,11],
[0,15,3],
[-15,0,11],
[0,15,7],
[-15,0,3],
[0,-15,3],
[-15,0,3],
[0,-15,15],
[15,0,15],
[0,15,3],
[-15,0,15],
[0,15,11],
[15,0,3],
[0,-15,11],
[15,0,11],
[0,15,3],
[15,0,1],
]

Clyde_directions = [
[-30,0,2],
[0,-15,4],
[15,0,5],
[0,15,7],
[-15,0,11],
[0,-15,7],
[-15,0,3],
[0,15,7],
[-15,0,7],
[0,15,15],
[15,0,15],
[0,-15,3],
[-15,0,11],
[0,-15,7],
[15,0,3],
[0,-15,11],
[15,0,9],
]

pl = len(Pinky_directions)-1
bl = len(Blinky_directions)-1
il = len(Inky_directions)-1
cl = len(Clyde_directions)-1

# Appele cette fonction pour que la bibliothèque Pygame puisse s'initialiser

pygame.init()
  
# Créer un écran de taille 606x606

ecran = pygame.display.set_mode([606, 606])

# Il s'agit d'une liste de "sprites". Chaque bloc du programme est
# ajouté à cette liste. La liste est gérée par une classe appelée "RenderPlain".


# Définit le titre de la fenêtre

pygame.display.set_caption('Pacman')

# Créer une surface sur laquelle nous pouvons dessiner

Fondd = pygame.Surface(ecran.get_size())

# Utilisé pour convertir des cartes de couleurs et autres

Fondd = Fondd.convert()
  
# Remplit l'écran avec un fond noir

Fondd.fill(noir)



horloge = pygame.time.Clock()

pygame.font.init()
font = pygame.font.Font("freesansbold.ttf", 24)

# emplacements par défaut pour Pacman et les monstres

w = 303-16 #Width
p_h = (7*60)+19 #Pacman taille
m_h = (4*60)+19 #Monstre taille
b_h = (3*60)+19 #Binky hauteur
i_w = 303-16-32 #Inky largeur
c_w = 303+(32-16) #Clyde largeur

def startGame():

  all_sprites_list = pygame.sprite.RenderPlain()

  block_list = pygame.sprite.RenderPlain()

  monsta_list = pygame.sprite.RenderPlain()

  pacman_collide = pygame.sprite.RenderPlain()

  wall_list = setupRoomOne(all_sprites_list)

  gate = setupGate(all_sprites_list)


  p_turn = 0
  p_steps = 0

  b_turn = 0
  b_steps = 0

  i_turn = 0
  i_steps = 0

  c_turn = 0
  c_steps = 0


  # Aspect graphique des personnages
  
  Pacman = Joueur( w, p_h, "images/Trollman.png" )
  all_sprites_list.add(Pacman)
  pacman_collide.add(Pacman)
   
  Blinky = fantome ( w, b_h, "images/Blinky.png" )
  monsta_list.add(Blinky)
  all_sprites_list.add(Blinky)

  Pinky = fantome ( w, m_h, "images/Pinky.png" )
  monsta_list.add(Pinky)
  all_sprites_list.add(Pinky)
   
  Inky = fantome ( i_w, m_h, "images/Inky.png" )
  monsta_list.add(Inky)
  all_sprites_list.add(Inky)
   
  Clyde = fantome ( c_w, m_h, "images/Clyde.png" )
  monsta_list.add(Clyde)
  all_sprites_list.add(Clyde)

  # Dessine la grille
  
  for row in range(19):
      for column in range(19):
          if (row == 7 or row == 8) and (column == 8 or column == 9 or column == 10):
              continue
          else:
            block = Block(jaune, 4, 4)

            # Définit un emplacement aléatoire pour le bloc
            
            block.rect.x = (30*column+6)+26
            block.rect.y = (30*row+6)+26

            b_collide = pygame.sprite.spritecollide(block, wall_list, False)
            p_collide = pygame.sprite.spritecollide(block, pacman_collide, False)
            if b_collide:
              continue
            elif p_collide:
              continue
            else:
              # Ajoute le bloc à la liste des objets
              
              block_list.add(block)
              all_sprites_list.add(block)

  bll = len(block_list)

  score = 0

  fait = False

  i = 0

  while fait == False:
      
      # Association des touches pour jouer
      
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              fait = True

          if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_LEFT:
                  Pacman.changespeed(-30,0)
              if event.key == pygame.K_RIGHT:
                  Pacman.changespeed(30,0)
              if event.key == pygame.K_UP:
                  Pacman.changespeed(0,-30)
              if event.key == pygame.K_DOWN:
                  Pacman.changespeed(0,30)

          if event.type == pygame.KEYUP:
              if event.key == pygame.K_LEFT:
                  Pacman.changespeed(30,0)
              if event.key == pygame.K_RIGHT:
                  Pacman.changespeed(-30,0)
              if event.key == pygame.K_UP:
                  Pacman.changespeed(0,30)
              if event.key == pygame.K_DOWN:
                  Pacman.changespeed(0,-30)
          
   
      # TOUTE LA LOGIQUE DU JEU DEVRAIT ALLER EN DESSOUS DE CE COMMENTAIRE
      
      Pacman.update(wall_list,gate)

      returned = Pinky.changespeed(Pinky_directions,False,p_turn,p_steps,pl)
      p_turn = returned[0]
      p_steps = returned[1]
      Pinky.changespeed(Pinky_directions,False,p_turn,p_steps,pl)
      Pinky.update(wall_list,False)

      returned = Blinky.changespeed(Blinky_directions,False,b_turn,b_steps,bl)
      b_turn = returned[0]
      b_steps = returned[1]
      Blinky.changespeed(Blinky_directions,False,b_turn,b_steps,bl)
      Blinky.update(wall_list,False)

      returned = Inky.changespeed(Inky_directions,False,i_turn,i_steps,il)
      i_turn = returned[0]
      i_steps = returned[1]
      Inky.changespeed(Inky_directions,False,i_turn,i_steps,il)
      Inky.update(wall_list,False)

      returned = Clyde.changespeed(Clyde_directions,"clyde",c_turn,c_steps,cl)
      c_turn = returned[0]
      c_steps = returned[1]
      Clyde.changespeed(Clyde_directions,"clyde",c_turn,c_steps,cl)
      Clyde.update(wall_list,False)

      # Voit si le bloc Pacman est entré en collision avec quoi que ce soit.
      
      blocks_hit_list = pygame.sprite.spritecollide(Pacman, block_list, True)
       
      # Check the list of collisions.
      
      if len(blocks_hit_list) > 0:
          score +=len(blocks_hit_list)
      
   
     # TOUT LE DESSIN DOIT PASSER EN DESSOUS DE CE COMMENTAIRE
     
      ecran.fill(noir)
        
      wall_list.draw(ecran)
      gate.draw(ecran)
      all_sprites_list.draw(ecran)
      monsta_list.draw(ecran)

      text=font.render("Score: "+str(score)+"/"+str(bll), True, rouge)
      ecran.blit(text, [10, 10])

      if score == bll:
        doNext("Bravo, tu as gagné !",145,all_sprites_list,block_list,monsta_list,pacman_collide,wall_list,gate)

      monsta_hit_list = pygame.sprite.spritecollide(Pacman, monsta_list, False)

      if monsta_hit_list:
        doNext("Game Over",235,all_sprites_list,block_list,monsta_list,pacman_collide,wall_list,gate)

      pygame.display.flip()
    
      horloge.tick(10)

def doNext(message,left,all_sprites_list,block_list,monsta_list,pacman_collide,wall_list,gate):
  while True:
      # TOUT LE TRAITEMENT D'ÉVÉNEMENT DOIT ALLER EN DESSOUS DE CE COMMENTAIRE
      
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            pygame.quit()
          if event.key == pygame.K_RETURN:
            del all_sprites_list
            del block_list
            del monsta_list
            del pacman_collide
            del wall_list
            del gate
            startGame()

      # Fond gris
      
      w = pygame.Surface((400,200))  # La taille de l'écran
      w.set_alpha(10)                # alpha level
      w.fill((128,128,128))           # Remplit la surface entière
      ecran.blit(w, (100,200))    # (0,0) sont les coordonncoordonnées en haut à gauche

      # Gagne ou perd
      
      text1=font.render(message, True, blanc)
      ecran.blit(text1, [left, 233])

      text2=font.render("Pour rejouer, appuie sur ENTRER.", True, blanc)
      ecran.blit(text2, [100, 303])
      text3=font.render("Pour quitter, appuie sur ESC.", True, blanc)
      ecran.blit(text3, [130, 333])

      pygame.display.flip()

      horloge.tick(10)

startGame()

pygame.quit()
