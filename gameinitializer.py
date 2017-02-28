import pygame, sys
import const
from enemy import Enemy
from tower import Tower
from enemies import Enemies
from pygame.locals import *

pygame.font.init()
class Block(pygame.sprite.Sprite):
	def __init__(self,color,width,height,x,y):
		super().__init__()
		self.image = pygame.Surface([width,height]) 
		self.image.fill(color)
		self.rect = self.image.get_rect()
		self.width = width
		self.height = height
		self.rect.x = x
		self.rect.y = y
	#kenttä palikan alustus

class Reader:
	def __init__(self,textfile):
		self.textfile = textfile
		self.enemyList = []
		self.cornerList = []
		self.towerTypesList = []
		self.player2 = []
		self.towerImages = []
		self.explanations = []
		self.startPoint = []
		self.gamefield = pygame.sprite.Group()
		self.towerGroup = pygame.sprite.Group()
	#lukijan alustus
	def readFile(self):

		with open(self.textfile) as file:
			for line in file:
				splittedLine = line.split(':')
				if splittedLine[0] == 'Enemy':
					enemy = splittedLine[1].split(',')
					enemyTemp = [int(enemy[0]),int(enemy[1]),int(enemy[2])]
					self.enemyList.append(enemyTemp)

				if splittedLine[0] == 'Field':
					startpoint = splittedLine[1].split(',')
					self.startPoint = [int(startpoint[0]),int(startpoint[1]),startpoint[2].rstrip()]
					self.cornerList.append(self.startPoint)

				if splittedLine[0] == 'Corner':
					corner = splittedLine[1].split(',')
					cornerTemp = [int(corner[0]),int(corner[1]),corner[2].rstrip()]
					self.cornerList.append(cornerTemp)

				if splittedLine[0] == 'Tower':
					tower = splittedLine[1].split(',')
					towerTemp = [int(tower[0]),int(tower[1]),int(tower[2]),int(tower[3]),int(tower[4])]
					self.towerTypesList.append(towerTemp)

				if splittedLine[0] == 'Player':
					player = splittedLine[1].split(',')
					self.player2 = [int(player[0]),int(player[1])]

		file.close()
		#luetaan asetustiedosto rivi riviltä ja lisäillään tiedot lukija self. tietoihin

	def getEnemiesList(self):
		return self.enemyList

	def getCornerList(self):
		return self.cornerList

	def getTowerTypes(self):
		return self.towerTypesList

	def getStartPoint(self):
		return self.startPoint

	def getGamefield(self):
		return self.gamefield

	def setTowerImages(self):
		length = len(self.towerTypesList)
		i = 0

		while i < length:
			tower_t = Tower(const.GREEN,40,40,self.towerTypesList[i][0],self.towerTypesList[i][1],self.towerTypesList[i][2],self.towerTypesList[i][3],self.towerTypesList[i][4])
			tower_t.rect.x = 200+i*50
			tower_t.rect.y = 20
			i += 1
			self.towerGroup.add(tower_t)
			font1 = pygame.font.SysFont('Arial',30)
			font = font1.render(str(i),True,(255,255,255),None)
			self.towerImages.append(font)
		#luodaan ns. tornikatalogi josta tornit ostetaan

	def drawTowerNumbers(self,surf):
		i = 0
		while i < len(self.towerImages):
			surf.blit(self.towerImages[i],(200+i*50,20))
			i += 1
		#numeroidaan katalogin tornit tunnistusta varten

	def initExplanations(self):
		i = 0
		font2 = pygame.font.SysFont('Arial',12)
		while i < len(self.towerTypesList):
			string ='Tower'+str(i+1)+'  Dmg:'+str(self.towerTypesList[i][0])\
			+' AttackSpeed:'+str(self.towerTypesList[i][1])\
			+' Radius:'+str(self.towerTypesList[i][2])\
			+' Cost:'+str(self.towerTypesList[i][3])
			if (self.towerTypesList[i][4]) == 1:
				string += ' Smart'
			fontb = font2.render(string,True,(255,255,255),None)
			self.explanations.append(fontb)
			i += 1
		#alustetaan tornien selitykset joissa kerrotaan kunkin tornin "tekniset tiedot"

	def drawExplanations(self,surf):
		i = 0
		while i < len(self.explanations):
			surf.blit(self.explanations[i],(450,20+i*15))
			i += 1
		#totetuttaa käytännön piirtämisen selityksille

	def initializeGamefield(self):
		a = 0
		point = self.startPoint
		list_length = len(self.cornerList)
		while a < list_length:
			width = height = 0
			turn = self.cornerList[a][2]
			if turn == 'left':
				if a == list_length-1:
					width = const.SCREEN_WIDTH - self.cornerList[a][0]+38
				else:
					width = self.cornerList[a][0] - self.cornerList[a+1][0]+38
				height = 50
				x = self.cornerList[a][0]-width+26
				y = self.cornerList[a][1]-12

			elif turn == 'up':	
				width = 50
				if a == list_length-1:
					height = const.SCREEN_HEIGHT -  self.cornerList[a+1][1]+38
				else :
					height = self.cornerList[a][1] - self.cornerList[a+1][1]+38
				x = self.cornerList[a][0]-12
				y = self.cornerList[a][1]-height+26

			elif turn == 'right':	
				if a == list_length-1:
					width = const.SCREEN_WIDTH - self.cornerList[a][0]+38
				else :
					width = self.cornerList[a+1][0] - self.cornerList[a][0]+38
				height = 50
				x = self.cornerList[a][0]
				y = self.cornerList[a][1]-12

			elif turn == 'down':	
				width = 50
				if a == list_length-1:
					height = const.SCREEN_HEIGHT - self.cornerList[a][1]+38
				else:
					height = self.cornerList[a+1][1] - self.cornerList[a][1]+38
				x = self.cornerList[a][0]-12
				y = self.cornerList[a][1]


			block = Block(const.BLUE,width,height,x,y)
			self.gamefield.add(block)
			a +=1

		#alustetaan reitti vihollisille lisätietoa dokumentoinnissa



			
 