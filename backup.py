import pygame,random,time,sys
from pygame.locals import*
pygame.init()
time=pygame.time.Clock()
size=(1000,700)
pygame.display.set_caption("Mr. Black")
screen=pygame.display.set_mode(size)

class player():
    def __init__(self,pos,size,speed):
        self.pos=pos
        self.size=size
        self.rect=(self.pos[0],self.pos[1],self.size[0],self.size[1])
        self.foot=(self.pos[0]+20,self.pos[1]+self.size[1]-2,self.size[0]-40,8) #this is the rectangle under the player that will serve as guard for falling
        self.Rhand=(self.pos[0]+(self.size[0]-8),self.pos[1]+50,8,self.size[1]-75)#Right hand rectangle used for obstacle collider detection
        self.Lhand=(self.pos[0],self.pos[1]+50,8,self.size[1]-75)#Legt hand rectangle .... as above
        self.damage=10 #the damage the bullets loaded by the hero will have
        self.count=0 #count for sprite animation
        self.state=[1,0]#[1=Right 0=Left, (0=idle, 1=move , 2=attack , 3=jump, 4=harmed , 5=die, 6=fall)]
        self.health=100
        self.speed=speed
        self.Jcount=10 #Jumpcount
        self.leftway=True # There is no obstacle on the emidiate left (initially)
        self.rightway=True # There is no obstacle ont the emidiate right  (initially)
        self.foot_on_ground=True
    
    def show(self):
        self.rect=(self.pos[0],self.pos[1],self.size[0],self.size[1])
        self.foot=(self.pos[0]+20,self.pos[1]+self.size[1]-8,self.size[0]-40,8)
        self.Rhand=(self.pos[0]+(self.size[0]-8),self.pos[1]+50,8,self.size[1]-75)
        self.Lhand=(self.pos[0],self.pos[1]+50,8,self.size[1]-75)
        pygame.draw.rect(screen,(12,56,216),self.rect)
        pygame.draw.rect(screen,(0,0,0),self.foot)
        pygame.draw.rect(screen,(103,88,115),self.Rhand)
        pygame.draw.rect(screen,(12,99,114),self.Lhand)
        print(self.pos[1])
    
    def check_foot(self,obstacle): #this function checks the foot of the player relative to the flour and all the obstacles to see if it standing on top of an obstacle or on top of the flour
        self.foot=(self.pos[0]+20,self.pos[1]+self.size[1]-8,self.size[0]-40,8)
        for i in range(len(obstacle)):
            obstacle[i].rect=(obstacle[i].pos[0],obstacle[i].pos[1],obstacle[i].size[0],obstacle[i].size[1])
            if  (pygame.Rect(self.foot).colliderect(obstacle[i].rect)) or (pygame.Rect(self.foot).colliderect(0,590,1000,200)): 
                self.foot_on_ground=True;break #if the foot rect is touching an obstacle or even the flour, the the player's foot is on a ground
                #print("Foot on ground"); #as soon as it is found that player is touching a surface, we break the loop to stop further search
            else:
                self.foot_on_ground=False # else, the player's foot is not on a ground
                #print("foot not! on ground")
        if pygame.Rect(self.foot).colliderect(0,580,1000,200):
            self.pos[1]=470
        if pygame.Rect(self.foot).colliderect(obstacle[i].rect):
            self.pos[1]=obstacle[i].pos[1]-self.size[1]+3

    def check_jump(self): #This function keeps track of jumping if the player is in the jumpstate(state==3)
        if self.state[1]==3 and not(self.foot_on_ground) :  # (if player is in the jump state..) (jump process stops)
            if (self.Jcount>=-10) : # is the jumpcount over and has player landed somewhere??..
                direction=1 # it  determines the going up or down of the sprite
                if self.Jcount<0:
                    direction=-1
                self.pos[1]-=(self.Jcount**2)*0.5*direction
                self.Jcount-=1
            else:
                self.Jcount=10 #setting back or initializing Jump count to 10
                self.state[1]=0 #when player has landed, we then set it's state to idle: to stop it from jumping further   
        #if the foot of the hero is not touching neither an obstacle(is not standing on an obstacle) nor the flour and is not in the jump state.. then it should be set to be falling
        if self.foot_on_ground:
            self.Jcount=10;self.state[1]=0

    def check_state(self,obstacle):
        self.Rhand=(self.pos[0]+(self.size[0]-8),self.pos[1]+50,8,self.size[1]-75)
        self.Lhand=(self.pos[0],self.pos[1]+50,8,self.size[1]-75)
        for i in range(len(obstacle)):
            obstacle[i].rect=(obstacle[i].pos[0],obstacle[i].pos[1],obstacle[i].size[0],obstacle[i].size[1])
            if not(self.foot_on_ground) and (self.state[1]!=3): #if player's foot are not touching the ground and he is not jumping,.. then he is falling!!
                print("you are falling!")
                self.Jcount=10
                self.pos[1]+=5
                self.state[1]=6 # state=6 is the falling state and will help to display the falling hero sprite
                
            if pygame.Rect(self.Rhand).colliderect(obstacle[i].rect): #if righthand rectangle is touching an obstacle, then there no way on the right. 
                self.rightway=False; break #as soon as we discover an obstacle on the right side, we don't seek further
            else:
                self.rightway=True
            if pygame.Rect(self.Lhand).colliderect(obstacle[i].rect): #same comment as above
                self.leftway=False; break #as soon we discover....(same comment as above)
            else:
                self.leftway=True

        
