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

OVERALL_GAME_SCORE_HOME = dict()

OVERALL_GAME_SCORE_AWAY = dict()

CURRENT_BAG_STATUS = {
	1 : 'NoRunner',
	2 : 'NoRunner',
	3 : 'NoRunner'
}

CURR_INNING_INFO = {
	'num' 	 : '1',
	'status' : 'TOP'
}

CURR_BATTING_STATUS = {
	'Strikes' : '0',
	'Balls'   : '0'
}

CURRENT_OUTS = '0'

CURRENT_TEAM_HOME_STATS = {
	'Runs'    : '0',
	'Hits' 	  : '0',
	'Errors'  : '0'
}

CURRENT_TEAM_AWAY_STATS = {
	'Runs'    : '0',
	'Hits' 	  : '0',
	'Errors'  : '0'
}



def display_LED_update_batter() :
	print("CurrBatterUp: Strikes[" + CURR_BATTING_STATUS['Strikes'] + "] Balls[" + CURR_BATTING_STATUS['Balls'] + "] Outs[" + CURRENT_OUTS + "]")

def display_LED_update_inning() :
	print("Current Inning: [" + CURR_INNING_INFO['status'] + "][" + CURR_INNING_INFO['num'] + "]")

def display_LED() :
	print("Altering the LED")

	#using OVER_GAME_SCORE, display the score on the LED board here. 
	global OVERALL_GAME_SCORE_AWAY
	global OVERALL_GAME_SCORE_HOME
	
	
	inning_num = 1
	for inning in OVERALL_GAME_SCORE_AWAY :
		print("inning: [" + str(inning_num) + "] [" + OVERALL_GAME_SCORE_AWAY[inning_num] + "] | [" + OVERALL_GAME_SCORE_HOME[inning_num] + "]")
		inning_num += 1
	
	print("------------------------------------------------------------")
	
	#After updating, go to update_inning_score to see if we have some new scores

def curr_batter_status() :

	
	game_info = mlbgame.day(today_year,today_month,today_day, 'Astros', 'Rangers')
	curr_game_id = game_info[0].game_id
	
	CURR_BATTING_STATUS[Balls] = str(status_of_game.balls)
	CURR_BATTING_STATUS[Strikes] = str(status_of_game.strikes)
	CURR_OUTS = status_of_game.outs

	print("current info: ["+curr_balls+"]["+curr_strikes+"]["+curr_outs+"]:[" +  curr_inning + "]")




def before_game() :
	
	print("Before the game")

	#reset the total score. 
	inning = 1
	for inning_score in OVERALL_GAME_SCORE_AWAY : 
		OVERALL_GAME_SCORE_AWAY[inning] = ' '
		inning += 1
		
	inning = 1
	for inning_score in OVERALL_GAME_SCORE_HOME : 
		OVERALL_GAME_SCORE_HOME[inning] = ' '
		inning += 1

	game_info = mlbgame.day(today_year,today_month,today_day, 'Astros', 'Rangers')
	
	while(game_info[0].game_status == "PRE_GAME") :
		print("GAME STARTS AT: " + game_info[0].game_start_time)
		game_info = mlbgame.day(today_year,today_month,today_day, 'Astros', 'Rangers')
		time.sleep(600)
		game_info = mlbgame.day(today_year,today_month,today_day, 'Astros', 'Rangers')

