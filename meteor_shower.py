import sys
import pygame
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from meteor import Meteor
from super_bullet import Super_bullet
from game_stats import Game_stats
from button import Button
from scoreboard import Scoreboard

class MeteorShower:
	def __init__(self):
		pygame.init()
		self.settings = Settings()
		self.screen = pygame.display.set_mode((0 , 0), pygame.FULLSCREEN)
		self.settings.screen_width = self.screen.get_rect().width
		self.settings.screen_height = self.screen.get_rect().height
		pygame.display.set_caption("Meteor shower")
		self.ship = Ship(self)	
		self.bullets = pygame.sprite.Group()
		self.meteors = pygame.sprite.Group()
		self._create_rain()
		self.super_bullets = pygame.sprite.Group()
		self.stats = Game_stats(self)
		self.sb = Scoreboard(self)
		self.play_button = Button(self , "Play")

	def _check_event(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)

	def _check_play_button(self , mouse_pos):
		if self.play_button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
			self.stats.reset_stats()
			self.stats.game_active = True
			self.sb.prep_score()
			self.sb.prep_hs()
			self.sb.prep_ships()
			self.sb.show_score()
			self.meteors.empty()
			self.bullets.empty()
			self._create_rain()
			self.ship.center_ship()
			self.settings.initialize_settings()
			pygame.mouse.set_visible(False)

	def _check_keydown_events(self, event):
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = True
		elif event.key == pygame.K_q:
			sys.exit()
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()
		elif event.key == pygame.K_s:
			self._fire_super_bullet()
		elif event.key == pygame.K_p:
			if not self.stats.game_active:
				self.stats.reset_stats()
				self.stats.game_active = True
				self.sb.prep_score()
				self.sb.prep_hs()
				self.sb.prep_ships()
				self.sb.show_score()
				self.meteors.empty()
				self.bullets.empty()
				self._create_rain()
				self.ship.center_ship()
				self.settings.initialize_settings()
				pygame.mouse.set_visible(False)
				

	def _check_keyup_events(self, event):
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False

	def _check_meteor_edges(self):
		for meteor in self.meteors.sprites():
			if meteor.check_edges():
				self._change_meteor_direction()
				break

	def _change_meteor_direction(self):
		for meteor in self.meteors.sprites():
			meteor.rect.y += meteor.settings.meteor_drop_speed
		self.settings.meteor_direction *= -1

	def _fire_bullet(self):
		if len(self.bullets) < self.settings.bullet_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)

	def _fire_super_bullet(self):
		if len(self.super_bullets) <= 1 :
			new_super_bullet = Super_bullet(self)
			self.super_bullets.add(new_super_bullet)

	def _create_rain(self):
		meteor = Meteor(self)
		meteor_width , meteor_height = meteor.rect.size
		available_space_x = self.settings.screen_width - (2 * meteor_width)
		number_meteor_x = available_space_x // (2 * meteor_width)
		ship_height = self.ship.rect.height
		available_space_y = (self.settings.screen_height - (3 * meteor_height) - ship_height)
		number_rows = available_space_y // (2 * meteor_height)
		for row_number in range(number_rows):
			for meteor_number in range(number_meteor_x):
				self._create_meteor(meteor_number , row_number)

	def _create_meteor(self , meteor_number , row_number):
		meteor = Meteor(self)
		meteor_width , meteor_height = meteor.rect.size
		meteor.x = 20 + meteor_width + 2 * meteor_width * meteor_number
		meteor.rect.x = meteor.x
		meteor.rect.y = meteor.rect.height + 2 * meteor.rect.height * row_number
		self.meteors.add(meteor)
	
	def _screen_update(self):
		self.screen.fill(self.settings.bg_color)
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		for bullet in self.super_bullets.sprites():
			bullet.draw_super_bullet()
		self.meteors.draw(self.screen)
		self._check_meteor_edges()
		self.sb.show_score()
		if not self.stats.game_active:
			self.play_button.draw_button()
		pygame.display.flip()

	def _bullet_update(self):
		self.bullets.update()
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)
		self._check_bullet_meteor_collision()

	def _super_bullet_update(self):
		self.super_bullets.update()
		for bullet in self.super_bullets.copy():
			if bullet.rect.bottom <= 0:
				self.super_bullets.remove(bullet)
		collisions = pygame.sprite.groupcollide(self.super_bullets , self.meteors , False , True)
		if collisions:
			for i in collisions.values():
				self.stats.score += self.settings.meteor_point * len(i)
			self.sb.prep_score()
			self.sb.check_high_score()

	def _check_bullet_meteor_collision(self):
		collisions = pygame.sprite.groupcollide(self.bullets , self.meteors , True , True)
		if collisions:
			for i in collisions.values():
				self.stats.score += self.settings.meteor_point * len(i)
			self.sb.prep_score()
			self.sb.check_high_score()
		if not self.meteors:
			self.super_bullets.empty()
			self.bullets.empty()
			self._create_rain()
			self.settings.increase()
			self.stats.level += 1
			self.sb.prep_level()

	def _meteor_update(self):
		self.meteors.update()
		if pygame.sprite.spritecollideany(self.ship , self.meteors):
			self.ship_hit()
		self._check_meteor_bottom()

	def ship_hit(self):
		if self.stats.ship_left >0:
			self.stats.ship_left -= 1
			self.sb.prep_ships()
			self.bullets.empty()
			self.meteors.empty()
			self.super_bullets.empty()
			self._create_rain()
			self.ship.center_ship()
			sleep(0.5)
		else:
			self.stats.game_active = False
			pygame.mouse.set_visible(True)

	def _check_meteor_bottom(self):
		screen_rect = self.screen.get_rect()
		for meteor in self.meteors.sprites():
			if meteor.rect.bottom >= screen_rect.bottom:
				self.ship_hit()
				break
	
	def run_game(self):
		while True:
			self._check_event()
			if self.stats.game_active:
				self.ship.update()
				self._bullet_update()
				self._super_bullet_update()
				self._meteor_update()
			self._screen_update() 		

if __name__ == '__main__':
	ms = MeteorShower()
	ms.run_game() 
