#!/usr/bin/env python
#
# Making Games with Pygame
#
#

import pygame
from pygame import mixer
import time
import math
import random

# Player
class Player:
	def __init__(self):
		self.Img = pygame.image.load('player.png')
		self.X = 370
		self.Y = 480
		self.X_change = 0

	def update(self, x, y):
		screen.blit(self.Img, (x, y))

# Enemy
class Enemy:
	def __init__(self):
		self.Img = pygame.image.load('invader.png')
		self.X = random.randint(100, 700)
		self.Y = random.randint(50, 150)
		self.X_change = 2
		self.Y_change = 40
	def update(self, x, y):
		screen.blit(self.Img, (x, y))

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
class Bullet:
	def __init__(self):
		self.Img = pygame.image.load('bullet.png')
		self.X = 370
		self.Y = 480
		self.X_change = 0
		self.Y_change = 7
		self.state = "ready"
		self.bullet_sound = mixer.Sound('bullet_sound.wav')

	def fire_bullet(self, x, y):
		self.state = "fire"
		screen.blit(self.Img, (x + 16, y + 10))

	def isCollision(self, enemyX, enemyY, bulletX, bulletY):
		distance = math.sqrt(((bulletX) - (enemyX))**2 + ((bulletY) - (enemyY))**2)
		if distance < 30:
			return True
		else:
			return False

# Score

class Score_text:
	def __init__(self):
		self.score_value = 0
		self.font = pygame.font.Font('ToyBox.ttf', 32)		
		self.textX = 10
		self.textY = 10
	
	def show_score(self, x, y):
		self.score = self.font.render("Score : " + str(self.score_value), True, (255, 255, 255))
		screen.blit(self.score, (x, y))

class Game_Over_text:
	def __init__(self):
		self.text = "GAME OVER"
		self.font = pygame.font.Font('ToyBox.ttf', 72)
		self.textX = 100
		self.textY = 200

	def show_text(self):
		self.texting = self.font.render(self.text, True, (55, 0, 25))
		screen.blit(self.texting, (self.textX, self.textY))

# Initilaize the pygame
pygame.init()

screen = pygame.display.set_mode((800, 600))

score = 0
# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("rocket.png")
pygame.display.set_icon(icon)

# Background
background = pygame.image.load('starry_background.png')

# Background Music
mixer.music.load('BackgroundNoise.wav')
mixer.music.set_volume(0.05)
mixer.music.play(-1)
# Objects
player = Player()
num_bullets = 5
bullets = []
bullet_counter = 0
for i in range(num_bullets):
	bullet = Bullet()
	bullets.append(bullet)
num_enemies = 10
enemies = []
for i in range(num_enemies):
	enemy = Enemy()
	enemies.append(enemy)
score = Score_text()
gameover = Game_Over_text()

# Game Loop
running = True
while running:

	# RGB = Red, Green, Blue
	screen.fill((0, 0, 0))
	# Background Image
	screen.blit(background, (0, 0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		# if keystroke is pressed check whether its right or left

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				player.X_change -= 4
			if event.key == pygame.K_RIGHT:
				player.X_change += 4
			if event.key == pygame.K_SPACE:
				bullet = bullets[bullet_counter]
				if bullet.state == "ready":
					# Get the current x coordinate of the spaceship
					bullet.X = player.X
					bullet.fire_bullet(bullet.X, bullet.Y)
					if bullet_counter < 4:
						bullet_counter += 1
					else:
						bullet_counter = 0
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				player.X_change += 4
			if event.key == pygame.K_RIGHT:
				player.X_change -= 4
	
	# Checking for boundaries of spaceship so it doesn't go out of bbounds
	player.X += player.X_change
	
	if player.X <= 0:
		player.X = 0
	elif player.X >= 736:
		player.X = 736
	# Enemy Movement
	for enemy in enemies:

		enemy.X += enemy.X_change
		
		# GAME OVER

		if enemy.Y > 480:
			for i in enemies:
				i.Y = 2000
			gameover.show_text()
		# Limit movement to inside window
		if enemy.X <= 0 or enemy.X >= 736:
			enemy.X_change *= -1
			enemy.Y += enemy.Y_change
	
	# Bullet Movement
	for bullet in bullets:
		if bullet.Y <= 0:
			bullet.Y = 480
			bullet.state = "ready"

		if bullet.state == "fire":
			bullet.fire_bullet(bullet.X, bullet.Y)
			bullet.Y -= bullet.Y_change

	# Collision
	for enemy in enemies:
		for bullet in bullets:
			if bullet.state == "fire":
				collision = bullet.isCollision(enemy.X, enemy.Y, bullet.X, bullet.Y)	
				if collision:
					bullet.Y = 480
					bullet.state = "ready"
					score.score_value += 1
					enemy.X = random.randint(100, 700)
					enemy.Y = random.randint(50, 150)
					bullet.bullet_sound.play()
	player.update(player.X, player.Y)
	for enemy in enemies:
		enemy.update(enemy.X, enemy.Y)
	score.show_score(score.textX, score.textY)
	pygame.display.update()			