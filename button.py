import pygame.font

class Button:
	def __init__(self , ms_game , msg):
		self.screen = ms_game.screen
		self.screen_rect = ms_game.screen.get_rect()
		self.width , self.height = 200 , 50
		self.button_color = (0 , 100 , 0)
		self.text_color = (250 , 250 , 250)
		self.rect = pygame.Rect(0 , 0 , self.width , self.height)
		self.rect.center = self.screen_rect.center
		self.font = pygame.font.SysFont(None , 48)
		self.prep_msg(msg)

	def prep_msg(self , msg):
		self.msg_image = self.font.render(msg , True , self.button_color , self.text_color)
		self.msg_image_rect = self.msg_image.get_rect()
		self.msg_image_rect.center = self.rect.center

	def draw_button(self):
		self.screen.fill(self.button_color , self.rect)
		self.screen.blit(self.msg_image , self.msg_image_rect)
