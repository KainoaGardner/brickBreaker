import pygame
import math
from random import randint
from settings import *

pygame.font.init()

class extraBall:
    def __init__(self,x,y,speed,xVel,yVel,size,color):
        self.x = x
        self.y = y
        self.speed = speed
        self.size = size
        self.backUpSize = size
        self.color = color 

        self.xVel = xVel
        self.yVel = yVel
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

    def checkinBoard(self,board): 
        pos = (self.x,self.y)
        if 0 <= pos[1] < len(board.board) * board.blockHeight and 0 < pos[0] < WIDTH:
            return True
        return False

    def checkHoriCollision(self,board,ball):
        if self.checkinBoard(board):
            diagonalSize = math.sqrt((self.size ** 2) * 2)
            sides = [(self.x - self.size,self.y),(self.x + self.size,self.y),(self.x,self.y - self.size),(self.x,self.y + self.size),(self.x - diagonalSize,self.y- diagonalSize),(self.x - diagonalSize,self.y+ diagonalSize),(self.x + diagonalSize,self.y - diagonalSize),(self.x+ diagonalSize,self.y + diagonalSize)]
            for side in sides:
                tile = (int(side[0] // board.blockWidth), int(side[1] // board.blockHeight))
                if tile[0] < len(board.board[0]) and tile[1] < len(board.board):
                    block = board.board[tile[1]][tile[0]]
                    if block:
                        if self.xVel > 0:
                            self.x = tile[0] * board.blockWidth
                        else:
                            self.x = (tile[0] + 1) * board.blockWidth 
                        self.xVel *= -1                

                        block.kill(board,tile,ball)
                        self.bounceCounter = 0

                    break
                
    def checkVertCollision(self,board,ball):
        if self.checkinBoard(board):
            sides = [(self.x - self.size,self.y),(self.x + self.size,self.y),(self.x,self.y - self.size),(self.x,self.y + self.size)]
            for side in sides:
                tile = (int(side[0] // board.blockWidth), int(side[1] // board.blockHeight))
                if tile[0] < len(board.board[0]) and tile[1] < len(board.board):
                    block = board.board[tile[1]][tile[0]]
                    if block:
                        if self.yVel > 0:
                            self.y = tile[1] * board.blockHeight
                        else:
                            self.y = (tile[1] + 1) * board.blockHeight
    
                        self.yVel *= -1 
    
                        block.kill(board,tile,ball)
                        self.bounceCounter = 0
                    break

                
    def update(self,board,ball):
        self.y += self.speed * self.yVel
        self.checkVertCollision(board,ball)
        self.x += self.speed * self.xVel
        self.checkHoriCollision(board,ball)

        if self.x - self.size // 2 < 0 or self.x + self.size // 2 > WIDTH:
            self.xVel *= -1
            self.bounceCounter = 0
        if self.y - self.size // 2 < 0:
            self.yVel *= -1
            self.bounceCounter = 0
        if self.y + self.size // 2 > HEIGHT and not self.dead:
            self.kill()

        self.bounceCounter += 1 

    def explode(self,screen):
        self.explosionCounter += 1

        if self.dead and self.explosionCounter <= 25: 
            for _ in range(self.explosionAmount):
                angle = randint(0,360)
                xPos = self.x + (self.explosionCounter + randint(-self.explosionRandom,self.explosionRandom)) * 2 * math.cos(math.degrees(angle))
                yPos = self.y + (self.explosionCounter + randint(-self.explosionRandom,self.explosionRandom)) * 2* math.sin(math.degrees(angle))
                pygame.draw.circle(screen,self.color,(xPos,yPos),randint(1,10))

    def display(self,screen):
        self.explode(screen)
        pygame.draw.circle(screen,self.color,(self.x,self.y),self.size)
 

class Ball(extraBall):
    def __init__(self,x,y,speed,xVel,yVel,size,color):
        super().__init__(x,y,speed,xVel,yVel,size,color)
        
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
            if self.y < pos[1] + size // 2 and pos[1]< self.y + self.height:
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
        self.blockHeight = (HEIGHT - HEIGHT // 2) // len(self.board)
        self.blockWidth = WIDTH // len(self.board[0])
        self.blockAmount = self.getBlockAmount()
        self.brokenBlocks = []
        self.particles = []
        self.extraBalls = []

        # self.startScore = self.getScore()
        self.score = 0
        self.font = pygame.font.Font("fonts/Lemon.otf",WIDTH // 2)
        self.text = self.font.render(str(self.score),True,LIGHTGRAY)

    def getBlockAmount(self):
        count = 0
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] != None:
                    count += 1
        return count

    def update(self,screen,ball):
        for i in range(len(self.brokenBlocks) - 1,-1,-1):
            block = self.brokenBlocks[i]
            block.explosionCounter += 1
            block.redExplode(screen,self,ball)
            block.blueBeam(screen,self,ball)
            block.yellowBeam(screen,self,ball)
            block.orangeBall(ball)
            if block.explosionCounter > 60 and block.explosion:
                block.explosion = False
                block.beam = False
                self.brokenBlocks.pop(i)
            if block.explosionCounter > 30 and block.beam:
                block.explosion = False
                block.beam = False
                self.brokenBlocks.pop(i)
            if block.explosionCounter > 300 and block.bigBall:
                block.bigBall = False
                ball.size = ball.backUpSize
                block.tempCounter = block.explosionCounter
            
    def displayParticles(self,screen):
        for i in range(len(self.particles)-1,-1,-1):
            particle = self.particles[i]
            if particle.y > HEIGHT:
                self.particles.pop(i)

            particle.display(screen)

    def displayScore(self,screen): 
        screen.blit(self.text,(WIDTH // 2 - self.text.get_width() // 2,HEIGHT // 2 - self.text.get_height() // 2))

    def display(self,screen,ball):
        self.displayScore(screen)
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                block = self.board[row][col]
                if block: 
                    pygame.draw.rect(screen,block.color, (col * self.blockWidth,row * self.blockHeight,self.blockWidth,self.blockHeight))
                    pygame.draw.rect(screen,BLACK, (col * self.blockWidth,row * self.blockHeight,self.blockWidth,self.blockHeight),3)

        self.update(screen,ball)

        self.displayParticles(screen)

class Block:
    def __init__(self,color):
        self.color = color
        self.explosionCounter = 0
        self.beam = False
        self.explosion = False
        self.explosionPos = ()
        self.bigBall = False
        self.tempCounter = 0

    def kill(self,board,tile,ball):
        board.board[tile[1]][tile[0]] = None
        board.brokenBlocks.append(self)
        board.score += 1
        board.text = board.font.render(str(board.score),True,LIGHTGRAY)
        pos = (tile[0] * board.blockWidth + board.blockWidth // 2,tile[1] * board.blockHeight + board.blockHeight // 2)

        for _ in range(randint(1,5)):
            board.particles.append(Particle(self.color,pos[0],pos[1],randint(15,15),randint(15,15),randint(-10,10),randint(-10,10)))

        if self.color == RED:
            self.explosionCounter = 0 
            self.explosionPos = pos
            self.explosion = True
        if self.color == BLUE or self.color == YELLOW:
            self.explosionCounter = 0 
            self.explosionPos = pos
            self.beam = True
        if self.color == GREEN:
            self.greenBall(board,pos)
        if self.color == ORANGE:
            self.tempCounter = 0
            self.explosionCounter = 0 
            ball.color = ORANGE
            self.bigBall = True
            

    def greenBall(self,board,pos):
        speed = math.sqrt(1 + 1)
        for _ in range(3):
            angle = randint(1,360)
            xVel = speed * math.cos(math.degrees(angle))
            yVel = speed * math.sin(math.degrees(angle))
            board.extraBalls.append(extraBall(pos[0],pos[1], 10,xVel,yVel,10,GREEN))


    def orangeBall(self,ball):
        if ball.dead:
            self.bigBall = False
            self.tempCounter = 0
        if self.bigBall:
            ball.size = min((self.explosionCounter * self.explosionCounter), 50)
        elif self.tempCounter:
            size = (self.explosionCounter % self.tempCounter) ** 2
            if size >= 50:
                self.tempCounter = 0
                ball.color = WHITE
            
            ball.size = max(50 - size, ball.backUpSize)
         

    def blueBeam(self,screen,board,ball):
        if self.explosionPos and self.beam and self.color == BLUE:
            size = min((self.explosionCounter * self.explosionCounter) * 5, HEIGHT)
            pygame.draw.rect(screen,BLUE,(self.explosionPos[0] - board.blockWidth // 2,self.explosionPos[1] - board.blockHeight //2 - size,board.blockWidth,size))
            pygame.draw.rect(screen,BLUE,(self.explosionPos[0] - board.blockWidth // 2,self.explosionPos[1] - board.blockHeight //2,board.blockWidth,size))
            col = self.explosionPos[0] // board.blockWidth
            for r in range(len(board.board)):
                block = board.board[r][col]
                if block:
                    blockY = r * board.blockHeight - board.blockHeight // 2
                    distance = abs(blockY - self.explosionPos[1])
                    if distance < size:
                        block.kill(board,(col,r),ball)
                        
    def yellowBeam(self,screen,board,ball): 
        if self.explosionPos and self.beam and self.color == YELLOW:
            size = min((self.explosionCounter * self.explosionCounter) * 5, WIDTH)
            pygame.draw.rect(screen,YELLOW,(self.explosionPos[0] - board.blockWidth // 2,self.explosionPos[1] - board.blockHeight //2,size,board.blockHeight))
            pygame.draw.rect(screen,YELLOW,(self.explosionPos[0] - board.blockWidth // 2 - size,self.explosionPos[1] - board.blockHeight //2,size,board.blockHeight))
            row = self.explosionPos[1] // board.blockHeight
            for c in range(len(board.board[0])):
                block = board.board[row][c]
                if block:
                    blockX = c * board.blockWidth - board.blockWidth // 2
                    distance = abs(blockX - self.explosionPos[0])
                    if distance < size:
                        block.kill(board,(c,row),ball) 

    def redExplode(self,screen,board,ball): 
        if self.explosionPos and self.explosion:
            radius = min(self.explosionCounter * self.explosionCounter, 200)
            pygame.draw.circle(screen,RED,(self.explosionPos),radius)
            for r in range(len(board.board)):
                for c in range(len(board.board[r])):
                    block = board.board[r][c]
                    if block:
                        blockPos = (c * board.blockWidth,r * board.blockHeight)
                        
                        corners = [blockPos,(blockPos[0] + board.blockWidth,blockPos[1]),(blockPos[0],blockPos[1] + board.blockHeight),(blockPos[0] + board.blockWidth,blockPos[1] + board.blockHeight)]
                        for corner in corners:
                            dif = (corner[0] - self.explosionPos[0],corner[1] - self.explosionPos[1])
                            distance = math.sqrt(dif[0] ** 2 + dif[1] ** 2)
                            if distance < radius:
                                block.kill(board,(c,r),ball)
                                break
 

class Particle():
    def __init__(self,color,x,y,width,height,xVel,yVel):
        self.color = color
        self.x = x
        self.y =y 
        self.width = width
        self.height = height
        # self.size = size
        self.xVel = xVel
        self.yVel = yVel

    def update(self):
        self.x += self.xVel
        self.y += self.yVel

        self.yVel += 1

    def display(self,screen):
        self.update()
        pygame.draw.rect(screen,self.color,(self.x,self.y,self.width,self.height))
        pygame.draw.rect(screen,BLACK,(self.x,self.y,self.width,self.height),3)
        # pygame.draw.circle(screen,self.color,(self.x,self.y),self.size)

    

