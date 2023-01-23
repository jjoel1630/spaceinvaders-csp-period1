import pygame
from pygame.locals import *
from pygame.sprite import *
from pygame import mixer
import random

# from gameObj import Spaceship
from globalVars import *
from gameObj import *

clock = pygame.time.Clock()
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

fps = 60;
countdown = 0
lastCount = pygame.time.get_ticks()
gameOver = 0;
bigShipTime = pygame.time.get_ticks()

def changeGameOver(status):
	gameOver = status

prevInvaderShot = pygame.time.get_ticks()

screenWidth = getWidthHeight()[0]
screenHeight = getWidthHeight()[1]

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Space Invaders')

font30 = pygame.font.SysFont('Constantia', 30)
font40 = pygame.font.SysFont('Constantia', 40)

explosionSound = pygame.mixer.Sound("sounds/explosion.wav")
explosionSound.set_volume(0.4)

explosionSound2 = pygame.mixer.Sound("sounds/explosion2.wav")
explosionSound2.set_volume(0.2)

laserSound = pygame.mixer.Sound("sounds/laser.wav")
laserSound.set_volume(0.05)

def drawBg():
	# load image and scale it to the screen width & height
	bgImage = pygame.image.load("images/background-img.jpeg")
	bgImage = pygame.transform.scale(bgImage, (screenWidth, screenHeight))

	screen.blit(bgImage, (0, 0))

def createText(tx, font,color, x, y):
	img = font.render(tx, True, color)
	screen.blit(img, (x, y))

# Sprite groups
spaceshipGrp = pygame.sprite.Group()
laserGrp = pygame.sprite.Group()
invaderLaserGrp = pygame.sprite.Group()
invaderGrp = pygame.sprite.Group()
explosionGrp = pygame.sprite.Group()
bigShipGrp = pygame.sprite.Group()

# init player
spaceship = Spaceship(int(screenWidth / 2), screenHeight - 100, 3, screenWidth, screenHeight, laserGrp, screen, invaderGrp, explosionGrp, explosionSound, laserSound, bigShipGrp)

for x in range(5):
	for y in range(5):
		invader = Invaders(100 + y * 100, 100 + x * 70)
		invaderGrp.add(invader)

spaceshipGrp.add(spaceship)

run = True

while run:
	clock.tick(fps)

	drawBg()

	if countdown == 0:
		curTime = pygame.time.get_ticks()
		if curTime - prevInvaderShot > 1000 and len(invaderGrp) > 0:
			shootingInvader = random.choice(invaderGrp.sprites())
			invaderLaser = InvaderLaser(shootingInvader.rect.center[0], shootingInvader.rect.center[1], screenHeight, spaceshipGrp, explosionGrp, explosionSound2)
			invaderLaserGrp.add(invaderLaser)
			prevInvaderShot = curTime

		genSpaceShip = random.randint(1, 100)
		# genSpaceShip = 4
		# if len(bigShipGrp) == 0 and genSpaceShip == 4 and bigShipTime - curTime > 100:
		if len(bigShipGrp) == 0 and genSpaceShip == 2:
			bigShip = BigSpaceship(screenWidth - 20, 600)
			bigShipGrp.add(bigShip)
			bigShipTime = pygame.time.get_ticks()

		if len(invaderGrp) == 0:
			gameOver = 1

		if gameOver == 0:
			gameOver = spaceship.update()
			laserGrp.update()
			invaderGrp.update()
			invaderLaserGrp.update()
			bigShipGrp.update()
		else:
			if gameOver == -1:
				createText('GAME OVER!!!', font40, (255, 255, 255), int(screenWidth / 2 - 110), int(screenHeight / 2 + 50))
			if gameOver == 1:
				createText('YOU WIN!!!', font40, (255, 255, 255), int(screenWidth / 2 - 90), int(screenHeight / 2 + 50))

	if countdown > 0:
		createText('Get Ready!!!', font40, (255, 255, 255), int(screenWidth / 2 - 110), int(screenHeight / 2 + 50))
		createText(str(countdown), font30, (255, 255, 255), int(screenWidth / 2 - 10), int(screenHeight / 2 + 100))
		countTimer = pygame.time.get_ticks()

		if countTimer - lastCount > 1000:
			countdown -= 1
			lastCount = countTimer

	explosionGrp.update()

	spaceshipGrp.draw(screen)
	laserGrp.draw(screen)
	invaderGrp.draw(screen)
	invaderLaserGrp.draw(screen)
	explosionGrp.draw(screen)
	bigShipGrp.draw(screen)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()
