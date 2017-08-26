import pygame, os, sys


class SoundModule():
	pygame.mixer.init()
	def __init__(self):
		filename = os.path.join("sounds", "sand_pour.wav")
		self.sandFallingSound = pygame.mixer.Sound(filename)

	def playFallingSand(self):
		self.sandFallingSound.play()
	def stopFallingSand(self):
		#self.sandFallingSound.stop()
	 	self.sandFallingSound.fadeout(1000)
	def isFallPlaying(self):
		return pygame.mixer.get_busy()
