from __future__ import print_function
import mlbgame
import datetime
import lxml.etree as etree
import time
  
#updated at 8pm

now = datetime.datetime.now()
today_year = now.year
today_month = now.month
today_day = now.day

OVERALL_GAME_SCORE_HOME = {
	1 : ' ',
	2 : ' ',
	3 : ' ',
	4 : ' ',
	5 : ' ',
	6 : ' ',
	7 : ' ',
	8 : ' ',
	9 : ' ',
}

OVERALL_GAME_SCORE_AWAY = {
	1 : ' ',
	2 : ' ',
	3 : ' ',
	4 : ' ',
	5 : ' ',
	6 : ' ',
	7 : ' ',
	8 : ' ',
	9 : ' ',
}


	
def display_LED() :
	#using OVER_GAME_SCORE, display the score on the LED board here. 
	global OVERALL_GAME_SCORE_AWAY
	global OVERALL_GAME_SCORE_HOME
	
	
	inning_num = 1
	for inning in OVERALL_GAME_SCORE_AWAY :
		print("inning: [" + str(inning_num) + "] " + OVERALL_GAME_SCORE_AWAY[inning_num] + " | " + OVERALL_GAME_SCORE_HOME[inning_num])
		inning_num += 1
	
	print("------------------------------------------------------------")
	
	#After updating, go to update_inning_score to see if we have some new scores
	update_inning_score()

def before_game() :
	
	game_info = mlbgame.day(today_year,today_month,today_day, 'Cubs', 'Braves')
	
	while(game_info[0].game_status == "PRE_GAME") :
		print("GAME STARTS AT: " + game_info[0].game_start_time)
		game_info = mlbgame.day(today_year,today_month,today_day, 'Cubs', 'Braves')
		time.sleep(600)
		game_info = mlbgame.day(today_year,today_month,today_day, 'Cubs', 'Braves')
		
def game_in_progress() :

	test_inning = 1
	if_update_scores = False
	
	display_LED()
	
	game_info = mlbgame.day(today_year,today_month,today_day, 'Cubs', 'Braves')
	curr_game_id = game_info[0].game_id
	
	while(game_info[0].game_status == "IN_PROGRESS") : 
		#need to get inning score
		data_game_score = mlbgame.data.get_box_score(curr_game_id) 
		parsed = etree.parse(data_game_score)
		root = parsed.getroot()
		linescore = root.find('linescore')
		results = dict()
		
		for info1 in linescore : 
			#print("checking " + str(test_inning) + " inning: " + str(info1.attrib['inning']))
			try :
				topScore = info1.attrib['away']
				bottomScore = info1.attrib['home']
			except :
				topScore = info1.attrib['away']
				bottomScore = " "

			#if the inning score doesnt match with the current score, then change it
			#print("Score MLB Gave me: " + topScore + bottomScore)
			if (OVERALL_GAME_SCORE_AWAY[test_inning] != topScore) or (OVERALL_GAME_SCORE_HOME[test_inning] != bottomScore) :
				#print("New Score Update. Old Scores: [" + OVERALL_GAME_SCORE_AWAY[test_inning] + "][" + OVERALL_GAME_SCORE_HOME[test_inning] + "]")
				OVERALL_GAME_SCORE_AWAY[test_inning] = str(topScore)
				OVERALL_GAME_SCORE_HOME[test_inning] = str(bottomScore)
				if_update_scores = True
				
			
			test_inning += 1 #test next inning
			
		if if_update_scores : #if the score has been updated, change the LED
			display_LED()
			
		
		if_update_scores = False
		test_inning = 1;
		time.sleep(30) #update scores every 30s
		game_info = mlbgame.day(today_year,today_month,today_day, 'Cubs', 'Braves')

def post_game() :

	game_info = mlbgame.day(today_year,today_month,today_day, 'Cubs', 'Braves')
	
	score_home = 0
	score_away = 0
	
	if(game_info[0].game_status == "FINAL") : #calculate the total score
		
		inning = 1
		for inning_score in OVERALL_GAME_SCORE_AWAY : 
			score_away = score_away + int(OVERALL_GAME_SCORE_AWAY[inning])
			inning += 1
		
		inning = 1
		
		for inning_score in OVERALL_GAME_SCORE_HOME : 
			if OVERALL_GAME_SCORE_HOME[inning] != 'x' :
				score_home = score_home + int(OVERALL_GAME_SCORE_HOME[inning])
				inning += 1
				
				
	while(game_info[0].game_status == "FINAL") :
		print("FINAL SCORE: [" + str(score_home) + "][" + str(score_away))
		
		time.sleep(600)
		game_info = mlbgame.day(today_year,today_month,today_day, 'Cubs', 'Braves')

def no_game() :
	print("Off day")
	time.sleep(300)
	
