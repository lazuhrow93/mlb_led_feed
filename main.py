from __future__ import print_function
from Team_Abrev import *
import mlbgame
import datetime
import lxml.etree as etree
import time
from Display_Board import *
import random
#updated at 8pm

now = datetime.datetime.now()
today_year = now.year
today_month = now.month
today_day = now.day

debug = 0

OVERALL_GAME_SCORE_HOME = dict()

OVERALL_GAME_SCORE_AWAY = dict()

CURRENT_BAG_STATUS = {
	1 : 0,
	2 : 0,
	3 : 0
}

CURR_INNING_INFO = {
	'num' 	 : '1',
	'status' : 'TOP'
}

CURR_BATTING_STATUS = {
	'Strikes' : '0',
	'Balls'   : '0'
}

CURRENT_OUTS = 0

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

#putting these the same will return game of the day for that team
HOME_TEAM = 'Astros' 
AWAY_TEAM = 'Astros'

def display_LED_update_baseRunners(first,second,third) :
	draw_base_runners(first,second,third)


def display_LED_update_batter() :

	global CURRENT_OUTS
	if(debug) : print("CurrBatterUp: Strikes[" + CURR_BATTING_STATUS['Strikes'] + "] Balls[" + CURR_BATTING_STATUS['Balls'] + "] Outs[" + str(CURRENT_OUTS) + "]")

	draw_new_balls_strikes(CURR_BATTING_STATUS['Balls'], CURR_BATTING_STATUS['Strikes'])
	draw_new_outs(CURRENT_OUTS)

def display_LED_update_inning() :
	if(debug) : print("Current Inning: [" + CURR_INNING_INFO['status'] + "][" + CURR_INNING_INFO['num'] + "]")
	draw_inning_status(CURR_INNING_INFO['status'], CURR_INNING_INFO['num'] )

def update_score_LED() :
	if(debug) : print("Altering the LED: Scores")

	#using OVER_GAME_SCORE, display the score on the LED board here. 
	global OVERALL_GAME_SCORE_AWAY
	global OVERALL_GAME_SCORE_HOME
	global CURR_INNING_INFO

	
	inning_num = 1
	for inning in OVERALL_GAME_SCORE_AWAY :
		draw_new_inning_score(inning_num, OVERALL_GAME_SCORE_AWAY[inning_num], 'AWAY')

		#if its the bottom of the inning and home team has not scored, put a '-'
		#if(debug) : print("status, score:" + CURR_INNING_INFO['status'] + ", " + OVERALL_GAME_SCORE_HOME[inning_num])
		if(CURR_INNING_INFO['status'] == 'Bottom' and OVERALL_GAME_SCORE_HOME[inning_num] == '') :
			home_score = '-' 
		else : home_score = OVERALL_GAME_SCORE_HOME[inning_num]

		draw_new_inning_score(inning_num, home_score, 'HOME')

		if(debug) : print("inning: [" + str(inning_num) + "] [" + OVERALL_GAME_SCORE_AWAY[inning_num] + "] | [" + OVERALL_GAME_SCORE_HOME[inning_num] + "]")
		inning_num += 1
	
	if(debug) : print("------------------------------------------------------------")
	
	#After updating, go to update_inning_score to see if we have some new scores

def update_RHE_LED() :
	global CURRENT_TEAM_HOME_STATS 
	global CURRENT_TEAM_AWAY_STATS

	draw_new_RHE(CURRENT_TEAM_AWAY_STATS['Runs'], CURRENT_TEAM_AWAY_STATS['Hits'], CURRENT_TEAM_AWAY_STATS['Errors'], 'AWAY')

	#if(debug) : print("HOME: " + CURRENT_TEAM_HOME_STATS['Runs'] + CURRENT_TEAM_HOME_STATS['Hits'] + CURRENT_TEAM_HOME_STATS['Errors'])
	draw_new_RHE(CURRENT_TEAM_HOME_STATS['Runs'], CURRENT_TEAM_HOME_STATS['Hits'], CURRENT_TEAM_HOME_STATS['Errors'], 'HOME')

