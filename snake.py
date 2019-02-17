'''
	SNAKE GAME
	By Piotr Mucha
	Based on tutorial @ http://inventwithpython.com/pygame
	
	v2.1 Changed the style of the snake
'''

import random, pygame, os, sys, shelve
from pygame.locals import *

WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE      = (255, 255, 255)
BLACK      = (  0,   0,   0)
RED        = (255,   0,   0)
GREEN      = (  0, 255,   0)
DARKRED    = (155,   0,   0)
DARKGREEN  = (  0, 155,   0)
DARKGRAY   = ( 40,  40,  40)
BLUE       = (  0,   0, 255)
LVLCOLOR   = ( 45, 204, 111)
CHOSENLVL  = (254, 204,   0)

BGCOLOR = BLACK

WORMCOLOR = GREEN

#if hasattr(sys, '_MEIPASS'):
#	appleImg = os.path.join(sys._MEIPASS, 'apple.png')
if getattr(sys, 'frozen', False):
    wd = sys._MEIPASS
else:
    wd = ''    
IMAGESDICT = {
	'apple': pygame.image.load(os.path.join(wd,"apple.png")),
	'snake_body': pygame.image.load(os.path.join(wd,"ball.png")),
	'snake_head': pygame.image.load(os.path.join(wd,"head.png"))
	}
FONT = os.path.join(wd,"alpha_echo.ttf")
		

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

EASY = 'easy'
MEDIUM = 'medium'
HARD = 'hard'

HEAD = 0

class SnakeGame(object):
	'''
		SnakeGame operates the game
	'''
	def __init__(self):
		# create the object operating drawing on and updating the display
		self.pf = PlayField()

	def startGame(self):
		'''
		Main loop of the game:
			Show main menu, run the main game
			load&save the best score and show the game over screen
		'''

		self.level = EASY # default level

		# run the loop till program is terminated
		while True:
			# draw level buttons and let the player choose the level of game
			self.level = self.pf.showStartScreen(self.level)

			# from a file load the best score saved after last game / if none, then bestscore equals zero
			self.loadBestScore()

			# run the main loop of the game
			self.runGame()

			# if failed (run on border/ate itself), then draw 'game-over screen'
			if self.isGameOver:
				self.pf.drawGameOver(self.score)

			# save the best score to file
			self.saveBestScore()

	def runGame(self):
		'''
		Main engine of the game.
		Draw&run the snake, check for collision & operate events
		'''
		self.isGameOver = False # failed and lost the game (game over)? or just quited the game?
		self.direction = RIGHT	# default direction at the beginning of the game
		self.returnToMainScreen = False # if True, then Q-key was pressed to quit to main menu
		self.score = 0
		self.pauseTheGame = False

		# set the beginning (x,y) position of the snake on the display
		x = CELLWIDTH / 2
		y = CELLHEIGHT / 2

		# create a snake as a list of dictionaries of {x,y} positions. As default, beginning length = 3
		snake = Snake(x,y)

		# create an apple at the random position as a dictionary {x,y} and does not collide with snake and border
		apple = Apple(snake, self.level)

		# for MEDIUM level draw a blue border on the display
		if self.level == MEDIUM:
			self.pf.drawBorder()

		#main loop run till terminated or quitted or failed
		while(True):
			# event handling loop
			self.onKeyDown()

			# quitted with Q-key to return to main menu?
			if self.returnToMainScreen:
				return

			if self.pauseTheGame:
				self.pauseTheGame = self.pf.showPauseGame(self.pauseTheGame)

			# if snake has eaten itself, then draw 'game over' & return to main menu
			if snake.hasEastenItself():
				self.isGameOver = True
				return

			# if apple not eaten, delete the tail apple is eaten, score +1 and redraw the apple
			if not snake.hasEastenApple(apple):
				snake.removeTail()
			else:
				del apple
				apple = Apple(snake, self.level)
				self.score += 1

			# make a "move' by adding a segment in the direction it is moving
			snake.addNewHead(self.direction)

			# check if the snake hits the borders
			# for MEDIUM lvl = game over
			# for EASY&HARD lvl snake enters the other side of the screen
			if snake.hitsBorder(self.level):
				if self.level == EASY or self.level == HARD:
					snake.changeSide(self.direction)
				elif self.level == MEDIUM:
					self.isGameOver = True
					return

			# update the screen
			self.pf.updateDisplay(self.level, self.score, self.bestScore, snake, apple)


	def onKeyDown(self):
		'''
		check if up/down/left/right/q/quit(escape) keys were pressed/clicked
		set direction for up/down/left/right pressed key
		'''
		for event in pygame.event.get():
			if event.type == QUIT:
				self.terminate()
			if event.type == KEYUP and (event.key == K_q or event.key == K_ESCAPE):
				self.returnToMainScreen = True
				return
			if (event.type == KEYUP and event.key == K_p):
				self.pauseTheGame = True
				return
			if event.type == pygame.KEYDOWN:
				if (event.key == K_LEFT) and self.direction != RIGHT:
					self.direction = LEFT
					return
				elif (event.key == K_RIGHT) and self.direction != LEFT:
					self.direction = RIGHT
					return
				elif (event.key == K_UP) and self.direction != DOWN:
					self.direction = UP
					return
				elif (event.key == K_DOWN) and self.direction != UP:
					self.direction = DOWN
					return

	def saveBestScore(self):
		'''
		Save to the file the game's best score corresponding to the chosen level.
		'''
		d = shelve.open('score.txt')
		if self.level == EASY and self.score > self.bestScore:
			d['scoreEasy'] = self.score
		elif self.level == MEDIUM and self.score > self.bestScore:
			d['scoreMedium'] = self.score
		elif self.level == HARD and self.score > self.bestScore:
			d['scoreHard'] = self.score
		d.close()

	def loadBestScore(self):
		'''
		Load from the file the game's best score corresponding to the chosen level.
		If file doesn't exists/no best score, then bestscore = 0
		'''
		d = shelve.open('score.txt')
		if self.level == EASY and d.get('scoreEasy', None):
			self.bestScore = d['scoreEasy']
		elif self.level == MEDIUM and d.get('scoreMedium', None):
			self.bestScore = d['scoreMedium']
		elif self.level == HARD and d.get('scoreHard', None):
			self.bestScore = d['scoreHard']
		else:
			self.bestScore = 0
		d.close()


	def terminate(self):
		'''
		Terminate the game
		'''
		pygame.quit()
		sys.exit()

