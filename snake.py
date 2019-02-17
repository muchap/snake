'''
	SNAKE GAME
	By Piotr Mucha
	
	Basic version of snake eating apples that dies when hit the edge of the screen  
	Based on tutorial @ http://inventwithpython.com/pygame
	
'''

import random, pygame, sys
from pygame.locals import *

WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK

WORMCOLOR = GREEN

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0
FPS = 15

def main():
	global DISPLAYSURF, BASICFONT, FPSCLOCK
	
	pygame.init()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
	FPSCLOCK = pygame.time.Clock()
	BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
	pygame.display.set_caption('Wormy')

	while True:
		runGame()
		terminate()
		
def runGame():
	x = CELLWIDTH / 2
	y = CELLHEIGHT / 2
	#draw snake
	wormCoords = [
		{'x':x  ,'y':y},
		{'x':x-1,'y':y},
		{'x':x-2,'y':y},

	]
	
	direction = RIGHT
	score = 0
	
	# Start the apple in a random place.
	apple = getRandomLocation(wormCoords)

	#main loop
	while(True):		
		# event handling loop
		# !!!! there is a problem when player hits simultanously 2 keys (e.g. quick down-right) -> "Snake its itself"
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
				terminate()
			if (event.type == KEYUP and event.key == K_q):
				return score
			elif event.type == KEYDOWN:
				if (event.key == K_LEFT) and direction != RIGHT:
					direction = LEFT
				elif (event.key == K_RIGHT) and direction != LEFT:
					direction = RIGHT
				elif (event.key == K_UP) and direction != DOWN:
					direction = UP
				elif (event.key == K_DOWN) and direction != UP:
					direction = DOWN

		# check if snake has eaten itself
		for wormBody in wormCoords[1:]:
			if wormCoords[HEAD]['x'] == wormBody['x'] and wormCoords[HEAD]['y'] == wormBody['y']:
				return
		
		# check if worm has eaten an apply
		if (wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']):
			apple = getRandomLocation(wormCoords)
			score += 1
		else:
			del wormCoords[-1] # remove worm's tail segment		
		
		# move the worm by adding a segment in the direction it is moving		
		if direction == LEFT:
			newHead = {'x':wormCoords[HEAD]['x'] - 1, 'y':wormCoords[HEAD]['y']}
		if direction == RIGHT:
			newHead = {'x':wormCoords[HEAD]['x'] + 1, 'y':wormCoords[HEAD]['y']}
		if direction == UP:
			newHead = {'x':wormCoords[HEAD]['x'], 'y':wormCoords[HEAD]['y'] - 1}
		if direction == DOWN:
			newHead = {'x':wormCoords[HEAD]['x'], 'y':wormCoords[HEAD]['y'] + 1}
		wormCoords.insert(0,newHead)

		# If snake crosses the boundaries, make it enter from the other side
		if 	(wormCoords[HEAD]['x'] == CELLWIDTH) or (wormCoords[HEAD]['x'] == -1) or (wormCoords[HEAD]['y'] == -1) or (wormCoords[HEAD]['y'] == CELLHEIGHT):
			return
		
	
		DISPLAYSURF.fill(BGCOLOR)
		drawGrid()
		drawWorm(wormCoords)
		drawApple(apple)
		drawScore(score)
		drawQMsg()
		pygame.display.update()
		FPSCLOCK.tick(FPS)
	

def drawQMsg():
	messageSurf = BASICFONT.render('[Q] for Quit', True, WHITE)
	messageRect = messageSurf.get_rect()
	messageRect.topleft = (20, 10)
	DISPLAYSURF.blit(messageSurf,messageRect)

	
def checkForKeyPress():
	if len(pygame.event.get(QUIT)) > 0:
		terminate()
		
	keyUpEvents = pygame.event.get(KEYUP)
	if len(keyUpEvents) == 0:
		return None
	if keyUpEvents[0].key == K_ESCAPE:
		terminate()
	return keyUpEvents[0].key
		
def getRandomLocation(wormCoords):
	while True:
		x = random.randint(0, CELLWIDTH - 1)
		y = random.randint(0, CELLHEIGHT - 1)
		if {'x': x, 'y': y} not in wormCoords:
			return {'x': x, 'y': y}
		
def drawWorm(wormCoords):
	for coord in wormCoords:
		x = coord['x'] * CELLSIZE
		y = coord['y'] * CELLSIZE
		wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
		pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
		wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
		pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)

def drawApple(apple):
	x = apple['x'] * CELLSIZE
	y = apple['y'] * CELLSIZE
	appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
	pygame.draw.rect(DISPLAYSURF, RED, appleRect)
				
def drawGrid():
	for celx in range(CELLWIDTH):
		left = celx * CELLSIZE
		pygame.draw.line(DISPLAYSURF,DARKGRAY, (left,0), (left,WINDOWHEIGHT))
	for cely in range(CELLHEIGHT):
		top = cely * CELLSIZE
		pygame.draw.line(DISPLAYSURF,DARKGRAY, (0,top), (WINDOWWIDTH,top))

def drawScore(score):
	scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
	scoreRect = scoreSurf.get_rect()
	scoreRect.topleft = (WINDOWWIDTH - 140, 10)
	DISPLAYSURF.blit(scoreSurf, scoreRect)
	
def terminate():
	pygame.quit()
	sys.exit()
	
if __name__ == '__main__':
	main()