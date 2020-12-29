import pygame
from queue import PriorityQueue

from pygame.constants import K_SPACE

pygame.init()

BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
PURPLE=(128,0,128)
GREY=(128,128,128)
CYAN=(0,255,255)

WIDTH=600
HEIGHT=600
WIN=pygame.display.set_mode((WIDTH,HEIGHT))

TOTAL_ROWS=30

class Node:
    def __init__(self,row,col,total_rows):
        self.color=WHITE
        self.size=WIDTH//total_rows
        self.row=row
        self.col=col
        self.x=self.col*self.size
        self.y=self.row*self.size
        self.total_rows=total_rows
        self.neighbours=[]
        self.h_score=float("inf")
        self.parent=None
    def reset(self):
        self.color=WHITE
    def get_pos(self):
        return self.row,self.col
    def is_open(self):
        return self.color==CYAN
    def make_open(self):
        self.color=CYAN
    def is_start(self):
        return self.color==GREEN
    def make_start(self):
        self.color=GREEN
    def is_end(self):
        return self.color==BLUE
    def make_end(self):
        self.color=BLUE
    
    def is_closed(self):
        return self.color==RED
    def make_closed(self):
        self.color=RED

    def is_barrier(self):
        return self.color==BLACK
    def make_barrier(self):
        self.color=BLACK

    def is_path(self):
        return self.color==PURPLE
    def make_path(self):
        self.color=PURPLE
    
    def get_neighbours(self,grid):

        if self.row>0 and not grid[self.row-1][self.col].is_barrier():#UP
            self.neighbours.append( grid[self.row-1][self.col])

        if self.row<self.total_rows-1 and not grid[self.row+1][self.col].is_barrier():#DOWN
            self.neighbours.append( grid[self.row+1][self.col])

        if self.col>0 and not grid[self.row][self.col-1].is_barrier():#LEFT
            self.neighbours.append( grid[self.row][self.col-1])

        if self.col<self.total_rows-1 and not grid[self.row][self.col+1].is_barrier():#RIGTH
            self.neighbours.append( grid[self.row][self.col+1])

    def draw(self,win): 
        pygame.draw.rect(win,self.color,(self.x,self.y,self.size,self.size))

    # def get_h_score(self,endPos):
    #     x,y=endPos
    #     self.h_score=abs(self.row-x)+abs(self.col-y)
    #     return self.h_score

    
def make_grid():
    grid=[]
    for i in range(TOTAL_ROWS):
        row=[]
        for j in range(TOTAL_ROWS):
            node=Node(i,j,TOTAL_ROWS)
            row.append(node)
        grid.append(row)
    return grid

def draw_grid(win,grid):
    nodeWidth=WIDTH//TOTAL_ROWS
    for i in range(TOTAL_ROWS):
        pygame.draw.line(WIN,GREY,(0,i*nodeWidth),(WIDTH,i*nodeWidth))
        for j in range(TOTAL_ROWS):
            pygame.draw.line(WIN,GREY,(j*nodeWidth,0),(j*nodeWidth,HEIGHT))

def draw(window,grid):
    window.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(window)
    draw_grid(window,grid)
    pygame.display.update()

def get_click_pos(pos):
    nodeWidth=WIDTH//TOTAL_ROWS
    x,y=pos
    row=y//nodeWidth
    col=x//nodeWidth

    return row , col

def a_star_algorithm(grid,startNode,endNode):
    count=0
    queue=PriorityQueue()
    g_score={node:float("inf") for row in grid for node in row}
    g_score[startNode]=0
    queue.put((g_score[startNode],count,startNode))
    openSet={startNode}
    while not queue.empty():
        checkExit()
        currentNode=queue.get()[2] # Node with least f_score
        openSet.remove(currentNode)
        if currentNode==endNode:
            redraw_path(endNode,grid)
            return True
        if not len(currentNode.neighbours):
            return False
        for neighbour in currentNode.neighbours:
            if neighbour.is_closed():
                continue
            temp_g_score=1+g_score[currentNode]
            if(g_score[neighbour]>temp_g_score):
                neighbour.parent=currentNode
                g_score[neighbour]=temp_g_score
            if(neighbour not in openSet):
                count+=1
                queue.put((g_score[neighbour],count,neighbour))
                openSet.add(neighbour)
                neighbour.make_open()
            # draw(WIN,grid)
        draw(WIN,grid)
        if currentNode!=startNode:
            currentNode.make_closed()   

def redraw_path(endNode,grid):
    node=endNode
    while node.parent:
        checkExit()
        node.make_path()
        draw(WIN,grid)
        node=node.parent
    node.make_path()
    draw(WIN,grid)

def checkExit():
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
def mainGame():
    running=True
    startNode=None
    endNode=None
    started=False
    grid=make_grid()
    while running:
        draw(WIN,grid)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                running=False
            if pygame.mouse.get_pressed()[0]:
                if not started:
                    pos=pygame.mouse.get_pos()
                    row,col=get_click_pos(pos)
                    node=grid[row][col]
                    if not startNode:
                        node.make_start()
                        startNode=node
                    elif not endNode and not node.is_start():
                        node.make_end()
                        endNode=node
                    elif not node.is_start() and not node.is_end():
                        node.make_barrier()

            if pygame.mouse.get_pressed()[2]:
                if not started:
                    pos=pygame.mouse.get_pos()
                    row,col=get_click_pos(pos)
                    node=grid[row][col]
                    node.reset()
                    if startNode==node:
                        startNode=None
                    if endNode==node:
                        endNode==None
            if event.type==pygame.KEYDOWN:
                if event.key==K_SPACE and not started:
                    started=True
                    for row in grid:
                        for node in row:
                            # node.get_h_score(endNode.get_pos())
                            node.get_neighbours(grid)
                    if not a_star_algorithm(grid,startNode,endNode):
                        grid=make_grid()
                        running=True
                        startNode=None
                        endNode=None
                        started=False
                if event.key==pygame.K_r:
                    grid=make_grid()
                    running=True
                    startNode=None
                    endNode=None
                    started=False

if __name__ == "__main__":
    mainGame()