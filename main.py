import pygame
from pygame.constants import MOUSEBUTTONDOWN
from dijkstras_algorithm import mainGame as dja
from a_start_no_diagonals import mainGame as a_no_diag
from a_star_with_diagonals import mainGame as a_with_diag
pygame.init()

WHITE=(255,255,255)
GREEN=(0,255,0)
WIN=pygame.display.set_mode((500,500))
pygame.display.set_caption("Main Menu")

class Button:
    def __init__(self,color,text,x,y,w,h) -> None:
        self.color=color
        self.text=text
        self.x=x
        self.y=y
        self.width=w
        self.height=h
        self.selected=False
    def draw(self,win,border=None):
        if border:
            pygame.draw.rect(win,border,(self.x-2,self.y,self.width+4,self.height+4))
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.height))
        if self.text!='':
            myfont = pygame.font.SysFont('Comic Sans MS', 25)
            text= myfont.render(self.text, 1, (0, 0, 0))
            win.blit(text,(self.x+(self.width/2-text.get_width()/2),self.y+(self.height/2-text.get_height()/2)))
    def isClicked(self,pos):
        x,y=pos
        return x>=self.x and x<=self.x+self.width and y>=self.y and y<=self.y+self.height



b1=Button(GREEN,"Dijkstra's Algorithm",50,50,400,100)
b2=Button(GREEN,"A* Algorithm Without Diagonals",50,160,400,100)
b3=Button(GREEN,"A* Algorithm With Diagonals",50,270,400,100)
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
        if event.type==MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                pos=pygame.mouse.get_pos()
                if b1.isClicked(pos):
                    dja()
                elif b2.isClicked(pos):
                    a_no_diag()
                elif b3.isClicked(pos):
                    a_with_diag()

    WIN.fill(WHITE)
    b1.draw(WIN,2)
    b2.draw(WIN,2)
    b3.draw(WIN,2)
    pygame.display.update()