def check_bases_status(status_of_game) :
	#status_of_game = mlbgame.overview(curr_game_id)

	#runner_on_1st = status_of_game.runner_on_1b
	#runner_on_2nd = status_of_game.runner_on_2b
	#runner_on_3rd = status_of_game.runner_on_3b

	try :
		runner_on_1st = status_of_game.runner_on_1b
	except :
		runner_on_1st = 0

	try :
		runner_on_2nd = status_of_game.runner_on_2b
	except :
		runner_on_2nd = 0
	
	try : 
		runner_on_3rd = status_of_game.runner_on_3b
	except :
		runner_on_3rd = 0

	if(debug) : 
		if(runner_on_1st) : print("1st occupied")
		if(runner_on_2nd) : print("2nd occupied")
		if(runner_on_3rd) : print("3rd occupied")

	updateLED = False

	if((CURRENT_BAG_STATUS[1] != runner_on_1st) or (CURRENT_BAG_STATUS[2] != runner_on_2nd) or (CURRENT_BAG_STATUS[3] != runner_on_3rd)) :
		updateLED = True
		CURRENT_BAG_STATUS[1] = runner_on_1st
		CURRENT_BAG_STATUS[2] = runner_on_2nd
		CURRENT_BAG_STATUS[3] = runner_on_3rd


	display_LED_update_baseRunners(runner_on_1st, runner_on_2nd, runner_on_3rd)

def check_batter_status(status_of_game) :

	update_batter_status = False

	global CURRENT_OUTS
	global CURR_BATTING_STATUS

	if(CURR_BATTING_STATUS['Strikes'] != str(status_of_game.strikes)) : #Strikes
		CURR_BATTING_STATUS['Strikes'] = str(status_of_game.strikes)
		#if(debug) : print("NEW Strikes: " + CURR_BATTING_STATUS['Strikes'] + " (" + str(status_of_game.strikes) + ")")
		update_batter_status = True

	if(CURR_BATTING_STATUS['Balls'] != str(status_of_game.balls)) : #Balls 
		CURR_BATTING_STATUS['Balls'] = str(status_of_game.balls)
		#if(debug) : print("NEW BALLS: " + CURR_BATTING_STATUS['Balls'] + " (" + str(status_of_game.balls) + ")")
		update_batter_status = True
	
	if(str(CURRENT_OUTS) != str(status_of_game.outs)) :
		CURRENT_OUTS = int(status_of_game.outs)
		#if(debug) : print("NEW Outs: " + CURRENT_OUTS + " (" + str(status_of_game.outs) + ")")
		update_batter_status = True

	if(update_batter_status) : 
		display_LED_update_batter()
		update_batter_status = False

def check_inning_status(status_of_game) :

	global CURR_INNING_INFO
	global CURR_BATTING_STATUS
	global CURRENT_OUTS
	update_inning_status = False

	if(CURR_INNING_INFO['num'] != str(status_of_game.inning)) : #current inning
			CURR_INNING_INFO['num'] = str(status_of_game.inning)
			update_inning_status = True

	if(CURR_INNING_INFO['status'] != str(status_of_game.inning_state)) : #Check if end or mid of a halfinning
		CURR_INNING_INFO['status'] = str(status_of_game.inning_state)

		#if(debug) : print("inning status chagne")
		#if status of inning changes, reset batting status since the inning is over, and bag status
		CURR_BATTING_STATUS['Strikes'] = '0'
		CURR_BATTING_STATUS['Balls'] = '0'
		CURRENT_OUTS = 0
		CURRENT_BAG_STATUS[1] = 0
		CURRENT_BAG_STATUS[2] = 0
		CURRENT_BAG_STATUS[3] = 0

		update_inning_status = True

		display_LED_update_batter() #restart batting status
	
	if(update_inning_status) : #update the inning status 
		display_LED_update_inning()
		update_inning_status = False

