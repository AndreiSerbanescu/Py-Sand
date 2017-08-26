import GlobalModule as gmod
import pygame



class Grid():
	def __init__(self, rowNo, colNo):
		self.rowNo = rowNo
		self.colNo = colNo
		width, height = int(gmod.screen.get_width()/(colNo-2)), int(gmod.screen.get_height()/(rowNo-1))
		self.matrix = [[Block(width, height) for x in range(self.colNo)] for y in range(self.rowNo)]
		
		self.posMovedBlocksArray = [] #array of all changed blocks positions in the matrix
		self.lastColour = gmod.Colour.colourMatrix[gmod.Colour.index]

		self.noWhiteBlocks = (colNo-2) * (rowNo-2)

		self.initMatrix(width, height)

		self.minMovBlocksNo = len(self.matrix[0])

	def initMatrix(self, width, height):
		#a = air, s = sand, g = gui (shouldn't be changed to a or s)
		#b = block

		newX = newY = 0 
		for i in range(self.rowNo-1):
			for j in range(1, self.colNo-1):
				self.matrix[i][j].change_pos(newX, newY)
				self.matrix[i][j].material = 'a'
				newX += width
			newY += height
			newX = 0
		for i in range(self.colNo):
			self.matrix[self.rowNo-1][i].material = 'b'
			self.matrix[0][i].material = 'g'
			self.matrix[0][i].colour = self.lastColour
		for i in range(self.rowNo):
			self.matrix[i][self.colNo-1].material = 'b'
			self.matrix[i][0].material = 'b'

	def afis(self):
		for pos in self.posMovedBlocksArray:
			block = self.matrix[pos[0]][pos[1]]
			if block.material == 'g':
				colour = self.lastColour
			else:
				colour = block.colour
			gmod.screen.fill(colour, block.rect)
		gmod.screen.fill(self.lastColour, self.matrix[0][1].rect)  #tiganeala!!!

	def findTouchedBlock(self, mouseCoord):
		row = int(mouseCoord[1] / self.matrix[1][1].height)
		col = int(mouseCoord[0] / self.matrix[1][1].width) + 1
		return (row, col)

	def activateArea(self, pos):
		if self.matrix[pos[0]][pos[1]].material == 'a':

			self.activateBlock(pos)
			if self.matrix[pos[0]][pos[1]-1].material == 'a':
				self.activateBlock((pos[0], pos[1]-1))
			if self.matrix[pos[0]][pos[1]+1].material == 'a':
				self.activateBlock((pos[0], pos[1]+1))

	def activateBlock(self, pos):
		self.matrix[pos[0]][pos[1]].material = 's'
		self.matrix[pos[0]][pos[1]].colour = self.lastColour
		self.posMovedBlocksArray.append(pos)
		self.noWhiteBlocks -= 1

	def updateBlocks(self):
		block = self.matrix[1][1]
		heightAndWidth = (block.width, block.height)
		for i in reversed(range(self.rowNo)):
			for j in range(self.colNo):
				if self.matrix[i][j].material == 's':
					if self.matrix[i+1][j].material == 'a':
						# self.matrix[i][j].material = 'a'
						# self.matrix[i+1][j].material = 's'
						self.swap((i, j), (i+1, j))
						# if self.matrix[i][j+1].material == 's':  #bug, dar e misto, trage intr-o parte
						# 	self.swap((i+1, j), (i+1, j+1))
						# if self.matrix[i][j+1].material == 's': 
						# 	self.swap((i+1, j), (i+1, j-1))
					else:
						if gmod.AlternatingCode == 1:
							pos1 = (i+1, j-1)
							pos2 = (i+1, j+1)
						elif gmod.AlternatingCode == 0:
							pos2 = (i+1, j-1)
							pos1 = (i+1, j+1)
						if self.matrix[pos1[0]][pos1[1]].material == 'a':
							self.swap((i, j), pos1)

							if gmod.AlternatingCode == 0: gmod.AlternatingCode = 1
							elif gmod.AlternatingCode == 1: gmod.AlternatingCode = 0

						elif self.matrix[pos2[0]][pos2[1]].material == 'a':
							# self.matrix[i][j].material = 'a'
							# self.matrix[pos2[0]][pos2[1]].material = 's'
							self.swap((i, j), pos2)


	def swap(self, pos1, pos2):
		block1 = self.matrix[pos1[0]][pos1[1]]
		block2 = self.matrix[pos2[0]][pos2[1]]
		aux = (block1.colour, block1.material)
		block1.material = block2.material
		block1.colour = block2.colour
		block2.colour = aux[0]
		block2.material = aux[1]

		self.posMovedBlocksArray.append(pos1)
		self.posMovedBlocksArray.append(pos2)

	def newFrameInit(self):
		self.posMovedBlocksArray.clear()
		for i in range(len(self.matrix[0])):
			self.posMovedBlocksArray.append((0, i))

	def getPosArray(self):
		return self.posMovedBlocksArray
	def changeLastColourUp(self):
		COLOUR = gmod.Colour
		COLOUR.index -= 1
		if gmod.Colour.index < 0:
			COLOUR.index = len(COLOUR.colourMatrix) - 1
		self.setLastColour(COLOUR.colourMatrix[COLOUR.index])
	def changeLastColourDown(self):
		COLOUR = gmod.Colour
		COLOUR.index += 1
		if COLOUR.index >= len(COLOUR.colourMatrix):
			COLOUR.index = 0
		self.setLastColour(COLOUR.colourMatrix[COLOUR.index])
	def setLastColour(self, colour):
		self.lastColour = colour

	def isSandMoving(self):
		return (len(self.posMovedBlocksArray) > self.minMovBlocksNo)


class Block():
	def __init__(self, width, height, x=0, y=0, material = 'a', colour = gmod.Colour.WHITE):
		self.width = width
		self.height = height
		self.pos = (x, y)
		self.rect = pygame.Rect(self.pos, (width, height))
		self.material = material
		self.colour = colour
	def change_pos(self, x, y):
		self.pos = (x, y)
		self.rect = (self.pos, (self.width, self.height))