def update_inning_score() :
	
	#declare global variables
	global OVERALL_GAME_SCORE_AWAY
	global OVERALL_GAME_SCORE_HOME

	display_LED() #update LED

	game_info = mlbgame.day(today_year,today_month,today_day, 'Astros', 'Astros')
	curr_game_id = game_info[0].game_id


	while(game_info[0].game_status == "PRE_GAME") :
		print("GAME STARTS AT: " + game_info[0].game_start_time)
		game_info = mlbgame.day(today_year,today_month,today_day, 'Astros', 'Astros')
		time.sleep(600)
		game_info = mlbgame.day(today_year,today_month,today_day, 'Astros', 'Astros')

	
	
	
	test_inning = 1
	if_update_scores = False
	
	
	while(game_info[0].game_status == "IN_PROGRESS") : 
		#need to get inning score
		data_game_score = mlbgame.data.get_box_score(curr_game_id) 
		parsed = etree.parse(data_game_score)
		root = parsed.getroot()
		linescore = root.find('linescore')
		results = dict()
		
		for info1 in linescore : 
			#print("checking " + str(test_inning) + " inning: " + str(info1.attrib['inning']))
			try :
				topScore = info1.attrib['away']
				bottomScore = info1.attrib['home']
			except :
				topScore = info1.attrib['away']
				bottomScore = " "

			#if the inning score doesnt match with the current score, then change it
			#print("Score MLB Gave me: " + topScore + bottomScore)
			if (OVERALL_GAME_SCORE_AWAY[test_inning] != topScore) or (OVERALL_GAME_SCORE_HOME[test_inning] != bottomScore) :
				#print("New Score Update. Old Scores: [" + OVERALL_GAME_SCORE_AWAY[test_inning] + "][" + OVERALL_GAME_SCORE_HOME[test_inning] + "]")
				OVERALL_GAME_SCORE_AWAY[test_inning] = str(topScore)
				OVERALL_GAME_SCORE_HOME[test_inning] = str(bottomScore)
				if_update_scores = True
				
			
			test_inning += 1 #test next inning
			
		if if_update_scores : #if the score has been updated, change the LED
			display_LED()
			
		
		if_update_scores = False
		test_inning = 1;
		time.sleep(60) #update scores every min
		game_info = mlbgame.day(today_year,today_month,today_day, 'Astros', 'Astros')
		
	game_info = mlbgame.day(today_year,today_month,today_day, 'Astros', 'Astros')
	
	score_home = 0
	score_away = 0
	
	if(game_info[0].game_status == "FINAL") : #calculate the total score
		
		inning = 1
		for inning_score in OVERALL_GAME_SCORE_AWAY : 
			score_away = score_away + int(OVERALL_GAME_SCORE_AWAY[inning])
			inning += 1
		
		inning = 1
		
		for inning_score in OVERALL_GAME_SCORE_HOME : 
			if OVERALL_GAME_SCORE_HOME[inning] != 'x' :
				score_home = score_home + int(OVERALL_GAME_SCORE_HOME[inning])
				inning += 1
				
				
	while(game_info[0].game_status == "FINAL") :
		print("FINAL SCORE: [" + str(score_home) + "][" + str(score_away))
		
		time.sleep(600)
		game_info = mlbgame.day(today_year,today_month,today_day, 'Astros', 'Astros')

	
	new_game_status()	
	
def new_game_status() : 
	
	while(True) :
		game_info = mlbgame.day(today_year,today_month,today_day, 'Cubs', 'Braves')
		
		if not game_info : no_game() #if there are no games today
		
		global OVERALL_GAME_SCORE_AWAY
		global OVERALL_GAME_SCORE_HOME
		
		#reset the total score. 
		inning = 1
		for inning_score in OVERALL_GAME_SCORE_AWAY : 
			OVERALL_GAME_SCORE_AWAY[inning] = ' '
			inning += 1
			
		inning = 1
		for inning_score in OVERALL_GAME_SCORE_HOME : 
			OVERALL_GAME_SCORE_HOME[inning] = ' '
			inning += 1

		if(game_info[0].game_status == "PRE_GAME") : before_game()
		elif(game_info[0].game_status == "IN_PROGRESS") :game_in_progress()
		elif(game_info[0].game_status == "FINAL" ) : post_game()
		else : print("Can't understand status")
		

	
def test() :

	#game_info = mlbgame.day(today_year,today_month,today_day, 'Astros', 'Astros')
	#curr_game_id = game_info[0].game_id
	
	
	
	while(True) :
		status_of_game = mlbgame.overview("2018_04_12_sfnmlb_sdnmlb_1")
		curr_balls = str(status_of_game.balls)
		curr_strikes = str(status_of_game.strikes)
		curr_outs = str(status_of_game.outs)
		curr_inning = str(status_of_game.inning)
		print("current info: ["+curr_balls+"]["+curr_strikes+"]["+curr_outs+"]:[" +  curr_inning + "]")
		time.sleep(10)
		
	
	
def main():
	
	new_game_status()
	
	#day_game_info = mlbgame.day(today_year,today_month,today_day, 'Astros', 'Astros')
	
	#Here we figure out how many games there are gonna be today
	#for game in day_game_info :  
		#print ("THIS IS OUR GAME ID: " + game_info.game_id)
		#print ("THIS IS WHEN THE GAME STARTS: " + game_info.game_start_time)
		#new_game_status (game)
	
	#print("NO GAME TODAY")
	
main()

