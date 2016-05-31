import pygame, sys
import const

class Player():
	def __init__(self,money,limit):
		self.towers = pygame.sprite.Group()
		self.money = money
		self.enemyPassLimit = limit
		self.infoFields = []
		#tässä alustetaan pelaaja ja sen perustiedot

	def addTower(self,tower):
		self.towers.add(tower)
		self.addMoney(-tower.getCost())
		#lisätään torneja pelaajan tornilistaan

	def moveTowers(self,tower,pos):
		self.towers.tower.rect.x = pos[0]
		self.towers.tower.rect.y = pos[1]
		#siirretään torni haluttuun paikkaan

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
		#peli hävitty -> peli sammuu 

	def gameWon(self):
		a = 1
		if a ==1:
			print('YOU WON!!!')
			pygame.quit()
			sys.exit()
		#tämä metodi ei toimi oikein siksi sitä ei käytetty loppujen lopuksi ollenkaan

	def enemyPassed(self):
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
		#jos vihollinen pääsee maaliin tätä metodia kutsutaan miinustaa pelaajan
		#vihollisrajasta 1 jos vihollis raja on nolla kutsutaan gameLost metodia
		#ellei salaominaisuus tule käyttöön

	def secret(self):
		if pygame.key.get_pressed()[pygame.K_s] != 0:
			print('Weeeell...Have another go!')
			return True
		else : return False
		#salaominaisuus

	def initInfo(self):
		self.infoFields = []
		font2 = pygame.font.SysFont('Arial',12)
		string ='Enemies may still pass: '+str(self.enemyPassLimit)
		string2 = 'Money left: '+ str(self.money)
		fonta = font2.render(string,True,(255,255,255),None)
		fontb = font2.render(string2,True,(255,255,255),None)
		self.infoFields.append(fonta)
		self.infoFields.append(fontb)
		#tässä alustetaan pelaajan tiedot ja fontti jolla se piirretään ruudulle

	def drawInfo(self,surf):
		i = 0
		while i < len(self.infoFields):
			surf.blit(self.infoFields[i],(450,60+i*15))
			i += 1
		#tämä funktio käytänössä toteuttaa piirätmisen ruudulle