class ennemies():
    def __init__(self,pos,size,health,damage): #damage and health will later be randomized to make ennemies have different effects
        self.pos=pos
        self.size=size
        self.rect=[self.pos[0],self.pos[1],self.size[0],self.size[1]]
        self.damage=damage
        self.count=1
        self.state=[0,1]#[left or right, 1=move 2=attack 3=harmed 4=dead]
        self.exist=True
        self.health=health
        self.type=1 #1=walker 2=Ghost 3=Boss
        self.speed=5

    def show(self):
        self.rect=[self.pos[0],self.pos[1],self.size[0],self.size[1]]
        pygame.draw.rect(screen,(55,200,166),self.rect)
    def keep_track(self,hero):
        if self.exist:#if the x coodinate of the ennemy is greater than that of the hero+it's size then ennemy will move forward
            if self.pos[0]>hero.pos[0]+hero.size[1]: 
                self.pos[0]-=self.speed #move left towards the hero
            if self.pos[0]+self.size[0]<hero.pos[0]:# if the x coodinate is instead less than( ennemy is at the left of hero)
                self.pos[0]+=self.speed  #move right towards the hero     
            self.show()
             
class bullet():
    def __init__(self,pos,size,damage,target,owner,direction,speed):
        self.pos=pos
        self.size=size
        self.rect=(self.pos[0],self.pos[1],self.size[0],self.size[1])
        self.damage=damage
        self.exist=False
        self.owner=owner #0=Player 1=ennemy This is what will determine the appearance of the bullet.
        self.target=target
        self.direction=direction #-1 and 1 
        self.speed=speed
    def move(self):
        self.pos[0]+=(self.speed*self.direction)
    
    def show(self):
        self.rect=(self.pos[0],self.pos[1],self.size[0],self.size[1])
        pygame.draw.rect(screen,(0,0,0),self.rect)
    
    def check(self):
        if self.pos[0]>1000 or self.pos[0]<-75 : #ie if ball has exceeded screen boundries, then it stops existing.
            self.exist=False 
        if self.owner==0: #if the owner of the bullet is our hero..
            print('owner is hero')
            for i in range(1):#cross checking all ennemies to see if the bullet has collide somewhere
                if self.target[i].exist: #Does the ennemy we are about to check for collision exists?...
                    if pygame.Rect(self.rect).colliderect(self.target[i].rect): #if the bullet collides with its target..
                        print('collided')
                        self.target[i].health-=self.damage # the health of the target reduces by the amount of damagecapacity given to the bullet by the sender 
                        if self.target[i].health<=0: #if target has no health left, then is must stop existing! :-] 
                            self.target[i].exist=False
                        self.exist=False #and the bullet stops existing
        
    def keep_track(self):
        if self.exist:
            self.show()
            self.move()
            self.check()
#def Track(): #This function is not!! part of the bullet class!!

class Environment():
    def __init__(self):
        self.pos=[0,0] #initialy we are at the begining of the game levels at x=0
        self.ground=[0,600,1200] #The initial x coodinate of the 3flour images
        self.mid=600 #the middle of the field. when traversed increases the x value of the self pos. Also, flour shifts behind , the buildings too , giving the impression of moving forward 
        self.speed=15 #this is the variable which will shift all the obstacles and ennemies to the visible screeen every time the player will cross screen mid as seen above
    def shift(self,obstacle,ennemy):
        for i in range(len(obstacle)): # crosschecking all the the obstacles
            obstacle[i].pos[0]-=self.speed # shifting progressively all the obstacles to the left, so they can be seen be the player
                                            #in order words we are giving the impression to the player of moving forward in a wide and long environment

class obstacles():
    def __init__(self,pos,size):
        self.size=size
        self.pos=pos
        self.rect=(self.pos[0],self.pos[1],self.size[0],self.size[1])
        self.exist=True # Later ennemies can destroy obstacles but not the player
    def show(self):
        self.rect=(self.pos[0],self.pos[1],self.size[0],self.size[1])
        if self.pos[0]<1300 and self.pos[0]>-300 : #if the obstacle exists on the field... (has not been destroyed by ennemy or player has simple reach its level )
            pygame.draw.rect(screen,(175,166,42),self.rect) #the 300 i added to the boarders above is to make the quiting out of the screen of the obstacles not brusque, but gentle and progressive till the last pixel of that obstacle

