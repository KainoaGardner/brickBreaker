import pygame
from settings import *
from random import choice
from game import Ball, Bar, Board
from levels import *


pygame.init()

screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

def display(screen,ball,bar,board):
    screen.fill(BLACK)
    pygame.draw.rect(screen,"#3f3f3f",(MARGINSIZE,MARGINSIZE,WIDTH - MARGINSIZE * 2,HEIGHT - MARGINSIZE * 2))
    pygame.draw.line(screen,BLACK,(0,HEIGHT - HEIGHT // 8),(WIDTH,HEIGHT - HEIGHT // 8),15)

    bar.move()
    bar.display(screen)

    board.display(screen)

    ball.update()
    ball.display(screen)

    pygame.display.update()
    clock.tick(FPS)

def checkCollisions(ball,bar):
    # if bar.checkHit((ball.x + (ball.xVel * ball.speed),ball.y + (ball.yVel * ball.speed))):
    if bar.checkHit((ball.x,ball.y),ball.size) and  ball.bounceCounter > 5:
        ball.bounceCounter = 0
        ball.yVel *= -1

def checkBlockCollisions(ball,board):
    if ball.bounceCounter > 0:
        tile = checkHit((ball.x,ball.y),board)
        
        if tile:
            newPos = [ball.x - ball.xVel,ball.y - ball.yVel]
            newTile = checkHit((newPos[0],newPos[1]),board)
            while newTile == tile:
                newPos = [newPos[0] - ball.xVel,newPos[1] - ball.yVel]
                newTile = checkHit((newPos[0],newPos[1]),board)
            if ball.bounceCounter > 3: 
                block = board.board[tile[1]][tile[0]]
                block.explosionPos = (tile[0] * board.blockWidth + board.blockWidth // 2, tile[1] * board.blockHeight + board.blockHeight // 2)
                board.brokenBlocks.append(block)

                board.board[tile[1]][tile[0]] = None
            
            a,b = (tile[0] * board.blockWidth, tile[1] * board.blockHeight)
            w,h = (board.blockWidth,board.blockHeight)
            x,y = newPos
            yA = -(h / w) * (x - a) + b + h
            yB = (h / w) * (x - a) + b
        
            area = [0,0]
            if y < yA: 
                area[0] = 1
            if y > yA:
                area[0] = 2
            if y < yB:
                area[1] = 3
            if y > yB:
                area[1] = 4
    
            if area == [1,3]:
                ball.yVel = -1
            elif area == [2,4]:
                ball.yVel = 1
            elif area == [1,4]:
                ball.xVel = -1
            elif area == [2,3]:
                ball.xVel = 1
            else:
                ball.yVel *= -1



def checkHit(pos,board):
    if 0 <= pos[1] < len(board.board) * board.blockHeight and 0 < pos[0] < WIDTH:
        tile = (pos[0] // board.blockWidth,pos[1] // board.blockHeight)
        if board.board[tile[1]][tile[0]]:
            return tile
    return False

def resetBall(ball,bar):
    if bar.direction == "right":
        ball.xVel = 1
    elif bar.direction == "left":
        ball.xVel = -1
    else:
        ball.xVel = choice((-1,1))
    ball.dead = False
    ball.yVel = -1

def displayScore(board):
    pass

def main():
    run = True
    ball = Ball(WIDTH // 2,HEIGHT - HEIGHT // 8, 10,10,WHITE)
    bar = Bar(WIDTH // 2 - 50,HEIGHT - HEIGHT // 16,(100,20),10,WHITE)
    board = Board(level1)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        if ball.dead and ball.explosionCounter >= 25:
            ball.size = ball.backUpSize   
            ball.x = bar.x + bar.width // 2
            ball.y = HEIGHT - HEIGHT // 8
            if ball.explosionCounter > 100:
                resetBall(ball,bar)

        checkCollisions(ball,bar)
        checkBlockCollisions(ball,board)
        display(screen,ball,bar,board)

    pygame.quit()


main()


