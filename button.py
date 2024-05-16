import pygame
from settings import *


class Button:
    def __init__(self,x,y,width,height,color,fontcolor,bordercolor,bordersize,fontsize,text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.bordercolor = bordercolor
        self.bordersize = bordersize
        self.font = pygame.font.Font("fonts/Lemon.otf",fontsize)
        self.text = self.font.render(text,True,fontcolor)


    def display(self,screen):
        pygame.draw.rect(screen,self.color,(self.x,self.y,self.width,self.height))
        pygame.draw.rect(screen,self.bordercolor,(self.x,self.y,self.width,self.height),self.bordersize)
        screen.blit(self.text,(self.x + self.width // 2 - self.text.get_width() // 2,self.y + self.height // 2 - self.text.get_height() // 2))



resetButton = Button(WIDTH // 2 - WIDTH // 4,HEIGHT - 200,WIDTH // 2,HEIGHT // 8,WHITE,BLACK,BLACK,5,30,"Press r to RESET")

buttons = [resetButton]
