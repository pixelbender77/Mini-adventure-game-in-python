import pygame,random,time,sys
from pygame.locals import*
pygame.init()
time=pygame.time.Clock()
size=(1000,700)
pygame.display.set_caption("Mr. Black")
screen=pygame.display.set_mode(size)

class player():
    def __init__(self,pos,size,speed,damage):
        self.pos=pos
        self.size=size
        self.rect=(self.pos[0],self.pos[1],self.size[0],self.size[1])
        self.foot=(self.pos[0]+20,self.pos[1]+self.size[1]-2,self.size[0]-40,8) #this is the rectangle under the player that will serve as guard for falling
        self.Rhand=(self.pos[0]+(self.size[0]-8),self.pos[1]+50,8,self.size[1]-75)#Right hand rectangle used for obstacle collider detection
        self.Lhand=(self.pos[0],self.pos[1]+50,8,self.size[1]-75)#Legt hand rectangle .... as above
        self.damage=damage #the damage the bullets loaded by the hero will have
        self.count=0 #count for sprite animation
        self.state=[1,0]#[1=Right 0=Left, (0=idle, 1=move , 2=attack , 3=jump, 4=harmed , 5=die, 6=fall)]
        self.health=200
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
        #print(self.pos[1])
    
    def check_foot(self,obstacle): #this function checks the foot of the player relative to the flour and all the obstacles to see if it standing on top of an obstacle or on top of the flour
        self.foot=(self.pos[0]+20,self.pos[1]+self.size[1]-8,self.size[0]-40,8)
        logical_foot=(self.pos[0]+20,self.pos[1]+self.size[1]-8,self.size[0]-40,20) #this logical foot is used for collision with obstacles
        for i in range(len(obstacle)):
            obstacle[i].rect=(obstacle[i].pos[0],obstacle[i].pos[1],obstacle[i].size[0],obstacle[i].size[1])
            if  (pygame.Rect(logical_foot).colliderect(obstacle[i].rect)) or (pygame.Rect(self.foot).colliderect(0,590,1000,200)): 
                self.foot_on_ground=True;break #if the foot rect is touching an obstacle or even the flour, the the player's foot is on a ground
                #print("Foot on ground"); #as soon as it is found that player is touching a surface, we break the loop to stop further search
            else:
                self.foot_on_ground=False # else, the player's foot is not on a ground
                #print("foot not! on ground")
        if pygame.Rect(self.foot).colliderect(0,580,1000,200):
            self.pos[1]=500
        if pygame.Rect(logical_foot).colliderect(obstacle[i].pos[0],obstacle[i].pos[1],obstacle[i].size[0],obstacle[i].size[1]): #here i did not put obstacle.rect because the logic rectangle is slightly different from the one shown on the screen
            self.pos[1]=obstacle[i].pos[1]-(self.size[1]) ; print("Adjusted")

    def check_jump(self): #This function keeps track of jumping if the player is in the jumpstate(state==3)
        if self.state[1]==3  :  # (if player is in the jump state..) (jump process stops)
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

    def check_state(self,obstacle,ennemy):
        self.rect=(self.pos[0],self.pos[1],self.size[0],self.size[1])
        self.Rhand=(self.pos[0]+(self.size[0]-8),self.pos[1]+50,8,self.size[1]-75)
        self.Lhand=(self.pos[0],self.pos[1]+50,8,self.size[1]-75)
        for i in range(len(obstacle)):
            obstacle[i].rect=(obstacle[i].pos[0],obstacle[i].pos[1],obstacle[i].size[0],obstacle[i].size[1])
            if not(self.foot_on_ground) and (self.state[1]!=3): #if player's foot are not touching the ground and he is not jumping,.. then he is falling!!
                print("you are falling!")
                self.Jcount=10
                self.pos[1]+=3
                self.state[1]=6 # state=6 is the falling state and will help to display the falling hero sprite
                
            if pygame.Rect(self.Rhand).colliderect(obstacle[i].rect): #if righthand rectangle is touching an obstacle, then there no way on the right. 
                self.rightway=False; break #as soon as we discover an obstacle on the right side, we don't seek further
            else:
                self.rightway=True
            if pygame.Rect(self.Lhand).colliderect(obstacle[i].rect): #same comment as above
                self.leftway=False; break #as soon we discover....(same comment as above)
            else:
                self.leftway=True
        for i in range(len(ennemy)):  #cross checking all ennemies to see if any of them are colliding(touching) our hero
            if ennemy[i].exist: #is the ennemy we are about to check for collision with our hero exist? if not, no need
                ennemy[i].rect=[ennemy[i].pos[0],ennemy[i].pos[1],ennemy[i].size[0],ennemy[i].size[1]]
                if pygame.Rect(self.rect).colliderect(ennemy[i].rect): #If the player touches the ennemy it's health decreases by 1
                    self.health-=ennemy[i].damage
                    if self.health<=0:
                        pygame.quit()
            
