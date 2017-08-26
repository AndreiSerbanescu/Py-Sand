import GlobalModule as gmod
import pygame, sys, time
from Grid import *
from SoundModule import *

class GameMaster():
	def __init__(self, width = 900, height = 600):
		gmod.WIDTH = width
		gmod.HEIGHT = height
		self.fpsClock = pygame.time.Clock()
		self.FPS = 30
		self.mousePressed = False
		gmod.colour = gmod.Colour()
		self.screenShotNo = 0
		self.dirtyRectArray = []
		self.sm = SoundModule()

	def initScreen(self):
		gmod.screen = pygame.display.set_mode((gmod.WIDTH, gmod.HEIGHT))
	def initGrid(self):
		gmod.AlternatingCode = 0
		self.grid = Grid(rowNo = 51, colNo = 102)   #51, 102 
		#rowNo - 1 divizibul cu height
		#colNo - 2 divizibil cu width
	def play(self):
		self.initScreen()
		self.initGrid()
		self.startGameLoop()
	def startGameLoop(self):
		gmod.screen.fill(gmod.Colour.WHITE)
		pygame.display.update()
		#print (Florin Salam Salam Salam)
		#print(self.grid.matrix[1][1].material, self.grid.matrix[1][1].colour)
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.exitGame()
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.exitGame()
					elif event.key == pygame.K_1:
						self.takeScreenshot()
				elif event.type == pygame.MOUSEBUTTONDOWN:
					if self.mousePressed == False and event.button == 1:
						self.mousePressed = True
					elif event.button == 5:   #scroll down
						self.grid.changeLastColourDown()
					elif event.button == 4:   #scroll up
						self.grid.changeLastColourUp()

				elif event.type == pygame.MOUSEBUTTONUP and self.mousePressed == True and \
				event.button == 1:
					self.mousePressed = False
			



			self.grid.updateBlocks()
			if self.mousePressed == True:
				tile = self.grid.findTouchedBlock(pygame.mouse.get_pos()) 
				self.grid.activateArea(tile)
				self.sm.playFallingSand()

			if not self.grid.isSandMoving() and self.sm.isFallPlaying:
				self.sm.stopFallingSand()


			self.grid.afis()

			matrix = self.grid.matrix
			for pos in self.grid.getPosArray():
				self.dirtyRectArray.append(matrix[pos[0]][pos[1]].rect)



			if self.grid.noWhiteBlocks == 0:
				self.grid.noWhiteBlocks -= 1  #tiganeala
				print("Florin Salam Salam!")
				self.takeScreenshot()

			pygame.display.update(self.dirtyRectArray)
			self.dirtyRectArray.clear()
			self.grid.newFrameInit()
			
			self.fpsClock.tick(self.FPS)


	def exitGame(self):
		pygame.quit()
		sys.exit()

	def takeScreenshot(self):
		subscreen = gmod.screen.subsurface(pygame.Rect((0, self.grid.matrix[0][0].height), \
			(gmod.screen.get_width(), gmod.screen.get_height()-self.grid.matrix[0][0].height)))
		if self.screenShotNo <= 9:
			pygame.image.save(subscreen, "screenshot0" + str(self.screenShotNo) + ".jpeg")
		else:
			pygame.image.save(subscreen, "screenshot" + str(self.screenShotNo) + ".jpeg")
		self.screenShotNo+=1
