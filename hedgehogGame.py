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
transparent = (0, 0, 0, 0)

#Hangfájlok betöltése
background_sound = pygame.mixer.music.load('background.mp3')		#mp3 eltér a wavtól
jump_sound = pygame.mixer.Sound('jump.wav')
bellring_sound = pygame.mixer.Sound('bellring.wav')
eating_apple_sound = pygame.mixer.Sound('eat.wav')

gameDisplay = pygame.display.set_mode((display_width, display_height))		#képernyő beállítás
pygame.display.set_caption('Hedgehog Adventure')		#cím
clock = pygame.time.Clock()		#időzítő beállítás

#Képek betöltése a változóikba
backgroundImg = pygame.image.load('field.png')
hedgehogImg = pygame.image.load('Hedgehog.png')
appleImg = pygame.image.load('apple.png')
smallAppleImg = pygame.image.load('apple_small.png')
lifeImg = pygame.image.load('heart.png')
wallImg = pygame.image.load('wall.png')
unkownImg = pygame.image.load('question_mark.png')
houseImg = pygame.image.load('house.png')

def show_lives(lives):			#életek mutatása
	font = pygame.font.SysFont(None, 25)
	text = font.render("x" + str(lives), True, black)
	gameDisplay.blit(lifeImg, (0,0))
	gameDisplay.blit(text, (35,8))
	
def reachNewLife(eaten_apple):		#fv, ami mutatja hány alma kell még az új élethez
	font = pygame.font.SysFont(None, 20)
	text = font.render("+" + str(eaten_apple), True, black)
	gameDisplay.blit(smallAppleImg, (70,5))
	gameDisplay.blit(text, (90,8))

def wall(wallx, wally, wallw, wallh):		#fal kép beillesztése, elvesz egy életet
	gameDisplay.blit(wallImg, (wallx, wally))
	
def hedgehog(x,y):		#sün kép beillesztése, vele játszol
	gameDisplay.blit(hedgehogImg, (x,y))
	
def apple(applex, appley, applew, appleh):		#alma kép beillesztése, ad egy életet
	gameDisplay.blit(appleImg, (applex, appley))
	
def surprise(question_markx, question_marky, question_markw, question_markh):		#kérdőjel kép beillesztése, nem lehet tudni mit ad, ha felszeded
	gameDisplay.blit(unkownImg, (question_markx, question_marky))
	
def text_objects(text, font):
	textSurface = font.render(text, True, black)		#crash szöveg elkészítése
	return textSurface, textSurface.get_rect()		#visszadja a szöveget, és a körülette lévő téglalapot
	
def message_display(text):		#crash szöveg kiírása
	largeText = pygame.font.Font('freesansbold.ttf', 90)
	TextSurf, TextRect = text_objects(text, largeText)
	TextRect.center = ((display_width / 2), (display_height / 3))
	gameDisplay.blit(TextSurf, TextRect)
	pygame.display.update()
	time.sleep(0.5)
	
def highscore_display(score):		#elért pont
	highscore_font = pygame.font.SysFont(None, 25)
	highscore_text = highscore_font.render("Score: " + str(score), True, black)
	gameDisplay.blit(highscore_text, (825, 1))
	
def record_highscore_display(record):		#rekord pont
	max_highscore_font = pygame.font.SysFont(None, 25)
	max_highscore_text = max_highscore_font.render("Your Best: " + str(record), True, black)
	gameDisplay.blit(max_highscore_text, (650, 1))
	
def crash():		#maga a crash szöveg
	message_display("Crash")
	
def restart_message():		#játék végi szöveg kialakítása (ha meghalsz)
	restartGame_text = pygame.font.Font('freesansbold.ttf', 40)
	restartGame_textSurface = restartGame_text.render('Game over! The game will start again in 5 seconds!', True, black)
	restartGame_textRect = restartGame_textSurface.get_rect()
	restartGame_textRect.center = ((display_width / 2), (display_height / 2))
	gameDisplay.blit(restartGame_textSurface, restartGame_textRect)
	pygame.display.update()
	time.sleep(5)
	
def end_message():		#játék végi szöveg kialakítása (ha nyersz)
	endGame_text = pygame.font.Font('freesansbold.ttf', 40)
	endGame_textSurface = endGame_text.render('You got home! You won!', True, black)
	endGame_textRect = endGame_textSurface.get_rect()
	endGame_textRect.center = ((display_width / 2), (display_height / 2))
	gameDisplay.blit(endGame_textSurface, endGame_textRect)
	pygame.display.update()
	time.sleep(1)
		
