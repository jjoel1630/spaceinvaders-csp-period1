import pygame
from pygame.locals import *
from pygame.sprite import *

from pygame import K_LEFT as leftKey
from pygame import K_SPACE as spaceKey
from pygame import K_RIGHT as rightKey

from globalVars import *

class Invaders(Sprite):
	def __init__(self, xPos, yPos):
		Sprite.__init__(self)
		self.image = pygame.image.load("images/invader.png")
		self.image = pygame.transform.scale(self.image, (50, 50))

		self.direction = 1
		self.move_counter = 0

		self.rect = self.image.get_rect()
		self.rect.center = [xPos, yPos]

	def update(self):
		self.rect.x += self.direction
		self.move_counter += 1
		if abs(self.move_counter) > 75:
			self.direction *= -1
			self.move_counter *= self.direction

class Lasers(Sprite):
	def __init__(self, xPos, yPos, invaderGrp, explosionGrp, explosionSound, bigShipGrp):
		Sprite.__init__(self)
		self.image = pygame.image.load("images/lazer.webp")
		self.image = pygame.transform.scale(self.image, (50, 50))

		self.rect = self.image.get_rect()
		self.rect.center = [xPos, yPos]

		self.invaderGrp = invaderGrp
		self.explosionGrp = explosionGrp

		self.explosionSound = explosionSound
		self.bigShipGrp = bigShipGrp

	def update(self):
		self.rect.y -= 5
		if self.rect.bottom < 0:
			self.kill()
		if spritecollide(self, self.invaderGrp, True):
			self.kill()
			explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
			self.explosionGrp.add(explosion)
			self.explosionSound.play()
		if spritecollide(self, self.bigShipGrp, True):
			self.kill()
			explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
			self.explosionGrp.add(explosion)
			self.explosionSound.play()

class InvaderLaser(Sprite):
	def __init__(self, xPos, yPos, screenHeight, spaceshipGrp, explosionGrp, laserSound):
		Sprite.__init__(self)
		self.image = pygame.image.load("images/lazer.webp")
		self.image = pygame.transform.scale(self.image, (50, 50))

		self.screenHeight = screenHeight
		self.spaceshipGrp = spaceshipGrp
		self.explosionGrp = explosionGrp
		self.laserSound = laserSound

		self.rect = self.image.get_rect()
		self.rect.center = [xPos, yPos]

	def update(self):
		self.rect.y += 5
		if self.rect.top > self.screenHeight:
			self.kill()		
		if spritecollide(self, self.spaceshipGrp, False, collide_mask):
			self.kill()
			self.laserSound.play()
			self.spaceshipGrp.sprites()[0].health_remaining -= 1
			explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
			self.explosionGrp.add(explosion)

class Spaceship(Sprite):
	def __init__(self, xPos, yPos, health, screenWidth, screenHeight, laserGrp, screen, invaderGrp, explosionGrp, explosionSound, laserSound, bigShipGrp):
		Sprite.__init__(self)
		self.image = pygame.image.load("images/spaceship.png")
		self.image = pygame.transform.scale(self.image, (50, 50))

		self.health_start = health
		self.health_remaining = health

		self.lastShot = pygame.time.get_ticks()

		self.rect = self.image.get_rect()
		self.rect.center = [xPos, yPos]

		self.screenWidth = screenWidth
		self.screenHeight = screenHeight
		self.screen = screen
		self.laserGrp = laserGrp
		self.invaderGrp = invaderGrp
		self.explosionGrp = explosionGrp
		self.explosionSound = explosionSound
		self.bigShipGrp = bigShipGrp

		self.laserSound = laserSound

	def update(self):
		speed = 8

		gmOver = 0

		keyPress = pygame.key.get_pressed()
		if keyPress[leftKey] and self.rect.x - 50 > 0:
			self.rect.x -= speed
		if keyPress[rightKey] and self.rect.x + 50 < self.screenWidth:
			self.rect.x += speed

		curTime = pygame.time.get_ticks()
		if keyPress[spaceKey] and curTime - self.lastShot >= 200:
			self.laserSound.play()
			laser = Lasers(self.rect.centerx, self.rect.top, self.invaderGrp, self.explosionGrp, self.explosionSound, self.bigShipGrp)
			self.laserGrp.add(laser)

			self.lastShot = curTime

		self.mask = pygame.mask.from_surface(self.image)

		pygame.draw.rect(self.screen, (255, 0, 0), (self.rect.x, self.rect.bottom + 10, self.rect.width, 15))
		if self.health_remaining > 0:
			pygame.draw.rect(self.screen, (0, 255, 0), (self.rect.x, self.rect.bottom + 10, int(self.rect.width * (self.health_remaining / self.health_start)), 15))
		elif self.health_remaining >= 0:
			explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
			self.explosionGrp.add(explosion)
			self.kill()
			gmOver = -1

		return gmOver

class Explosion(Sprite):
	def __init__(self, xPos, yPos, size):
		Sprite.__init__(self)
		self.images = []
		for num in range(1, 6):
			img = pygame.image.load(f"images/exp{num}.png")
			if size == 1:
				img = pygame.transform.scale(img, (20, 20))
			if size == 2:
				img = pygame.transform.scale(img, (40, 40))
			if size == 3:
				img = pygame.transform.scale(img, (160, 160))
			#add the image to the list
			self.images.append(img)

		self.index = 0
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [xPos, yPos]
		self.counter = 0

	def update(self):
		explosionSpeed = 3
		self.counter += 1

		if self.counter >= explosionSpeed and self.index < len(self.images) - 1:
			self.counter = 0
			self.index += 1
			self.image = self.images[self.index]

		if self.index >= len(self.images) - 1 and self.counter >= explosionSpeed:
			self.kill()

class BigSpaceship(Sprite):
	def __init__(self, xPos, yPos):
		Sprite.__init__(self)
		self.image = pygame.image.load("images/bigship.png")
		self.image = pygame.transform.scale(self.image, (50, 50))

		self.rect = self.image.get_rect()
		self.rect.center = [xPos, yPos]
	
	def update(self):
		self.rect.x -= 10
		if self.rect.right < 0:
			self.kill()
