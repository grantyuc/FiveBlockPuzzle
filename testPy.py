#!/usr/bin/env python3
# coding=utf-8
# First try in 2017 fall with recursively DFS
# By Grant Chen

class BlockBox:
    def __init__(self, hight, width):
        self.hight = hight
        self.width = width
        self.slot = [[0 for x in range(6)] for y in range(10)]
        self.blocksPos = []

    def put(self, block, position):
        self.blocksPos.append((block, position))
        for i in range(len(block.shape)): 
            for j in range(len(block.shape[0])):
                self.slot[i+position[0]][j+position[1]] += block.shape[i][j]

    def pop(self):
        block, position = self.blocksPos.pop()
        for i in range(len(block.shape)): 
            for j in range(len(block.shape[0])):
                self.slot[i+position[0]][j+position[1]] -= block.shape[i][j]
        return block

    def isConflict(self):
        for row in self.slot:
            for x in row:
                if x>1:
                    return True
        return self.withHole()

    def withHole(self):
        emptyAdjNum = [[0 for x in range(6)] for y in range(10)]
        emptyAdjNum = [[emptyAdjNum[i][j]+1 if i<9 and self.slot[i+1][j] == 0 else emptyAdjNum[i][j] for j in range(6)] for i in range(10)]
        emptyAdjNum = [[emptyAdjNum[i][j]+1 if i>0 and self.slot[i-1][j] == 0 else emptyAdjNum[i][j] for j in range(6)] for i in range(10)]
        emptyAdjNum = [[emptyAdjNum[i][j]+1 if j<5 and self.slot[i][j+1] == 0 else emptyAdjNum[i][j] for j in range(6)] for i in range(10)]
        emptyAdjNum = [[emptyAdjNum[i][j]+1 if j>0 and self.slot[i][j-1] == 0 else emptyAdjNum[i][j] for j in range(6)] for i in range(10)]
        emptyAdjNum = [[9 if self.slot[i][j]   == 1 else emptyAdjNum[i][j] for j in range(6)] for i in range(10)]
        
#        print('EmptyAdjNum:')
#        for row in emptyAdjNum:
#            for x in row:
#                print(x, end=' ')
#            print()
        
        for j in range(10):
            ls = emptyAdjNum[j]
            if 0 in ls:
                return True
            i=-1
            while 1 in ls[i+1:]:
                i = ls.index(1)
                if j<9 and emptyAdjNum[j+1][i] == 1 or i<5 and ls[i+1] == 1 or \
                    j<9 and emptyAdjNum[j+1][i] == 2 and \
                    (i<5 and emptyAdjNum[j+1][i+1] == 1 or i>0 and emptyAdjNum[j+1][i-1] == 1 or j<8 and emptyAdjNum[j+2][i] == 1) or \
                    i<5 and emptyAdjNum[j][i+1] == 2 and (j<9 and emptyAdjNum[j+1][i+1] == 1 or i<4 and emptyAdjNum[j][i+2] == 1) or \
                    i>0 and emptyAdjNum[j][i-1] == 2 and (j<9 and emptyAdjNum[j+1][i-1] == 1):
                    return True
                else: 
                    break
        return False

    def printBox(self):
        for row in self.slot:
            for x in row:
                print(x, end= ' ')
            print()
        for block, pos in self.blocksPos:
            print('At', pos, end=' ')
            block.printBlock()

class Block:
    blocks = [[0,1,0],[1,1,1],[0,1,0]], [[1,1,1,1,1]], [[1,1,1],[1,0,1]], [[1,1,1],[1,0,0],[1,0,0]], [[1,0,0],[1,1,1],[0,0,1]], [[1,1,1],[0,1,0],[0,1,0]], [[0,1,1],[1,1,0],[1,0,0]], [[1,1,1],[1,1,0]], [[1,1,1,1],[0,1,0,0]], [[1,1,1,1],[1,0,0,0]], [[1,1,1,0],[0,0,1,1]], [[1,0,0],[1,1,1],[0,1,0]]
    oriens = 1, 2, *(4 for x in range(10))
    flips = *(1 for x in range(6)), *(2 for x in range(6))

    def __init__(self, blockType):
        self.blockType = blockType
        self.shape = Block.blocks[blockType]
        self.orien = 0
        self.flip = 0

    def getOrienNum(self):
        return Block.oriens[self.blockType]

    def getFlipNum(self):
        return Block.flips[self.blockType]

    def cwRotate(self):
        self.orien = self.orien + 1
        self.orien %= self.getOrienNum()
        self.shape.reverse()
        self.shape = [[row[x] for row in self.shape] for x in range(len(self.shape[0]))]

    def udFlip(self):
        if self.getFlipNum() != 1:
            self.flip = 1 - self.flip
        self.shape.reverse()

    def printBlock(self):
        print("Block Type", self.blockType, "with Orientation:", self.orien, "Flip:", self.flip)
        for row in self.shape:
            for x in row:
                print(x, end=' ')
            print()

def SolveBlockPuzzle(box, blocks):
#    print('Enter SBP Part')
    if not blocks:
        print('Find a solution!')
        return True
    else:
        block = blocks[0]
        if len(blocks) < 3:
#            print('.', end='')
#            if len(blocks) < 3:
            box.printBox()
#        print('Try put ', end='')
#        block.printBlock()
#        print('in box')
#        box.printBox()
        for orien in range(block.getOrienNum()):
            for flip in range(block.getFlipNum()):
                for i in range(0, 10-len(block.shape)+1):
                    for j in range(0, 6-len(block.shape[0])+1):
                        position = (i, j)
                        box.put(block, position)
                        if box.isConflict():
                            box.pop()
                        else:
#                            print('At', position, ', Put ', end='')
#                            block.printBlock()
#                            print('Box:')
#                            box.printBox()
                            result = SolveBlockPuzzle(box, blocks[1:])
                            if not result:
                                box.pop()
                            else:
                                return True
                if block.getFlipNum() != 1:
                    block.udFlip()
            block.cwRotate()
#        print('Leaving SBP Part False')
        return False

boxSolutions = []
box = BlockBox(10, 6)
print("A", box.hight, "x", box.width, "blockbox.")
#box.printBox()

blocks = [Block(i) for i in range(12)]

for i0 in range(0,4):
    for j0 in range(0,2):
        if i0==j0==0:
           continue 
        position = (i0, j0)
        box.put(blocks[0], position)
        if box.isConflict():
            box.pop()
        else:
            print('At', position, ', Put ', end='')
            blocks[0].printBlock()
#            print('Box:')
#            box.printBox()
            result = SolveBlockPuzzle(box, blocks[1:])
            if result == True:
                boxSolutions.append(box)
                box.printBox()
                box = BlockBox(10, 6)
else:
    print('\n***********************************\n')   
    print('Solution Number:', len(boxSolutions))
    for boxsol in boxSolutions:
        boxsol.printBox()
        print()  


'''
for block in blocks:
    block.printBlock()
        print('Try put ', block)
        print('Try put ', block)
        print('Try put ', block)
        print('Try put ', block)
        print('Try put ', block)
        print('Try put ', block)
        print('Try put ', block)
    print("CW Rotate:")
    block.cwRotate()
    block.printBlock()
    print("UD Flip:")
    block.udFlip()
    block.printBlock()
    '''