class PlayField(SnakeGame):
	'''
	PlayField operates the display and pygame.module.
	'''
	def __init__(self):
		'''
		Initiate pygame module, surface for drawing,
		clock for the speed of the snake and the default font type&size
		'''
		pygame.init()
		self.DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
		self.FPSCLOCK = pygame.time.Clock()
		self.BASICFONT = pygame.font.Font(FONT, 18)
		pygame.display.set_caption('Snake Game by Piotr Mucha')
		self.FPS = 15

	def updateDisplay(self, level, score, bestScore, snake, apple):
		'''
		Function updates the display.
		It's the one "showing" everything to the user
		'''
		self.DISPLAYSURF.fill(BGCOLOR)
		#self.fill_gradient(self.DISPLAYSURF, (170, 255, 255), (255, 255, 255))
		if level == MEDIUM:
			self.drawBorder()
		#self.drawGrid()

		apple.drawApple(self.DISPLAYSURF)
		snake.drawWorm(self.DISPLAYSURF)
		self.drawScore(score, bestScore)
		self.drawMsg('[P] for Pause', WHITE, 18, 70, 10)
		self.drawMsg('[Q] for Quit', WHITE, 18, 60, 30)
		pygame.display.update()
		if level == HARD:
			FPS = 35
		else:
			FPS = self.FPS
		self.FPSCLOCK.tick(FPS)

	def animateSnake(self):
		'''
		Show snake animation running around the SNAKE word and eating apples
		'''
		if len(self.wormCoords) == (25-6+1):
			x = 14
			y = 9
			self.wormCoords = [
				{'x': x, 'y': y},
				{'x': x - 1, 'y': y},
				{'x': x - 2, 'y': y},
			]

		if not (self.wormCoords[HEAD]['x'] == self.applex and self.wormCoords[HEAD]['y'] == self.appley):
			del self.wormCoords[-1]
		else:
			while True:
				self.applex = random.randint(6 , 25)
				self.appley = 9
				if {'x': self.applex, 'y': self.appley} not in self.wormCoords:
					break


		if {'x': self.applex, 'y': self.appley} not in self.wormCoords:
			x = self.applex * CELLSIZE
			y = self.appley * CELLSIZE
			appleRect = IMAGESDICT['apple'].get_rect()
			appleRect.topleft = (x,y)
			self.DISPLAYSURF.blit(IMAGESDICT['apple'],appleRect)
			
		if 	(self.wormCoords[HEAD]['x'] < 25 and self.wormCoords[HEAD]['y'] == 9):
			newHead = {'x':self.wormCoords[HEAD]['x'] + 1, 'y':self.wormCoords[HEAD]['y']}
		elif (self.wormCoords[HEAD]['x'] == 25 and self.wormCoords[HEAD]['y'] > 2):
			newHead = {'x':self.wormCoords[HEAD]['x'], 'y':self.wormCoords[HEAD]['y'] - 1}
		elif (self.wormCoords[HEAD]['x'] > 6 and self.wormCoords[HEAD]['y'] == 2):
			newHead = {'x':self.wormCoords[HEAD]['x'] - 1, 'y':self.wormCoords[HEAD]['y']}
		elif (self.wormCoords[HEAD]['x'] == 6 and self.wormCoords[HEAD]['y'] < 9):
			newHead = {'x':self.wormCoords[HEAD]['x'], 'y':self.wormCoords[HEAD]['y'] + 1}

		self.wormCoords.insert(0,newHead)

		for coord in self.wormCoords:
			x = coord['x'] * CELLSIZE
			y = coord['y'] * CELLSIZE
			if self.wormCoords[0] == coord:
				snakeHeadRect = IMAGESDICT['snake_head'].get_rect()
				snakeHeadRect.topleft = (x,y)
				self.DISPLAYSURF.blit(IMAGESDICT['snake_head'],snakeHeadRect)
			else:
				snakeBodyRect = IMAGESDICT['snake_body'].get_rect()
				snakeBodyRect.topleft = (x,y)
				self.DISPLAYSURF.blit(IMAGESDICT['snake_body'],snakeBodyRect)
	def showStartScreen(self, level):
		'''
		Generate the main menu and waits till the user chooses difficulty level
		'''
		highlightedLvl = level
		x = 14
		y = 9
		self.applex = 20
		self.appley = 9
		self.wormCoords = [
			{'x':x  ,'y':y},
			{'x':x-1,'y':y},
			{'x':x-2,'y':y},
		]

		while True:
			# fill the screen with background color
			self.DISPLAYSURF.fill(BGCOLOR)

			# Draw a big "SNAKE" logo on the screen
			mainLogo = pygame.font.Font(FONT, 100)
			mainLogoSurf = mainLogo.render('SNAKE', True, GREEN)
			mainLogoRect = mainLogoSurf.get_rect()
			mainLogoRect.center = (WINDOWWIDTH / 2, 120)
			self.DISPLAYSURF.blit(mainLogoSurf,mainLogoRect)

			self.animateSnake()

			# level options - easy (no boundries), medium (boundries), hard (boundries + speed)
			self.drawLevels(highlightedLvl)

			for event in pygame.event.get(): # event handling loop
				# check if mouse is over one of the diff_lvls
				mousex, mousey = pygame.mouse.get_pos()
				if self.easyRect.collidepoint(mousex, mousey):
					highlightedLvl = EASY
				if self.mediumRect.collidepoint(mousex, mousey):
					highlightedLvl = MEDIUM
				if self.hardRect.collidepoint(mousex, mousey):
					highlightedLvl = HARD
				self.drawLevels(highlightedLvl)

				# check if clicked on one of the diff_lvl
				if event.type == MOUSEBUTTONUP:
					mousex, mousey = event.pos
					if self.easyRect.collidepoint(mousex, mousey):
						return EASY
					if self.mediumRect.collidepoint(mousex, mousey):
						return MEDIUM
					if self.hardRect.collidepoint(mousex, mousey):
						return HARD

				# check if was pressed left/right key
				# and highlight chosen level
				if event.type == KEYDOWN:
					if event.key == K_RIGHT:
						if highlightedLvl == EASY:
							highlightedLvl = MEDIUM
						elif highlightedLvl == MEDIUM:
							highlightedLvl = HARD
						elif highlightedLvl == HARD:
							highlightedLvl = EASY
						self.drawLevels(highlightedLvl)
					if event.key == K_LEFT:
						if highlightedLvl == EASY:
							highlightedLvl = HARD
						elif highlightedLvl == MEDIUM:
							highlightedLvl = EASY
						elif highlightedLvl == HARD:
							highlightedLvl = MEDIUM
						self.drawLevels(highlightedLvl)

				# check if ENTER key was pressed
				if (event.type == KEYDOWN and event.key in [K_KP_ENTER, K_RETURN]):
					return highlightedLvl
				if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
					super().terminate()


			self.drawMsg('Press Escape to exit', WHITE, 16, WINDOWWIDTH / 2, WINDOWHEIGHT - 30)

			pygame.display.update()
			self.FPSCLOCK.tick(self.FPS)

	def drawBorder(self):
		'''
		Draw a blue border that kills the snake when he hits the border
		Playing field is smaller by CELLSIZE compared to the field without the border
		'''
		pygame.draw.rect(self.DISPLAYSURF, DARKGRAY, pygame.Rect(0,0,WINDOWWIDTH,CELLSIZE))
		pygame.draw.rect(self.DISPLAYSURF, DARKGRAY, pygame.Rect(WINDOWWIDTH-CELLSIZE,0,WINDOWWIDTH-CELLSIZE,WINDOWHEIGHT))
		pygame.draw.rect(self.DISPLAYSURF, DARKGRAY, pygame.Rect(0,0,CELLSIZE,WINDOWHEIGHT))
		pygame.draw.rect(self.DISPLAYSURF, DARKGRAY, pygame.Rect(0,WINDOWHEIGHT-CELLSIZE,WINDOWWIDTH,WINDOWHEIGHT))
		pygame.draw.rect(self.DISPLAYSURF, BLUE, pygame.Rect(CELLSIZE-1,CELLSIZE-1,WINDOWWIDTH-2*CELLSIZE+1,WINDOWHEIGHT-2*CELLSIZE+1),1)

	def drawGrid(self):
		'''
		Draw a gray grid on the surface
		'''
		for celx in range(CELLWIDTH):
			left = celx * CELLSIZE
			pygame.draw.line(self.DISPLAYSURF,DARKGRAY, (left,0), (left,WINDOWHEIGHT))
		for cely in range(CELLHEIGHT):
			top = cely * CELLSIZE
			pygame.draw.line(self.DISPLAYSURF,DARKGRAY, (0,top), (WINDOWWIDTH,top))

	def drawScore(self, score, bestScore):
		'''
		Draw current score and best score
		'''
		scoreSurf = self.BASICFONT.render('Score: %s' % (score), True, WHITE)
		scoreRect = scoreSurf.get_rect()
		scoreRect.topleft = (WINDOWWIDTH - 150, 10)
		self.DISPLAYSURF.blit(scoreSurf, scoreRect)

		bestscoreSurf = self.BASICFONT.render('Best score: %s' % (bestScore), True, WHITE)
		bestscoreRect = bestscoreSurf.get_rect()
		bestscoreRect.topleft = (WINDOWWIDTH - 150, 40)
		self.DISPLAYSURF.blit(bestscoreSurf, bestscoreRect)

	def drawLevels(self, highlightedLvl):
		'''
		Draw on the surface difficulty levels
		'''
		OPTIONFONT = pygame.font.Font(FONT, 40)
		color = LVLCOLOR

		easySurf = OPTIONFONT.render('EASY', True, color)
		if highlightedLvl == EASY:
			easySurf = OPTIONFONT.render('EASY', True, CHOSENLVL)
		self.easyRect = easySurf.get_rect()
		self.easyRect.topleft = (100, WINDOWHEIGHT - 100)
		self.DISPLAYSURF.blit(easySurf,self.easyRect)

		mediumSurf = OPTIONFONT.render('MEDIUM', True, color)
		if highlightedLvl == MEDIUM:
			mediumSurf = OPTIONFONT.render('MEDIUM', True, CHOSENLVL)
		self.mediumRect = mediumSurf.get_rect()
		self.mediumRect.topleft = (240, WINDOWHEIGHT - 100)
		self.DISPLAYSURF.blit(mediumSurf,self.mediumRect)

		hardSurf = OPTIONFONT.render('HARD', True, color)
		if highlightedLvl == HARD:
			hardSurf = OPTIONFONT.render('HARD', True, CHOSENLVL)
		self.hardRect = hardSurf.get_rect()
		self.hardRect.topleft = (440, WINDOWHEIGHT - 100)
		self.DISPLAYSURF.blit(hardSurf,self.hardRect)

	def drawGameOver(self, score):
		'''
		Draw 'GAME OVER' when player fails
		'''
		#self.DISPLAYSURF.fill(BGCOLOR)
		gameOverFont = pygame.font.Font(FONT, 150)
		GOverSurface1 = gameOverFont.render('Game', True, WHITE)
		GOverSurface2 = gameOverFont.render('Over', True, WHITE)
		GOverRect1 = GOverSurface1.get_rect()
		GOverRect2 = GOverSurface2.get_rect()
		GOverRect1.midtop = (WINDOWWIDTH / 2, 50)
		GOverRect2.midtop = (WINDOWWIDTH / 2,GOverRect1.height + 50 + 25)

		self.DISPLAYSURF.blit(GOverSurface1,GOverRect1)
		self.DISPLAYSURF.blit(GOverSurface2,GOverRect2)

		# HOW TO MAKE A BLINKING TEXT WIHTOUT "CLEARING" THE BACKGROUND?????
		self.drawMsg('Your score: %s' % (score), RED, 25, WINDOWWIDTH / 2, WINDOWHEIGHT - 80)
		self.drawMsg('Press Enter to continue', WHITE, 18, WINDOWWIDTH / 2 + 10, WINDOWHEIGHT - 30)

		pygame.display.update()

		while True:
			for event in pygame.event.get():
				if (event.type == KEYDOWN and event.key in [K_KP_ENTER, K_RETURN]):
					return
				if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
					super().terminate()

	def showPauseGame(self, pauseTheGame):
		'''
		Pause the game, draw "PAUSED" on the screen and wait till Enter pressed
		'''
		while pauseTheGame:
			self.drawMsg('PAUSED', GREEN, 55, WINDOWWIDTH / 2, WINDOWHEIGHT / 2 - 70)
			self.drawMsg('Press Enter to continue', WHITE, 16, WINDOWWIDTH / 2, WINDOWHEIGHT / 2)

			pygame.display.update()
			for event in pygame.event.get():
				if (event.type == KEYDOWN and event.key in [K_KP_ENTER, K_RETURN]):
					pauseTheGame = False
					return pauseTheGame
				if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
					super().terminate()

	def drawMsg(self, message, color, size, midtopx, midtopy):
		'''
		Draw message of default font on the surface
		'''
		BASICFONT = pygame.font.Font(FONT, size)
		pressKeySurf = BASICFONT.render(message, True, color)
		pressKeyRect = pressKeySurf.get_rect()
		pressKeyRect.midtop = (midtopx, midtopy)
		self.DISPLAYSURF.blit(pressKeySurf,pressKeyRect)

	def fill_gradient(self, surface, color, gradient, rect=None, vertical=True, forward=True):
		'''fill a surface with a gradient pattern
		Parameters:
		color -> starting color
		gradient -> final color
		rect -> area to fill; default is surface's rect
		vertical -> True=vertical; False=horizontal
		forward -> True=forward; False=reverse
		
		Pygame recipe: http://www.pygame.org/wiki/GradientCode
		'''
		if rect is None: rect = surface.get_rect()
		x1,x2 = (rect.left, rect.right)
		y1,y2 = rect.top, rect.bottom
		if vertical: h = y2-y1
		else:        h = x2-x1
		if forward: a, b = color, gradient
		else:       b, a = color, gradient
		rate = (
			float(b[0]-a[0])/h,
			float(b[1]-a[1])/h,
			float(b[2]-a[2])/h
		)
		fn_line = pygame.draw.line
		if vertical:
			for line in range(y1,y2):
				color = (
					min(max(a[0]+(rate[0]*(line-y1)),0),255),
					min(max(a[1]+(rate[1]*(line-y1)),0),255),
					min(max(a[2]+(rate[2]*(line-y1)),0),255)
				)
				fn_line(surface, color, (x1,line), (x2,line))
		else:
			for col in range(x1,x2):
				color = (
					min(max(a[0]+(rate[0]*(col-x1)),0),255),
					min(max(a[1]+(rate[1]*(col-x1)),0),255),
					min(max(a[2]+(rate[2]*(col-x1)),0),255)
				)
				fn_line(surface, color, (col,y1), (col,y2))
	
