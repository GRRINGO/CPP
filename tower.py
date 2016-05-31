import pygame
import math
import const
from enemy import Enemy
from pygame.locals import *


class Tower(pygame.sprite.Sprite):
	def __init__(self,color,width,height,dmg,attackSpeed,radius,cost,smart):
		super().__init__()

		self.dmg = dmg
		self.attackSpeed = attackSpeed
		self.radius = radius
		self.towerSet = False
		self.cost = cost
		self.alive = False
		self.smartTower = smart
		self.target = Enemy(const.JOKU,1,1,100000,0,10000,10000,0)

		self.filler = 0

		self.image = pygame.Surface([width,height]) 
		self.image.fill(color)
		self.rect = self.image.get_rect()
		#alustetaan torni

	def towerSelected(self):
		mouse_pos = pygame.mouse.get_pos()
		pos = self.getPos()
		if pos[0] < mouse_pos[0] < pos[0]+self.rect.width and pos[1] < mouse_pos[1] < pos[1]+self.rect.height :
			return True
		else : return False
		#tarkastellaan onko hiiri tornin päällä. Metodi tulee tarpeen kun torneja ostetaan

	def getDmg(self):
		return self.dmg

	def getAttackSpeed(self):
		return self.attackSpeed

	def getRadius(self):
		return self.radius

	def getTowerState(self):
		return self.towerSet

	def getCost(self):
		return self.cost

	def getAlive(self):
		return self.alive

	def getPos(self):
		pos = (self.rect.x,self.rect.y)
		return pos

	def getIfSmart(self):
		return self.smartTower

	def setAlive(self,aliveValue):
		self.alive = aliveValue

	def shoot(self,enemy,player):
		e_pos = enemy.getPos()
		dist2 = self.distanceToEnemy(enemy)

		self.image.fill((255,255,255))

		enemy.reduceHp(self.dmg)
		if enemy.getHp() <= 0:
			enemy.killEnemy(player)

		#metodi hoitaa ampumisen eli väläyttää tornia valkoisena hetken
		#kutsuu viholliselle metodia jolla siltä vähennetään hp:ta
		#ja lisäksi tarkastelee kuoliko vihollinen iskusta

	def moveTower(self,pos_x,pos_y):
		if self.towerSet == False:
			self.rect.x = pos_x
			self.rect.y = pos_y
			self.alive = True
			self.towerSet = True
		#liikuttaa tornia ja asettaa sen aktiiviseksi ja merkitsee että
		#tornia ei voi enää liikuttaa

	def setTowerState(self,setValue):
		self.towerSet = setValue

	def distanceToEnemy(self,enemy):
		t_pos = self.getPos()
		e_pos = enemy.getPos()


		if t_pos[0] < e_pos[0]:
			x = e_pos[0] - t_pos[0]
		else :
			x = t_pos[0] - e_pos[0]

		if t_pos[1] < e_pos[1]:
			y = e_pos[1] - t_pos[1]
		else:
			y = t_pos[1] - e_pos[1]

		if x != t_pos[0] and y != t_pos[1]:
			dist1 = math.sqrt(x*x + y*y)
		else :
			dist1 = self.radius+10

		return dist1
		#lasketaan etäisyys tornin ja vihollisen välillä
		#lisätietoa dokumentoinnissa kohdassa algoritmit

	def closestEnemy(self,enemyList):
		closest = Enemy(const.JOKU,1,1,1,0,0,0,0)
		dist = self.radius+1
		for i in enemyList:
			tempDist = self.distanceToEnemy(i)
			if tempDist < dist:
				closest = i
		return closest
		#laskee mikä kaikista elävistä vihollisista on lähimpänä tornia
		#tässä vertaillaan vihollisten etäisyyttä torniin ja katsotaan mikä
		#loppujen lopuksi on lähimpänä ja palautetaan se

	def enemyInRange(self,enemy):
		distance = self.distanceToEnemy(enemy)
		if distance < self.radius+1:
			return True
		else:
			return False
		#tarkastellaan onko jokin vihollinen kantamalla

	def notInPath(self,blocks,pos):
		check = 0
		for i in blocks :
			if ((pos[0] < i.rect.x and pos[0]+40 < i.rect.x )
			or (pos[0] > i.rect.x+i.width and pos[0]+40 > i.rect.x + i.width)
			or (pos[1] < i.rect.y and pos[1]+40 < i.rect.y) 
			or (pos[1] > i.rect.y+i.height and pos[1]+40 > i.rect.y + i.height)):
				check = 0

			else: 
				return False
		if check == 0:
			return True
		#tarkastellaan onko torni vihollisten reitin päällä kun torni ostetaan
		#ja se yritetään asettaa tiettyyn paikkaan

		