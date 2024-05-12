from game import Block
from settings import *
from random import choice,randint
from collections import defaultdict

colors = [RED,ORANGE,YELLOW,GREEN,BLUE,PURPLE]

def createLevel():
    level = []

    choice = randint(0,1)
    height = randint(8,16)
    width = randint(8,16)


    while WIDTH // width != WIDTH / width:
        width -= 1
        
    if choice == 0:
        noPlace = defaultdict(bool)
        for _ in range(randint(1,height // 2)):
            noPlace[randint(0,height - 1)] = True

        for r in range(height):
            row = []
            color = randint(0,5)
            for c in range(width):
                if not noPlace[r]:
                    color = randint(0,10)
                    if color == 0:
                        row.append(Block(colors[randint(0,len(colors) - 1)]))
                    else:
                        row.append(Block(TILEGRAY))
                else:
                    row.append(None)
            level.append(row)

    if choice == 1:
        noPlace = defaultdict(bool)
        for _ in range(randint(1,width // 2)):
            noPlace[randint(0,width - 1)] = True

        for r in range(height):
            row = []
            for c in range(width):
                if not noPlace[c]:
                    color = randint(0,10)
                    if color == 0:
                        row.append(Block(colors[randint(0,len(colors) - 1)]))
                    else:
                        row.append(Block(TILEGRAY))
                else:
                    row.append(None)
            level.append(row)


   # else:
    #     for r in range(height):
    #         row = []
    #         for c in range(width):
    #             color = randint(0,5)
    #             row.append(Block(colors[color]))
    #         level.append(row)
    #
    return level
