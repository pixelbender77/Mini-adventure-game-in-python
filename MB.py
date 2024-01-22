import pygame,random,time,sys
from pygame.locals import*
pygame.init()
time=pygame.time.Clock()
size=(1000,700)
pygame.display.set_caption("Mr. Black")
screen=pygame.display.set_mode(size)
FPS=24
def load(name):
    return pygame.image.load(name)
def resize(image_obj,size):
    return pygame.transform.scale(image_obj,size)
def message(word,xy,size,color,writing):
    font=pygame.font.SysFont(writing,size,False)
    msg=font.render(str(word),True,color)
    screen.blit(msg,xy)
#initial size of sprite [121,220]
#def load_sprites():#here each object owns its list, and a list contains different other lists e.g player's 0 address contain the list for the running sprites and 1 addres for the attack
player_sprites=[];guns=[]; ennemy_sprites=[] ; object_sprites=[]
player_sprites.append([load("skins/player/run/r1.png"),load("skins/player/run/r2.png"),load("skins/player/run/r3.png"),load("skins/player/run/r4.png"),load("skins/player/run/r5.png"),load("skins/player/run/r6.png"),load("skins/player/run/r7.png"),load("skins/player/run/r8.png"),load("skins/player/run/r9.png")])
player_sprites.append([load("skins/player/idle/body.png"),load("skins/player/idle/the arm.png"),load("skins/player/idle/chest.png"),load("skins/player/idle/jump.png")])#body, hand, chest and jump sprites respectively
player_sprites.append([load("skins/player/idle/angry.png"),load("skins/player/idle/happy.png"),load("skins/player/idle/harmed.png")])#angry,happy and harmed face sprites respectively
guns.append([load("skins/player/guns/yellow_flash.png"),load("skins/player/guns/blue_flash.png")]) #the first element of the gun array is the list of gun lightflashs
guns.append([load("skins/player/guns/gun1.png"),load("skins/player/guns/fired1.png"),load("skins/player/guns/bullet1.png"),load("skins/player/guns/bullet11.png")]) #each gun has a settled, fired state,a respective bullet and a corresponding active state bullet #GUN 1
for i in range (9): 
    player_sprites[0][i]=resize(player_sprites[0][i],[121,200])
ennemy_sprites.append([load("skins/ennemy/run/r1.png"),load("skins/ennemy/run/r2.png"),load("skins/ennemy/run/r3.png"),load("skins/ennemy/run/r4.png"),load("skins/ennemy/run/r5.png"),load("skins/ennemy/run/r6.png"),load("skins/ennemy/run/r7.png"),load("skins/ennemy/run/r8.png"),load("skins/ennemy/run/jump.png")]) #loading the running sprites in memory
ennemy_sprites.append([load("skins/ennemy/all/idle.png"),load("skins/ennemy/all/idlechest.png"),load("skins/ennemy/all/idleface.png"),load("skins/ennemy/all/attack.png"),load("skins/ennemy/all/hurted.png")]) #idle,ichest,iface,attack,hurted
ennemy_sprites.append([load("skins/ennemy/all/hair1.png"),load("skins/ennemy/all/hair2.png"),load("skins/ennemy/all/hair3.png")]) #hairstyles
ennemy_sprites.append([load("skins/ennemy/all/bullet.png")])#bullets

object_sprites.append([[load("maps/ground/f1.png"),load("maps/ground/f2.png")],[load("maps/ground/b1.png"),load("maps/ground/b2.png"),load("maps/ground/b3.png")]]) #the flours each in it's own sublist
object_sprites.append([load("maps/objects/wall1.png"),load("maps/objects/wall2.png")]) #the walls
object_sprites.append([load("maps/objects/silver.png"),load("maps/objects/platinum.png"),load("maps/objects/Gold.png")]) #coins
object_sprites.append([load("maps/objects/cloud1.png"),load("maps/objects/cloud2.png"),load("maps/objects/cloud3.png")]) #the three clouds
object_sprites.append([load("maps/objects/cb.png"),load("maps/objects/pb.png"),load("maps/objects/hb.png")]) #coin bar,powerbar,healthbar
for i in range(3):
    object_sprites[3][i]=pygame.transform.scale(object_sprites[3][i],[150,60])
back=load("maps/menu.png")
day=pygame.image.load("maps/day.png");day=pygame.transform.scale(day,[1000,700])#;day=pygame.transform.rotate(day,180);day=pygame.transform.flip(day,True,False)
dawn=pygame.image.load("maps/dawn.png");dawn=pygame.transform.scale(dawn,[1000,700])
night=pygame.image.load("maps/night.png");night=pygame.transform.scale(night,[1000,700])
sky=[day,dawn,night]



