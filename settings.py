class Settings:
	def __init__(self):
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (250 , 250 , 250)
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (250 , 0 , 0)
		self.bullet_allowed = 10
		self.meteor_drop_speed = 15
		self.super_bullet_width = 300
		self.super_bullet_height = 30
		self.super_bullet_color = (0 , 0 , 250)
		self.ship_limit = 2
		self.speedup_scale = 1.1
		self.meteor_point_scale = 1.5
		self.initialize_settings()
	
	def initialize_settings(self):
		self.ship_speed = 20
		self.bullet_speed = 3
		self.meteor_speed = 3
		self.super_bullet_speed = 20
		self.meteor_direction = 1
		self.meteor_point = 50
	
	def increase(self):
#		self.ship_speed *= self.speedup_scale
		self.bullet_speed *= self.speedup_scale
		self.meteor_speed *= self.speedup_scale
		self.super_bullet_speed *= self.speedup_scale
		self.meteor_point = int(self.meteor_point * self.meteor_point_scale)
