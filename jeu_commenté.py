# -*-coding:Latin-1 -*


'''




Amusez-vous !


 '''


import time
import pygame
from pygame.locals import *
import copy

pygame.init()  #initialisation de la fenetre pygame



epaisseur = 1024 #on definit l' epaisseur de la fenetre
hauteur = 768 #on definit la hauteur de la fenetre

taille_tuile = 32

epaisseur_grille = epaisseur / taille_tuile
hauteur_grille = hauteur / taille_tuile



clock = pygame.time.Clock() #fps

pygame.key.set_repeat(1,70) #repetitions clavier


pygame.display.set_caption("Python Survival")
fenetre = pygame.display.set_mode((epaisseur, hauteur)) # on fait apparaitre la fenetre du jeu

x = 32
y = 32

speed = 1
tk = 0

position_hero_base_x = 512 #position x du personnage
position_hero_base_y = 384 #position y du personnage

son = pygame.mixer.Sound("music/main.wav")
score = 0

pygame.key.set_repeat(1,50)

accueil = 1
playing = 0
run = 1

fond_jeu = pygame.image.load("images/white.png").convert()  #on definit le fond du jeu

fond_accueil = pygame.image.load("images/image_accueil.jpg").convert() #on definit le fond d'acceuil

font = pygame.font.Font(None, 35)
text = font.render("Appuyez sur une touche pour jouer",1,(255,255,255)) #texte pour lancer le jeu

font_score=pygame.font.Font('vgasys.ttf',30)
font_end =pygame.font.Font('vgasys.ttf', 60)

bullet = pygame.image.load("images/ball.png").convert_alpha() #on definit l'image des balles
vitesse_missile = 0


class Hero(pygame.sprite.Sprite): #
    def __init__(self):
        self.image_face = pygame.image.load("images/bas2.png").convert_alpha()
        self.image_left = pygame.image.load("images/gauche2.png").convert_alpha()
        self.image_right = pygame.image.load("images/droite2.png").convert_alpha()        #defiition du hero
        self.image_back = pygame.image.load("images/haut2.png").convert_alpha()
        self.image = self.image_face
        self.position = pygame.Rect(position_hero_base_x, position_hero_base_y, 32, 32)
        self.life = 3
        self.alive = 1
hero = Hero()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, life):
        self.image_face = pygame.image.load("images/mob_bas2.png").convert_alpha()
        self.image_left = pygame.image.load("images/mob_gauche2.png").convert_alpha()
        self.image_right = pygame.image.load("images/mob_droite2.png").convert_alpha() #definition des ennemis
        self.image_back = pygame.image.load("images/mob_haut2.png").convert_alpha()
        self.image = self.image_face
        self.position = pygame.Rect(x, y, 32, 32)
        self.life = 3
        self.alive = 1

enemy1 = Enemy(100, 100, 5)
enemy2 = Enemy(100, 200, 5)
enemy3 = Enemy(100, 300, 5)

ennemis = [enemy1, enemy2, enemy3]
ennemis_images=[enemy1.image, enemy2.image, enemy3.image]

class Ball(pygame.sprite.Sprite):
    def __init__(self, direction):
        super(Ball, self).__init__()
        self.image = pygame.image.load("images/ball2.png").convert_alpha() #definition balles
        self.position = copy.deepcopy(hero.position)
        self.direction = direction


    def update(self):
        if hero.image == hero.image_back:
            self.position.y -= 3             #mouvement balles
        elif hero.image == hero.image_right:
            self.position.x += 3
        elif hero.image == hero.image_left:
            self.position.x -= 3
        elif hero.image == hero.image_face:
            self.position.y += 3


def texts(score):

   scoretext=font_score.render("Score:"+str(score), 1,(0,0,0)) # texte du score
   fenetre.blit(scoretext, (700, 50)) #on affiche le score


ball_list = pygame.sprite.Group()