def check_inning_scores(curr_game_id) :
	#need to get inning score
	if_update_scores = False
	test_inning = 1
	data_game_score = mlbgame.data.get_box_score(curr_game_id) 
	parsed = etree.parse(data_game_score)
	root = parsed.getroot()
	linescore = root.find('linescore')
	#results = dict()
	
	for inningInfo in linescore : 

		#add another inning if its a new one
		if test_inning not in OVERALL_GAME_SCORE_AWAY : #if its a new inning, only AWAY would be populated. 
			OVERALL_GAME_SCORE_AWAY[test_inning] = '-'
			OVERALL_GAME_SCORE_HOME[test_inning] = ' '
			if_update_scores = True #update LED since we added new inning

		try :
			topScore = inningInfo.attrib['away']
			bottomScore = inningInfo.attrib['home']
		except :#Since if its a new inning, home attrib doesnt exist
			topScore = inningInfo.attrib['away']
			bottomScore = ""

		#if the inning score doesnt match with the current score, then change it
		#if(debug) : print("Score MLB Gave me: " + topScore + bottomScore)
		if (OVERALL_GAME_SCORE_AWAY[test_inning] != topScore) :
			#if(debug) : print("New Score Update. Old Scores: [" + OVERALL_GAME_SCORE_AWAY[test_inning] + "][" + OVERALL_GAME_SCORE_HOME[test_inning] + "]")
			
			if(topScore) : #could be empty, dont change
				OVERALL_GAME_SCORE_AWAY[test_inning] = str(topScore)
				if_update_scores = True

		if  (OVERALL_GAME_SCORE_HOME[test_inning] != bottomScore) :
			if(bottomScore) :  #could be emtpy, dont change 
				OVERALL_GAME_SCORE_HOME[test_inning] = str(bottomScore)
				if_update_scores = True
				
			
		
		test_inning += 1 #test next inning

	if if_update_scores : #if the score has been updated, change the LED
		update_score_LED()

	if_update_scores = False
	test_inning = 1;

def check_RHE_status(status_of_game) :
	global CURRENT_TEAM_HOME_STATS 
	global CURRENT_TEAM_AWAY_STATS

	newRHE = False

	if(CURRENT_TEAM_AWAY_STATS['Runs'] != status_of_game.away_team_runs) :
		CURRENT_TEAM_AWAY_STATS['Runs'] = str(status_of_game.away_team_runs)
		newRHE = True

	if(CURRENT_TEAM_AWAY_STATS['Hits'] != status_of_game.away_team_hits) :
		CURRENT_TEAM_AWAY_STATS['Hits'] = str(status_of_game.away_team_hits)
		newRHE = True

	if(CURRENT_TEAM_AWAY_STATS['Errors'] != status_of_game.away_team_errors) :
		CURRENT_TEAM_AWAY_STATS['Errors'] = str(status_of_game.away_team_errors)
		newRHE = True

	if(CURRENT_TEAM_HOME_STATS['Runs'] != status_of_game.home_team_runs) :
		CURRENT_TEAM_HOME_STATS['Runs'] = str(status_of_game.home_team_runs)
		newRHE = True

	if(CURRENT_TEAM_HOME_STATS['Hits'] != status_of_game.home_team_hits) :
		CURRENT_TEAM_HOME_STATS['Hits'] = str(status_of_game.home_team_hits)
		newRHE = True

	if(CURRENT_TEAM_HOME_STATS['Errors'] != status_of_game.home_team_errors) :
		CURRENT_TEAM_HOME_STATS['Errors'] = str(status_of_game.home_team_errors)
		newRHE = True

	if(newRHE == True) :
		update_RHE_LED()
		
def curr_batter_status() :

	
	game_info = mlbgame.day(today_year,today_month,today_day, HOME_TEAM, AWAY_TEAM)
	curr_game_id = game_info[0].game_id
	
	CURR_BATTING_STATUS[Balls] = str(status_of_game.balls)
	CURR_BATTING_STATUS[Strikes] = str(status_of_game.strikes)
	CURR_OUTS = status_of_game.outs

	if(debug) : print("current info: ["+curr_balls+"]["+curr_strikes+"]["+curr_outs+"]:[" +  curr_inning + "]")

