import pygame
import const


class Enemy(pygame.sprite.Sprite):
	def __init__(self,color,width,height,hp,speed,x,y,direct):
		super().__init__()

		self.direction = direct
		self.hp = hp
		self.speed = speed
		self.reward = hp*speed

		self.image = pygame.Surface([width,height]) 
		self.image.fill(color)

		self.rect = self.image.get_rect()

		self.mask = pygame.mask.from_surface(self.image)

		self.rect.x = x
		self.rect.y = y
		#vihollisen alustus

	def reduceHp(self,dmgTaken):
		self.hp = self.hp - dmgTaken

	def setEnemy(self,x,y):
		self.rect.x = x	
		self.rect.y = y

	def move(self,direction):
		if (direction == 'left'):
			self.rect.x -= self.speed

		if (direction == 'down'):
			self.rect.y += self.speed

		if (direction == 'right'):
			self.rect.x += self.speed

		if (direction == 'up'):
			self.rect.y -= self.speed
		#metodi liikuttaa yhtä vihollista tiettyyn suuntaan, suunnat on merkitty
		#pelin alustustekstitiedossa
	def getPos(self):
		pos = (self.rect.x,self.rect.y)
		return pos

	def getHp(self):
		return self.hp

	def killEnemy(self,player):
		player.addMoney(self.reward)
		self.kill()
		#tämä metodi tuhoaa vihollisen ja antaa pelaajalle palkkion tappamisesta

	def didEnemySurvive(self,player):
		if self.rect.x >= const.SCREEN_WIDTH or self.rect.y >= const.SCREEN_HEIGHT:
			player.enemyPassed()
			self.kill()
		#tarkastelee selvisikö vihollinen maaliin. Toisin sanoen tarkastelee
		#onko vihollisen sijainti näkyvän ruudun ulkopuolella