class ennemies():
    def __init__(self,pos,size,health,damage,shoot_probability,max_bullets): #damage and health will later be randomized to make ennemies have different effects
        self.pos=pos
        self.size=size
        self.rect=[self.pos[0],self.pos[1],self.size[0],self.size[1]]
        self.damage=damage
        self.count=1
        self.state=[0,1]#[left or right, 1=move 2=attack 3=harmed 4=dead]
        self.exist=True
        self.health=health
        self.type=1 #1=walker 2=Ghost 3=Boss
        self.speed=4.5
        self.shoot_probability=shoot_probability #This will determine how frequent the ennemy will shoot
        self.max_bullets=max_bullets
        self.shot=0 # initialy ennemy has shot no ball . but later when ennemy will shoot, we will make sure the number of bullets shot
                    #does not exeed the max_bullet
    def show(self):
        self.rect=[self.pos[0],self.pos[1],self.size[0],self.size[1]]
        pygame.draw.rect(screen,(55,200,166),self.rect)
    def keep_track(self,hero,fire2):
        if self.pos[0]<=1300: #we begin keeping track of ennemies when they are already close to the screen
            if self.exist:#if the x coodinate of the ennemy is greater than that of the hero+it's size then ennemy will move forward
                if self.pos[0]>hero.pos[0]+hero.size[1]-50: 
                    self.pos[0]-=self.speed #move left towards the hero
                    self.state=[0,1] #left and move state
                if self.pos[0]+self.size[0]<hero.pos[0]+50: #   if the x coodinate is instead less than( ennemy is at the left of hero)
                    self.pos[0]+=self.speed  #move right towards the hero     
                    self.state=[1,1] #rigth and move state
                self.show()
            
            if self.shot<=self.max_bullets: #if ennemy has not yet exeeded his limited number of bullets,then we can give him a chance to shoot
                shoot=random.randrange(self.shoot_probability) #....
                if shoot==10: # The probability of shooting is 1/self.shoot_probability
                    if self.state[0]==0 : #if ennemy is looking left , we have to load a bullet in the left direction
                                #        pos                            size damage target owner direction speed
                        fire2.append(bullet([self.pos[0]-5,self.pos[1]],[75,50],2, hero,     1  ,    -1 ,     15))
                    if self.state[0]==1 : #if ennemy is looking right, we instead load a bullet in the right direction
                        fire2.append(bullet([self.pos[0]+self.size[0]+5,self.pos[1]],[75,50],2,hero,1  ,    1 ,     15))
                    fire2[-1].exist=True # setting to True the existance of the last bullet(-1) of the list, that we just created
    
                
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
        if self.owner==0:
            color=(0,7,3)
        else :
            color=(91,2,22)
        pygame.draw.rect(screen,color,self.rect)
    
    def check(self):
        pop_it=0 #This is the variable the function will return telling the parent function to pop this particular bullet from the list or not                               
        if self.owner==0: #if the owner of the bullet is our hero..
            if self.pos[0]>1000 or self.pos[0]<-75 : #ie if ball has exceeded screen boundries, then it stops existing.
                self.exist=False; pop_it=1 # since bullet has exceeded screen boundries, it stops existing and we pop it from our list to save space:-)) 
            else:# since bullet has not yet exceeded boundries, then we can check the rest 
                print('owner is hero')
                for i in range(len(self.target)):#cross checking all ennemies to see if the bullet has collide somewhere
                    if self.target[i].exist: #Does the ennemy we are about to check for collision exists?...
                        if pygame.Rect(self.rect).colliderect(self.target[i].rect): #if the bullet collides with its target..
                            print('collided')
                            print(i)
                            self.target[i].health-=self.damage # the health of the target reduces by the amount of damagecapacity given to the bullet by the sender 
                            self.exist=False #and the bullet stops existing
                            pop_it=1 #Since bullet has collided with it's target, it stops existing an we can then permit it to be poped(removed)from our list to save space
                            if self.target[i].health<=0: #if target has no health left, then is must stop existing! :-] 
                                self.target[i].exist=False
                                    #and we can pop the target(ennemy ) from it's list to liberate space
            
        elif self.owner==1: #if the owner of the bullet is an ennemy..
            if self.pos[0]>1000 or self.pos[0]<-75 : #ie if ball has exceeded screen boundries, then it stops existing.
                    self.exist=False; pop_it=2 # since bullet has exceeded screen boundries, it stops existing and we pop it from our list to save space:-)) 
            else : # since bullet has not yet exceeded boundries, then we can check the rest 
                print('owner is ennemy')
                if pygame.Rect(self.rect).colliderect(self.target.rect): #if the bullet collides with its target..(hero in this case)
                    print('collided')
                    self.target.health-=self.damage # the health of the target reduces by the amount of damagecapacity given to the bullet by the sender 
                    self.exist=False #and the bullet stops existing
                    pop_it=2 #Since bullet has collided with it's target, it stops existing an we can then permit it to be poped(removed)from our list to save space
                    if self.target.health<=0: #if target has no health left, then is must stop existing! :-] 
                        self.target.exist=False
                        #since the target of the bullet in this case is the hero and that the hero is not a list, we write target.rect,target.exist.. etc.. since it is not a list :-}
        return pop_it
                        
        
    def keep_track(self):
        pop_it=False
        if self.exist:
            self.show()
            self.move()
            pop_it=self.check()
        return pop_it
