import pygame, sys
import const

class Player():
	"""Class for the player information on towers and simple functions to add and move them."""
	def __init__(self,money,limit):
		self.towers = pygame.sprite.Group()
		self.money = money
		self.enemyPassLimit = limit
		self.infoFields = []

	def addTower(self,tower):
		self.towers.add(tower)
		self.addMoney(-tower.getCost())

	def moveTowers(self,tower,pos):
		self.towers.tower.rect.x = pos[0]
		self.towers.tower.rect.y = pos[1]

	def getMoney(self):
		return self.money

	def getTowers(self):
		return self.towers

	def addMoney(self,amount):
		self.money += amount


	def gameLost(self):
		print('YOU LOST THE GAME....loser!')
		if self.secret() == False:
			pygame.quit()
			sys.exit()
		

	def enemyPassed(self):
		"""If an enemy survived call this function to reduce the limit that can pass beofre losing the game."""
		self.enemyPassLimit -= 1
		if self.enemyPassLimit == 0:
			self.gameLost()
			print(self.enemyPassLimit)

		elif self.enemyPassLimit == -1:
			print('Really another one')

		elif self.enemyPassLimit == -2:
			print('Come on this is just ridiculous')
	
		elif self.enemyPassLimit == -3:
			print("Just hit the x button, you're not getting anywhere")

		elif self.enemyPassLimit == -4:
			print('LAST Warning....QUIT')

		elif self.enemyPassLimit == -5:
			pygame.quit()
			sys.exit()

	def secret(self):
		"""Try pressing S when you would lose..."""
		if pygame.key.get_pressed()[pygame.K_s] != 0:
			print('Weeeell...Have another go!')
			return True
		else : return False

	def initInfo(self):
		"""Initialize the player's information to show on screen."""
		self.infoFields = []
		font2 = pygame.font.SysFont('Arial',12)
		string ='Enemies may still pass: '+str(self.enemyPassLimit)
		string2 = 'Money left: '+ str(self.money)
		fonta = font2.render(string,True,(255,255,255),None)
		fontb = font2.render(string2,True,(255,255,255),None)
		self.infoFields.append(fonta)
		self.infoFields.append(fontb)

	def drawInfo(self,surf):
		i = 0
		while i < len(self.infoFields):
			surf.blit(self.infoFields[i],(450,60+i*15))
			i += 1

