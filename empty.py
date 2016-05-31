import pygame, sys
import const
from enemy import Enemy
from tower import Tower
from enemies import Enemies
from gameinitializer import Block
from gameinitializer import Reader
from player import Player
from pygame.locals import *

#aluksi alustetaan kaikenlaista tarpeellista ja pyydetään luettava tiedosto pelaajalta
reader = Reader(input('Enter the name of the file(must be in the same folder):'))
clock = pygame.time.Clock()
SCREEN = pygame.display.set_mode((const.SCREEN_WIDTH,const.SCREEN_HEIGHT))
#luodaan ruutu

reader.readFile()
reader.initializeGamefield()
reader.setTowerImages()
reader.initExplanations()

gamefield = reader.getGamefield()
player1 = Player(reader.player2[0],reader.player2[1])
corners = reader.getCornerList()
towerTypes = reader.getTowerTypes()

pygame.init()
pygame.font.init()

enemiess = Enemies(reader.getEnemiesList(),reader.getStartPoint())
waveNumber = enemiess.getWaves()
waveCount = 0
spawnCount = 0
shotCount = 0
enemyCount = -1
buyTime = True
k = 1
r = 1
#itse game loop
while True:  
	#tarkastellaan eventit käytännössä suurin osa on napin tai hiiren painalluksia
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN:
			if event.key == pygame.K_n and enemiess.getWaves() > 0 and (enemyCount == 0 or enemyCount == -1):
				spawnCount = 0
				enemyCount = enemiess.getWaveEnemyNumber(waveCount)
		if event.type == MOUSEBUTTONDOWN :
			for i in reader.towerGroup:
				if i.towerSelected() == True and player1.getMoney() > i.getCost() and buyTime == True:
					towerT = Tower(const.JOKU2,40,40,i.getDmg(),i.getAttackSpeed(),i.getRadius(),i.getCost(),i.getIfSmart())
					towerT.rect.x = i.rect.x
					towerT.rect.y = i.rect.y
					player1.addTower(towerT)

		if event.type == MOUSEBUTTONUP:
			for i in player1.towers:
				if buyTime == True:
					pos = pygame.mouse.get_pos()
					if i.notInPath(reader.gamefield,pos) == True:
						i.moveTower(pos[0],pos[1])
						i.setAlive(True)
					elif i.getAlive() == False:
						player1.towers.remove(i)
						player1.addMoney(i.getCost())
						print('Cannot move to path try again!')
			#tässä tarkastellaan voiko tornin asettaa oikeasti paikkaan johon se yritettiin asetta
			#jos ei niin sen luonti perutaan ja pelaajan täytyy asettaa se uuteen paikkaan.


		if event.type == KEYDOWN and event.key == pygame.K_e:
			k += 1 

		if event.type == KEYDOWN and event.key == pygame.K_i:
			player1.initInfo()
			r += 1
		#näillä toteutetaan tietojen alustus näytöllä


		pygame.display.update()


	
	enemy_0 = Enemy(const.JOKU2,1,1,1,0,0,0,'down')
	SCREEN.fill((0,0,0))
	gamefield.draw(SCREEN)
	#piirretään kenttä
	if spawnCount % 2000 == 0 and enemyCount > 0:
		spawnCount = 0
		enemiess.spawn(waveCount,enemyCount,spawnCount,enemiess.enemyGroup)
		enemyCount -= 1
	#luodaan viholliset aina kun sille on tarvetta spawnCountilla tarkastellaan että
	#viholliset luodaan pienellä viiveellä toisistaan

	if enemiess.getEnemyList().sprites() != []	:
		buyTime = False
	else : buyTime = True
	#määritellään milloin voidaan ostaa torneja eli silloin kun vihollisia ei liiku kentällä
	
	enemiess.drawEnemies(SCREEN)
	enemiess.moveEnemies(corners,player1)
	reader.towerGroup.draw(SCREEN)
	player1.towers.draw(SCREEN)
	reader.drawTowerNumbers(SCREEN)
	#piirto komentojen kutsu

	for t in player1.towers:
		pygame.draw.circle(SCREEN,const.JOKU5,t.getPos(),t.getRadius(),2)
	#piirretään tornien katama ympyrät

	if k % 2 == 0:
		reader.drawExplanations(SCREEN)

	if r % 2 == 0:
		player1.drawInfo(SCREEN)
	#piirretään infot ja selitykset

	elist = enemiess.getEnemyList()
	for h in player1.towers:
		enemy_t = h.closestEnemy(elist)
		if h.smartTower == 1:
			if h.enemyInRange(h.target) == False or h.target.groups() == []:
				h.target = enemy_t
			if shotCount % (20000/h.getAttackSpeed()) == 0 and h.enemyInRange(h.target) == True:
				h.shoot(h.target,player1)
				h.filler = shotCount
	#tarkastellaan ja tarvittaessa kutsutaan ampumakomentoa torneille

		if h.smartTower == 0:
			if shotCount % (20000/h.getAttackSpeed()) == 0:
				if h.enemyInRange(enemy_t) == True:
					h.shoot(enemy_t,player1)
					h.filler = shotCount

		if h.filler +80 == shotCount:
			h.image.fill(const.JOKU2)
	#tässä myös erotellaan toiminnot tyhmille ja fiksuille torneille

	pygame.display.update()

	if enemyCount > 0:
		spawnCount += const.FPS
	else:
		spawnCount = 1

	shotCount += const.FPS
	clock.tick(const.FPS)
	#lisäillään FPS:ää laskureihin