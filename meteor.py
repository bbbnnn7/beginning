import pygame 
from pygame.sprite import Sprite

class Meteor(Sprite):
	def __init__(self , ms_game):
		super().__init__()
		self.screen = ms_game.screen
		self.image = pygame.image.load("images/meteor.bmp")
		self.rect = self.image.get_rect()
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height
		self.x = float(self.rect.x)
		self.settings = ms_game.settings
		
	def check_edges(self):
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right or self.rect.left <= 0:
			return True

	def update(self):
		self.x += (self.settings.meteor_speed * self.settings.meteor_direction )
		self.rect.x = self.x
		