def game_loop():		#játék főciklusa

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
	apple_starty = random.uniform(display_height * 0.4, display_height * 0.92)		#bármely két érték közötti random szám, randrange csak integereket fogad el
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
	
	pygame.mixer.music.set_volume(0.2)		#háttérzene hangereje
	pygame.mixer.music.play(-1)		#folyamatosan játssza a háttérzenét
	
	#====Fő ciklus====
	gameExit = True
	
	while gameExit:		#addig fut le, amíg a feltétel igaz
	
		pygame.mixer.music.unpause()		#zene újraindul a játék újrakezdése után
		
		random_event_number = random.randrange(1, 3)		#random szám generátor 1-3 között, ez alapján történik meg egy esemény
															#amikor kérdőjelet szedünk fel
	
		rel_bgx = bgx % backgroundImg.get_rect().width
		gameDisplay.blit(backgroundImg, (rel_bgx - backgroundImg.get_rect().width, 0))		#elindul a kép
		if rel_bgx < display_width:
			gameDisplay.blit(backgroundImg, (rel_bgx, 0))		#amint elindul rögtön utánnatesszük a képet mégegyszer
		bgx -= 3		#kép sebessége
		
		for event in pygame.event.get():
		
			if event.type == pygame.QUIT:		#ha bezárjuk a játékot vége lesz
				pygame.quit()
				quit()
			
			if y == display_height * 0.93:		#csak akkor tud ugrani, ha már a földön van
				if event.type == pygame.KEYDOWN:		#space billentyű lenyomására ugrás
					if event.key == pygame.K_SPACE:
						y_change = -10
						pygame.mixer.Sound.play(jump_sound)		#ugrás hang lejátszása
		
		y += y_change		#ténylegesen ugrik, y koordinátához hozzáadjuk a delta_y-t
		
		if y < display_height * 0.65:		#sün ugrás, felső határ  
			y_change += 11	
		
		if y > display_height * 0.93:		#sün ugrás, nem tud leesni a semmibe, alsó határ
			y = display_height * 0.93
			y_change = 0
		
		#Függvényhívások
		hedgehog(x,y)
		highscore_display(hedgehog_actual_score)
		record_highscore_display(hedgehog_max_score)
		show_lives(hedgehog_life)
		reachNewLife(apple_counter)
			
		apple_startx -= apple_speed		#mozog az alma
		apple(apple_startx, apple_starty, apple_width, apple_height)
		
		wall_startx -= wall_speed		#mozog a fal
		wall(wall_startx, wall_starty, wall_width, wall_height)
		
		qm_startx -= qm_speed		#kérdőjel mozog	(qm: question mark)
		surprise(qm_startx, qm_starty, qm_width, qm_height)
		
		if hedgehog_life > 0:		#pontozási rendszer
			hedgehog_actual_score += 1
			actual_score_1000 += 1		#ha elérjük az 1000 pontot, akkor betesszük egy változóba
			if hedgehog_actual_score > hedgehog_max_score:
				hedgehog_max_score = hedgehog_actual_score
			if actual_score_1000 == 1000:
				pygame.mixer.Sound.play(bellring_sound)		#minden 1000 pont elérése után szól a csengő
				actual_score_1000 = 0
		
		if apple_startx + apple_width < 0:		#ha eltűnik az alma a képernyőről
			apple_startx = display_width + apple_width
			apple_starty = random.uniform(display_height * 0.5, display_height * 0.92)
		
		if x + hedgehog_width > apple_startx:		#ha ütközünk az almával
			if y + hedgehog_height >= apple_starty and y + hedgehog_height <= apple_starty + apple_height or y < apple_starty + apple_height and y > apple_starty:
				pygame.mixer.Sound.play(eating_apple_sound)		#alma evés hang lejátszása
				apple_counter += 1
				reachNewLife(apple_counter)		#megevett almát kiírja, ha eléri a 10-et, újra 0-tól számol
				if apple_counter >= 10:
					hedgehog_life += 1		#ha 10 almát felszedünk kapunk egy új életet
					apple_counter = 0
				apple_startx = -40		#amint hozzáérünk eltűnik, hogy csak egyetlen pontban érintse, ne az egész képet
				apple_starty = -40		#amint hozzáérünk eltűnik, hogy csak egyetlen pontban érintse, ne az egész képet
				
		if wall_startx + wall_width < 0:					#ha eltűnik a fal a képernyőről
			wall_startx = random.uniform(1200, 3000)
			wall_starty = display_height - wall_height
		
		if y + hedgehog_height >= wall_starty:		#ha ütközünk a fallal
			if (x + hedgehog_width >= wall_startx and x + hedgehog_width <= wall_startx + wall_width) or (x >= wall_startx and x <= wall_startx + wall_width):
				crash()
				hedgehog_life -= 1
				if hedgehog_life == 0:		#ha elfogy az életünk
					pygame.mixer.music.pause()		#zene stop
					'''pygame.mixer.Sound.stop()		#többi hang stop'''
					restart_message()		#játék vége üzenet
					hedgehog_actual_score = 0		#pont ismét 0-tól indul
					actual_score_1000 = 0		#lenullázzuk a csengő hanghoz tartozó pontszámot
					hedgehog_life = 5		#újra 5 élet
					apple_counter = 0
				wall_startx = -60		#amint hozzáérünk eltűnik, hogy csak egyetlen pontban érintse, ne az egész képet
				wall_starty = -60		#amint hozzáérünk eltűnik, hogy csak egyetlen pontban érintse, ne az egész képet
				
		if qm_startx + qm_width < 0:		#ha eltűnik a kérdőjel a képernyőről
			qm_startx = random.uniform(3000, 5000)
			qm_starty = random.uniform(display_height * 0.4, display_height * 0.92)
			
		if x + hedgehog_width > qm_startx:		#ha ütközünk a kérdőjellel
			if y + hedgehog_height >= qm_starty and y + hedgehog_height <= qm_starty + qm_height or y < qm_starty + qm_height and y > qm_starty:
				if random_event_number == 1:
					hedgehog_life += random.randrange(-2, 3)		#-2-tól 2-ig bármennyi életet kaphatsz, szóval nyerhetsz és veszthetsz is vele, vagy semmi sem történik
				elif random_event_number == 2:
					apple_counter += random.randrange(-3, 4)	#-3-tól 3-ig bármennyi almát kaphatsz, szóval nyerhetsz és veszthetsz is vele, vagy semmi sem történik
				else:
					pass		#nem történik semmi
				if apple_counter < 0:		#apple counter számláló nem lehet negatív
					apple_counter = 0
				if apple_counter >= 10:
					hedgehog_life += 1		#ha 10 almát felszedünk kapunk egy új életet
					apple_counter = 0
				if hedgehog_life <= 0:		#ha elfogy az életünk
					pygame.mixer.music.pause()		#zene stop
					'''pygame.mixer.Sound.stop()		#többi hang stop'''
					restart_message()		#játék vége üzenet
					hedgehog_actual_score = 0		#pont ismét 0-tól indul
					actual_score_1000 = 0		#lenullázzuk a csengő hanghoz tartozó pontszámot
					hedgehog_life = 5		#újra 5 élet
					apple_counter = 0
				qm_startx = -50		#amint hozzáérünk eltűnik, hogy csak egyetlen pontban érintse, ne az egész képet
				qm_starty = -50		#amint hozzáérünk eltűnik, hogy csak egyetlen pontban érintse, ne az egész képet
				
		if hedgehog_actual_score >= 10000:			#előkerül a ház, ami a játék végét jelzi
			housex -= house_speed
			gameDisplay.blit(houseImg, (housex, housey))
			hedgehog_actual_score -= 1		#számláló leállítása
			actual_score_1000 -= 1		#csengő hang leállítása
			apple_startx = 2000		#alma eltűnik
			wall_startx = 2000		#fal eltűnik
			qm_startx = 2000		#kérdőjel eltűnik
			
		if x + hedgehog_width >= (housex + housew) / 4:		#ha elérjük az ajtót vége a játéknak, nyertünk
			gameDisplay.blit(hedgehogImg, (x,y))		#sün a ház elé kerül
			house_speed = 0		#megáll a ház
			bgx = 0		#megáll a háttér			#olyan, mintha a sün állna meg	
			end_message()		#játék vége üzenet
			'''gameDisplay.blit(hedgehogImg, (2000,y))'''
			
		pygame.display.update()		#képernyő frissítés
		clock.tick(60)		#játék sebessége
	
game_loop()
