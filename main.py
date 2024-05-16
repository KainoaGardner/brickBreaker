import pygame
from settings import *
from random import choice
from game import Ball, Bar, Board
from button import buttons
from levels import *


pygame.init()
pygame.mixer.init()

gameOverSound = pygame.mixer.Sound("sounds/gameOver.wav")
gameOverSound.set_volume(0.5)
levelUpSound = pygame.mixer.Sound("sounds/getLevel.wav")
levelUpSound.set_volume(0.3)

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

def resetBall(ball,bar):
    if bar.direction == "right":
        ball.xVel = 1
    elif bar.direction == "left":
        ball.xVel = -1
    else:
        ball.xVel = choice((-1,1))
    ball.dead = False
    ball.yVel = -1

def killBall(ball,extraBalls,bar,board):
    if ball.dead and ball.explosionCounter >= 25:
        if ball.explosionCounter == 25:
            board.lives -= 1

            
        ball.color = WHITE
        ball.size = ball.backUpSize   
        ball.x = bar.x + bar.width // 2 - ball.size
        ball.y = HEIGHT - HEIGHT // 8
        if ball.explosionCounter > 100:
            resetBall(ball,bar)

    for i in range(len(extraBalls) - 1,-1,-1):
        if extraBalls[i].dead and ball.explosionCounter > 100:
            extraBalls.pop(i)       

def resetBoard(ball,board):
    if board.getBlockAmount() == 0:
        levelUpSound.play()       
        board.lives += 2
        board.board = createLevel() 
        board.extraBalls = []
        ball.y = HEIGHT + HEIGHT // 2
        board.blockHeight = (HEIGHT - HEIGHT // 2) // len(board.board)
        board.blockWidth = WIDTH // len(board.board[0])
        board.brokenBlocks = []

def updateGame(board):
    if board.lives <= 0:
        gameOverSound.play()
        return "Gameover"
    return "play"

font = pygame.font.Font("fonts/Lemon.otf",WIDTH // 16)
font2 = pygame.font.Font("fonts/Lemon.otf",WIDTH // 32)
titleText = font.render("Brick Breaker",True,WHITE)
startText = font2.render("Press SPACE to start!",True,WHITE)
gameOverText = font.render("Game Over!",True,WHITE)
resetText = font2.render("Press r to start!",True,WHITE)



def displayGameover(screen):
    screen.blit(gameOverText,(WIDTH // 2 - gameOverText.get_width() // 2,HEIGHT // 2 - gameOverText.get_height() // 2))
    screen.blit(resetText,(WIDTH // 2 - resetText.get_width() // 2,HEIGHT // 2 + gameOverText.get_height() - resetText.get_height() // 2)) 
    pygame.display.update()
    clock.tick(FPS)

def displayTitle(screen):
    screen.fill(BLACK)
    pygame.draw.rect(screen,"#3f3f3f",(MARGINSIZE,MARGINSIZE,WIDTH - MARGINSIZE * 2,HEIGHT - MARGINSIZE * 2))

    screen.blit(titleText,(WIDTH // 2 - titleText.get_width() // 2,HEIGHT // 2 - titleText.get_height() // 2))
    screen.blit(startText,(WIDTH // 2 - startText.get_width() // 2,HEIGHT // 2 + titleText.get_height() - startText.get_height() // 2))
    
    pygame.display.update()
    clock.tick(FPS)


def resetGame(ball,board,bar):
    ball.dead = True
    ball.explosionCounter = 26
    board.board = createLevel()
    board.lives = 3
    bar.x = WIDTH // 2 - 50
    bar.y = HEIGHT - HEIGHT // 16
    board.blockHeight = (HEIGHT - HEIGHT // 2) // len(board.board)
    board.blockWidth = WIDTH // len(board.board[0])
    board.brokenBlocks = []
    board.particles = []
    board.extraBalls = []
    board.score = 0
    board.text = board.font.render(str(board.score),True,LIGHTGRAY)

    
def main():
    run = True
    gameType = "Title"
    ball = Ball(WIDTH // 2,HEIGHT - HEIGHT // 8, 10,1,-1,10,WHITE)
    bar = Bar(WIDTH // 2 - 50,HEIGHT - HEIGHT // 16,(100,20),10,WHITE)
    board = Board(createLevel())
    resetGame(ball,board,bar)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and gameType != "Title":
                    resetGame(ball,board,bar)
                    gameType = "play"
                elif (event.key == pygame.K_r or event.key == pygame.K_SPACE) and gameType == "Title":
                    resetGame(ball,board,bar)
                    gameType = "play"


        
        if gameType == "Title":
            displayTitle(screen)
        elif gameType == "Gameover":
            displayGameover(screen)
        else:
            killBall(ball,board.extraBalls,bar,board)
            resetBoard(ball,board)
            gameType = updateGame(board)
            checkCollisions(ball,board.extraBalls,bar)
            display(screen,ball,bar,board)
            # print(clock.get_fps())

    pygame.quit()


main()