class player():
    def __init__(self,pos,size,speed,damage):
        self.sprite=player_sprites
        self.guns=guns
        self.pos=pos
        self.size=size
        self.rect=(self.pos[0],self.pos[1]-80,self.size[0],self.size[1])
        self.foot=(self.pos[0]+20,self.pos[1]+self.size[1]-2,self.size[0]-40,8) #this is the rectangle under the player that will serve as guard for falling
        self.Rhand=(self.pos[0]+(self.size[0]-8),self.pos[1]+50,8,self.size[1]-75)#Right hand rectangle used for obstacle collider detection
        self.Lhand=(self.pos[0],self.pos[1]+50,8,self.size[1]-75)#Legt hand rectangle .... as above
        self.damage=damage #the damage the bullets loaded by the hero will have
        self.count=0 #count for sprite animation
        self.img_frame=0 #tells which frame(or image) of the animation is to be displayed
        self.state=[1,0]#[1=Right 0=Left, (0=idle, 1=move , 2=[empty role due to a better understanding during the game programing.replaced by self.fired] , 3=jump, 4=[canceled(harmed.. replaces by self.harmed)], 5=die, 6=fall)]
        self.health=200
        self.initial_health=200 #this variable(which will remain constant) will be used for the health bar ratio
        self.speed=speed
        self.Jcount=10 #Jumpcount
        self.leftway=True # There is no obstacle on the emidiate left (initially)
        self.rightway=True # There is no obstacle ont the emidiate right  (initially)
        self.foot_on_ground=True
        self.fired=False #is player shooting?
        self.hurted=False #is player beeing hurted?
        self.max_bullets=5# The maximum number of bullets which can be shot by the player at a "screen time" i.e within the range of the screen
        self.bullet_speed=35 #(initialy)this is the speed bullets will have everytime they are shot by the hero or player.
        self.power_points=0 #1ennemy killed=1powerpoint, when the power points reach the power goal below, you obtain power balls
        self.power_goal=10 #the number of power points to reach in orther to have power balls
        self.powerball=False #To Launch an unlaunch powerballs
        self.decrement=10 #this variable will be used to decrement the powerbar when it will have filled
        self.power_state=[0,0,0] #1st sprite in gun array(sprite of lighted bullet),increment of speed of bullet , increment of bullet damage 
        self.coins=0 #initialy your player is very poor and has 0 coin in his account

    def show(self):
        alter=3
        self.rect=(self.pos[0],self.pos[1]-80,self.size[0],self.size[1])
        self.foot=(self.pos[0]+20,self.pos[1]+self.size[1]-8,self.size[0]-40,8)
        self.Rhand=(self.pos[0]+(self.size[0]-8),self.pos[1]+50,8,self.size[1]-75)
        self.Lhand=(self.pos[0],self.pos[1]+50,8,self.size[1]-75)
        #pygame.draw.rect(screen,(12,56,216),(self.pos[0]+10,self.pos[1]-95,self.size[0]-25,self.size[1]*2-6))
        #pygame.draw.rect(screen,(0,0,0),self.foot)
        #pygame.draw.rect(screen,(103,88,115),self.Rhand)
        #pygame.draw.rect(screen,(12,99,114),self.Lhand)
        self.count+=1
        if self.state[1]==0 or self.state[1]==6:#if player is idle, then we should display the player idle image
            if self.state[0]==1:#no need reflecting the image since the sprite is already looking in the right direction
                screen.blit(self.sprite[1][0],[self.pos[0]-20,self.pos[1]-110+alter])#body
            else:#else , the player is looking left we flip the image .. i.e we reflect it , for the sprite to look at the left
                screen.blit(pygame.transform.flip(self.sprite[1][0],1,0),[self.pos[0]-20,self.pos[1]-110+alter])#body
        else: # if the player is not idle the we should print at least print the chest,since no matter the state of the player, the chest is the same :-)
            if self.state[0]==1:#player is looking right
                screen.blit(self.sprite[1][2],[self.pos[0]-20,self.pos[1]-110+alter]) #The chest
            else:#Looking left
                screen.blit(pygame.transform.flip(self.sprite[1][2],1,0),[self.pos[0]-20,self.pos[1]-110+alter]) #The Chest reflected
        

        if self.state[1]==1:#if player is in run state.. then we should display the running animation            
            if self.img_frame==8:#if the last img of the animation is being shown, the we set the location to 0 , to avoid addressing error
                self.img_frame=0
            else: 
                self.img_frame+=1
            self.count=0 #we initialize back the count to avoid long numbers in memory
            if self.state[0]==1:#if  player is moving to the right, we don't reflect the image since it is initialy looking at the right
                screen.blit(self.sprite[2][0],[self.pos[0]-20,self.pos[1]-110+alter]) #The Face
                screen.blit(self.sprite[0][self.img_frame],[self.pos[0]-20,self.pos[1]-99+2]) #The legs (motion)
            else: #else ,..the player is looking left we flip the image .. i.e we reflect it , for the sprite to look at the left
                screen.blit(pygame.transform.flip(self.sprite[2][0],1,0),[self.pos[0]-20,self.pos[1]-110+2]) #The Face
                screen.blit(pygame.transform.flip(self.sprite[0][self.img_frame],1,0),[self.pos[0]-20,self.pos[1]-99+alter]) #The legs(motion)
      
    
        if self.state[1]==3: #is player jumping?
            if self.state[0]==1:#Looking right?
                screen.blit(self.sprite[2][1],[self.pos[0]-20,self.pos[1]-110+alter]) #The happy jumping face 
                screen.blit(self.sprite[1][3],[self.pos[0]-20,self.pos[1]-113]) #The jumping leg sprite
            else: #Looking left! 
                screen.blit(pygame.transform.flip(self.sprite[2][1],1,0),[self.pos[0]-20,self.pos[1]-110+alter]) #The Face(reflected)
                screen.blit(pygame.transform.flip(self.sprite[1][3],1,0),[self.pos[0]-20,self.pos[1]-113]) #The jumping leg sprite (reflected)

        if self.fired: #if player is shooting..
            if self.state[0]==1:#player is looking right
                screen.blit(self.sprite[2][0],[self.pos[0]-20,self.pos[1]-110]) #An angry face while shooting
                screen.blit(self.guns[1][1],[self.pos[0]-2,self.pos[1]])#fired gun image, since player is shooting
                screen.blit(self.guns[0][1],[self.pos[0]+80,self.pos[1]-3])#Gun flash
                screen.blit(self.sprite[1][1],[self.pos[0]+4,self.pos[1]-6])#hand(lifted shooting)
            else:#looking left!
                screen.blit(pygame.transform.flip(self.sprite[2][0],1,0),[self.pos[0]-20,self.pos[1]-110]) #The same angry Face(reflected)
                screen.blit(pygame.transform.flip(self.guns[1][1],1,0),[self.pos[0]-9,self.pos[1]-2])#fired gun image
                screen.blit(pygame.transform.flip(self.guns[0][1],1,0),[self.pos[0]-21,self.pos[1]-4])#Gun flash
                screen.blit(pygame.transform.flip(self.sprite[1][1],1,0),[self.pos[0]+9,self.pos[1]-6])#hand(lifted during shooting)
            self.fired=False #we set back the variable to False to prevent permanent flash
        else:
            if self.state[0]==1: #if player is looking right..
                screen.blit(self.guns[1][0],[self.pos[0],self.pos[1]])#the gun
                screen.blit(self.sprite[1][1],[self.pos[0]+4,self.pos[1]-3])#hand
            else: #if instead he is looking left(state==0)
                screen.blit(pygame.transform.flip(self.guns[1][0],1,0),[self.pos[0]-9,self.pos[1]-2])#the gun
                screen.blit(pygame.transform.flip(self.sprite[1][1],1,0),[self.pos[0]+9,self.pos[1]-3])#hand
        
        if self.hurted: #if player is being hurted..
            if self.state[0]==1:#Looking right?
                screen.blit(self.sprite[2][2],[self.pos[0]-20,self.pos[1]-110+alter]) #The hurted sprite's face
            else: #Looking left!
                screen.blit(pygame.transform.flip(self.sprite[2][2],1,0),[self.pos[0]-20 ,self.pos[1]-110+alter]) #same image, just reflected since player is looking left
            self.hurted=False #after all we set back the variable to False to prevent this hurted face image to be shown continuously
        
        # [POWER BALL]
        add=46
        #pygame.draw.rect(screen,(23,137,99),[10+add,200,120,20],2)
        if self.powerball :#if a powerball is already obtained(the bar was filled already), then we keep track of the decrementing bar
            for i in range(10+add,self.decrement+add,1):
                pygame.draw.rect(screen,(0, 217, 255),[i,201,1,20]) 
            self.decrement-=1
            if self.decrement<=10: #if the bar is emptied..
                self.power_points=0
                self.powerball=False #then we remove the power of powerballs to the player
                self.power_state=[0,0,0]#normalbullet,no more increase in speed of bullets,no more increase in damage ( Your power is finish :p :-))
            

        else: #else we keep on increamenting the bar following the number of power_points
            for i in range(1,self.power_points+1):
                pygame.draw.rect(screen,(0, 124, 253),[(10*i)+add,201,14,20 ])
            if self.power_points>=self.power_goal and 10*i>=110: #if the limit of the bar is attained.. then we set powerball true, to let the user use power balls and to set out bar decrement :-) (power balls are not infinite ;)
                self.decrement=100 #used for decrementing the bar
                self.powerball=True
                self.power_state=[1,8,20]#lighted sprite(index 1 in array),speed increases by 1, increase damage by 20
        screen.blit(object_sprites[4][1],[8,185]) #the power bar sprite




    def check_foot(self,obstacle): #this function checks the foot of the player relative to the flour and all the obstacles to see if it standing on top of an obstacle or on top of the flour
        self.foot=(self.pos[0]+20,self.pos[1]+self.size[1]-8,self.size[0]-40,8)
        logical_foot=(self.pos[0]+20,self.pos[1]+self.size[1]-8,self.size[0]-40,15        ) #this logical foot is used for collision with obstacles
        for i in range(len(obstacle)):
            obstacle[i].rect=(obstacle[i].pos[0],obstacle[i].pos[1],obstacle[i].size[0],obstacle[i].size[1])
            if  (pygame.Rect(logical_foot).colliderect(obstacle[i].rect)) or (pygame.Rect(self.foot).colliderect(0,590,1000,200)): 
                self.foot_on_ground=True; #if the foot rect is touching an obstacle or even the flour, the the player's foot is on a ground
                self.pos[1]=obstacle[i].pos[1]+self.size[1] #when the player's foot touches the obstacle, it's position is automatically set to be above that obstacle(to literally land on the obstacle!)
                break #we then break the loop to prevent further cheking
                #print("Foot on ground"); #as soon as it is found that player is touching a surface, we break the loop to stop further search
            else:
                self.foot_on_ground=False # else, the player's foot is not on a ground
                #print("foot not! on ground")
        if pygame.Rect(self.foot).colliderect(0,580,1000,200):
            self.pos[1]=500
        if pygame.Rect(logical_foot).colliderect(obstacle[i].pos[0],obstacle[i].pos[1],obstacle[i].size[0],obstacle[i].size[1]): #here i did not put obstacle.rect because the logic rectangle is slightly different from the one shown on the screen
            self.pos[1]=obstacle[i].pos[1]-(self.size[1]) ; #print("Adjusted")

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
                
            if pygame.Rect(self.Rhand).colliderect(obstacle[i].rect) or self.pos[0]>=910: #if righthand rectangle is touching an obstacle, then there no way on the right or about to exceed screen.. 
                self.rightway=False; break #as soon as we discover an obstacle on the right side, we don't seek further
            else:
                self.rightway=True
            if pygame.Rect(self.Lhand).colliderect(obstacle[i].rect) or self.pos[0]<=10: #same comment as above
                self.leftway=False; break #as soon we discover....(same comment as above)
            else:
                self.leftway=True
        for i in range(len(ennemy)):  #cross checking all ennemies to see if any of them are colliding(touching) our hero
            if ennemy[i].exist: #is the ennemy we are about to check for collision with our hero exist? if not, no need
                ennemy[i].rect=[ennemy[i].pos[0],ennemy[i].pos[1],ennemy[i].size[0],ennemy[i].size[1]]
                if (pygame.Rect(self.rect).colliderect(ennemy[i].rect) or pygame.Rect(self.Lhand).colliderect(ennemy[i].rect) or pygame.Rect(self.Rhand).colliderect(ennemy[i].rect)): #If the player(Rect,Lefthand or Righthand) touches the ennemy it's health decreases by 1
                    self.health-=ennemy[i].damage
                    self.hurted=True #to show a hurted expression on the face of our hero
                    if self.health<=0:
                        pygame.quit()
            
