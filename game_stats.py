import pygame

class Game_stats():
	def __init__(self , ms_game):
		self.settings = ms_game.settings
		self.reset_stats()
		self.game_active = False
		self.file_open = open('text')
		self.high_score = int(self.file_open.readline())
		self.file_open.close()
		self.level = 1

	def reset_stats(self):
		self.ship_left = self.settings.ship_limit
		self.score = 0
