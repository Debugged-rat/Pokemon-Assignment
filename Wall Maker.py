import pygame, sys, os
from pygame import *

def getPath(file, join="/"):
    return os.path.dirname(os.path.abspath(__file__)) + join + file

pygame.init()

FPS = 60
fpsClock = pygame.time.Clock()

WIN = pygame.display.set_mode((600, 600))
pygame.display.set_caption("")

gameMap = pygame.image.load(getPath("Game Map.png"))

wallList = []
eachWall = []

while True:
    WIN.blit(gameMap, (0, 0))
    pos = pygame.mouse.get_pos()
    print(pos)

    for x in wallList:
        pygame.draw.rect(WIN, (200, 0, 0), (x[0], x[1], x[2], x[3]), 5)
        pygame.draw.rect(WIN, (0, 200, 0), (x[0], x[1], x[2], x[3]))

    for event in pygame.event.get():
        if event.type == QUIT:
            print(wallList)
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if len(eachWall) == 0:
                eachWall.append(pos[0])
                eachWall.append(pos[1])
            elif len(eachWall) == 2:
                eachWall.append(pos[0] -  eachWall[0])
                eachWall.append(pos[1] -  eachWall[1])
                wallList.append(eachWall)
                eachWall = []
   
    pygame.display.update()
    fpsClock.tick(FPS)