class ennemies():
    def __init__(self,pos,size,health,damage,shoot_probability,max_bullets,bullet_speed,intelligent,_type): #damage and health will later be randomized to make ennemies have different effects
        self.sprites=ennemy_sprites
        self.battle=False 
        self.pos=pos
        self.size=size
        self.rect=[self.pos[0],self.pos[1],self.size[0],self.size[1]]
        self.damage=damage
        self.count=1 #This is for the sprites animation
        self.state=[0,1]#[left or right, 1=idle 2=move 3=jump  ]
        self.exist=True
        self.intelligent=intelligent # the magic variable! :-O
        self.health=health
        self.initial_health=health #this variable will be used in the health bar function
        self._type=[1,_type[1]] #[1=walker 2=Ghost 3=Boss,hair style] type[1]is the hairstyle passed while creating the object
        self.speed=4.5
        self.shoot_probability=shoot_probability #This will determine how frequent the ennemy will shoot
        self.max_bullets=max_bullets
        self.shot=0 # initialy ennemy has shot no ball . but later when ennemy will shoot, we will make sure the number of bullets shot
                    #does not exeed the max_bullet
        self.Jcount=10 #this is to manage the jump of the ennemies
        #self.loaded=False # this variable tells us that somewhere in the list of bullets there is a bullet loaded by this particular ennemy,
                            #and will be set to true when possible
        self.bullet_speed=bullet_speed #this is the speed bullets will have everytime they are shoot by this particular ennemy
        self.attack=False #initialy when created, the ennemy is not attacking
        self.hurted=False  #and is not hurted..
        self.semi_count=1# this count will be used to make the frames of  attack and hurt appear longer on the screen and not just like a strike(non realistic)
        #self.sign=1 #sign will be used to read back in reverse order the sprites of the ennemy
        self.hairstyle=ennemy_sprites[2] #the hairstyle images are found in the second address index of the ennemy spritec class
    def show(self):
        adjust=139; adjustx=39 #sign will be used to read back in reverse order the sprites of the ennemy
        if self.pos[0]<=1300 and self.exist: #for the ennemy's bar to be displayed it must be beside the screen and must exist
            x=self.pos[0]+10; y=self.pos[1]-20 #setting the cordinates of the bar (above the head of the ennemy)
            segment=self.initial_health/3 # ennemies' health bar
            #pygame.draw.rect(screen,(204, 7, 24),(x,y-1,44,10)) #the red bar behind
            pygame.draw.rect(screen,(0, 10, 10),(x-2,y-2,46,12)) #the black bar behind
            #pygame.draw.rect(screen,(26, 49, 219),(x-3,y-3,47,13),2) #the blue "cadre"
            #fragment=self.health/segment
            fragment=1
            for i in range(fragment):
                pygame.draw.rect(screen,(0, 255, 76),(x+(i*15)-1,y-1,15,10)) 
                #Above is the health bar of the ennemies(above them)
            self.rect=[self.pos[0],self.pos[1],self.size[0],self.size[1]]
            #pygame.draw.rect(screen,(55,200,166),self.rect)
            
            
            if self.state[1]==2 or self.state[1]==3 : #since jumping and running have same chest and face, then we factorise them out;-) 
                if self.state[0]==0 : #if ennemy is in left direction, then we show the normal sprites
                    if not self.attack: #if player is not attacking , then we show the normal chest and face. else we will display the according image for chest and face in attack state
                        screen.blit(self.sprites[1][1],[self.pos[0]-adjustx,self.pos[1]-adjust]) #the chest
                        screen.blit(self.sprites[1][2],[self.pos[0]-adjustx,self.pos[1]-adjust]) #the face
                    else: 
                        screen.blit(self.sprites[1][3],[self.pos[0]-adjustx,self.pos[1]-adjust])#chest and face in attack state
                        if self.semi_count==3: self.attack=False; self.semi_count=1 #setting back variable to false to go back to normal state sprite(since ennemy attacks during an instant only :-) )
                        else : self.semi_count+=1
                else: #else, we reflect them to look at the right direction
                    if not self.attack: #same comment as above
                        screen.blit(pygame.transform.flip(self.sprites[1][1],1,0),[self.pos[0]-adjustx,self.pos[1]-adjust]) #the chest
                        screen.blit(pygame.transform.flip(self.sprites[1][2],1,0),[self.pos[0]-adjustx,self.pos[1]-adjust])  #the face
                    else: 
                        screen.blit(pygame.transform.flip(self.sprites[1][3],1,0),[self.pos[0]-adjustx,self.pos[1]-adjust]) #chest and face in attack state
                        if self.semi_count>=3: self.attack=False; self.semi_count=1 #setting back variable to false to go back to normal state sprite(since ennemy attacks during an instant only :-) )
                        else : self.semi_count+=1
                # Above the normal chest is show only if the ennemy is not attacking, else we show the attack,else we show the attacking face and chest
            #[WALKING]
            print("COUNT:",self.count)
            if self.state[1]==2: #if ennemy is walking.. then we should print the walking sprites of the ennemy
                if self.state[0]==0 : #if ennemy is in left direction, then we show the normal sprites
                    screen.blit(self.sprites[0][self.count],[self.pos[0]-adjustx,self.pos[1]-adjust-2]) #running legs
                else: #else, we reflect them to look at the right direction
                    screen.blit(pygame.transform.flip(self.sprites[0][self.count],1,0),[self.pos[0]-adjustx,self.pos[1]-adjust-2])
                #else: # else we increment count to point at the next sprite which will be later shown
                if self.count>=7:#if latest image sprite is reached, reinitialize every thing to avoid indexing error
                    self.count=0  #realise that the whole number division sign " / " is to make sprites last longer on the screen 
                self.count+=1
            #[JUMPING]
            if self.state[1]==3: #if player is jumping.. then we should display the jumping sprites
                if self.state[0]==0:#if ennemy is looking left we display the normal image
                    screen.blit(self.sprites[0][8],[self.pos[0]-adjustx,self.pos[1]-adjust]) #jumping legs
                else: #else, we reflect them to look at the right direction
                    screen.blit(pygame.transform.flip(self.sprites[0][8],1,0),[self.pos[0]-adjustx,self.pos[1]-adjust]) #jumping legs
            #[IDLE]
            if self.state[1]==1 : #if player is not jumping nor walking, then it is idle!
                if self.state[0]==0:#if ennemy is looking left we display the normal image
                    #screen.blit(self.sprites[1][2],[self.pos[0],self.pos[1]-adjust])#idle face
                    if not self.attack: screen.blit(self.sprites[1][0],[self.pos[0]-adjustx,self.pos[1]-adjust])#idle body
                    else: 
                        screen.blit(self.sprites[1][3],[self.pos[0]-adjustx,self.pos[1]-adjust])#chest and face in attack state
                        self.attack=False
                    
                else: #else, we reflect them to look at the right direction
                    screen.blit(pygame.transform.flip(self.sprites[1][2],1,0),[self.pos[0]-adjustx,self.pos[1]-adjust]) #idle face
                    if not self.attack: screen.blit(pygame.transform.flip(self.sprites[1][0],1,0),[self.pos[0]-adjustx,self.pos[1]-adjust])#idle body
                    else:
                        screen.blit(pygame.transform.flip(self.sprites[1][3],1,0),[self.pos[0]-adjustx,self.pos[1]-adjust]) #chest and face in attack state
                        self.attack=False
            #[HURTED]
            if self.hurted:
                if self.state[0]==0:#if ennemy is looking left we display the normal image                     
                    screen.blit(self.sprites[1][4],[self.pos[0]-adjustx,self.pos[1]-adjust])
                else: #else, we reflect them to look at the right direction
                    screen.blit(pygame.transform.flip(self.sprites[1][4],1,0),[self.pos[0]-adjustx,self.pos[1]-adjust])
                if self.semi_count>=2:self.hurted=False; self.semi_count=1 #reset variable to avoid infinite hurting ;-)
                else: self.semi_count+=1
            
            if self.state[0]==0:#[HAIRSTYLE]
                screen.blit(self.hairstyle[self._type[1]],[self.pos[0]-adjustx,self.pos[1]-adjust]) 
            else:
                screen.blit(pygame.transform.flip(self.hairstyle[self._type[1]],1,0),[self.pos[0]-adjustx,self.pos[1]-adjust])
        
    def keep_track(self,hero,fire2):
        if self.pos[0]<=1300 : #we begin keeping track of ennemies when they are already close to the screen
            if self.exist:#if the x coodinate of the ennemy is greater than that of the hero+it's size then ennemy will move forward
                if self.state[1]!=3 : # if the ennemy is not jumping.. 
                    if self.pos[0]>hero.pos[0]+hero.size[1]-50: #if the hero is at the left of the ennemy..
                        self.pos[0]-=self.speed #move left towards the hero
                        self.state=[0,2] #left and move state
                    if self.pos[0]+self.size[0]<hero.pos[0]+50: #   if the x coodinate is instead less than( ennemy is at the left of hero)
                        self.pos[0]+=self.speed  #move right towards the hero     
                        self.state=[1,2] #rigth and move state
            
            if (self.pos[0]==hero.pos[0]+hero.size[1]-50 or self.pos[0]+self.size[0]==hero.pos[0]+50) and self.state[1]!=3 and not self.attack: #if ennemy is at the same position with player, is not jumping and is not attacking, then it should be idle!
                self.state[1]=1 #since ennemy is doing nothing , then let it be idle!

            if self.state[1]==3: #if ennemy is jumping.. then let's keep track of it's jump
                if (self.Jcount>=-10) : # is the jumpcount over and has player landed somewhere??..
                    direction=1 # it  determines the going up or down of the sprite. 
                    if self.Jcount==0 : #If ennemy has reached its maximum height of it's jump, then it shouts its bullet 
                        if self.state[0]==0 : #if ennemy is looking left , we have to load a bullet in the left direction
                                #                                pos                  size                      damage target  owner direction   speed
                            fire2.append(bullet([self.pos[0]-40,self.pos[1]+8]     ,   [40,30],self.damage, hero,     1  ,    -1 ,self.bullet_speed)) #Creating a bullet proportional to the length of the ennemy
                        if self.state[0]==1 : #if ennemy is looking right, we instead load a bullet in the right direction
                            fire2.append(bullet([self.pos[0]+self.size[0]+40,self.pos[1]+8],[40,30],self.damage,hero,1  ,    1 ,self.bullet_speed)) #same comment as above
                        fire2[-1].exist=True #Setting Firering the bullet ,ie. setting true the bullet the ennemy earlier loaded
                        self.attack=True # then we will display the attack sprites!
                    
                    if self.Jcount<0: #since ennemy has reached max height, we invert it's vertical motion by
                        direction=-1  #drecrementing it by 1
                    self.pos[1]-=(self.Jcount**2)*0.4*direction
                    self.Jcount-=1
                else:
                    self.Jcount=10 #setting back or initializing Jump count to 10
                    self.state[1]=0 #when player has landed, we then set it's state to idle: to stop it from jumping further 

            if self.state[1]!=3: # a normal bullet_shoot should occcure only if ennemy is not jumping
                if self.shot<=self.max_bullets: #if ennemy has not yet exeeded his limited number of bullets,then we can give him a chance to shoot
                    shoot=random.randrange(self.shoot_probability) #....
                    if shoot==10: # The probability of shooting is 1/self.shoot_probability
                        
                        #Below we are deciding if ennemy will jump before shouting or will shout while being on the ground
                        if self.intelligent and hero.pos[1]<self.pos[1] : #if the ennemy is intelligent, it should jump before shooting it's bullet, and the player's position is above that of the ennemy.. 
                                self.state[1]=3 #then it will jump before shooting
                                #realise that we did not create and append a bullet to the list of bullet as above because,the position of the 
                                #bullet will be given when ennemy would have reached the max height of it's jump. so it will we done in the jump keep_track
                        else: #but if it is a not intelligent ennemy or ennemy is higher than hero, it will shout simply
                            if self.state[0]==0 : #if ennemy is looking left , we have to load a bullet in the left direction
                                          #        pos                            size damage target owner direction speed
                                fire2.append(bullet([self.pos[0]-40,self.pos[1]+11],[40,30],self.damage, hero,     1  ,    -1 ,     self.bullet_speed)) #Creating a bullet proportional to the length of the ennemy
                            if self.state[0]==1 : #if ennemy is looking right, we instead load a bullet in the right direction
                                fire2.append(bullet([self.pos[0]+self.size[0]+30,self.pos[1]+11],[40,30],self.damage,hero,1  ,    1 ,     self.bullet_speed)) #same comment as above
                            self.attack=True #then we will show the shooting sprite of the ennemy

                            fire2[-1].exist=True # setting to True the existance of the last bullet(-1) of the list, that we just created
                            self.state[1]=2     
            

            self.show() #displaying the ennemy    

