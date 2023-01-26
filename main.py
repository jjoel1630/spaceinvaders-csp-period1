import pygame
from pygame.locals import *
from pygame.sprite import *
from pygame import mixer
import random

from globalVars import *
from gameObj import *


# start clokc + init main objects
clock = pygame.time.Clock()
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

# Set some global varriables for game data
fps = 60;
countdown = 0
lastCount = pygame.time.get_ticks()
gameOver = 0;
bigShipTime = pygame.time.get_ticks()
prevInvaderShot = pygame.time.get_ticks()

# Change the game status
def changeGameOver(status):
	gameOver = status

# Set width + fonts + load sounds
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

# Draw background image
def drawBg():
	# load image and scale it to the screen width & height
	bgImage = pygame.image.load("images/background-img.jpeg")
	bgImage = pygame.transform.scale(bgImage, (screenWidth, screenHeight))

	screen.blit(bgImage, (0, 0))

# Create text on screen
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

# Creat invaders in a 5*5 grid
for x in range(5):
	for y in range(5):
		invader = Invaders(100 + y * 100, 100 + x * 70)
		invaderGrp.add(invader)

spaceshipGrp.add(spaceship)

run = True

# Main loop
while run:
	clock.tick(fps)

	drawBg()

	# If the countdown is 0, that means the game has started
	if countdown == 0:
		# Get current time & shoot lasers from the invaders
		curTime = pygame.time.get_ticks()
		if curTime - prevInvaderShot > 1000 and len(invaderGrp) > 0:
			shootingInvader = random.choice(invaderGrp.sprites())
			invaderLaser = InvaderLaser(shootingInvader.rect.center[0], shootingInvader.rect.center[1], screenHeight, spaceshipGrp, explosionGrp, explosionSound2)
			invaderLaserGrp.add(invaderLaser)
			prevInvaderShot = curTime

		# Custom game element generation
		genSpaceShip = random.randint(1, 100)

		if len(bigShipGrp) == 0 and genSpaceShip == 2:
			bigShip = BigSpaceship(screenWidth - 20, 600)
			bigShipGrp.add(bigShip)
			bigShipTime = pygame.time.get_ticks()

		if len(invaderGrp) == 0:
			gameOver = 1

		# If game is not over, update everything; if it is,. stop
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

	# Draw spaceship groups
	spaceshipGrp.draw(screen)
	laserGrp.draw(screen)
	invaderGrp.draw(screen)
	invaderLaserGrp.draw(screen)
	explosionGrp.draw(screen)
	bigShipGrp.draw(screen)


	# Check for pygame event
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()
