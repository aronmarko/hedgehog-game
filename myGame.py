import pygame
import time
import random

pygame.init()

display_width = 1000
display_height = 600
hedgehog_width = 65
hedgehog_height = 50

black = (0, 0, 0)
white = (255, 255, 255)

#Loading sound files
background_sound = pygame.mixer.music.load('background.mp3')
jump_sound = pygame.mixer.Sound('jump.wav')
bellring_sound = pygame.mixer.Sound('bellring.wav')
eating_apple_sound = pygame.mixer.Sound('eat.wav')

gameDisplay = pygame.display.set_mode((display_width, display_height))		#display setting
pygame.display.set_caption('Hedgehog Adventure')		#caption setting
clock = pygame.time.Clock()		#clock setting

#Loading images
backgroundImg = pygame.image.load('field.png')
hedgehogImg = pygame.image.load('Hedgehog.png')
appleImg = pygame.image.load('apple.png')
smallAppleImg = pygame.image.load('apple_small.png')
lifeImg = pygame.image.load('heart.png')
wallImg = pygame.image.load('wall.png')
unkownImg = pygame.image.load('question_mark.png')
houseImg = pygame.image.load('house.png')

def show_lives(lives):			#lives on the top left corner
	font = pygame.font.SysFont(None, 25)
	text = font.render("x" + str(lives), True, black)
	gameDisplay.blit(lifeImg, (0,0))
	gameDisplay.blit(text, (35,8))
	
def reachNewLife(eaten_apple):		#how many apple needed for a new life (10 apple = 1 new life)
	font = pygame.font.SysFont(None, 20)
	text = font.render("+" + str(eaten_apple), True, black)
	gameDisplay.blit(smallAppleImg, (70,5))
	gameDisplay.blit(text, (90,8))

def wall(wallx, wally, wallw, wallh):		#insert wall image, (hit the wall = minus 1 life)
	gameDisplay.blit(wallImg, (wallx, wally))
	
def hedgehog(x,y):		#insert hedgehog image
	gameDisplay.blit(hedgehogImg, (x,y))
	
def apple(applex, appley, applew, appleh):		#insert apple image
	gameDisplay.blit(appleImg, (applex, appley))
	
def surprise(question_markx, question_marky, question_markw, question_markh):		#insert question mark image, qm causes a random event (add or extract lives or apples)
	gameDisplay.blit(unkownImg, (question_markx, question_marky))
	
def text_objects(text, font):
	textSurface = font.render(text, True, black)		#make crash string
	return textSurface, textSurface.get_rect()
	
def message_display(text):		#write on the screen the crash string
	largeText = pygame.font.Font('freesansbold.ttf', 90)
	TextSurf, TextRect = text_objects(text, largeText)
	TextRect.center = ((display_width / 2), (display_height / 3))
	gameDisplay.blit(TextSurf, TextRect)
	pygame.display.update()
	time.sleep(0.5)
	
def highscore_display(score):		#show actual score
	highscore_font = pygame.font.SysFont(None, 25)
	highscore_text = highscore_font.render("Score: " + str(score), True, black)
	gameDisplay.blit(highscore_text, (825, 1))
	
def record_highscore_display(record):		#show maximum score(your best result))
	max_highscore_font = pygame.font.SysFont(None, 25)
	max_highscore_text = max_highscore_font.render("Your Best: " + str(record), True, black)
	gameDisplay.blit(max_highscore_text, (650, 1))
	
def crash():		#
	message_display("Crash")
	
def restart_message():		#game ending message (if you died)
	restartGame_text = pygame.font.Font('freesansbold.ttf', 40)
	restartGame_textSurface = restartGame_text.render('Game over! The game will start again in 5 seconds!', True, black)
	restartGame_textRect = restartGame_textSurface.get_rect()
	restartGame_textRect.center = ((display_width / 2), (display_height / 2))
	gameDisplay.blit(restartGame_textSurface, restartGame_textRect)
	pygame.display.update()
	time.sleep(5)
	
def end_message():		#game ending message (if you win)
	endGame_text = pygame.font.Font('freesansbold.ttf', 40)
	endGame_textSurface = endGame_text.render('You got home! You won!', True, black)
	endGame_textRect = endGame_textSurface.get_rect()
	endGame_textRect.center = ((display_width / 2), (display_height / 2))
	gameDisplay.blit(endGame_textSurface, endGame_textRect)
	pygame.display.update()
	time.sleep(1)
		