class bullet():
    def __init__(self,pos,size,damage,target,owner,direction,speed):
        self.pos=pos
        self.size=size
        self.rect=[self.pos[0],self.pos[1],self.size[0],self.size[1]]
        self.damage=damage
        self.exist=False
        self.owner=owner #0=Player 1=ennemy This is what will determine the appearance of the bullet.
        self.target=target
        self.direction=direction #-1 and 1 
        self.speed=speed
        self.guns=guns #the list of gun sprites
        self.ennemy_sprites=ennemy_sprites
    def move(self):
        self.pos[0]+=(self.speed*self.direction)
    
    def show(self):
        self.rect=[self.pos[0],self.pos[1],self.size[0],self.size[1]]
        if self.owner==0: #if owner is player
            #color=(0,7,3)
            #pygame.draw.rect(screen,color,self.rect)
            if self.direction==1: #if bullet is going in right direction
                screen.blit(self.guns[1][hero.power_state[0]+2],[self.pos[0]-8,self.pos[1]-6])#remark that we are considering the power state and applying it to the bullet(state+2 since unlighted is at 2 and lighted at 3,when state=1 lighted bullet is printed,and unlighted when state=0)
            else:#bullet is going in left direction
                screen.blit(pygame.transform.flip(self.guns[1][hero.power_state[0]+2],1,0),[self.pos[0]-8,self.pos[1]-6])
        else : #else owner is an ennemy
            #color=(91,2,22)
            #pygame.draw.rect(screen,color,self.rect)
            if self.direction==1:
                screen.blit(pygame.transform.flip(self.ennemy_sprites[3][0],1,0),[self.pos[0],self.pos[1]+11])
            else:
                screen.blit(self.ennemy_sprites[3][0],[self.pos[0],self.pos[1]+11])
    def check(self,hero):
        pop_it=0 #This is the variable the function will return telling the parent function to pop this particular bullet from the list or not                               
        if self.owner==0: #if the owner of the bullet is our hero..
            if self.pos[0]>1000 or self.pos[0]<-75 : #ie if ball has exceeded screen boundries, then it stops existing.
                self.exist=False; pop_it=1 # since bullet has exceeded screen boundries, it stops existing and we pop it from our list to save space:-)) 
            else:# since bullet has not yet exceeded boundries, then we can check the rest 
                for i in range(len(self.target)):#cross checking all ennemies to see if the bullet has collide somewhere
                    if self.target[i].exist: #Does the ennemy we are about to check for collision exists?...
                        if pygame.Rect(self.rect).colliderect(self.target[i].rect): #if the bullet collides with its target..
                            self.target[i].health-=self.damage # the health of the target reduces by the amount of damagecapacity given to the bullet by the sender 
                            self.exist=False #and the bullet stops existing
                            pop_it=1 #Since bullet has collided with it's target, it stops existing an we can then permit it to be poped(removed)from our list to save space
                            self.target[i].hurted=True #inorder to print the hurted face of the ennemy
                            if self.target[i].health<=0: #if target has no health left, then is must stop existing! :-] 
                                self.target[i].exist=False
                                hero.power_points+=1
                                    #and we can pop the target(ennemy ) from it's list to liberate space
            
        elif self.owner==1: #if the owner of the bullet is an ennemy..
            if self.pos[0]>1000 or self.pos[0]<-75 : #ie if ball has exceeded screen boundries, then it stops existing.
                    self.exist=False; pop_it=2 # since bullet has exceeded screen boundries, it stops existing and we pop it from our list to save space:-)) 
            else : # since bullet has not yet exceeded boundries, then we can check the rest 
                self.rect=[self.pos[0],self.pos[1]-15,self.size[0],self.size[1]*2-6]
                if pygame.Rect(self.rect).colliderect([self.target.pos[0]+10,self.target.pos[1]-80,self.target.size[0]-25,self.target.size[1]*2]) :#i prefared to not put target.rect here because i need to change the logical rectangle since it was short, and bullets could not collide with the legs of the player
                    self.target.health-=self.damage # the health of the target reduces by the amount of damagecapacity given to the bullet by the sender 
                    self.exist=False #and the bullet stops existing
                    self.target.hurted=True #Inorder to show the hurt face expression on the hero
                    pop_it=2 #Since bullet has collided with it's target, it stops existing an we can then permit it to be poped(removed)from our list to save space
                    if self.target.health<=0: #if target has no health left, then is must stop existing! :-] 
                        self.target.exist=False
                        #GAME_OVER instruction
                        pygame.quit()
                        #since the target of the bullet in this case is the hero and that the hero is not a list, we write target.rect,target.exist.. etc.. since it is not a list :-}
        return pop_it
                        
        
    def keep_track(self):
        pop_it=False
        if self.exist:
            self.show()
            self.move()
            pop_it=self.check(hero)
        return pop_it
