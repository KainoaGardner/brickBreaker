from game import Block
from settings import *
from random import choice,randint
from collections import defaultdict

colors = [RED,ORANGE,YELLOW,GREEN,BLUE,PURPLE]

def createLevel():
    level = []

    choice = randint(0,3)
    height = randint(6,12)
    width = height
    while WIDTH // width != WIDTH / width:
        width -= 1

    match choice:
        case 0:
            level = level1(height,width)
        case 1:
            level = level2(height,width)
        case 2:
            level = level3(height,width)
        case 3:
            level = level4(height,width)

    return level

       

def level1(height,width):
    level = []
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
    return level

def level2(height,width):
    level = []
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

    return level

def level3(height,width):
    level = []
    for r in range(height):
       row = []
       for c in range(width):
           if randint(1,3) <= 1:
               color = randint(0,10)
               if color == 0:
                   row.append(Block(colors[randint(0,len(colors) - 1)]))
               else:
                   row.append(Block(TILEGRAY))
           else:
               row.append(None)
       level.append(row)
    
    return level

def level4(height,width):
    level = []

    noPlaceC = defaultdict(bool)
    for _ in range(randint(1,width // 2)):
        noPlaceC[randint(0,width - 1)] = True

    noPlaceR = defaultdict(bool)
    for _ in range(randint(1,height // 2)):
        noPlaceR[randint(0,height - 1)] = True



    for r in range(height):
        row = []
        for c in range(width):
            if c not in noPlaceC:
                color = randint(0,10)
                if color == 0:
                    row.append(Block(colors[randint(0,len(colors) - 1)]))
                else:
                    row.append(Block(TILEGRAY))
            else:
                row.append(None)
        if r not in noPlaceR:
            level.append(row)
        else:
            level.append([None] * width)


    return level


   # else:
    #     for r in range(height):
    #         row = []
    #         for c in range(width):
    #             color = randint(0,5)
    #             row.append(Block(colors[color]))
    #         level.append(row)
    #
    return level
