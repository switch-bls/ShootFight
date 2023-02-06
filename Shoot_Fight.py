import pygame
from random import randint

pygame.init()

class player(object):													
	def __init__(self,x,y,k_l,k_r,k_j,k_s,k_c1,k_c2,face,skin):						
						
		self.rect=skin[3].get_rect()									
		self.rect.x=x
		self.rect.y=y
															
		self.time_shoot=0
		self.xvel=0												
		self.yvel=0														
		self.health=500													
		self.skin=skin
		
		self.walkCount=0												
		self.ground=False										
		self.double_jump=False
		self.jump_count=0
		self.recoil=False	
		self.anim_count=0
		self.sneak=False
		self.cadence=40
		self.b_alea=0
		self.b_count=0
				
		self.k_l=k_l													#definition des touche clavier comme evenement(gauche)
		self.k_r=k_r													#droite
		self.k_j=k_j													#saut
		self.k_s=k_s													#tire
		self.k_c1=k_c1
		self.k_c2=k_c2
		
		self.other = []													
		self.face=face													#etat de la face(vers la ghauche ou la droite)
		self.bullets = []
		ToDraw.append(self)												#liste de projectile emis par le joueur
		player_list.append(self)
		
	def event(self):													#fonction qui contient l'entiereté des evenement en rapport avec le joueur

		keys = pygame.key.get_pressed()									#definition de l'evenement "touche presser sur le clavier"			
		
		if round(self.xvel)!=0 and self.ground:												#sinon pas de direction 
				self.xvel = self.xvel*0.7
				
		self.yvel+=1	
		
		if keys[self.k_s]:
				self.rect=pygame.Rect(self.rect.x,self.rect.y,48,45)
				self.sneak=True
			
		elif not self.recoil:
			
			if keys[self.k_l]:												#si la touche gauche est pressé, alors
				self.xvel= -7												
				self.face= -1												
				
			elif keys[self.k_r]:					
				self.xvel= 7											
				self.face=1													
			
			if keys[self.k_j] and self.ground:													
				self.yvel -= 20
				self.ground=False
			
			
			if keys[self.k_j]==0 and not self.ground and self.jump_count==0:
				self.double_jump=True
				self.jump_count+=1

			
			if keys[self.k_j] and self.double_jump:
				self.yvel = -20
				self.double_jump=False

			if self.time_shoot!=self.cadence:											
				self.time_shoot+=1											
				
			if keys[self.k_c1] and self.time_shoot>=self.cadence:											
				self.bullets.append(bill(self.rect.x,self.rect.y,self.face))												
				self.time_shoot=0	
				
			if keys[self.k_c2] and self.time_shoot>=self.cadence:											
				self.bullets.append(fire_ball(self.rect.x,self.rect.y,self.face))												
				self.time_shoot=0
			
			if self.sneak:
				self.sneak=False
				self.rect=pygame.Rect(self.rect.x,self.rect.y-40,48,85)

		else:
			
			if self.anim_count == 0:
				self.yvel -= 7
				self.xvel=5*self.face*(-1)
			
			if self.anim_count == 25:
				self.anim_count = 0
				self.recoil=False
			else:self.anim_count+=1
			
			if self.sneak:
				self.sneak=False
				self.rect=pygame.Rect(self.rect.x,self.rect.y-40,48,85)
			
		for bullet in self.bullets:																	
			for entity in entities:
				if bullet.rect.colliderect(entity.rect):
					self.bullets.pop(self.bullets.index(bullet))
					animations.append(explosion(bullet.rect.x,bullet.rect.y))

		if self.health<=0:												
			self.health=0				
		
	def take_damage(self):
		for bullet in self.bullets:
			for victim in self.other:											
				if victim.rect.colliderect(bullet.rect):							
					victim.health -= 50												
					self.bullets.pop(self.bullets.index(bullet))
					animations.append(explosion(bullet.rect.x,bullet.rect.y))
					victim.recoil=True
					victim.face=bullet.face*(-1)
								
	def move(self):
		
		if  self.xvel != 0:self.move_single_axis(round(self.xvel), 0)

		if  self.yvel != 0:self.move_single_axis(0, round(self.yvel))
		
	def move_single_axis(self, xvel, yvel):
		
		global time_speed
		
		self.ground=False
		self.rect.x += xvel
		self.rect.y += yvel
		
		for entity in entities:
			
			if self.rect.colliderect(entity.rect):
				
				if xvel > 0:
					self.rect.right = entity.rect.left
				
				if xvel < 0:
					self.rect.left = entity.rect.right
				
				if yvel > 0:
					self.rect.bottom = entity.rect.top
					self.ground=True
					self.double_jump=False
					self.yvel = 0
					self.jump_count=0
					
				if yvel < 0:
					self.rect.top = entity.rect.bottom
					if entity.genre==1:
						entity.give_bonus=True
						entity.receiver=self
					self.yvel = 0
													
	def draw(self):														
		self.event()
		self.move()			
		self.take_damage()	
									
		if self.sneak:
			if self.face==-1:
					win.blit(self.skin[10], (self.rect.x, self.rect.y))	
			if self.face==1:
					win.blit(self.skin[11], (self.rect.x, self.rect.y))
					
		elif self.time_shoot<5:
			if self.face==-1:
					win.blit(self.skin[12], (self.rect.x, self.rect.y))	
			if self.face==1:
					win.blit(self.skin[13], (self.rect.x, self.rect.y))
		
		elif not self.recoil:
			if self.walkCount+1 > 12:										
				self.walkCount = 0
															
			if not self.ground:
				if self.face==-1:
					win.blit(self.skin[12], (self.rect.x, self.rect.y))	
				if self.face==1:
					win.blit(self.skin[13], (self.rect.x, self.rect.y))	
				
			elif self.xvel==-7:
				win.blit(self.skin[round(self.walkCount)//3], (self.rect.x,self.rect.y))#Si le personnage va à gauche on lit l'image dans la liste walkLeft
				self.walkCount += 0.4										#On incrémente la variable walkCount de 0.5 pour la vitesse de l'animation
			
			elif self.xvel==7:
				win.blit (self.skin[round(self.walkCount)//3+4], (self.rect.x,self.rect.y))#De même vers la droite
				self.walkCount += 0.4
			
			else:
				if self.face== -1:                                         
					win.blit(self.skin[3], (self.rect.x, self.rect.y))			
				elif self.face== 1:											
					win.blit(self.skin[7], (self.rect.x, self.rect.y))
				
		else:
			if self.face==-1:
					win.blit(self.skin[8], (self.rect.x, self.rect.y))	
			if self.face==1:
					win.blit(self.skin[9], (self.rect.x, self.rect.y))
								
class bill(object):								
	def __init__(self,x,y,face):										
		self.rect = bulletl.get_rect()	
		self.rect.x = x
		self.rect.y = y+11
		self.face = face												#une face vers la quel ils se dirige
		self.xvel= 15													
			
	def move(self):
		self.rect.x += self.xvel*self.face		
										
	def draw(self):
		self.move()
			
		if self.face==-1:												
			win.blit(bulletl,(self.rect.x,self.rect.y,10,10))
		if self.face==1:												
			win.blit(bulletr,(self.rect.x,self.rect.y,10,10))	
			
class fire_ball(object):
	def	__init__(self,x,y,face):										
		self.rect = fire_ball1.get_rect()	
		self.rect.x = x
		self.rect.y = y+30
		self.face = face
		self.anim_count=0
		self.yvel=0											
		self.xvel=7*self.face
		
	def move(self):
		
		self.yvel+=0.7
		
		if  self.xvel != 0:self.move_single_axis(self.xvel, 0)

		if  self.yvel != 0:self.move_single_axis(0,self.yvel)
		
	def move_single_axis(self, xvel, yvel):
		
		self.rect.y += yvel
		self.rect.x += xvel
		
		for entity in entities:
			
			if self.rect.colliderect(entity.rect):
				
				if xvel > 0:
					self.rect.right = entity.rect.left
					self.face=self.face*(-1)
				if xvel < 0:
					self.rect.left = entity.rect.right
					self.face=self.face*(-1)
				if yvel > 0:
					self.rect.bottom = entity.rect.top
					self.yvel=-10
					
		self.xvel=7*self.face
							
	def draw(self):
		
		self.move()
		
		self.anim_count+=0.5
		if self.anim_count+1>12:
			self.anim_count=0
														
		win.blit(fire_ball_anim[round(self.anim_count)//3],(self.rect.x,self.rect.y,10,10))				
													
class platform(object):													
	def __init__(self,x,y,image):										
		self.image=image												
		self.rect=image.get_rect()										
		self.rect.y=y													
		self.rect.x=x
		self.genre = 0
		entities.append(self)										
		ToDraw.append(self)																
	def draw(self):
		win.blit(self.image,(self.rect.x,self.rect.y))
		
class block_mist(object):
	def __init__(self,x,y):										
		self.image=mist_block										
		self.rect=self.image.get_rect()									
		self.rect.y=y													
		self.rect.x=x
		self.rect[3]+=1
		self.genre = 1
		
		self.count = 0
		self.give_bonus=False
		
		self.receiver=0
		
		entities.append(self)										
		ToDraw.append(self)	
		
	def bonus(self):
		
		alea=0
		
		if self.give_bonus and self.image == mist_block:
			alea=randint(1,2)
			self.image=block
		
		if self.give_bonus:
			self.count+=1
			if self.count == 1000:
				self.give_bonus=False
				self.image=mist_block
				self.receiver.cadence=40			
				self.count=0
			
			if alea>0:
				animations.append(pop(self,bonus_pop[alea-1]))
				
			if alea==1:
				self.receiver.health+=100
			if alea==2:
				self.receiver.cadence=20
			
		
																			
	def draw(self):
		self.bonus()	
				
		win.blit(self.image,(self.rect.x,self.rect.y))

class explosion(object):
	def __init__(self,x,y):
		self.rect=explosion3.get_rect()
		self.rect.y=y													
		self.rect.x=x
		self.anim_count=0
		ToDraw.append(self)
		
	def draw(self):
		win.blit(explosion_anim[round(self.anim_count)//3],(self.rect.x,self.rect.y,32,32))
		self.anim_count+=1
		if self.anim_count+1>15:
			animations.pop(animations.index(self))
			ToDraw.pop(ToDraw.index(self))
		
class pop(object):
	def __init__(self,entity,image):
		self.image=image
		self.rect=image.get_rect()
		self.rect.x = entity.rect.x-2
		self.rect.y = entity.rect.y-56
		self.yvel=-3
		ToDraw.append(self)
		
	def draw(self):
		self.yvel+=0.1
		self.rect.y += self.yvel
		win.blit(self.image,(self.rect.x,self.rect.y,32,32))
		if round(self.yvel)==1:
			animations.pop(animations.index(self))
			ToDraw.pop(ToDraw.index(self))

class health_bar(object):
	def __init__(self,entity,x,y,reverse):
		self.x=x
		self.y=y
		self.entity=entity
		self.reverse=reverse
		ToDraw.append(self)
		self.health=entity.health
		
	def draw(self):
		
		self.health=self.entity.health
		if self.reverse:
			pygame.draw.rect(win,(0,200,0),(self.x+500-self.health,self.y,self.health,30))
			
		else:pygame.draw.rect(win,(0,200,0),(self.y,self.y,self.health,30))
		
def redraw(win):
	win.blit(fond,(0,0))
	
	for things in ToDraw:
		things.draw()
	
	for player in player_list:	
		for bullet in player.bullets:											#affiche les balles de chaque joueurs
			bullet.draw()
			
	pygame.display.update()

win = pygame.display.set_mode((1280,720))								
pygame.display.set_caption("Shoot Fight!")								
clock = pygame.time.Clock()												
time_speed=80

entities=[]
ToDraw=[]
player_list=[]
animations=[]

mario_skin = [pygame.image.load('asset/mario/mario_run1l.png').convert_alpha()		#0	
			,pygame.image.load('asset/mario/mario_run2l.png').convert_alpha()  		#1   	
			,pygame.image.load('asset/mario/mario_run1l.png').convert_alpha()		#2
			,pygame.image.load('asset/mario/mario_standingl.png').convert_alpha()	#3 
			,pygame.image.load('asset/mario/mario_run1r.png').convert_alpha()		#4
			,pygame.image.load('asset/mario/mario_run2r.png').convert_alpha()		#5
			,pygame.image.load('asset/mario/mario_run1r.png').convert_alpha()		#6
			,pygame.image.load('asset/mario/mario_standingr.png').convert_alpha()	#7
			,pygame.image.load('asset/mario/mario_damagel.png').convert_alpha()    	#8
			,pygame.image.load('asset/mario/mario_damager.png').convert_alpha()    	#9
			,pygame.image.load('asset/mario/mario_sneakl.png').convert_alpha()      #10
			,pygame.image.load('asset/mario/mario_sneakr.png').convert_alpha()		#11
			,pygame.image.load('asset/mario/mario_jumpl.png').convert_alpha()    	#12
			,pygame.image.load('asset/mario/mario_jumpr.png').convert_alpha()]   	#13
			
luigi_skin = [pygame.image.load('asset/luigi/luigi_run1l.png').convert_alpha()
			,pygame.image.load('asset/luigi/luigi_run2l.png').convert_alpha()
			,pygame.image.load('asset/luigi/luigi_run1l.png').convert_alpha()
			,pygame.image.load('asset/luigi/luigi_standingl.png').convert_alpha()		
			,pygame.image.load('asset/luigi/luigi_run1r.png').convert_alpha()
			,pygame.image.load('asset/luigi/luigi_run2r.png').convert_alpha()
			,pygame.image.load('asset/luigi/luigi_run1r.png').convert_alpha()
			,pygame.image.load('asset/luigi/luigi_standingr.png').convert_alpha()
			,pygame.image.load('asset/luigi/luigi_damagel.png').convert_alpha()
			,pygame.image.load('asset/luigi/luigi_damager.png').convert_alpha()
			,pygame.image.load('asset/luigi/luigi_sneakl.png').convert_alpha()
			,pygame.image.load('asset/luigi/luigi_sneakr.png').convert_alpha()
			,pygame.image.load('asset/luigi/luigi_jumpl.png').convert_alpha()
			,pygame.image.load('asset/luigi/luigi_jumpr.png').convert_alpha()]

bulletr = pygame.image.load("asset/bulletr.png").convert_alpha()
bulletl = pygame.image.load("asset/bulletl.png").convert_alpha()

fire_ball1 = pygame.image.load("asset/fire_ball1.png").convert_alpha()
fire_ball2 = pygame.image.load("asset/fire_ball2.png").convert_alpha()
fire_ball3 = pygame.image.load("asset/fire_ball3.png").convert_alpha()
fire_ball4 = pygame.image.load("asset/fire_ball4.png").convert_alpha()

explosion1 = pygame.image.load("asset/explosion1.png").convert_alpha()
explosion2 = pygame.image.load("asset/explosion2.png").convert_alpha()
explosion3 = pygame.image.load("asset/explosion3.png").convert_alpha()

sol = pygame.image.load("asset/sol.png").convert()	
brick_sol = pygame.image.load("asset/brick_sol.png").convert()
mist_block = pygame.image.load("asset/block2.png").convert_alpha()
block = pygame.image.load("asset/block1.png").convert_alpha()
brick = pygame.image.load("asset/brick.png").convert()
fond = pygame.image.load("asset/fond.jpg").convert()
p1_win = pygame.image.load("asset/p1_win.png").convert_alpha()
p2_win = pygame.image.load("asset/p2_win.png").convert_alpha()
wall1 = pygame.image.load("asset/wall1.png").convert()
bonus1 = pygame.image.load("asset/bonus1.png").convert_alpha()
bonus2 = pygame.image.load("asset/bonus2.png").convert_alpha()

fire_ball_anim=[fire_ball1,fire_ball2,fire_ball3,fire_ball4]
explosion_anim=[explosion1,explosion2,explosion3,explosion2,explosion1]
bonus_pop=[bonus2,bonus1]	
												
plat2=platform(360,330,brick)
plat3=platform(420,330,brick)
plat4=platform(240,330,brick)
plat5=platform(980,330,brick)
plat6=platform(800,330,brick)
plat7=platform(860,330,brick)
plat8=block_mist(920,330)
plat1=block_mist(300,330)
plat9=platform(550,200,block)
plat10=platform(610,200,block)
plat11=platform(670,200,block)
plat11=platform(610,536,brick_sol)
plat11=platform(674,536,brick_sol)
plat11=platform(546,536,brick_sol)
wallleft=platform(-100,-280,wall1)
wallrigth=platform(1280,-280,wall1)
sol=platform(0,600,sol)	

p1=player(1080,450,pygame.K_LEFT,pygame.K_RIGHT,pygame.K_UP,pygame.K_DOWN,pygame.K_KP5,pygame.K_KP6,-1,mario_skin) 
p2=player(200,450,pygame.K_a,pygame.K_d,pygame.K_w,pygame.K_s,pygame.K_t,pygame.K_y,1,luigi_skin)		
bar_p2=health_bar(p2,30,30,0)
bar_p1=health_bar(p1,720,30,1)
for player in player_list:
			player.other+=player_list
			player.other.remove(player)							
												
run = True
while run:																
	clock.tick(time_speed)														
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	redraw(win)
