import pygame
import time
import const
from enemy import Enemy
from pygame.locals import *


class Enemies(pygame.sprite.Sprite) :
	def __init__(self,enemyList,startPoint): 
		super().__init__()
		self.enemyList = enemyList
		self.enemyGroup = pygame.sprite.Group()
		self.startPoint = startPoint
		self.waves = []
		#alustetaan enemies myös tämä luokka perii pygame.sprite.Sprite luokalta koska
		#täytyy pystyä käyttämään Groups tietorakennetta

	def getWaveEnemyNumber(self,waveNumber):
		return self.enemyList[waveNumber][0]

	def getIfWavesLeft(self):
		if len(self.enemyList) == 0 :
			return False
		else:
			return True

	def getWaves(self):
		return len(self.enemyList)

	def getEnemyList(self):
		return self.enemyGroup

	def moveEnemies(self,corners,player):
		
		for i in self.enemyGroup:
			for h in corners:
				pos = i.getPos()
				if h[0]-5<= pos[0] and pos[0]<=h[0]+5 and h[1]-5 <=pos[1] and pos[1] <= h[1]+5:
					i.direction = h[2]

			i.move(i.direction)
			i.didEnemySurvive(player)
		#tämä metodi hoitaa vihollisjoukkojen liikuttelun tiettyyn suuntaan
		#eli tarpeen mukaan kutsuu yhdelle viholliselle move funktiota ja tarkastelee
		#selvisikö vihollinen maaliin asti. Vihollisen liikkumisessa on 5 pikselin
		#toleranssit, muuten tietyllä nopeudella liikkuvat ohittaisivat 

	def drawEnemies(self,surf):
		for j in self.enemyGroup:
			surf.blit(j.image,(j.rect.x,j.rect.y))
		#metodi hoitaa vihollisten piirtämisen ruudulle

	def spawn(self,waveNumber,enemyCounter,spawnCounter,drawList):
		wave = self.enemyList[waveNumber]
		list1 = drawList
		list1.add(Enemy(const.ORANGE,30,30,wave[1],wave[2],self.startPoint[0],self.startPoint[1],self.startPoint[2]))
		self.enemyGroup = list1
		if enemyCounter == 1:
			self.enemyList.remove(wave)
		#metodi hoitaa uusien vihollisten luomisen 