class Apple(object):
	def __init__(self, snake, level):
		'''
		Initiate the apple instance with the coordinates
		Coordinates cannot be on the snake's body
		'''
		while True:
			x = random.randint(0 + 1*(level==MEDIUM), CELLWIDTH - 1 - 1*(level==MEDIUM))
			y = random.randint(0 + 1*(level==MEDIUM), CELLHEIGHT - 1 - 1*(level==MEDIUM))
			if {'x': x, 'y': y} not in snake.wormCoords:
				self.x = x
				self.y = y
				return

	def drawApple(self, surface):
		'''
		Calculate pixel coordinates of an apple and
		draw it on the surface
		'''
		x = self.x * CELLSIZE
		y = self.y * CELLSIZE
		appleRect = IMAGESDICT['apple'].get_rect()
		appleRect.topleft = (x,y)
		surface.blit(IMAGESDICT['apple'],appleRect)
		#appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
		#pygame.draw.rect(surface, RED, appleRect)

class Snake(object):
	def __init__(self, x, y):
		'''
		Initialize body of the snake as 3 segments as list of dictionaries
		'''
		self.wormCoords = [
			{'x':x  ,'y':y},
			{'x':x-1,'y':y},
			{'x':x-2,'y':y},
		]

	def hasEastenItself(self):
		'''
		Check if snake has eaten itself
		'''
		for wormBody in self.wormCoords[1:]:
			if self.wormCoords[HEAD]['x'] == wormBody['x'] and self.wormCoords[HEAD]['y'] == wormBody['y']:
				return True
		return False

	def hasEastenApple(self,apple):
		'''
		Check if snake has eaten the apple
		'''
		if (self.wormCoords[HEAD]['x'] == apple.x and self.wormCoords[HEAD]['y'] == apple.y):
			return True

	def removeTail(self):
		'''
		Remove worm's tail segment
		'''
		del self.wormCoords[-1]

	def addNewHead(self, direction):
		'''
		Add a new segment/head (dictionary of x,y) in front of the body (list)
		'''
		if direction == LEFT:
			newHead = {'x':self.wormCoords[HEAD]['x'] - 1, 'y':self.wormCoords[HEAD]['y']}
		if direction == RIGHT:
			newHead = {'x':self.wormCoords[HEAD]['x'] + 1, 'y':self.wormCoords[HEAD]['y']}
		if direction == UP:
			newHead = {'x':self.wormCoords[HEAD]['x'], 'y':self.wormCoords[HEAD]['y'] - 1}
		if direction == DOWN:
			newHead = {'x':self.wormCoords[HEAD]['x'], 'y':self.wormCoords[HEAD]['y'] + 1}
		self.wormCoords.insert(0,newHead)

	def hitsBorder(self, level):
		'''
		Check if the snake hits the border.
		For MEDIUM lvl the border/playing field is one CELLSIZE smaller
		'''
		if level == EASY or level == HARD:
			if 	(self.wormCoords[HEAD]['x'] >= CELLWIDTH) or (self.wormCoords[HEAD]['x'] <= -1) or (self.wormCoords[HEAD]['y'] <= -1) or (self.wormCoords[HEAD]['y'] >= CELLHEIGHT):
				return True
		elif level == MEDIUM:
			if 	(self.wormCoords[HEAD]['x'] == CELLWIDTH - 1) or (self.wormCoords[HEAD]['x'] == 0) or (self.wormCoords[HEAD]['y'] == 0) or (self.wormCoords[HEAD]['y'] == CELLHEIGHT - 1):
				return True

	def changeSide(self, direction):
		'''
		Make the snake enter the other side of the screen
		'''
		if direction == LEFT:
			self.wormCoords[HEAD]['x'] = CELLWIDTH - 1
		if direction == RIGHT:
			self.wormCoords[HEAD]['x'] = 0
		if direction == UP:
			self.wormCoords[HEAD]['y'] = CELLHEIGHT - 1
		if direction == DOWN:
			self.wormCoords[HEAD]['y'] = 0

	def drawWorm(self, surface):
		'''
		Calculate pixel coordinates on the screen and
		draw on the surface the snake body
		'''
		for coord in self.wormCoords:
			x = coord['x'] * CELLSIZE
			y = coord['y'] * CELLSIZE
			if self.wormCoords[0] == coord:
				snakeHeadRect = IMAGESDICT['snake_head'].get_rect()
				snakeHeadRect.topleft = (x,y)
				surface.blit(IMAGESDICT['snake_head'],snakeHeadRect)
			else:
				snakeBodyRect = IMAGESDICT['snake_body'].get_rect()
				snakeBodyRect.topleft = (x,y)
				surface.blit(IMAGESDICT['snake_body'],snakeBodyRect)

def main():
	snake = SnakeGame()
	snake.startGame()

if __name__ == '__main__':
	main()