def before_game() :
	
	if(debug) : print("Before the game")
	
	#reset the total score. 
	inning = 1
	for inning_score in OVERALL_GAME_SCORE_AWAY : 
		OVERALL_GAME_SCORE_AWAY[inning] = ' '
		inning += 1
		
	inning = 1
	for inning_score in OVERALL_GAME_SCORE_HOME : 
		OVERALL_GAME_SCORE_HOME[inning] = ' '
		inning += 1

	game_info = mlbgame.day(today_year,today_month,today_day, HOME_TEAM, AWAY_TEAM)
	
	
	already_displayed = False #so we dont have to keep refreshing the matrix
	while(game_info[0].game_status == "PRE_GAME") :

		#display pregame message on LED board
		if(not already_displayed) : 
			init_pre_game_board(game_info[0].game_start_time) #turn on board to display start time
			already_displayed = True
			if(debug) : print("1st time if(debug) : printing")

		if(debug) : print("GAME STARTS AT: " + game_info[0].game_start_time)
		game_info = mlbgame.day(today_year,today_month,today_day, HOME_TEAM, AWAY_TEAM)
		time.sleep(30)

	#Game is either starting/in_progress, init the board with team names, inning numbers, and "R H E"
	init_board(team_abrev[game_info[0].home_team], team_abrev[game_info[0].away_team])

def game_in_progress() :

	if(debug) : print("Game is in Progress")

	
	game_info = mlbgame.day(today_year,today_month,today_day, HOME_TEAM, AWAY_TEAM)
	curr_game_id = game_info[0].game_id
	global CURR_INNING_INFO

	status_of_game = mlbgame.overview(curr_game_id)
	#if(debug) : print("status: " + status_of_game.status)
	while(status_of_game.status == "In Progress") : #game_info[0].game_status == IN_PROGRESS
		
		#status_of_game = mlbgame.overview(curr_game_id)

		#####################################################
		#####################################################
		#Check status of batter (balls and strikes)
		check_batter_status(status_of_game)

		#####################################################
		#####################################################
		#check if anyones one base
		check_bases_status(status_of_game)

		#####################################################
		#####################################################
		#Check status of inning (balls and strikes)
		check_inning_status(status_of_game)

		#####################################################
		#####################################################
		#check the current inning scores
		check_inning_scores(curr_game_id)

		#####################################################
		#####################################################
		check_RHE_status(status_of_game)

		#hold the updates until "MID or END of inning" is over
		midOrEnd = str(status_of_game.inning_state)
		while(midOrEnd == 'Middle' or midOrEnd == 'End') :
			#if(debug) : print("mid or end of inning")
			#time.sleep(10)
			status_of_game = mlbgame.overview(curr_game_id)
			midOrEnd = str(status_of_game.inning_state)

		#time.sleep(5) #update scores every 30s
		#game_info = mlbgame.day(today_year,today_month,today_day, HOME_TEAM, AWAY_TEAM)
		status_of_game = mlbgame.overview(curr_game_id)


def post_game() :
	game_info = mlbgame.day(today_year,today_month,today_day, HOME_TEAM, AWAY_TEAM)
	curr_game_id = game_info[0].game_id
	status_of_game = mlbgame.overview(curr_game_id)


	if(debug) : print("In the post_game state: ")

	game_info = mlbgame.day(today_year,today_month,today_day, HOME_TEAM, AWAY_TEAM)
	
	while(game_info[0].game_status == "FINAL") :
		if(debug) : print("FINAL SCORE: [" + str(status_of_game.home_team_runs) + "][" + str(status_of_game.away_team_runs) + "]")
		init_post_game_board(str(status_of_game.home_team_runs), str(status_of_game.away_team_runs), team_abrev[status_of_game.home_team_name], team_abrev[status_of_game.away_team_name])
		time.sleep(600)
		game_info = mlbgame.day(today_year,today_month,today_day, HOME_TEAM, AWAY_TEAM)

def no_game() :
	if(debug) : print("Off day")
	time.sleep(1800)
	
