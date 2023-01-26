import pygame

screenWidth = 600
screenHeight = 800

def getWidthHeight():
	return [screenWidth, screenHeight]

def getScreen():
	return pygame.display.set_mode((screenWidth, screenHeight))

def updatePoints(pts):
	return pts + 5