def game_in_progress() :

	print("Game is in Progress")

	if_update_scores = False
	update_inning_status = False
	update_batter_status = False
	test_inning = 1
	global CURRENT_OUTS
	global CURR_BATTING_STATUS
	global CURR_INNING_INFO

	game_info = mlbgame.day(today_year,today_month,today_day, 'Astros', 'Rangers')
	curr_game_id = game_info[0].game_id
	
	while(game_info[0].game_status == "IN_PROGRESS") : 
		
		status_of_game = mlbgame.overview(curr_game_id)

		#####################################################
		#####################################################
		#Check status of batter (balls and strikes)

		#print("CurrBatter: Strikes[" + str(status_of_game.strikes) + "] Balls[" + str(status_of_game.balls) + "] Outs[" + str(status_of_game.outs) + "]")

		if(CURR_BATTING_STATUS['Strikes'] != str(status_of_game.strikes)) : #Strikes
			CURR_BATTING_STATUS['Strikes'] = str(status_of_game.strikes)
			#print("NEW Strikes: " + CURR_BATTING_STATUS['Strikes'] + " (" + str(status_of_game.strikes) + ")")
			update_batter_status = True

		if(CURR_BATTING_STATUS['Balls'] != str(status_of_game.balls)) : #Balls 
			CURR_BATTING_STATUS['Balls'] = str(status_of_game.balls)
			#print("NEW BALLS: " + CURR_BATTING_STATUS['Balls'] + " (" + str(status_of_game.balls) + ")")
			update_batter_status = True
		
		if(CURRENT_OUTS != str(status_of_game.outs)) :
			CURRENT_OUTS = str(status_of_game.outs)
			#print("NEW Outs: " + CURRENT_OUTS + " (" + str(status_of_game.outs) + ")")
			update_batter_status = True

		if(update_batter_status) : 
			display_LED_update_batter()
			update_batter_status = False

		#####################################################
		#####################################################
		#Check status of inning (balls and strikes)

		if(CURR_INNING_INFO['num'] != str(status_of_game.inning)) : #current inning
			CURR_INNING_INFO['num'] = str(status_of_game.inning)
			update_inning_status = True

		if(CURR_INNING_INFO['status'] != str(status_of_game.inning_state)) : #Check if end of a halfinning
			CURR_INNING_INFO['status'] = str(status_of_game.inning_state)

			#print("inning status chagne")
			#if status of inning changes, reset batting status since the inning is over
			CURR_BATTING_STATUS['Strikes'] = '0'
			CURR_BATTING_STATUS['Balls'] = '0'
			CURRENT_OUTS = '0'

			display_LED_update_batter()

			update_inning_status = True
		
		if(update_inning_status) : 
			display_LED_update_inning()
			update_inning_status = False

		#####################################################
		#####################################################

		#need to get inning score
		data_game_score = mlbgame.data.get_box_score(curr_game_id) 
		parsed = etree.parse(data_game_score)
		root = parsed.getroot()
		linescore = root.find('linescore')
		#results = dict()
		
		for info1 in linescore : 

			#add another inning if its a new one
			if test_inning not in OVERALL_GAME_SCORE_AWAY : #if its a new inning, only home would be populated. 
				OVERALL_GAME_SCORE_AWAY[test_inning] = '-'
				OVERALL_GAME_SCORE_HOME[test_inning] = ' '
				if_update_scores = True #update LED since we added new inning

			try :
				topScore = info1.attrib['away']
				bottomScore = info1.attrib['home']
			except :
				topScore = info1.attrib['away']
				bottomScore = ""

			#if the inning score doesnt match with the current score, then change it
			#print("Score MLB Gave me: " + topScore + bottomScore)
			if (OVERALL_GAME_SCORE_AWAY[test_inning] != topScore) :
				#print("New Score Update. Old Scores: [" + OVERALL_GAME_SCORE_AWAY[test_inning] + "][" + OVERALL_GAME_SCORE_HOME[test_inning] + "]")
				
				if(topScore) : #could be empty, dont change
					OVERALL_GAME_SCORE_AWAY[test_inning] = str(topScore)
					if_update_scores = True

			if  (OVERALL_GAME_SCORE_HOME[test_inning] != bottomScore) :
				if(bottomScore) :  #could be emtpy, dont change 
					OVERALL_GAME_SCORE_HOME[test_inning] = str(bottomScore)
					if_update_scores = True
					
				
			
			test_inning += 1 #test next inning
			
		if if_update_scores : #if the score has been updated, change the LED
			display_LED()
			
		
		if_update_scores = False
		test_inning = 1;
		time.sleep(5) #update scores every 30s
		game_info = mlbgame.day(today_year,today_month,today_day, 'Astros', 'Rangers')
		
def post_game() :

	print("In the post_game state: ")

	game_info = mlbgame.day(today_year,today_month,today_day, 'Astros', 'Rangers')
	
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
		print("FINAL SCORE: [" + str(score_home) + "][" + str(score_away) + "]")
		
		time.sleep(600)
		game_info = mlbgame.day(today_year,today_month,today_day, 'Astros', 'Rangers')

def no_game() :
	print("Off day")
	time.sleep(1800)
	
