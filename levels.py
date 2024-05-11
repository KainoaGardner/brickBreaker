from game import Block
from settings import *

level1 = []

for r in range(20):
    row = []
    for c in range(20):
        if c < 18:
            row.append(Block(RED))     
        else:
            row.append(None)
    if 2 < r < 10 or r > 14 :
        level1.append(row)
    else:
        level1.append([None] * 20)