obstacle=[]
def generate_obstacles():
    for count in range(0,10): #Creating 10 obstacles
        i=random.randrange(0,30)#randomizing the length of the obstacles
        obstacle.append(obstacles([500,430-i],[131+i,165+i]) )
    obstacle[0].pos[0]=500; obstacle[1].pos[0]=521; obstacle[2].pos[0]=1031; obstacle[3].pos[0]=1906; obstacle[4].pos[0]=2013
    obstacle[5].pos[0]=2600; obstacle[6].pos[0]=4000; obstacle[7].pos[0]=4500; obstacle[8].pos[0]=5003; obstacle[9].pos[0]=6000
    #Above, we are saying exactly were (in terms of x coordinate) the obstacles will be


ennemy=[ennemies([600,500],[95,120],100,5)]
hero=player([100,470],[100,130],10)
fire1=[bullet([100,580],[20,8],10,ennemy,hero,1,5)]
badball=[bullet([100,580],[20,8],10,hero,ennemy,1,10)]
environment=Environment()
day=pygame.image.load("maps/day.png");day=pygame.transform.scale(day,[1000,700])#;day=pygame.transform.rotate(day,180);day=pygame.transform.flip(day,True,False)
dawn=pygame.image.load("maps/dawn.png");dawn=pygame.transform.scale(dawn,[1000,700])
night=pygame.image.load("maps/night.png");night=pygame.transform.scale(night,[1000,700])
sky=[day,dawn,night]
done=False
generate_obstacles()
while not done :
    screen.fill((250,240,231))
    for event in pygame.event.get():
        if event.type==QUIT:
            done=True
    keys=pygame.key.get_pressed()
    if keys[K_RIGHT] and hero.rightway :# if key is pressed and there are no obstacles on the right side of the player
        if hero.pos[0]>=environment.mid: #if player has traversed the middle of the screen, he does not move forward anymore, but the environment(obstacles,ennemies) infront shifts back to him
            environment.shift(obstacle,ennemy)
        else:
            hero.pos[0]+=hero.speed #but if player is not after mid, then he moves forward
        if hero.state[1]!=3: #if the player is not in the jump state, then we assign the running sprite. else we leave the game to show us the jumping sprite image
            hero.state=[1,1] #right,motion

    elif keys[K_LEFT] and hero.leftway : # if key is pressed and there are no obstacles on the left side of the player
        hero.pos[0]-=hero.speed
        if hero.state[1]!=3: #(same comment as above) state 3 is the jumping state
            hero.state=[0,1] #left,motion
    else:  
        if hero.state[1]!=3 and hero.state[1]!=6:# if player is not going left,not going right,not jumping and not falling..;-) then player should be set to idle state
            hero.state[1]=0 #state 0 is the idle state
    
    if keys[K_f] :
        if (not fire1[0].exist): #ie a new ball is created only if there exist no other one on the field
            if hero.state[0]==0 : #if player is looking left , we have to load a bullet in the left direction
                                #        pos                size  damage target owner direction speed
                fire1=[(bullet([hero.pos[0]-5,hero.pos[1]],[75,50],  10 ,ennemy,0  ,    -1 ,     20))]
            if hero.state[0]==1 : #if player is looking right, we instead load a bullet in the right direction
               fire1=[(bullet([hero.pos[0]+hero.size[0]+5,hero.pos[1]],[75,50],  10 ,ennemy,0  ,    1 ,     20))]
            fire1[0].exist=True
    
    elif keys[K_SPACE]:
        if hero.state[1]!=3 and hero.foot_on_ground : # if player is not jumping already,not falling,and has his foot on the ground, then a jump is possible( if user presses space)
            hero.state[1]=3
            hero.pos[1]-=10 #to avoid foot_on_ground inorder for the jump function to load
         
    #else:
    #    hero.state[1]=0 # if no key is pressed, we maintain the direction player is looking to, but set him to be idle


    
    hero.check_foot(obstacle) #checking whether or not player's foot is on ground( standing on an obstacle or on the ground).if not foot_on_ground is set to False else it is set to True
    hero.check_jump() #keeping track of the jumping motion if hero is in jumping state(state=3)
    hero.check_state(obstacle) #checking if player if does not have foot on ground and is not jumping and making him fall
    
    

    screen.blit(sky[0],[0,0]) #diplaying the sky
    hero.show()#displaying player
    fire1[0].keep_track()  #displaying and keeping track of the bullet 
    ennemy[0].keep_track(hero) # displaying and keeping track of the ennemies

    for i in range(len(obstacle)):
        obstacle[i].show() #displaying obstacles
    pygame.draw.rect(screen,(75,61,214),(0,595,1000,200)) #the flour
    pygame.display.update()
    time.tick(20)

pygame.quit()