#def Track(): #This function is not!! part of the bullet class!!

class Environment():
    def __init__(self,length):
        self.pos=[0,0] #initialy we are at the begining of the game levels at x=0
        self.ground=[0,600,1200] #The initial x coodinate of the 3flour images
        self.mid=600 #the middle of the field. when traversed increases the x value of the self pos. Also, flour shifts behind , the buildings too , giving the impression of moving forward 
        self.speed=12 #this is the variable which will shift all the obstacles and ennemies to the visible screeen every time the player will cross screen mid as seen above
        self.max_bullets=3 #a maximum of 3 bullets can be loaded on the field at a time. for a fourth to be loaded, one of three must either exceed the screen boundries or collide a target
        self.length=length
    def shift(self,obstacle,ennemy,fire1):
        self.pos[0]+=self.speed #incrementing the actual distance(pos[0] or x cordinate) of the environment
        print(self.pos[0])
        for i in range(len(obstacle)): # crosschecking all the the obstacles
            obstacle[i].pos[0]-=self.speed # shifting progressively all the obstacles to the left, so they can be seen be the player
                                          #in order words we are giving the impression to the player of moving forward in a wide and long environment
        for i in range(len(fire1)): #we will also slithly shift the moving bullets to the left to make the game look more realistic!
            fire1[i].pos[0]-=5 #also shift the bullets to the left, but by 5pixels only since they are in the right direction already, and even faster  
        for i in range(len(ennemy)):
            ennemy[i].pos[0]-=10 #shifting the ennemies to the left

