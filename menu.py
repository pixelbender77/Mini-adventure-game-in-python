import pygame, sys,time, random
from pygame.locals import*
pygame.init()
pygame.display.set_caption("Game menu")
size=(1000,700)
screen=pygame.display.set_mode(size)
time=pygame.time.Clock()
blur=pygame.Surface(size); block=pygame.Surface(size)
def load(name):
    return pygame.image.load(name)
def resize(image_obj,size):
    return pygame.transform.scale(image_obj,size)
def message(word,xy,size,color,writing):
    font=pygame.font.SysFont(writing,size,False)
    msg=font.render(str(word),True,color)
    screen.blit(msg,xy)

def Menu():
    blur=pygame.Surface(size); block=pygame.Surface(size); out=False
    form=[(0, 0, 66),(255, 255, 0)] #lighted and nor lighted
    state=[0,0,0]
    while not out :
        screen.fill((100,200,250)) #this represents everything that will be behind( inside the darkened layer)

        blur.set_alpha(100)
        blur.fill((0,0,0))
        block.set_alpha(200)
        screen.blit(blur,[0,0])
        pygame.draw.rect(block,(0, 150, 255),(295,145,410,410));pygame.draw.rect(block,(0, 50, 100),(300,150,400,400));sub=40
        message("Paused",[390,100],70,(0, 0, 0),"forte")
        message("Resume",[320,270-sub],40,form[state[0]],"calibri")
        message("Options",[320,360-sub],40,form[state[1]],"calibri")
        message("Main Menu",[320,450-sub],40,form[state[2]],"calibri")
        j=0
        for i in range(230,500,90):#checking the 3 rectangles
            pygame.draw.rect(block,(0, 15, 55),(320,i,250,40))
            if pygame.Rect(320,i,250,40).collidepoint(pygame.mouse.get_pos()):
                state[j]=1 #if mouse  collids with button, then we switch it's state to 1
            else: 
                state[j]=0 #and if it is'nt, we set it to 0
            j+=1  #increamenting j , to point at the next button index
        screen.blit(block,[0,0])
        for event in pygame.event.get():
            if event.type==QUIT:
                out=True
            if event.type==MOUSEBUTTONDOWN: #if mouse is pressed..
                if state[0]==1: #if the mouse was on the first button, we start the game since button says "start game"
                    fade(fade_surface,0) # Fading out the screen(in black) to introduce the game, speed of fading
                    print("Start Game")
                if state[1]==1: #same comment as above and below
                    print("Credits")
                if state[2]==1: # if the state of the 3 button is 1(the mouse is on it).Then we exit since the button says"Exit":-]
                    out=True

        
        pygame.display.update()  
        time.tick(20)  

fade_surface=pygame.Surface(size) # Creating a surface
fade_surface.fill((0,0,0)) # the color of the surface is black
def fade(surface,speed):
    for alpha in range(0,250,25): #darkening the screen progressively by 25 units each time
        fade_surface.set_alpha(alpha)  #setting a darker transparency at each loop
        screen.blit(back,[-5,-10])
        #Below we are redrawing the Game menu
        pygame.draw.rect(screen,state[ste[0]][0],[355,205,250,state[ste[0]][1]]) #ste is the state for a particular button
        pygame.draw.rect(screen,state[ste[1]][0],[355,305,250,state[ste[1]][1]]) #state holds the two possible states
        pygame.draw.rect(screen,state[ste[2]][0],[355,405,250,state[ste[2]][1]]) #ste passes it's value to state and the color and button size for that 
        message("Start Game",[405,210],state[ste[0]][3],state[ste[0]][2],"28 Days Later")
        message("Credits",[435,310],state[ste[1]][3],state[ste[1]][2],"28 Days Later")
        message("Exit",[460,410],state[ste[2]][3],state[ste[2]][2],"28 Days Later")
        screen.blit(fade_surface,[0,0])
        pygame.display.update()
        pygame.time.delay(speed)

exit_=False
back=load("maps/menu.png")
#back=resize(back,[1010,710]) # below in each of the two sublists, we have color,size of button and font,size of writing for each of the two state(lighted or pointed and unlighted)
state=[[(63,49,81),40,(159, 90, 125),30],[(0,32,96),55,(33, 137, 197),33]] #the first part of the list contains the size and color of the unlighted button, and the second for the lighted button
ste=[0,0,0] #this is the list that will contain the state of each of the 3 buttons
#Main Loop
screen.fill((100,200,250))
while not exit_ :

    mouse=pygame.mouse.get_pos()
    screen.blit(back,[-5,-10])
    pygame.draw.rect(screen,(0,0,0),[mouse[0],mouse[1],0.5,0.5])
    pygame.draw.rect(screen,state[ste[0]][0],[355,205,250,state[ste[0]][1]]) #ste is the state for a particular button
    pygame.draw.rect(screen,state[ste[1]][0],[355,305,250,state[ste[1]][1]]) #state holds the two possible states
    pygame.draw.rect(screen,state[ste[2]][0],[355,405,250,state[ste[2]][1]]) #ste passes it's value to state and the color and button size for that 
    message("Start Game",[405,210],state[ste[0]][3],state[ste[0]][2],"28 Days Later")
    message("Credits",[435,310],state[ste[1]][3],state[ste[1]][2],"28 Days Later")
    message("Exit",[460,410],state[ste[2]][3],state[ste[2]][2],"28 Days Later")
    j=0                                                                      #state is applied :-)
    for i in range(205,406,100):#checking the 3 rectangles
        if pygame.Rect(355,i,250,40).collidepoint(pygame.mouse.get_pos()):
            ste[j]=1 #if mouse  collids with button, then we switch it's state to 1
        else: 
            ste[j]=0 #and if it is'nt, we set it to 0
        j+=1  #increamenting j , to point at the next button index
    
    for event in pygame.event.get():
        if event.type==QUIT:
            exit_=True
        if event.type==MOUSEBUTTONDOWN: #if mouse is pressed..
            if ste[0]==1: #if the mouse was on the first button, we start the game since button says "start game"
                fade(fade_surface,0) # Fading out the screen(in black) to introduce the game, speed of fading
                print("Start Game")
            if ste[1]==1: #same comment as above and below
                print("Credits")
            if ste[2]==1: # if the state of the 3 button is 1(the mouse is on it).Then we exit since the button says"Exit":-]
                exit_=True
    
    #message("Surviver Escape",[150,100],110,(0,0,0),"chiller")
    #screen.blit(bult,[300,500])
    pygame.display.update()
    time.tick(40)
pygame.quit()