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

    board.display(screen,ball)
    for extraBall in board.extraBalls:
        extraBall.update(board,ball)
        extraBall.display(screen)

    ball.update(board,ball)
    ball.display(screen)

    pygame.display.update()
    clock.tick(FPS)

def checkCollisions(ball,extraBalls,bar):
    if bar.checkHit((ball.x,ball.y),ball.size) and ball.bounceCounter > 1:
        ball.bounceCounter = 0
        ball.yVel *= -1

    for extraBall in extraBalls:
        if bar.checkHit((extraBall.x,extraBall.y),extraBall.size) and  extraBall.bounceCounter > 1:
            extraBall.bounceCounter = 0
            extraBall.yVel *= -1

# def checkHit(pos,board):
#     if 0 <= pos[1] < len(board.board) * board.blockHeight and 0 < pos[0] < WIDTH:
#         tile = (pos[0] // board.blockWidth,pos[1] // board.blockHeight)
#         if board.board[tile[1]][tile[0]]:
#             return tile
#     return False

def resetBall(ball,bar):
    if bar.direction == "right":
        ball.xVel = 1
    elif bar.direction == "left":
        ball.xVel = -1
    else:
        ball.xVel = choice((-1,1))
    ball.dead = False
    ball.yVel = -1

def killBall(ball,extraBalls,bar):
    if ball.dead and ball.explosionCounter >= 25:
        ball.color = WHITE
        ball.size = ball.backUpSize   
        ball.x = bar.x + bar.width // 2
        ball.y = HEIGHT - HEIGHT // 8
        if ball.explosionCounter > 100:
            resetBall(ball,bar)

    for i in range(len(extraBalls) - 1,-1,-1):
        if extraBalls[i].dead and ball.explosionCounter > 100:
            extraBalls.pop(i)       

def resetBoard(ball,board):
    if board.getBlockAmount() == 0:
        board.board = createLevel() 
        board.extraBalls = []
        ball.y = HEIGHT + HEIGHT // 2
        board.blockHeight = (HEIGHT - HEIGHT // 2) // len(board.board)
        board.blockWidth = WIDTH // len(board.board[0])


def main():
    run = True
    ball = Ball(WIDTH // 2,HEIGHT - HEIGHT // 8, 10,1,-1,10,WHITE)
    bar = Bar(WIDTH // 2 - 50,HEIGHT - HEIGHT // 16,(100,20),10,WHITE)
    board = Board(createLevel())
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        killBall(ball,board.extraBalls,bar)
        resetBoard(ball,board)
        
        checkCollisions(ball,board.extraBalls,bar)
        display(screen,ball,bar,board)
        # print(clock.get_fps())

    pygame.quit()


main()