def game_loop():		#game loop

	x = display_width * 0.01
	y = display_height * 0.93
	y_change = 0
	bgx = 0
	apple_counter = 0
	hedgehog_life = 5
	hedgehog_actual_score = 0
	actual_score_1000 = 0
	hedgehog_max_score = 0
	
	apple_startx = 1080
	apple_starty = random.uniform(display_height * 0.4, display_height * 0.92)
	apple_speed = 7
	apple_width = 34
	apple_height = 33
	
	qm_startx = random.uniform(3000, 5000)
	qm_starty = random.uniform(display_height * 0.4, display_height * 0.92)
	qm_width = 25
	qm_height = 36
	qm_speed = 7
	
	wall_height = 100
	wall_width = 16
	wall_speed = 7
	wall_startx = random.uniform(1200, 3000)
	wall_starty = display_height - wall_height
	
	housex = 1100
	housey = 420
	housew = 450
	househ = 219
	house_speed = 3
	
	pygame.mixer.music.set_volume(0.2)		#background music volume
	pygame.mixer.music.play(-1)
	
	#====Main lop====
	gameExit = True
	
	while gameExit:	
	
		pygame.mixer.music.unpause()
		
		random_event_number = random.randrange(1, 3)		#random number generator between 1-3, a random event happens, when you pick up a question mark
	
		rel_bgx = bgx % backgroundImg.get_rect().width
		gameDisplay.blit(backgroundImg, (rel_bgx - backgroundImg.get_rect().width, 0))		#moving background image
		if rel_bgx < display_width:
			gameDisplay.blit(backgroundImg, (rel_bgx, 0))
		bgx -= 3		#image speed
		
		for event in pygame.event.get():
		
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			
			if y == display_height * 0.93:
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						y_change = -10
						pygame.mixer.Sound.play(jump_sound)
		
		y += y_change
		
		if y < display_height * 0.65:		#maximum jumping boundary  
			y_change += 11	
		
		if y > display_height * 0.93:		#hedgehog hit the ground
			y = display_height * 0.93
			y_change = 0
		
		#function calls
		hedgehog(x,y)
		highscore_display(hedgehog_actual_score)
		record_highscore_display(hedgehog_max_score)
		show_lives(hedgehog_life)
		reachNewLife(apple_counter)
			
		apple_startx -= apple_speed		#moving apples
		apple(apple_startx, apple_starty, apple_width, apple_height)
		
		wall_startx -= wall_speed		#moving walls
		wall(wall_startx, wall_starty, wall_width, wall_height)
		
		qm_startx -= qm_speed		#moving qm
		surprise(qm_startx, qm_starty, qm_width, qm_height)
		
		if hedgehog_life > 0:		#scoring system settings
			hedgehog_actual_score += 1
			actual_score_1000 += 1
			if hedgehog_actual_score > hedgehog_max_score:
				hedgehog_max_score = hedgehog_actual_score
			if actual_score_1000 == 1000:
				pygame.mixer.Sound.play(bellring_sound)		#bell rings after every 1000 point
				actual_score_1000 = 0
		
		if apple_startx + apple_width < 0:		#if an apple dissapear from the screen
			apple_startx = display_width + apple_width
			apple_starty = random.uniform(display_height * 0.5, display_height * 0.92)
		
		if x + hedgehog_width > apple_startx:		#if hit an apple
			if y + hedgehog_height >= apple_starty and y + hedgehog_height <= apple_starty + apple_height or y < apple_starty + apple_height and y > apple_starty:
				pygame.mixer.Sound.play(eating_apple_sound)
				apple_counter += 1
				reachNewLife(apple_counter)
				if apple_counter >= 10:
					hedgehog_life += 1
					apple_counter = 0
				apple_startx = -40
				apple_starty = -40
				
		if wall_startx + wall_width < 0:					#if a wall dissapear from the screen
			wall_startx = random.uniform(1200, 3000)
			wall_starty = display_height - wall_height
		
		if y + hedgehog_height >= wall_starty:		#if hit the wall
			if (x + hedgehog_width >= wall_startx and x + hedgehog_width <= wall_startx + wall_width) or (x >= wall_startx and x <= wall_startx + wall_width):
				crash()
				hedgehog_life -= 1
				if hedgehog_life == 0:
					pygame.mixer.music.pause()
					restart_message()
					hedgehog_actual_score = 0
					actual_score_1000 = 0
					hedgehog_life = 5
					apple_counter = 0
				wall_startx = -60
				wall_starty = -60
				
		if qm_startx + qm_width < 0:		#if qm dissapear from the screen
			qm_startx = random.uniform(3000, 5000)
			qm_starty = random.uniform(display_height * 0.4, display_height * 0.92)
			
		if x + hedgehog_width > qm_startx:		#if hit the qm
			if y + hedgehog_height >= qm_starty and y + hedgehog_height <= qm_starty + qm_height or y < qm_starty + qm_height and y > qm_starty:
				if random_event_number == 1:
					hedgehog_life += random.randrange(-2, 3)		#get or lose lives between -2 and 2
				elif random_event_number == 2:
					apple_counter += random.randrange(-3, 4)	#get or lose apples between -3 and 3
				else:
					pass		#nothing will happen
				if apple_counter < 0:
					apple_counter = 0
				if apple_counter >= 10:
					hedgehog_life += 1
					apple_counter = 0
				if hedgehog_life <= 0:
					pygame.mixer.music.pause()
					restart_message()
					hedgehog_actual_score = 0
					actual_score_1000 = 0
					hedgehog_life = 5
					apple_counter = 0
				qm_startx = -50	
				qm_starty = -50
				
		if hedgehog_actual_score >= 10000:			#you reach your house
			housex -= house_speed
			gameDisplay.blit(houseImg, (housex, housey))
			hedgehog_actual_score -= 1		#counter stop
			actual_score_1000 -= 1		#bellring stop
			apple_startx = 2000		#apple dissapear
			wall_startx = 2000		#wall dissapear
			qm_startx = 2000		#qm dissapear
			
		if x + hedgehog_width >= (housex + housew) / 4:
			gameDisplay.blit(hedgehogImg, (x,y))
			house_speed = 0
			bgx = 0
			end_message()
			
		pygame.display.update()
		clock.tick(60)		#frame per second
	
game_loop()
