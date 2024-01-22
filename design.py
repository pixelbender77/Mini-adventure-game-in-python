import pygame, sys,time, random
from pygame.locals import*
pygame.init()
pygame.display.set_caption("Game designs")
size=(1000,700)
screen=pygame.display.set_mode(size)
time=pygame.time.Clock()
done=False
def polygons(x,y):
    pale_color=(8, 88, 182);light_color=(8, 186, 254)
    pygame.draw.polygon(screen,light_color,([x-2,y-1],[x+20,y+8],[x+23,y+25],[x+5,y+35],[x-16,y+28],[x-20,y+10]));x-=27;y-=27
    pygame.draw.polygon(screen,pale_color,([x-2,y-1],[x+20,y+8],[x+23,y+25],[x+5,y+35],[x-16,y+28],[x-20,y+10]));x-=16;y+=31
    pygame.draw.polygon(screen,pale_color,([x-2,y-1],[x+20,y+8],[x+23,y+25],[x+5,y+35],[x-16,y+28],[x-20,y+10]))
    
while not done:
    for event in pygame.event.get():
        if event.type==QUIT:
            done=True
    polygons(900,600)
    
    pygame.display.update()
pygame.quit()