def update_inning_score() :
	
	#declare global variables
	global OVERALL_GAME_SCORE_AWAY
	global OVERALL_GAME_SCORE_HOME

	display_LED() #update LED

	game_info = mlbgame.day(today_year,today_month,today_day, HOME_TEAM, AWAY_TEAM)
	curr_game_id = game_info[0].game_id


	while(game_info[0].game_status == "PRE_GAME") :
		if(debug) : print("GAME STARTS AT: " + game_info[0].game_start_time)
		game_info = mlbgame.day(today_year,today_month,today_day, HOME_TEAM, AWAY_TEAM)
		time.sleep(600)
		game_info = mlbgame.day(today_year,today_month,today_day, HOME_TEAM, AWAY_TEAM)

	
	
	
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
		game_info = mlbgame.day(today_year,today_month,today_day, HOME_TEAM, AWAY_TEAM)
		
	game_info = mlbgame.day(today_year,today_month,today_day, HOME_TEAM, AWAY_TEAM)
	
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
		if(debug) : print("FINAL SCORE: [" + str(score_home) + "][" + str(score_away))
		
		time.sleep(600)
		game_info = mlbgame.day(today_year,today_month,today_day, HOME_TEAM, AWAY_TEAM)

	
	new_game_status()	
	
def new_game_status() : 
	
	if(debug) : print("determining where to start: ")

	while(True) :
		game_info = mlbgame.day(today_year,today_month,today_day, HOME_TEAM, AWAY_TEAM)
		
		if not game_info : no_game() #if there are no games today
		
		global OVERALL_GAME_SCORE_AWAY
		global OVERALL_GAME_SCORE_HOME

		if(game_info[0].game_status == "PRE_GAME") : before_game()
		elif(game_info[0].game_status == "IN_PROGRESS") :game_in_progress()
		elif(game_info[0].game_status == "FINAL" ) : post_game()
		else : 
			if(debug) : print("Can't understand status")
		
def test() :

	#game_info = mlbgame.day(today_year,today_month,today_day, 'cinmlb', HOME_TEAM)
	#curr_game_id = game_info[0].game_id
	if(debug) : print("test")

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
				if(debug) : print("NEW INNING")
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
			#if(debug) : print("Score MLB Gave me: " + topScore + bottomScore)
			if (OVERALL_GAME_SCORE_AWAY[test_inning] != topScore) :
				#if(debug) : print("New Score Update. Old Scores: [" + OVERALL_GAME_SCORE_AWAY[test_inning] + "][" + OVERALL_GAME_SCORE_HOME[test_inning] + "]")
				
				if(topScore) : #could be empty, dont change
					if(debug) : print("TopScore: |" + topScore + "|" + OVERALL_GAME_SCORE_AWAY[test_inning])
					OVERALL_GAME_SCORE_AWAY[test_inning] = str(topScore)
					if_update_scores = True

			if  (OVERALL_GAME_SCORE_HOME[test_inning] != bottomScore) :
				if(bottomScore) :  #could be emtpy, dont change 
					if(debug) : print("bottomScore: |" + bottomScore + "|" + OVERALL_GAME_SCORE_AWAY[test_inning])
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

	#while(True) : 
	#	init_board('H0U', 'TEX')
	#	time.sleep(30)


	#check if any games today
	game_info = mlbgame.day(today_year,today_month,today_day, HOME_TEAM, AWAY_TEAM)		
	if not game_info : # if there are no games today
		no_game()
		new_game_status()

	before_game() #initialize the board
	new_game_status()
	

	#if(debug) : print("HERES THE INFO: ", game_info[0].away_team)
	#inning = 1
	#while(True) : 
	#	if(debug) : print("waiting to terminate") 
	#	time.sleep(5)
	#	if(debug) : print("Fixing to update:")
	#	time.sleep(5)


	#	draw_new_inning_score(inning, str(random.randint(1,19)))
	#	inning = inning + 1

	#if(debug) : print("LED_board: Starts")

	#new_game_status()
	
main()

