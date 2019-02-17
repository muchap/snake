'''
	SNAKE GAME
	By Piotr Mucha
	
	Basic version of snake eating apples that dies when hit the edge of the screen  
	Based on tutorial @ http://inventwithpython.com/pygame
	
	v0.5 Added graphics of border when level is MEDIUM
'''

import random, pygame, sys, shelve
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
BLUE      = (  0,   0, 255)
BGCOLOR = BLACK

WORMCOLOR = GREEN

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

EASY = 'easy'
MEDIUM = 'medium'
HARD = 'hard'

HEAD = 0
FPS = 15

def main():
	global DISPLAYSURF, BASICFONT, FPSCLOCK, isGameOver
	
	pygame.init()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
	FPSCLOCK = pygame.time.Clock()
	BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
	pygame.display.set_caption('Wormy')

	while True:
		isGameOver = False
		level = showStartScreen()

		d = shelve.open('score.txt')
		if level == EASY and d.get('scoreEasy', None):
			bestScore = d['scoreEasy']
		elif level == MEDIUM and d.get('scoreMedium', None):
			bestScore = d['scoreMedium']
		elif level == HARD and d.get('scoreHard', None):
			bestScore = d['scoreHard']
		else:
			bestScore = 0
		d.close()

		score = runGame(level, bestScore)
		if isGameOver:
			drawGameOver()

		d = shelve.open('score.txt')
		if level == EASY and score > bestScore:
			d['scoreEasy'] = score
		elif level == MEDIUM and score > bestScore:
			d['scoreMedium'] = score
		elif level == HARD and score > bestScore:
			d['scoreHard'] = score
		d.close()
		