class obstacles():
    def __init__(self,pos,size):
        self.size=size
        self.pos=pos
        self.rect=(self.pos[0],self.pos[1],self.size[0],self.size[1])
        self.exist=True # Later ennemies can destroy obstacles but not the player
    def show(self):
        self.rect=(self.pos[0],self.pos[1],self.size[0],self.size[1])
        if self.pos[0]<1300 and self.pos[0]>-300 : #if the obstacle exists on the field... (has not been destroyed by ennemy or player has simple reach its level )
            pygame.draw.rect(screen,(125,106,202),self.rect) #the 300 i added to the boarders above is to make the quiting out of the screen of the obstacles not brusque, but gentle and progressive till the last pixel of that obstacle

obstacle=[]
def generate_obstacles(environment):
    environment.pos[0]=environment.mid #pro reasons
    for dis in range(1000,environment.length+1000,1000): #Creating obstacles on from the base 1000 to the max length of the field, and increment by 1000
        obstacles_in_sector=random.randrange(3)#the number of obstacles in each sector vary from 0 to 2
        for i in range(obstacles_in_sector): #creating (obstacles_in_sector) number of obstacles 
            x=random.randrange(dis-1000,dis) # here we subdivide the field in sub sectors of 1000m, randomize thier x cordinates and create obstacles for each block
            width=random.randrange(50);length=random.randrange(30) # Randomizing the length and the width of the obstaclse
            obstacle.append(obstacles([x,440-length],[121+width,175+length])) #Adding the new obstacle to the list of obstacles
    #Above, we are saying exactly were (in terms of x coordinate) the obstacles will be
ennemy=[] #pos , size, health and damage
def generate_ennemies(ennemy,environment):
    for count in range(100):
        health=(count*8)/5; damage=1
        x=random.randrange(1000,environment.length)
        length=random.randrange(0,75)
        ennemy.append(ennemies([x,520-length],[87+(length/2),100+length],health,damage,50,10))#pos, size, health, damage, shoot_probability, max_bullets




