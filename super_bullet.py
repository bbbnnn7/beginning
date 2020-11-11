import pygame
from pygame.sprite import Sprite
from settings import Settings

class Super_bullet(Sprite):
	def __init__(self , ms_game):
		super().__init__()
		self.screen = ms_game.screen
		self.settings = ms_game.settings
		self.color = self.settings.super_bullet_color
		self.rect = pygame.Rect( 0 , 0 , self.settings.super_bullet_width , self.settings.super_bullet_height )
		self.rect.midtop = ms_game.ship.rect.midtop
		self.y = float(self.rect.y)

	def update(self):
		self.y -= self.settings.super_bullet_speed
		self.rect.y = self.y

	def draw_super_bullet(self):
		pygame.draw.rect(self.screen , self.color , self.rect)
