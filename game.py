
import time
import pygame
from pygame.locals import *
import copy

pygame.init()


#   Resolution
epaisseur = 1024 
hauteur = 768 

taille_tuile = 32

epaisseur_grille = epaisseur / taille_tuile
hauteur_grille = hauteur / taille_tuile


#fps
clock = pygame.time.Clock() 

#   keyboard repetition
pygame.key.set_repeat(1,70) 


pygame.display.set_caption("Python Survival")

#   show the window of the game
fenetre = pygame.display.set_mode((epaisseur, hauteur)) 
x = 32
y = 32

speed = 1
tk = 0

#   x and y coordinate of the character
position_hero_base_x = 512 
position_hero_base_y = 384 

score = 0

pygame.key.set_repeat(1,50)

accueil = 1
playing = 0
run = 1

#   background of the game
fond_jeu = pygame.image.load("images/white.png").convert() 

#   home background of the game
fond_accueil = pygame.image.load("images/image_accueil.jpg").convert() 

font = pygame.font.Font(None, 35)
text = font.render("press any key to start the game",1,(255,255,255))

font_score=pygame.font.Font('vgasys.ttf',30)
font_end =pygame.font.Font('vgasys.ttf', 60)

#   image of bullet
bullet = pygame.image.load("images/ball2.png").convert_alpha() 
vitesse_missile = 0

#   Hero Class
class Hero(pygame.sprite.Sprite): 
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


#   Enemy class
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

#   Ball Class
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
   scoretext=font_score.render("Score:"+str(score), 1,(0,0,0)) 
   fenetre.blit(scoretext, (700, 50)) 


ball_list = pygame.sprite.Group()
while run == 1:
    while accueil == 1:
        fenetre.blit(fond_accueil, (0,0))
        fenetre.blit(text, (300, 300))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == KEYDOWN: 
                playing = 1 
                accueil = 0

        while playing == 1:
            accueil = 0
            for event in pygame.event.get():        
                if event.type == QUIT:
                    run = 0
                    playing = 0
                    pygame.display.flip()
                    pygame.quit()
                    exit()

                if event.type == KEYDOWN:           
                    if hero.position.colliderect(enemy1.position) or  hero.position.colliderect(enemy2.position) or hero.position.colliderect(enemy3.position): 
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
                            playing = 0
                            accueil = 1
                            fenetre.blit(fond_accueil, (0,0))
                            pygame.display.flip()

                        if hero.alive == 1:
                            if event.key == K_UP:       
                                hero.position.y -=  y
                                hero.image = hero.image_back
                                fenetre.blit(hero.image, hero.position)
                                pygame.display.flip()


                            elif event.key == K_DOWN:
                                hero.image = hero.image_face  
                                hero.position.y +=  y
                                fenetre.blit(hero.image, hero.position)
                                pygame.display.flip()


                            elif event.key == K_RIGHT:
                                hero.image = hero.image_right 
                                hero.position.x +=  x
                                fenetre.blit(hero.image, hero.position)
                                pygame.display.flip()


                            elif event.key == K_LEFT:
                                hero.image = hero.image_left 
                                hero.position.x -= x
                                fenetre.blit(hero.image, hero.position)
                                pygame.display.flip()


                            if event.key == K_SPACE:
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
                hero.position.y = 680                         


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
                        pass                                                             
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
                enemy1.image = pygame.image.load("images/grave2.png").convert_alpha() 
                enemy1.alive = 0
                score += 10000

            elif enemy2.life == 0:
                enemy2.image = pygame.image.load("images/grave2.png").convert_alpha() 
                enemy2.alive = 0
                score += 10000

            elif enemy3.life == 0:
                enemy3.image = pygame.image.load("images/grave2.png").convert_alpha() 
                enemy3.alive = 0
                score += 10000

            if hero.life == 0 or hero.life < 0:
                hero.image =  pygame.image.load("images/grave2.png").convert_alpha()
                text_end = font_end.render("GAME OVER", 1, (255,255,255)) 
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
                    enemy1.position.y -= 1+speed                  

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



            if  enemy1.position.colliderect(enemy2.position) or enemy1.position.colliderect(enemy3.position):  
                enemy1.position.x -= 5
                enemy1.position.y -= 5

            if enemy2.position.colliderect(enemy1.position) or enemy2.position.colliderect(enemy3.position):
                enemy2.position.x += 5
                enemy2.position.y += 5




            fenetre.blit(fond_jeu, (0,0))    
            fenetre.blit(enemy1.image, enemy1.position)
            fenetre.blit(enemy2.image, enemy2.position)
            fenetre.blit(enemy3.image, enemy3.position)

            for ball in ball_list:
                fenetre.blit(ball.image, ball.position)

            if enemy1.alive == 0 and enemy2.alive == 0 and enemy3.alive == 0:           
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

            fenetre.blit(hero.image, hero.position) 
            texts(score)  
            pygame.display.flip()
            clock.tick(60) #fps



''' CREDITS :

Musique :

Titre:  Reset
Auteur: Jaunter
Source: https://jaunter.bandcamp.com
Licence: https://creativecommons.org/licenses/by/3.0/
Téléchargement (6MB): https://www.auboutdufil.com/index.php?id=497

Images : https://opengameart.org/'''