hero=player([100,500],[89,100],10,500) # x,y pos, size, speed , damage
fire1=[] #creating a list of bullets for our hero
fire2=[bullet([100,580],[20,8],10,hero,ennemy,1,10)]
environment=Environment(25000) #The field will be 25000m (pixels long). but only 1000 pixels(size of screen) length of the field can be seen at a time( this is an apparent distance, since player doesnot move, but obstacles and ennemies shift to the left)
day=pygame.image.load("Environment/day.png");day=pygame.transform.scale(day,[1000,700])#;day=pygame.transform.rotate(day,180);day=pygame.transform.flip(day,True,False)
dawn=pygame.image.load("Environment/dawn.png");dawn=pygame.transform.scale(dawn,[1000,700])
night=pygame.image.load("Environment/night.png");night=pygame.transform.scale(night,[1000,700])
sky=[day,dawn,night]
done=False
generate_obstacles(environment)
generate_ennemies(ennemy,environment)
#MAIN LOOP
while not done :
    screen.fill((250,240,231))
    for event in pygame.event.get():
        if event.type==QUIT:
            done=True
    keys=pygame.key.get_pressed()
    if keys[K_RIGHT] :# if key is pressed and there are no obstacles on the right side of the player
        if  hero.rightway:
            if hero.pos[0]>=environment.mid: #if player has traversed the middle of the screen, he does not move forward anymore, but the environment(obstacles,ennemies) infront shifts back to him
                environment.shift(obstacle,ennemy,fire1)
            else:
                hero.pos[0]+=hero.speed #but if player is not after mid, then he moves forward
            if hero.state[1]!=3: #if the player is not in the jump state, then we assign the running sprite. else we leave the game to show us the jumping sprite image
                hero.state=[1,1] #right,motion
        else:
            hero.state[0]=1 # ie, even if the player if facing an obstacle, he can still turn to the right, but not move


    elif keys[K_LEFT] : # if key is pressed and there are no obstacles on the left side of the player
        if hero.leftway :
            hero.pos[0]-=hero.speed
            if hero.state[1]!=3: #(same comment as above) state 3 is the jumping state
                hero.state=[0,1] #left,motion
        else:
            hero.state[0]=0  # ie, even if the player if facing an obstacle, he can still turn to the left, but not move
    else:  
        if hero.state[1]!=3 and hero.state[1]!=6 and hero.state[1]!=2:# if player is not going left,not going right,not jumping and not falling, and not shooting..;-) then player should be set to idle state
            hero.state[1]=0 #state 0 is the idle state
            print("idle!!")
    
    if keys[K_f] :
        if (len(fire1)<environment.max_bullets): #ie a new ball is created iff the maximum number of simultaneous bullets on field is not exceeded
            if hero.state[0]==0 : #if player is looking left , we have to load a bullet in the left direction
                                #        pos                    size  damage target owner direction speed
                fire1.append(bullet([hero.pos[0]-5,hero.pos[1]],[75,50],  hero.damage,ennemy, 0  ,    -1 ,     20))
            if hero.state[0]==1 : #if player is looking right, we instead load a bullet in the right direction
               fire1.append(bullet([hero.pos[0]+hero.size[0]+5,hero.pos[1]],[75,50], hero.damage ,ennemy,0  ,    1 ,     20))
            fire1[-1].exist=True # setting to True the existance of the last bullet(-1) of the list, that we just created
    
    elif keys[K_SPACE]:
        if hero.state[1]!=3 and hero.foot_on_ground : # if player is not jumping already,not falling,and has his foot on the ground, then a jump is possible( if user presses space)
            hero.state[1]=3
            if hero.pos[1]==500:
                hero.pos[1]-=10 #to avoid foot_on_ground inorder for the jump function to load
            else: 
                hero.pos[1]-=15
         
    
    
        #DISPLAYING and Keeping Track of events
    hero.check_foot(obstacle) #checking whether or not player's foot is on ground( standing on an obstacle or on the ground).if not foot_on_ground is set to False else it is set to True
    hero.check_jump() #keeping track of the jumping motion if hero is in jumping state(state=3)
    hero.check_state(obstacle,ennemy) #checking if player if does not have foot on ground and is not jumping to then make him fall, AND checking if he is not touching any ennemy.. to then reduce his health
    
    
    print(len(fire1)); print(hero.health)
    screen.blit(sky[1],[0,0]) #diplaying the sky
    for i in range(len(obstacle)):
        obstacle[i].show() #displaying obstacles

    hero.show()#displaying player
    for i in range(len(fire1)): #cross checking all the bullets sent by our hero
        pop_it=fire1[i].keep_track()  #displaying and keeping track of the bullet 
        if pop_it==1: #when value of pop_it==1, it means that the bullet should be poped from fire1
            fire1.pop(i); break #if inside the function, the bullet collided and stoped existing, then we can pop that bullet from our list
    for i in range((len(fire2))):
        pop_it=fire2[i].keep_track()
        if pop_it==2: #pop_it==2 means that a bullet should be poped or removed from fire2( the list of bullets of the ennemy)
            fire2.pop(i); break
    
    for i in range(len(ennemy)):
        ennemy[i].keep_track(hero,fire2) # displaying and keeping track of the ennemies 
    for i in range(len(ennemy)):   
        if not(ennemy[i].exist): # we remove from our list all ennemies that do not exist : to save space
            ennemy.pop(i); break # This is why we must break!! the pop reduces the len of the list, while the initial length has already been passed to the
    print(len(ennemy))            # for loop , and so it will cause an error since to loop will finially want to acces a memory location that does not exist again!
    
    
    pygame.draw.rect(screen,(75,61,214),(0,595,1000,200)) #the flour
    pygame.display.update()
    time.tick(20)

pygame.quit()