class money():
    def __init__(self,pos,_type,value,duration):
        self.sprites=object_sprites[2] #coins are found in index 2 of the sprite list
        self.pos=pos 
        self.exist=True #Initialy all the coins exist!
        self._type=_type #There 3 type: silver :100, platinum :200, Gold :500
        self.value=100 #100 here is the coin value of platinum
        self.count=0 #this is to make the coin disapear after a certain time.( to make the quest for coins interesting)
        self.duration=duration #this is the time the coin will be visible to the player, when this time is over, coin disapears and stops existing

    def show(self):
        if  self.exist and self.pos[0]<1300 and self.pos[0]>-300 : #if the coin exists and is found between the boarders of the screen
        #pygame.draw.rect(screen,(241, 224, 11),[self.pos[0],505,42,30])
            screen.blit(self.sprites[self._type],[self.pos[0]-10,self.pos[1]-70])

    def collect(self,hero):
        if self.exist and self.pos[0]<1300 and self.pos[0]>-300:#if coin exist and is in the range of the screen
            if pygame.Rect(hero.pos[0]+10,hero.pos[1]-80,hero.size[0]-25,hero.size[1]*2).colliderect([self.pos[0],505,42,30])  : #when the player touches this coin,
                hero.coins+=self.value #the coins of the player increase by the value of that coin
                self.exist=False # And the coin stops existing to avoid the player from repeaking the same coin over and over ;-)
                message(hero.coins,[10,280],25,(64,250,233),"Calibri") #showing the total coins with a larger size, to indicate to the player that there is an increase
            if self.count>=self.duration : #if the life span of the coin is attained..
                self.exist=False #coins stop existing, but we don't increment player's money, since he has did not pick the coin but it disapered alone after it's lifespan was over
            self.count+=1 #we increment the count