#boucle infinie qui represente le programme dans l'ensemble
while run == 1:

    son.play()
     #boucle qui correspond ?l'ecran d'accueil
    while accueil == 1:

        fenetre.blit(fond_accueil, (0,0))

        fenetre.blit(text, (300, 300))

        pygame.display.flip()


        for event in pygame.event.get():

            if event.type == KEYDOWN: #si entrée clavier détectée

                playing = 1 #on lance le jeu et on sort de l'accuei

                accueil = 0


        while playing == 1:

            accueil = 0


            for event in pygame.event.get():        #pour quitter le jeu
                if event.type == QUIT:
                    run = 0
                    playing = 0
                    pygame.display.flip()
                    pygame.quit()
                    exit()

                if event.type == KEYDOWN:           #si il detecte une touche ...


                    if hero.position.colliderect(enemy1.position) or  hero.position.colliderect(enemy2.position) or hero.position.colliderect(enemy3.position): #gestion des collisions entre heros et ennemis
                        hero.life -= 1
                        if hero.image == hero.image_back:
                             hero.position.y = hero.position.y + y
                        elif hero.image == hero.image_right:
                             hero.position.x = hero.position.x - x
                        elif hero.image == hero.image_left:
                             hero.position.x = hero.position.x + x
                        elif hero.image == hero.image_face:
                             hero.position.y = hero.position.y - y


                    else:


                        if event.key == K_ESCAPE:
                            #si  ECHAP appuyé, alors on retourne sur l'ecran d'accueil
                            playing = 0
                            accueil = 1
                            fenetre.blit(fond_accueil, (0,0))
                            pygame.display.flip()

                        if hero.alive == 1:
                            if event.key == K_UP:       #Ici c'est la detection des fleches directionnelles et les
                                #actions associ?s ( mouvement )
                                hero.position.y -=  y
                                hero.image = hero.image_back
                                fenetre.blit(hero.image, hero.position)
                                pygame.display.flip()


                            elif event.key == K_DOWN:
                                hero.image = hero.image_face  #on change l'orientation du bonhomme selon la direction qu'il veut emprunter et on bouge
                                hero.position.y +=  y
                                fenetre.blit(hero.image, hero.position)
                                pygame.display.flip()


                            elif event.key == K_RIGHT:
                                hero.image = hero.image_right #on change l'orientation du bonhomme selon la direction qu'il veut emprunter et on bouge
                                hero.position.x +=  x
                                fenetre.blit(hero.image, hero.position)
                                pygame.display.flip()


                            elif event.key == K_LEFT:
                                hero.image = hero.image_left #on change l'orientation du bonhomme selon la direction qu'il veut emprunter et on bouge
                                hero.position.x -= x
                                fenetre.blit(hero.image, hero.position)
                                pygame.display.flip()


                            if event.key == K_SPACE: # touche pour tirer
                                pygame.key.set_repeat(1, 800)
                                if hero.image == hero.image_back:
                                    ball = Ball('up')
                                    ball.position.y -= 50
                                elif hero.image == hero.image_right:
                                    ball = Ball('right')
                                    ball.position.x += 50
                                elif hero.image == hero.image_left:
                                    ball = Ball('left')
                                    ball.position.x -= 50
                                elif hero.image == hero.image_face:
                                    ball = Ball('down')
                                    ball.position.y += 50
                                ball_list.add(ball)
                                pygame.key.set_repeat(1, 80)




            if hero.position.x < 0:
                hero.position.x = 0

            elif hero.position.x > 1000:
                hero.position.x = 1000

            elif hero.position.y < 0:
                hero.position.y = 0

            elif hero.position.y > 680:
                hero.position.y = 680                         #ici on a interdi a tout les personnages de sortir de l'ecran


            if enemy1.position.x < 0:
                enemy1.position.x = 0

            elif enemy1.position.x > 1024:
                enemy1.position.x = 1024

            elif enemy1.position.y < 0:
                enemy1.position.y = 0

            elif enemy1.position.y > 768:
                enemy1.position.y = 768

            if enemy2.position.x < 0:
                enemy2.position.x = 0

            elif enemy2.position.x > 1024:
                enemy2.position.x = 1024

            elif enemy2.position.y < 0:
                enemy2.position.y = 0

            elif enemy2.position.y > 768:
                enemy2.position.y = 768

            if enemy3.position.x < 0:
                enemy3.position.x = 0

            elif enemy3.position.x > 1024:
                enemy3.position.x = 1024

            elif enemy3.position.y < 0:
                enemy3.position.y = 0

            elif enemy3.position.y > 768:
                enemy3.position.y = 768

            for ball in ball_list:
                if ball.position.x < 0 or ball.position.x > 1024 or ball.position.y < 0 or ball.position.y > 768:
                    ball_list.remove(ball)


                if ball.position.colliderect(enemy1.position):
                    if ball.position == hero.position:
                        pass                                                             #ici collisions entre la balle et l'ennemi
                    else:
                        ball_list.remove(ball)
                        enemy1.life -= 1
                        ball.position = hero.position

                if ball.position.colliderect(enemy2.position):
                    if ball.position == hero.position:
                        pass
                    else:
                        ball_list.remove(ball)
                        enemy2.life -= 1
                        ball.position = hero.position

                if ball.position.colliderect(enemy3.position):
                    if ball.position == hero.position:
                        pass
                    else:
                        ball_list.remove(ball)
                        enemy3.life -= 1
                        ball.position = hero.position

                if ball.position != hero.position:
                    if ball.direction == 'up':
                        ball.position.y -= 4
                    elif ball.direction == 'right':
                        ball.position.x += 4
                    elif ball.direction == 'left':
                        ball.position.x -= 4
                    elif ball.direction == 'down':
                        ball.position.y += 4


            if enemy1.life == 0:
                enemy1.image = pygame.image.load("images/grave2.png").convert_alpha() #charge l'image de tombe quand l'enemi est mort
                enemy1.alive = 0
                score += 10000

            elif enemy2.life == 0:
                enemy2.image = pygame.image.load("images/grave2.png").convert_alpha() #charge l'image de tombe quand l'enemi est mort
                enemy2.alive = 0
                score += 10000

            elif enemy3.life == 0:
                enemy3.image = pygame.image.load("images/grave2.png").convert_alpha() #charge l'image de tombe quand l'enemi est mort
                enemy3.alive = 0
                score += 10000

            if hero.life == 0 or hero.life < 0:
                hero.image =  pygame.image.load("images/grave2.png").convert_alpha() #charge l'image de tombe quand le heros est mort
                text_end = font_end.render("GAME OVER", 1, (255,255,255)) #affiche game over lors de la mort
                fenetre.blit(fond_jeu, (0,0))
                fenetre.blit(text_end, (30, 30))
                hero.alive = 0


            if enemy1.alive == 1:

                if enemy1.position.x <= hero.position.x:

                    enemy1.position.x += 1+speed

                if enemy1.position.y <= hero.position.y:

                    enemy1.position.y += 1+speed

                if enemy1.position.x >= hero.position.x:

                    enemy1.position.x -= 1+speed

                if enemy1.position.y >= hero.position.y:

                    enemy1.position.y -= 1+speed                     #ici c'est l'automatisation des mouvements de l'ennemi, très simple car il va juste dans la direction du heros

            if enemy2.alive ==1:

                if enemy2.position.x <= hero.position.x:

                    enemy2.position.x += 1+speed

                if enemy2.position.y <= hero.position.y:

                    enemy2.position.y += 1+speed

                if enemy2.position.x >= hero.position.x:

                    enemy2.position.x -= 1+speed

                if enemy2.position.y >= hero.position.y:

                    enemy2.position.y -= 1+speed

            if enemy3.alive == 1:

                if enemy3.position.x <= hero.position.x:

                    enemy3.position.x += 1+speed

                if enemy3.position.y <= hero.position.y:

                    enemy3.position.y += 1+speed

                if enemy3.position.x >= hero.position.x:

                    enemy3.position.x -= 1+speed

                if enemy3.position.y >= hero.position.y:

                    enemy3.position.y -= 1 + speed



            if  enemy1.position.colliderect(enemy2.position) or enemy1.position.colliderect(enemy3.position):  #collisions entre ninjas
                enemy1.position.x -= 5
                enemy1.position.y -= 5

            if enemy2.position.colliderect(enemy1.position) or enemy2.position.colliderect(enemy3.position):
                enemy2.position.x += 5
                enemy2.position.y += 5




            fenetre.blit(fond_jeu, (0,0))    #on réaffiche le fond et tous les personnages
            fenetre.blit(enemy1.image, enemy1.position)
            fenetre.blit(enemy2.image, enemy2.position)
            fenetre.blit(enemy3.image, enemy3.position)

            for ball in ball_list:
                fenetre.blit(ball.image, ball.position)

            if enemy1.alive == 0 and enemy2.alive == 0 and enemy3.alive == 0:           #gestion des vagues d'ennemis et du respawn

                enemy1.image = enemy1.image_right
                enemy1.position.x = 100
                enemy1.position.y = 100
                enemy1.life = 5
                enemy2.image = enemy1.image_right
                enemy2.position.x = 100
                enemy2.position.y = 200
                enemy2.life = 5
                enemy3.image = enemy1.image_right
                enemy3.position.x = 100
                enemy3.position.y = 300
                enemy3.life = 5
                speed += 1
                enemy1.alive = 1
                enemy2.alive = 1
                enemy3.alive = 1
                score += 100

            if hero.alive == 1:
                score += 1

            fenetre.blit(hero.image, hero.position) #on affiche le heros
            #Rafraichissement
            texts(score)  # on affiche le score
            pygame.display.flip() # on actualise
            clock.tick(60) #fps



''' CREDITS :

Musique :

Titre:  Reset
Auteur: Jaunter
Source: https://jaunter.bandcamp.com
Licence: https://creativecommons.org/licenses/by/3.0/
Téléchargement (6MB): https://www.auboutdufil.com/index.php?id=497

Images : https://opengameart.org/'''
