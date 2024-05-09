import pygame
import math
from random import randint
from settings import *

class Ball:
    def __init__(self,x,y,speed,size,color):
        self.x = x
        self.y = y
        self.speed = speed
        self.size = size
        self.backUpSize = size
        self.color = color 

        self.xVel = 1
        self.yVel = -1
        self.barX = 0
        self.barY = 0
        self.bounceCounter = 0

        self.dead = False
        self.explosionCounter = 0
        self.explosionAmount = 36
        self.explosionRandom = 8
        self.explosionAngleAmount = 360 // self.explosionAmount

    def kill(self):
        self.dead = True
        self.xVel = 0
        self.yVel = 0
        self.size = 0
        self.explosionCounter = 0

    def explode(self,screen):
        self.explosionCounter += 1

        if self.dead and self.explosionCounter <= 25: 
            for _ in range(self.explosionAmount):
                angle = randint(0,360)
                xPos = self.x + (self.explosionCounter + randint(-self.explosionRandom,self.explosionRandom)) * 2 * math.cos(math.degrees(angle))
                yPos = self.y + (self.explosionCounter + randint(-self.explosionRandom,self.explosionRandom)) * 2* math.sin(math.degrees(angle))
                pygame.draw.circle(screen,self.color,(xPos,yPos),randint(1,10))




    def update(self):
        self.bounceCounter += 1
        self.x += self.speed * self.xVel
        self.y += self.speed * self.yVel

        if self.x - self.size // 2 < 0 or self.x + self.size // 2 > WIDTH:
            self.xVel *= -1
        if self.y - self.size // 2 < 0:
            self.yVel *= -1
        if self.y + self.size // 2 > HEIGHT and not self.dead:
            self.kill()

    
    # def checkCollison(self,pos,size):
    #     if pos[0] < self.x - self.size // 2 and self.x + self.size // 2 < pos[0] + size[0]:
    #         if pos[1] < self.y - self.size // 2 and self.y + self.size // 2 < pos[1] + size[1]:
    #             return True
    #     return False


    def display(self,screen):
        self.explode(screen)
        pygame.draw.circle(screen,self.color,(self.x,self.y),self.size)

        

class Bar:
    def __init__(self,x,y,size,speed,color):
        self.x = x
        self.y = y
        self.direction = "right"
        self.width,self.height = size
        self.speed = speed
        self.color = color


    def checkHit(self,pos,size):
        if self.x < pos[0] + size // 2 and pos[0] - size // 2 < self.x + self.width:
            if self.y < pos[1] + size // 2 and pos[1] - size // 2 < self.y + self.height:
                return True
        return False

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
            self.direction = "left"
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.width:
            self.x += self.speed
            self.direction = "right"

        if keys[pygame.K_LEFT] == False and keys[pygame.K_RIGHT] == False or (keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]):
            pass
            # self.direction = ""

            
    def display(self,screen):
        pygame.draw.rect(screen,self.color,(self.x,self.y,self.width,self.height))

class Board:
    def __init__(self,board):
        self.board = board
        self.blockHeight = (HEIGHT - HEIGHT // 3) // len(self.board)
        self.blockWidth = WIDTH // len(self.board[0])
        self.blockAmount = self.getBlockAmount()
        self.brokenBlocks = []

    def getBlockAmount(self):
        count = 0
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] != None:
                    count += 1
        return count

    def update(self,screen):
        for i in range(len(self.brokenBlocks) - 1,-1,-1):
            block = self.brokenBlocks[i]
            block.breakBlock(screen)
            if block.explosionCounter > 10:
                self.brokenBlocks.pop(i)

            

    def display(self,screen):
        self.update(screen)
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                block = self.board[row][col]
                if block:
                    pygame.draw.rect(screen,block.color, (col * self.blockWidth,row * self.blockHeight,self.blockWidth,self.blockHeight))
                    pygame.draw.rect(screen,BLACK, (col * self.blockWidth,row * self.blockHeight,self.blockWidth,self.blockHeight),3)


class Block:
    def __init__(self,color):
        self.color = color
        self.explosionCounter = 0
        self.explosionPos = ()

    def breakBlock(self,screen): 
        self.explosionCounter += 1
        if self.explosionPos:
            for _ in range(4):
                angle = randint(0,360)
                xPos = self.explosionPos[0] + (self.explosionCounter + randint(-5,5)) * 2 * math.cos(math.degrees(angle))
                yPos = self.explosionPos[1] + (self.explosionCounter + randint(-5,5)) * 2* math.sin(math.degrees(angle))
                pygame.draw.circle(screen,self.color,(xPos,yPos),randint(2,10))


        