class Sky():
    def __init__(self,pos,type_,speed):
        self.pos=pos
        self.type_=type_
        self.sprite=object_sprites[3] #clouds are found in index 3 of the object sprite list
        self.speed=speed
    def show(self):
        self.pos[0]-=self.speed #all the clouds are shifting to the left
        if self.pos[0]<=-300: self.pos[0]=environment.length #when a cloud traverses the left screen boundry, it is sent back to the end of the game level, and will continue moving to the right
        if  self.pos[0]<1300 and self.pos[0]>-300 : #if cloud's logical position is found in the screen range..
            #pygame.draw.rect(screen,(17,84,209),[self.pos[0],self.pos[1],90,50]) #then we show that cloud
            screen.blit(self.sprite[self.type_],self.pos)

class Environment():
    def __init__(self,length):
        self.pos=[0,0] #initialy we are at the begining of the game levels at x=0
        self.ground=[0,700,1400] #The initial x coodinate of the 2flour images
        self.ground_img=[0,1,0] #two ground images will be shown at a time so we create a list to keep track of each image's location
        self.mid=600 #the middle of the field. when traversed increases the x value of the self pos. Also, flour shifts behind , the buildings too , giving the impression of moving forward 
        self.speed=12 #this is the variable which will shift all the obstacles and ennemies to the visible screeen every time the player will cross screen mid as seen above
        self.max_bullets=3 #a maximum of 3 bullets can be loaded on the field at a time. for a fourth to be loaded, one of three must either exceed the screen boundries or collide a target
        self.length=length
        self.ground_level=595
        self.battle=False #will say whether or not a battle is going on on the field
        self.i=10 #i shall be used to vary the color of the lighted polygon(-1 or +1):-)
        self.fade_count=1 #incremented to a certain value before i (above) is incremented to fade the color.( that certain value is the speed , that will be determined by the speed passed to the polygon function)
        self.fade=1 #this is the variable that directely affects the color of the lighted polygon
        self.period_of_day=0 #0:day 1:dawn 2:night #this variable will later be passed to the show funtion to display the correct time or period image(sky,flour and clouds)
        self.ground_sprites=object_sprites[0]#ground images are stored in location 0 in the object_sprites list

    def shift(self,obstacle,ennemy,fire1,coin,cloud):
        self.ground[0]-=self.speed;self.ground[1]-=self.speed;self.ground[2]-=self.speed
        for i in range(3):
            if self.ground[i]+800<=0 : #if the position of the image + it's size <=0 (the right end of the image) 
                self.ground[i]=1195
                self.ground_img[i]=random.randrange(2) #randomizing image of the next flour(logical four 1)
        
        self.pos[0]+=self.speed #incrementing the actual distance(pos[0] or x cordinate) of the environment
        print(self.pos[0])
        for i in range(len(obstacle)): # crosschecking all the the obstacles
            obstacle[i].pos[0]-=self.speed # shifting progressively all the obstacles to the left, so they can be seen be the player
                                          #in order words we are giving the impression to the player of moving forward in a wide and long environment
        for i in range(len(fire1)): #we will also slithly shift the moving bullets to the left to make the game look more realistic!
            fire1[i].pos[0]-=5 #also shift the bullets to the left, but by 5pixels only since they are in the right direction already, and even faster  
        for i in range(len(ennemy)):
            ennemy[i].pos[0]-=10 #shifting the ennemies to the left
        for i in range(len(coin)): 
            coin[i].pos[0]-=10 #shifting coins to the left
        for i in range(len(cloud)):
            cloud[i].pos[0]-=7
    def show(self,hero):
        screen.blit(object_sprites[4][0],[10,280])
        message(hero.coins,[55,304],20,(56,10,204),"Calibri") #Writing the number of coins #notice we don't need any condition to show the number of coins.. 
        screen.blit(self.ground_sprites[0][self.period_of_day],[0,self.ground_level-10])#displaying the permanent, according to the period of the day
        screen.blit(self.ground_sprites[0][self.period_of_day],[600,self.ground_level-10]) #period_of_day corresponds to an index to fetch the corresponding image in the list
        for i in range(3): #showing the 3 ground images
            screen.blit(self.ground_sprites[1][self.ground_img[i]],[self.ground[i],self.ground_level-10]) #the blocks of the flour

    def health_bars(self,hero):
        segment=hero.initial_health/20;x,y=26,26; # Player's health bar
        #pygame.draw.rect(screen,(58, 217, 254),(27+x,5+y,403,30),2)
        #fragment=hero.health/segment
        fragment=1
        for i in range(1,fragment+1):
            pygame.draw.rect(screen,(210,70+i%2,125),(9+(i*20)+x,7+y,20,22))
        screen.blit(object_sprites[4][2],[20,10]) #health bar image
       
    def polygons(self,x,y,speed): #x,y are the coordinates, speed is will determine the speed at which the lighted polygon fade
        #if(self.fade_count%speed==0):#a color fade will occure once every "speed" time.(modulo)
        self.fade+=self.i
        if (self.fade+186>=255): #if the color is already at the lightest point(beyond which an RGB color error will appear),we start subtracting instead: to make the color fade down, and the inverse is true for the beginning spot
            self.i*=-1;self.fade=68
        if (self.fade+186<=186): #if the color is below or equal to the initial color, we init the fade and inverse the direction progress of the fading(i*=-1)(the negative sign)
            self.i*=-1;self.fade=1
        #self.fade_count=1 #initialinzing back the count, inorder to not have very large number in memory
        print("FADED!")
        print("color",186+self.fade)
        #else:
        #    self.fade_count+=1
        pale_color=(8, 88, 182);light_color=(8, 186+self.fade, 254)
        pygame.draw.polygon(screen,light_color,([x-2,y-1],[x+20,y+8],[x+23,y+25],[x+5,y+35],[x-16,y+28],[x-20,y+10]));x-=27;y-=27
        pygame.draw.polygon(screen,pale_color,([x-2,y-1],[x+20,y+8],[x+23,y+25],[x+5,y+35],[x-16,y+28],[x-20,y+10]));x-=16;y+=30
        pygame.draw.polygon(screen,pale_color,([x-2,y-1],[x+20,y+8],[x+23,y+25],[x+5,y+35],[x-16,y+28],[x-20,y+10]))
        
    #def show(show):

class obstacles():
    def __init__(self,pos,size,_type):
        self.size=size
        self.pos=pos
        self.rect=(self.pos[0],self.pos[1],self.size[0],self.size[1])
        self.exist=True # Later ennemies can destroy obstacles but not the player
        self.sprites=object_sprites[1]#obstacles sprites are found in location 1 inside the object_sprites list
        self._type=_type #_type here is the _type of obstacle that will be displayed on the screen
    def show(self):
        self.rect=(self.pos[0],self.pos[1],self.size[0],self.size[1])
        if self.pos[0]<1300 and self.pos[0]>-300 : #if the obstacle exists on the field... (has not been destroyed by ennemy or player has simple reach its level )
            pygame.draw.rect(screen,(125,106,202),self.rect) #the 300 i added to the boarders above is to make the quiting out of the screen of the obstacles not brusque, but gentle and progressive till the last pixel of that obstacle
            screen.blit(self.sprites[self._type],[self.pos[0]-13,self.pos[1]-10])
        
