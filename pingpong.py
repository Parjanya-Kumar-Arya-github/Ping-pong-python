import math
import sys 
import pygame
from pygame.locals import *
import time


FPS = 32
width = 900
height = 500
SCREEN = pygame.display.set_mode((width, height))
BG=pygame.image.load('bg.png').convert_alpha()
GAME_SOUNDS={}


class Game:
    def __init__(self):
        
        self.bot_paddlex=0
        self.bot_paddley=height//2-50
        self.playerx=width-20
        self.playery = height//2-50
        self.ballx=width//2
        self.bally=height//2
        self.nety=0
        self.vel=15
        self.bot_score=0
        self.player_score=0
        

    def collision(self,p):
        if p=="bot":
            ptop = self.bot_paddley
            pbottom = self.bot_paddley + 100
            pleft = self.bot_paddlex
            pright = self.bot_paddlex + 20
        
        else:
            ptop = self.playery
            pbottom = self.playery + 100
            pleft = self.playerx
            pright = self.playerx + 20
        
        btop = self.bally - 15
        bbottom = self.bally + 15
        bleft = self.ballx - 15
        bright = self.ballx + 15
        
        return pleft < bright and ptop < bbottom and pright > bleft and pbottom > btop

    def bot_paddle(self):
        if 0<=self.bot_paddley<=height-100:
            self.bot_paddley += ((self.bally - (self.bot_paddley + 100/2)))*self.mistake
        elif 0>=self.bot_paddley:
            self.bot_paddley += 2
        else:
            self.bot_paddley -= 2
    def who_won(self,p):
        if p=="bot":
            smallfont = pygame.font.SysFont('Corbel',60)
            text = smallfont.render('YOU LOSE!' , True , (255,255,255)) 
            
            SCREEN.blit(text , (width//5+150,height/3))
            pygame.display.update()
            FPSCLOCK.tick(FPS)
            time.sleep(3)
            self.player_score=0
            self.bot_score=0
            self.intro()
            
        else:
            smallfont = pygame.font.SysFont('Corbel',60)
            text = smallfont.render('YOU WON!' , True , (255,255,255)) 
            SCREEN.blit(text , (width//5+150,height/3))
            pygame.display.update()
            FPSCLOCK.tick(FPS)
            time.sleep(3)
            self.player_score=0
            self.bot_score=0
            self.intro()
            
    def reset(self):
        self.playery=height//2-50
        self.bot_paddley=height//2-50
        self.ballx = width//2
        self.bally = height//2
        self.ballvelx = -self.ballvelx
        self.ballspeed = 10

    def controlscreen(self):
        
        while True:
            self.mouse = pygame.mouse.get_pos() 
            self.ms_posx=290
            self.ms_posy=250
            self.key_posx=475
            self.key_posy=250
            
            SCREEN.blit(BG,(0,0)) 
            pygame.draw.rect(SCREEN,(255,255,255),[0,0,width,height],2)

            smallfont = pygame.font.SysFont('Corbel',40)

            text = smallfont.render('WANNNA CONTROL WITH ?' , True , (255,255,255)) 
            
            SCREEN.blit(text , (width/5+25,height/3))
            if self.ms_posx <= self.mouse[0] <= self.ms_posx+140 and self.ms_posy <= self.mouse[1] <= self.ms_posy+40: 
                pygame.draw.rect(SCREEN,(190,190,190),[self.ms_posx,self.ms_posy,140,40]) 
                smallfont = pygame.font.SysFont('Corbel',30)
                text = smallfont.render('USE YOUR MOUSE TO MOVE THE PADDLE' , True , (255,255,255)) 
            
                SCREEN.blit(text , (width//5+10,height/1.5))
                
            else: 
                pygame.draw.rect(SCREEN,(255,255,255),[self.ms_posx,self.ms_posy,140,40])
            smallfont = pygame.font.SysFont('Corbel',30)
            text = smallfont.render('MOUSE' , True , (0,0,0)) 
            
            SCREEN.blit(text , (self.ms_posx+20,self.ms_posy+7))

            if self.key_posx <= self.mouse[0] <= self.key_posx+140 and self.key_posy <= self.mouse[1] <= self.key_posy+40: 
                pygame.draw.rect(SCREEN,(190,190,190),[self.key_posx,self.key_posy,140,40])
                smallfont = pygame.font.SysFont('Corbel',30)
                text = smallfont.render('USE YOUR \"W\" or UP arrow key TO MOVE THE PADDLE UP' , True , (255,255,255))                 
                SCREEN.blit(text , (width//6-30,height/1.5))
                text = smallfont.render('USE YOUR \"S\" or DOWN arrow key TO MOVE THE PADDLE DOWN' , True , (255,255,255))                 
                SCREEN.blit(text , (width//6-75,height/1.5+30))
                
            else: 
                pygame.draw.rect(SCREEN,(255,255,255),[self.key_posx,self.key_posy,140,40])
            smallfont = pygame.font.SysFont('Corbel',27)
            text = smallfont.render('KEYBOARD' , True , (0,0,0)) 
            
            SCREEN.blit(text , (self.key_posx+6,self.key_posy+8))
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    run=False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN: 
                    if (self.ms_posx <= self.mouse[0] <= self.ms_posx+140 and self.ms_posy <= self.mouse[1] <= self.ms_posy+40): 
                        
                        self.control="mouse"
                        self.maingame(self.mode)
                    elif (self.key_posx <= self.mouse[0] <= self.key_posx+140 and self.key_posy <= self.mouse[1] <= self.key_posy+40):
                    
                        self.control="keyboard"
                        self.maingame(self.mode)
            
            pygame.display.update()
            FPSCLOCK.tick(FPS)


    def controls(self,choosed):
        if choosed=="mouse":
            self.mouse = pygame.mouse.get_pos()
            if (width//2 <= self.mouse[0] <= width//2+450 and 0<=self.mouse[1]<=height-100):
                self.playery = self.mouse[1]
        else:
            keys = pygame.key.get_pressed() 
            
            if (keys[pygame.K_UP] or pygame.key.get_pressed()[K_w]) and self.playery>0: 
                
                self.playery -= self.vel 
                
            if (keys[pygame.K_DOWN] or pygame.key.get_pressed()[K_s]) and self.playery<height-100: 
                self.playery += self.vel
            

    def maingame(self,m):
        if m=="easy":
            self.ballvelx=6
            self.ballvely=6
            self.ballspeed=10
            self.mistake=0.03
        elif m=="medium":
            self.ballvelx=8
            self.ballvely=8
            self.ballspeed=12
            self.mistake=0.1
        else:
            self.ballvelx=15
            self.ballvely=15
            self.ballspeed=21
            self.mistake=0.2
        
        
        
        run=True
        while run:
            for event in pygame.event.get(): 
                
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    run=False
                    pygame.quit()
                    sys.exit()

            
            self.controls(self.control)

            self.ballx += self.ballvelx
            self.bally += self.ballvely
            
            
            
            if(self.ballx + 15 < width/2):
                player="bot"
            else:
                player="player"

            if( self.ballx - 15 < 0 ):
                self.player_score+=1
                GAME_SOUNDS['userScore'].play()
                self.reset()
            elif( self.ballx + 15 > width):
                self.bot_score+=1
                GAME_SOUNDS['botScore'].play()
                self.reset()
        
            self.bot_paddle()


            if(self.bally - 15 < 0 or self.bally + 15 > height):
                GAME_SOUNDS['wall'].play()
                self.ballvely = -self.ballvely

            if(self.collision(player)):
                GAME_SOUNDS['hit'].play()
                if player=="bot":
                    self.y=self.bot_paddley
                else:
                    self.y=self.playery
                self.collidePoint = (self.bally - (self.y + 100/2))
                self.collidePoint = self.collidePoint / (100/2)
                self.angleRad = (math.pi/4) * self.collidePoint
            
                if (self.ballx + 15 < width/2):
                    self.direction =  1
                else:
                    self.direction = -1
                self.ballvelx = self.direction * self.ballspeed * math.cos(self.angleRad)
                self.ballvely = self.ballspeed * math.sin(self.angleRad)
                
            
                self.ballspeed += 0.1


            
                
                    
            
            SCREEN.fill((0, 0, 0)) 
             
            pygame.draw.rect(SCREEN, (255, 255, 255), (self.playerx, self.playery, 20, 100))
            pygame.draw.rect(SCREEN, (255, 255, 255), (self.bot_paddlex, self.bot_paddley, 20, 100))
            pygame.draw.circle(SCREEN,(255,255,255),(self.ballx,self.bally),15)
            font = pygame.font.Font('freesansbold.ttf', 80)
            text = font.render(f'{self.bot_score}', True, (255,255,255))
            
            SCREEN.blit(text,(width//5,height//5))
            text = font.render(f'{self.player_score}', True, (255,255,255))
            
            SCREEN.blit(text,(width-250,height//5))
            pygame.draw.rect(SCREEN, (255, 255, 255), (width//2, self.nety, 8, 500))
            pygame.display.update()
            FPSCLOCK.tick(FPS)
            if self.player_score==7:
                self.who_won("player")
            if self.bot_score==7:
                self.who_won("bot")

    def intro(self):
        SCREEN.blit(BG,(0,0))
        run = True
        while run:
            self.mouse = pygame.mouse.get_pos() 
            self.easy_posx=380
            self.easy_posy=250
            self.mid_posx=380
            self.mid_posy=300
            self.dif_posx=380
            self.dif_posy=350

            if self.easy_posx <= self.mouse[0] <= self.easy_posx+140 and self.easy_posy <= self.mouse[1] <= self.easy_posy+40: 
                pygame.draw.rect(SCREEN,(190,190,190),[self.easy_posx,self.easy_posy,140,40]) 
                
            else: 
                pygame.draw.rect(SCREEN,(255,255,255),[self.easy_posx,self.easy_posy,140,40]) 
            smallfont = pygame.font.SysFont('Corbel',35)

            text = smallfont.render('Easy' , True , (0,0,0)) 
            
            SCREEN.blit(text , (self.easy_posx+37,self.easy_posy+5))

            if self.mid_posx <= self.mouse[0] <= self.mid_posx+140 and self.mid_posy <= self.mouse[1] <= self.mid_posy+40: 
                pygame.draw.rect(SCREEN,(190,190,190),[self.mid_posx,self.mid_posy,140,40]) 
                
            else: 
                pygame.draw.rect(SCREEN,(255,255,255),[self.mid_posx,self.mid_posy,140,40])
            text = smallfont.render('Medium' , True , (0,0,0)) 
            
            SCREEN.blit(text , (self.mid_posx+15,self.mid_posy+5))

            if self.dif_posx <= self.mouse[0] <= self.dif_posx+140 and self.dif_posy <= self.mouse[1] <= self.dif_posy+40: 
                pygame.draw.rect(SCREEN,(190,190,190),[self.dif_posx,self.dif_posy,140,40]) 
                
            else: 
                pygame.draw.rect(SCREEN,(255,255,255),[self.dif_posx,self.dif_posy,140,40])
            text = smallfont.render('Difficult' , True , (0,0,0)) 
            
            SCREEN.blit(text , (self.dif_posx+15,self.dif_posy+5))

            font = pygame.font.SysFont('Corbel',70)
            text = font.render('PING PONG GAME' , True , (255,255,255)) 
            
            SCREEN.blit(text , (width//3-125,height//4))

            
            pygame.display.update()
            FPSCLOCK.tick(FPS)
            for event in pygame.event.get():                 
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    run=False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN: 
                    if (self.easy_posx <= self.mouse[0] <= self.easy_posx+140 and self.easy_posy <= self.mouse[1] <= self.easy_posy+40): 
                        self.mode="easy"
                        self.controlscreen()
                    elif (self.mid_posx <= self.mouse[0] <= self.mid_posx+140 and self.mid_posy <= self.mouse[1] <= self.mid_posy+40):
                        self.mode="medium"
                        self.controlscreen()
                    elif (self.dif_posx <= self.mouse[0] <= self.dif_posx+140 and self.dif_posy <= self.mouse[1] <= self.dif_posy+40):
                        self.mode="difficult"
                        self.controlscreen()
            









if __name__ == "__main__":
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Ping Pong game by Parjanya')
    GAME_SOUNDS['botScore'] = pygame.mixer.Sound('sound/comScore.mp3')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('sound/hit.mp3')
    GAME_SOUNDS['userScore'] = pygame.mixer.Sound('sound/userScore.mp3')
    GAME_SOUNDS['wall'] = pygame.mixer.Sound('sound/wall.mp3')
    MAIN=Game()
    while True:
        MAIN.intro()