import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard:
	def __init__(self , ms_game):
		self.screen = ms_game.screen
		self.screen_rect = ms_game.screen.get_rect()
		self.settings = ms_game.settings
		self.stats = ms_game.stats
		self.ms_game = ms_game
		self.text_color = (30 , 30 , 30)
		self.font = pygame.font.SysFont(None , 48)
		self.prep_score()
		self.prep_hs()
		self.prep_ships()
		self.prep_level()

	def prep_score(self):
		round_score = round(self.stats.score , -1)
		score_str = "{:,}".format(round_score)
		self.score_image = self.font.render(score_str , True , self.text_color , self.settings.bg_color)
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right -20
		self.score_rect.top = 20

	def prep_hs(self):
		round_hs = round(self.stats.high_score , -1)
		hs_str = "{:,}".format(round_hs)
		self.hs_image = self.font.render(hs_str , True , self.text_color , self.settings.bg_color)
		self.hs_rect = self.hs_image.get_rect()
		self.hs_rect.centerx = self.screen_rect.centerx
		self.hs_rect.top = self.screen_rect.top

	def prep_ships(self):
		self.ships = Group()
		for ship_number in range(self.stats.ship_left +1):
			ship = Ship(self.ms_game)
			ship.rect.x = 10 + ship_number * ship.rect.width
			ship.rect.y = 10
			self.ships.add(ship)

	def prep_level(self):
		level_str = str(self.stats.level)
		self.level_image = self.font.render(level_str , True , self.text_color , self.settings.bg_color)
		self.level_rect = self.level_image.get_rect()
		self.level_rect.right = self.score_rect.right
		self.level_rect.top  = self.score_rect.bottom + 10

	def check_high_score(self):
		if self.stats.score > self.stats.high_score:
			self.stats.high_score = self.stats.score
			self.file_open = open('text' , 'w')
			self.file_open.write(str(self.stats.high_score))
			self.file_open.close()
			self.prep_hs()

	def show_score(self):
		self.screen.blit(self.score_image , self.score_rect)
		self.screen.blit(self.hs_image , self.hs_rect)
		self.screen.blit(self.level_image , self.level_rect)
		sel.ships.draw(self.screen)