class battles():
    def __init__(self,pos,normalEnnemies,avg_health,avg_size,avg_damage,avg_spawnspeed,intelligentEnnemies):
        self.pos=pos 
        self.done=False #when the battle is over, this variable is set to true
        self.going_on=False #If true, player will be unable to move further distance, and battle will go on
        self.normalEnnemies=normalEnnemies #the number of ennemies for the particular battle
        self.ennemies_loaded=0 #initialy no ennemy has been loaded yet
        self.intelligentsLoaded=0 #initialy the number of intelligent ennemies is 0
        self.avg_health=avg_health #the average health of the ennemies for that particular battle
        self.avg_damage=avg_damage# the standard damage was 2
        self.avg_size=avg_size #the standard size is [50,30]
        self.avg_spawnspeed=avg_spawnspeed
        self.intelligentEnnemies=intelligentEnnemies #the  number of smart ennemies in that battle
        self.pending_ennemies=0   # initialy it is Zero but it will be changed to the number of ennemies remaining in the game level before those of
                                                # the battle are added to it. This number will be used as a condition to reload the game after the ennemies of the battle will all be killed    
    def check_proximity(self,environment,ennemy):
        if not(self.going_on) and not (done): #if this battle is not already going on, and we are(were) not done with it, then we check it's proximity 
            #if environment.pos[0]>=self.pos[0] and environment.pos[0]<self.pos[0]+200 : # if the position of the environment(player) is in the zone(range) of the battle, then the battle should be loaded!
            #    self.going_on=True # then the battle should start
            #    environment.battle=True #To stop the player from going forward , since there is a battle to finish first
                #self.pending_ennemies=len(ennemy) #these are the remaining ennemies on the field before those of the battle are produced. it will be used later to check if all the ennemies of the battle have been killed
                print("Ambuscade loaded")
    
    def keep_track(self,ennemy):
        total_ennemies=self.intelligentEnnemies+self.normalEnnemies
        total_loaded=self.intelligentsLoaded+self.ennemies_loaded
        if self.going_on :#if the battle is going on
            if (total_ennemies!=total_loaded): # and all the ennemies intended for the battle have not all been spawned yet, then we go on with the production :-)
                time_interval=random.randrange(self.avg_spawnspeed) # This is just for the function to not create an ennemy at every program loop, 
                if time_interval==3:                                  #but to leave a certain time_interval(randomized) between successive spawns, also to make
                    #intelligent=False                               #the scene and event realistic, not just all the ennemies spawning at the same time#PERFECT COMMENT
                    print('Ambuscade!!')
                    smart=random.randrange(10) #would determine if a smart(intelligent) ennemy or a normal ennemy will be spawned
                    if smart<=4:# ie 4 3 2 1 0
                        if self.intelligentsLoaded<self.intelligentEnnemies: #if the number of intelligent ennemies to be loaded has not yet exceeded the normal..
                            intelligent=True
                            self.intelligentsLoaded+=1 #since an intelligent ennemy will be loaded, then we increase the number of intelligent ennemies loaded 
                        else:
                            intelligent=False #if the number of intelligent ennemies to be loaded has been reached already, then we produce a normal ennemy instead
                    else: # ie 5 6 7 8 9
                        if self.ennemies_loaded<self.normalEnnemies:
                            intelligent=False
                            self.ennemies_loaded+=1 #increament number of normal ennemies loaded
                        else:
                            intelligent=True#if the number of normal ennemies to be produced is reached, we produce an intelligent ennemy at the place

                    side=random.randrange(2) #to say whether ennemy will come from left or right side( 2 means from 0 to 1)
                    width=50;length=140 # randomizing the size of the ennemies
                    health=random.randrange(self.avg_health)+20
                    damage=random.randrange(self.avg_damage)+3
                    if side==1:
                        x=1200 #we spawn the ennemy at right , just after the screen
                    else:
                        x=-200 #we spaxn the ennemy at the left, just before the screen
                    hairstyle=random.randrange(3)#randomizing the hairstyle of the ennemy
                    ennemy.append(ennemies([x,475],[width,length],health,damage,50,10,15,intelligent,[1,hairstyle]))#False is for ( not intelligent)
                    ennemy[-1].battle=True # The ennemies created are all battle ennemies( this variable shall be used to effectively continue adventure after a battle)
                    print("Spawned!!") 
            total_ennemies=self.intelligentEnnemies+self.normalEnnemies
            total_loaded=self.intelligentsLoaded+self.ennemies_loaded
            # Below,: if the number of ennemies left is already equal to the number left before the battle started(before some were added) 
            #and if all the ennemies to be spawned for that battle have been spawned ..
            print("Total ennemies:",total_ennemies); print("Loaded:",total_loaded,self.ennemies_loaded,self.intelligentsLoaded)
            allkilled=True
            for i in range(len(ennemy)): # here we check all the list of ennemies to see if battle ennemies exist again
                if ennemy[i].battle:
                    allkilled=False; break #if at least one exists again, then all are not killed, and we break the loop
            if allkilled and(total_loaded==total_ennemies): #inorder words all the ennemies for that battle must have been produced and killed:-)
                self.going_on=False   #inorder to allow the player move forward and continue it's adventure
                self.done=True # we are done with this battle. therefor the program will not consider it any more
                environment.battle=False #Also (this is the variable that stops player from going further) so we set it to false:-) 
                    
hero=player([100,500],[89,100],10,500) # x,y pos, size, speed , damage
fire1=[] #creating a list of bullets for our hero
fire2=[bullet([100,580],[20,8],10,hero,1,1,10)]
environment=Environment(25000) #The field will be 25000m (pixels long). but only 1000 pixels(size of screen) length of the field can be seen at a time( this is an apparent distance, since player doesnot move, but obstacles and ennemies shift to the left)
battle=[battles(3000,5,50,[23,34],50,3,4),battles(6000,5,50,[23,34],60,3,4)]
done=False               
obstacle=[]
def generate_obstacles(environment):
    environment.pos[0]=environment.mid #pro reasons
    for dis in range(2000,environment.length+1000,1000): #Creating obstacles on from the base 1000 to the max length of the field, and increment by 1000
        obstacles_in_sector=random.randrange(1,3)#the number of obstacles in each sector vary from 1 to 2
        for i in range(obstacles_in_sector): #creating (obstacles_in_sector) number of obstacles 
            x=random.randrange(dis-1000,dis) # here we subdivide the field in sub sectors of 1000m, randomize thier x cordinates and create obstacles for each block
            width=165;length=190 # Randomizing the length and the width of the obstaclse
            _type=random.randrange(2) #randomizing the type of obstacle that will be displayed
            obstacle.append(obstacles([x,390],[width,length],_type)) #Adding the new obstacle to the list of obstacles
    #Above, we are saying exactly were (in terms of x coordinate) the obstacles will be