def runGame(level, bestScore):
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
	apple = getRandomLocation(wormCoords, level)
	
	if level == HARD:
		FPS = 35
	else:
		FPS = 15
	
	
	global isGameOver
	isGameOver = False
	if level == MEDIUM:
		drawBorder()
	
	
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
				isGameOver = True
				return score
		
		# check if worm has eaten an apply
		if (wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']):
			apple = getRandomLocation(wormCoords, level)
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

		#DIFFICULT LEVEL
		if level == EASY or level == HARD:
			# If snake crosses the boundaries, make it enter from the other side
			if 	(wormCoords[HEAD]['x'] >= CELLWIDTH) or (wormCoords[HEAD]['x'] <= -1) or (wormCoords[HEAD]['y'] <= -1) or (wormCoords[HEAD]['y'] >= CELLHEIGHT):
				if direction == LEFT:
					wormCoords[HEAD]['x'] = CELLWIDTH - 1
				if direction == RIGHT:
					wormCoords[HEAD]['x'] = 0
				if direction == UP:
					wormCoords[HEAD]['y'] = CELLHEIGHT - 1
				if direction == DOWN:
					wormCoords[HEAD]['y'] = 0
		elif level == MEDIUM:
			# If snake hits the boundaries, game over
			if 	(wormCoords[HEAD]['x'] == CELLWIDTH - 1) or (wormCoords[HEAD]['x'] == 0) or (wormCoords[HEAD]['y'] == 0) or (wormCoords[HEAD]['y'] == CELLHEIGHT - 1):
				isGameOver = True
				return score
		
	
		DISPLAYSURF.fill(BGCOLOR)
		if level == MEDIUM:
			drawBorder()
		drawGrid()
		drawWorm(wormCoords)
		drawApple(apple)
		drawScore(score, bestScore)
		drawQMsg()
		pygame.display.update()
		FPSCLOCK.tick(FPS)
	
def showStartScreen():
	# TODO: running snake eating apples in the background

	fontsize = 100
	blink = 0

	while True:
		DISPLAYSURF.fill(BGCOLOR)
		
		mainLogo = pygame.font.Font('freesansbold.ttf', fontsize)
		mainLogoSurf = mainLogo.render('SNAKE', True, GREEN)
		mainLogoRect = mainLogoSurf.get_rect()
		mainLogoRect.center = (WINDOWWIDTH / 2, 120)
		DISPLAYSURF.blit(mainLogoSurf,mainLogoRect)
		
		if blink%5<2:
			drawMsg('Press a key to play......')
			
		# level options - easy (no boundries), medium (boundries), hard (boundries + speed)
		easyRect, mediumRect, hardRect = drawLevels()
		
		for event in pygame.event.get(): # event handling loop
			if event.type == MOUSEBUTTONUP:
				mousex, mousey = event.pos # syntactic sugar
				
				# check for clicks on the difficulty buttons
				if easyRect.collidepoint(mousex, mousey):
					return EASY
				if mediumRect.collidepoint(mousex, mousey):
					return MEDIUM
				if hardRect.collidepoint(mousex, mousey):
					return HARD					
			if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
				terminate()		

		pygame.display.update()
		FPSCLOCK.tick(FPS)
		blink += 1
		
	
	#TODO: hall of fame

def drawBorder():
	pygame.draw.rect(DISPLAYSURF, DARKGRAY, pygame.Rect(0,0,WINDOWWIDTH,CELLSIZE))
	pygame.draw.rect(DISPLAYSURF, DARKGRAY, pygame.Rect(WINDOWWIDTH-CELLSIZE,0,WINDOWWIDTH-CELLSIZE,WINDOWHEIGHT))
	pygame.draw.rect(DISPLAYSURF, DARKGRAY, pygame.Rect(0,0,CELLSIZE,WINDOWHEIGHT))
	pygame.draw.rect(DISPLAYSURF, DARKGRAY, pygame.Rect(0,WINDOWHEIGHT-CELLSIZE,WINDOWWIDTH,WINDOWHEIGHT))
	pygame.draw.rect(DISPLAYSURF, BLUE, pygame.Rect(CELLSIZE-1,CELLSIZE-1,WINDOWWIDTH-2*CELLSIZE+1,WINDOWHEIGHT-2*CELLSIZE+1),1)
	
def drawLevels():
	OPTIONFONT = pygame.font.Font('freesansbold.ttf', 30)
	easySurf = OPTIONFONT.render('EASY', True, WHITE, DARKGREEN)
	easyRect = easySurf.get_rect()
	easyRect.topleft = (80, WINDOWHEIGHT - 100)
	DISPLAYSURF.blit(easySurf,easyRect)
	
	mediumSurf = OPTIONFONT.render('MEDIUM', True, WHITE, DARKGREEN)
	mediumRect = mediumSurf.get_rect()
	mediumRect.topleft = (220, WINDOWHEIGHT - 100)
	DISPLAYSURF.blit(mediumSurf,mediumRect)

	hardSurf = OPTIONFONT.render('HARD', True, WHITE, DARKGREEN)
	hardRect = hardSurf.get_rect()
	hardRect.topleft = (400, WINDOWHEIGHT - 100)
	DISPLAYSURF.blit(hardSurf,hardRect)
	
	return easyRect, mediumRect, hardRect

def drawGameOver():
	gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
	GOverSurface1 = gameOverFont.render('Game', True, WHITE)
	GOverSurface2 = gameOverFont.render('Over', True, WHITE)
	GOverRect1 = GOverSurface1.get_rect()
	GOverRect2 = GOverSurface1.get_rect()
	GOverRect1.midtop = (WINDOWWIDTH / 2, 10)
	GOverRect2.midtop = (WINDOWWIDTH / 2,GOverRect1.height + 10 + 25)
	
	DISPLAYSURF.blit(GOverSurface1,GOverRect1)
	DISPLAYSURF.blit(GOverSurface2,GOverRect2)
	drawPressMsg()
	pygame.display.update()
	pygame.time.wait(500)
	
	checkForKeyPress() # clear out any key presses in the event queue
	
	while True:
		if checkForKeyPress():
			pygame.event.get() # clear event queue
			return

def drawPressMsg():
	pressKeySurf = BASICFONT.render('Press a key to play...', True, WHITE)
	pressKeyRect = pressKeySurf.get_rect()
	pressKeyRect.midtop = (WINDOWWIDTH / 2, WINDOWHEIGHT - 30)
	DISPLAYSURF.blit(pressKeySurf,pressKeyRect)

def drawMsg(message):
	pressKeySurf = BASICFONT.render(message, True, WHITE)
	pressKeyRect = pressKeySurf.get_rect()
	pressKeyRect.midtop = (WINDOWWIDTH / 2, WINDOWHEIGHT - 30)
	DISPLAYSURF.blit(pressKeySurf,pressKeyRect)

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
		
def getRandomLocation(wormCoords, level):
	while True:
		x = random.randint(0 + 1*(level==MEDIUM), CELLWIDTH - 1 - 1*(level==MEDIUM))
		y = random.randint(0 + 1*(level==MEDIUM), CELLHEIGHT - 1 - 1*(level==MEDIUM))
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

def drawScore(score, bestScore):
	scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
	scoreRect = scoreSurf.get_rect()
	scoreRect.topleft = (WINDOWWIDTH - 140, 10)
	DISPLAYSURF.blit(scoreSurf, scoreRect)
	
	bestscoreSurf = BASICFONT.render('Best score: %s' % (bestScore), True, WHITE)
	bestscoreRect = bestscoreSurf.get_rect()
	bestscoreRect.topleft = (WINDOWWIDTH - 140, 40)
	DISPLAYSURF.blit(bestscoreSurf, bestscoreRect)

def terminate():
	pygame.quit()
	sys.exit()
	
if __name__ == '__main__':
	main()