def update_inning_score() :
	
	#declare global variables
	global OVERALL_GAME_SCORE_AWAY
	global OVERALL_GAME_SCORE_HOME

	display_LED() #update LED

	game_info = mlbgame.day(today_year,today_month,today_day, 'Astros', 'Rangers')
	curr_game_id = game_info[0].game_id


	while(game_info[0].game_status == "PRE_GAME") :
		print("GAME STARTS AT: " + game_info[0].game_start_time)
		game_info = mlbgame.day(today_year,today_month,today_day, 'Astros', 'Rangers')
		time.sleep(600)
		game_info = mlbgame.day(today_year,today_month,today_day, 'Astros', 'Rangers')

	
	
	
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
		game_info = mlbgame.day(today_year,today_month,today_day, 'Astros', 'Rangers')
		
	game_info = mlbgame.day(today_year,today_month,today_day, 'Astros', 'Rangers')
	
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
		game_info = mlbgame.day(today_year,today_month,today_day, 'Astros', 'Rangers')

	
	new_game_status()	
	
def new_game_status() : 
	
	print("determining where to start: ")

	while(True) :
		game_info = mlbgame.day(today_year,today_month,today_day, 'Astros', 'Rangers')
		
		if not game_info : no_game() #if there are no games today
		
		global OVERALL_GAME_SCORE_AWAY
		global OVERALL_GAME_SCORE_HOME

		if(game_info[0].game_status == "PRE_GAME") : before_game()
		elif(game_info[0].game_status == "IN_PROGRESS") :game_in_progress()
		elif(game_info[0].game_status == "FINAL" ) : post_game()
		else : print("Can't understand status")
		
def test() :

	#game_info = mlbgame.day(today_year,today_month,today_day, 'cinmlb', 'Astros')
	#curr_game_id = game_info[0].game_id
	print("test")

	if_update_scores = False
	test_inning = 1
	
	game_info = mlbgame.day(today_year,today_month,today_day, 'Cubs', 'Braves')
	curr_game_id = game_info[0].game_id
	
	while(game_info[0].game_status == "IN_PROGRESS") : 
		
		#need to get inning score
		data_game_score = mlbgame.data.get_box_score(curr_game_id) 
		parsed = etree.parse(data_game_score)
		root = parsed.getroot()
		linescore = root.find('linescore')
		#results = dict()
		
		for info1 in linescore : 

			#add another inning if its a new one
			if test_inning not in OVERALL_GAME_SCORE_AWAY : #if its a new inning, only home would be populated. 
				print("NEW INNING")
				OVERALL_GAME_SCORE_AWAY[test_inning] = '-'
				OVERALL_GAME_SCORE_HOME[test_inning] = ' '
				if_update_scores = True #update LED since we added new inning

			try :
				topScore = info1.attrib['away']
				bottomScore = info1.attrib['home']
			except :
				topScore = info1.attrib['away']
				bottomScore = ""

			#if the inning score doesnt match with the current score, then change it
			#print("Score MLB Gave me: " + topScore + bottomScore)
			if (OVERALL_GAME_SCORE_AWAY[test_inning] != topScore) :
				#print("New Score Update. Old Scores: [" + OVERALL_GAME_SCORE_AWAY[test_inning] + "][" + OVERALL_GAME_SCORE_HOME[test_inning] + "]")
				
				if(topScore) : #could be empty, dont change
					print("TopScore: |" + topScore + "|" + OVERALL_GAME_SCORE_AWAY[test_inning])
					OVERALL_GAME_SCORE_AWAY[test_inning] = str(topScore)
					if_update_scores = True

			if  (OVERALL_GAME_SCORE_HOME[test_inning] != bottomScore) :
				if(bottomScore) :  #could be emtpy, dont change 
					print("bottomScore: |" + bottomScore + "|" + OVERALL_GAME_SCORE_AWAY[test_inning])
					if_update_scores = True
					OVERALL_GAME_SCORE_HOME[test_inning] = str(bottomScore)
				
			
			test_inning += 1 #test next inning
			
		if if_update_scores : #if the score has been updated, change the LED
			display_LED()
			
		
		if_update_scores = False
		test_inning = 1;
		time.sleep(5) #update scores every 30s
		game_info = mlbgame.day(today_year,today_month,today_day, 'Cubs', 'Braves')
		
def main():
	
	print("LED_board: Starts")

	new_game_status()
	
main()