ennemy=[] #pos , size, health and damage
#battle_ennemies=[] This list was delated
coin=[] #this list will contain all the coins which will be found on the field  
cloud=[] #this list will contain all the clouds
def generate_coins_and_clouds(environment): #pos type value
    for dis in range(1000,environment.length+1000,1000):
        coins_in_sector=random.randrange(1,6) #coins in a sector range from 1 to 6
        clouds_in_sector=random.randrange(1,4) #clouds in sector range from 1 to 4
        for i in range(clouds_in_sector):   
            x=random.randrange(dis-1000,dis+100)#please don't mine the "+100", it was just for a test
            y=random.randrange(50,150)#the y coordinate of each cloud vary in this range
            rand=random.randrange(3); speed=random.randrange(1,3)
            type_=rand #the 3 clouds will be stored in an array (0 to 2), and so will correspond to a type when passed to the show function(later..)
            cloud.append(Sky([x,y],type_,speed))

        for i in range(coins_in_sector):
            x=random.randrange(dis-1000,dis) #randomize the position of the coin in the sector
            rand=random.randrange(7)
            if rand<3:#probability(4/7) i.e 0,1,2 or 3
                type_=0;value=100;duration=100
            elif rand>=3 or rand<=5: #probability(2/7) i.e  4 or 5
                type_=1;value=200; duration=75
            else :#probability (1/7) i.e 6 
                type_=2;value=500; duration=50
            coin.append(money([x,550],type_,value,duration)) #appending a new coin to the list of coins. #pos typeofcoin and valueofcoin            

def generate_ennemies(ennemy,environment):
    for count in range(100):
        if count%5 == 0: #Creating 1 intelligent ennemy on every 5 created
            intelligent=True
        else: 
            intelligent=False
        health=(count+8)*2; damage=1
        x=random.randrange(1000,environment.length)
        length=140;width=50; hairstyle=random.randrange(3) #randomizing to choose one of the 3 hair styles
        ennemy.append(ennemies([x,475],[width,length],health,damage,50,10,15,intelligent,[1,hairstyle]))#this last parameter is the type of ennemy and it's hairstyle
                                #pos,size, health, damage, shoot_probability, max_bullets,bullets_speed, intelligence




 #[FADING SURFACE]
fade_surface=pygame.Surface(size) # Creating a surface
fade_surface.fill((0,0,0)) # the color of the surface is black
def fade(surface,speed):
    state=[[(63,49,81),40,(159, 90, 125),30],[(0,32,96),55,(33, 137, 197),33]] #the first part of the list contains the size and color of the unlighted button, and the second for the lighted button
    ste=[0,0,0] #this is the list that will contain the state of each of the 3 buttons
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

#[PAUSE MENU]
def pause_menu():
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
                    out=True
                    print("Start Game")
                if state[1]==1: #same comment as above and below
                    print("OPTIONS")
                if state[2]==1: # if the state of the 3 button is 1(the mouse is on it).Then we exit since the button says"Exit":-]
                    out=True;done=True
        pygame.display.update()  
        time.tick(20)

#[MAIN MENU]
def main_menu():
    exit_=False
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
                    play()
                if ste[1]==1: #same comment as above and below
                    print("Credits")
                if ste[2]==1: # if the state of the 3 button is 1(the mouse is on it).Then we exit since the button says"Exit":-]
                    exit_=True
        
        #message("Surviver Escape",[150,100],110,(0,0,0),"chiller")
        #screen.blit(bult,[300,500])
        pygame.display.update()
        time.tick(40)


#[ P L A Y ! ]
def play():
    done=False
    generate_obstacles(environment)
    generate_ennemies(ennemy,environment)
    generate_coins_and_clouds(environment)
    #MAIN LOOP
    while not done :
        for event in pygame.event.get():
            if event.type==QUIT:
                done=True
        keys=pygame.key.get_pressed()
        if keys[K_RIGHT] :# if key is pressed and there are no obstacles on the right side of the player
            if  hero.rightway: #below, if player is not at shifting point and there is not a battle going on, then it can move normally
                if hero.pos[0]>=environment.mid and not(environment.battle): #if player has traversed the middle of the screen, he does not move forward anymore, but the environment(obstacles,ennemies) infront shifts back to him
                    environment.shift(obstacle,ennemy,fire1,coin,cloud)
                else: #but if there is a battle going on or environment mid is reached..
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
                #print("idle!!")
        
        if keys[K_f] :
            #if (len(fire1)<hero.max_bullets): #ie a new ball is created iff the maximum number of simultaneous bullets on field is not exceeded
            if hero.state[0]==0 : #if player is looking left , we have to load a bullet in the left direction
                                #        pos                    size  damage target owner direction speed
                fire1.append(bullet([hero.pos[0]-40,hero.pos[1]+8],[20,10],  hero.damage+hero.power_state[2],ennemy, 0  ,    -1 ,hero.bullet_speed+hero.power_state[1]))
            if hero.state[0]==1 : #if player is looking right, we instead load a bullet in the right direction
                fire1.append(bullet([hero.pos[0]+hero.size[0]+5,hero.pos[1]+8],[20,10], hero.damage ,ennemy,0  ,    1 ,hero.bullet_speed))
            fire1[-1].exist=True # setting to True the existance of the last bullet(-1) of the list, that we just created
            hero.fired=True

        elif keys[K_d]:
            if hero.state[1]!=3 and hero.foot_on_ground : # if player is not jumping already,not falling,and has his foot on the ground, then a jump is possible( if user presses d)
                hero.state[1]=3
                if hero.pos[1]==500:
                    hero.pos[1]-=10 #to avoid foot_on_ground inorder for the jump function to load
                else: 
                    hero.pos[1]-=15
        elif keys[K_SPACE]:
            pause_menu()
            
        
        
            #DISPLAYING and Keeping Track of events
        hero.check_foot(obstacle) #checking whether or not player's foot is on ground( standing on an obstacle or on the ground).if not foot_on_ground is set to False else it is set to True
        hero.check_jump() #keeping track of the jumping motion if hero is in jumping state(state=3)
        hero.check_state(obstacle,ennemy) #checking if player if does not have foot on ground and is not jumping to then make him fall, AND checking if he is not touching any ennemy.. to then reduce his health
        hero.initial_health
        
        #print(hero.health)
        
        screen.fill((67,11,46))
        screen.blit(sky[1],[0,0]) #diplaying the sky
        pygame.draw.rect(screen,(163, 163, 169),(0,environment.ground_level,1000,200)) #the flour
        #environment.polygons(900,625,1) #displaying and keeping track of the polygons
        environment.health_bars(hero) # computing and displaying health bars
        environment.show(hero) #hero is passed because the number of coins to be shawn on the bar is owned by the player's class (hero!) :-)

        for i in range(len(coin)): #--COINS--
            if coin[i].exist and coin[i].pos[0]<1300 and coin[i].pos[0]>-300 :
                coin[i].collect(hero) #keeping track of each coin, hero is passed because it is the hero that collects the coins, and so we need he coordinates
                coin[i].show() #displaying the coins

        for i in range(len(cloud)):# --CLOUDS--
            cloud[i].show()

        for i in range(len(battle)):
            battle[i].check_proximity(environment,ennemy)
            battle[i].keep_track(ennemy)

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
    
        pygame.display.update()
        time.tick(FPS)
if __name__=="__main__":
    main_menu()
    pygame.quit()
