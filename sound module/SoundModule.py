import pygame, os, sys


class SoundModule():
	def __init__(self):
		pygame.mixer.init()
		filename = os.path.join("sounds", "sand_pour.wav")
		self.sandFallingSound = pygame.mixer.Sound(filename)
	def play(self):
		
		self.sandFallingSound.play(loops = 2)
		# pygame.mixer.Channel.play(self.sandFallingSound)
		print("play")

SM = SoundModule()
SM.play()
