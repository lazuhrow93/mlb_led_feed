#!/usr/bin/env python
from samplebase import SampleBase
from PIL import Image
from PIL import ImageDraw, ImageFont
from rgbmatrix import graphics
import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from Team_Attr import *

#global Variables, since we want to matrix to always be on. 
options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 2
options.cols = 64
options.hardware_mapping = 'regular'

matrix = RGBMatrix(options = options)

def init_board (homeTeam, awayTeam) :

	#this function will display the scoreboard template. with team names, inning numbers, bag status, batter status

	image = Image.new("RGB", (128, 32))  # Can be larger than matrix if wanted!!
	draw = ImageDraw.Draw(image)  # Declare Draw instance before prims

	#####################################################################
	#initialze scoreboard template 
	draw.rectangle((-1, 1, 112, 25), fill=(0, 0, 0), outline=(255, 255, 0))
	draw.line((86, 1, 86, 25), fill=(255, 255, 0))
	draw.line((0, 9, 112, 9), fill=(255, 255, 0))
	draw.line((0, 17, 112, 17), fill=(255,255,0))
	draw.line((13, 2, 13, 25), fill=(255,255,0))

	#####################################################################
	#initialize team name 
	teamNamesFont = ImageFont.truetype('pixelated.ttf', size = 8)
	draw.rectangle((0,10, 12, 16), fill=team_colors_background[awayTeam], outline = team_colors_background[awayTeam])
	draw.text((0, 9), team_abrev[awayTeam], fill=team_colors_text[awayTeam], font=teamNamesFont)

	draw.rectangle((0,18, 12, 24), fill=team_colors_background[homeTeam], outline = team_colors_background[homeTeam])
	draw.text((0, 17), team_abrev[homeTeam], fill=team_colors_text[homeTeam], font=teamNamesFont)

	fontYValue = 1

	#####################################################################
	#initialize inning numbers 
	#pixelated is perfect
	inningFonts = ImageFont.truetype('pixelated.ttf', size = 8)
	draw.text((16,fontYValue), '1', fill=(255,255,255), font=inningFonts)
	draw.text((24,fontYValue), '2', fill=(255,255,255), font=inningFonts)
	draw.text((32,fontYValue), '3', fill=(255,255,255), font=inningFonts)
	draw.text((39,fontYValue), '4', fill=(255,255,255), font=inningFonts)
	draw.text((48,fontYValue), '5', fill=(255,255,255), font=inningFonts)
	draw.text((56,fontYValue), '6', fill=(255,255,255), font=inningFonts)
	draw.text((64,fontYValue), '7', fill=(255,255,255), font=inningFonts)
	draw.text((72,fontYValue), '8', fill=(255,255,255), font=inningFonts)
	draw.text((80,fontYValue), '9', fill=(255,255,255), font=inningFonts)
	#runs, hits, errors
	draw.text((90,fontYValue), 'R', fill= (255,255,255), font=inningFonts)
	draw.text((98,fontYValue), 'H', fill = (255,255,255), font=inningFonts)
	draw.text((106,fontYValue), 'E', fill = (255,255,255), font=inningFonts)

	#####################################################################
	#initialize RHE section
	yValueRHE_away = 9
	draw.text((90,yValueRHE_away), '0', fill= (255,255,255), font=inningFonts)
	draw.text((98,yValueRHE_away), '0', fill = (255,255,255), font=inningFonts)
	draw.text((106,yValueRHE_away), '0', fill = (255,255,255), font=inningFonts)

	yValueRHE_home = 17
	draw.text((90,yValueRHE_home), '0', fill= (255,255,255), font=inningFonts)
	draw.text((98,yValueRHE_home), '0', fill = (255,255,255), font=inningFonts)
	draw.text((106,yValueRHE_home), '0', fill = (255,255,255), font=inningFonts)

	
	#####################################################################
	#initialize base status picture.

	yValueForGameStatus=1 #use this value to move this whole section either up or down
	draw.polygon([(114, yValueForGameStatus+6), (116,yValueForGameStatus+4), (118,yValueForGameStatus+6), (116, yValueForGameStatus+8)], fill=(0, 0, 0), outline=(255,255,0)) #1st base
	draw.polygon([(118, yValueForGameStatus+2), (120,yValueForGameStatus), (122,yValueForGameStatus+2), (120, yValueForGameStatus+4)], fill=(0, 0, 0), outline=(255,255,0))  #2nd base
	draw.polygon([(122, yValueForGameStatus+6), (124,yValueForGameStatus+4), (126,yValueForGameStatus+6), (124, yValueForGameStatus+8)], fill=(0, 0, 0), outline=(255,255,0)) #3rd base

	#seperate from scoreboard.
	draw.line([(112,1), (112,31)], fill=(255,255,0), width=1)

	#####################################################################
	#initialize current inning

	#top/bottom (start at the top)
	draw.polygon([(115, yValueForGameStatus+13), (119, yValueForGameStatus+13), (117, yValueForGameStatus+11)], fill=(255, 255, 0), outline=(255,255,0))
	#inning
	draw.text((123, yValueForGameStatus+9), '1', fill=(255,255,0), font=inningFonts)

	#####################################################################
	#initialize batter status

	#strikes/balls
	draw.text((115, yValueForGameStatus+16), '0', fill=(255,255,0), font=inningFonts)
	draw.text((123,yValueForGameStatus+16), '0', fill=(255,255,0), font=inningFonts)
	draw.line([(119,yValueForGameStatus+20), (121, yValueForGameStatus+20)], fill=(255,255,0), width=1)

	#outs
	draw.rectangle((115, yValueForGameStatus+25, 117, yValueForGameStatus+27), fill=(0, 0, 0), outline=(255, 255, 0)) #one out
	draw.rectangle((119, yValueForGameStatus+25, 121,  yValueForGameStatus+27), fill=(0, 0, 0), outline=(255, 255, 0)) #two outs
	draw.rectangle((123, yValueForGameStatus+25, 125,  yValueForGameStatus+27), fill=(0, 0, 0), outline=(255, 255, 0)) #three

	######################################################################
	matrix.Clear()
	matrix.SetImage(image, 0, 0)

def init_pre_game_board(game_start_time) :
	image = Image.new("RGB", (128, 32))  # Can be larger than matrix if wanted!!
	draw = ImageDraw.Draw(image)  # Declare Draw instance before prims

	teamNamesFont = ImageFont.truetype('Virtual Pet Sans.otf', size = 8)

	draw.text((15, 3), 'GAME STARTS AT', fill=(255, 255, 0), font=teamNamesFont)
	draw.text((39, 16), game_start_time, fill=(255,255,0), font=teamNamesFont)

	matrix.Clear()
	matrix.SetImage(image, 0, 0)

def init_post_game_board(homeScore, awayScore, homeTeam, awayTeam) :

	image = Image.new("RGB", (128, 32))  # Can be larger than matrix if wanted!!
	draw = ImageDraw.Draw(image)  # Declare Draw instance before prims

	teamNamesFont = ImageFont.truetype('Virtual Pet Sans.otf', size = 8)

	draw.text((15, 3), 'Final Score: ', fill=(255, 255, 0), font=teamNamesFont)
	draw.text((29, 16), homeTeam + " " + homeScore + " v " + awayTeam + " " + awayScore, fill=(255,255,0), font=teamNamesFont)

	matrix.Clear()
	matrix.SetImage(image, 0, 0)


def draw_new_extra_innings_score(curr_inning, curr_home_scores, curr_away_scores) :


	#shift innings numbers one space to the left to make room for extra innings
	newInningsImage = Image.new("RGB", (72, 7)) #create image for the innings
	drawInnings = ImageDraw.Draw(newInningsImage) 

	inningFonts = ImageFont.truetype('pixelated.ttf', size = 8)

	xCoorZeroed = 2
	fontYValue = -1

	for inning in range(curr_inning-8,curr_inning+1) : #from first innign to be displayed, all the way to the current extra inning 
		
		if(len(str(inning)) > 1) : #center double digit innings
			draw.text((xCoorZeroed-2,fontYValue), str(inning), fill=(255,255,255), font=inningFonts)
		else :
			draw.text((xCoorZeroed, fontYValue), str(inning), fill=(255,255,255), font=inningFonts)

		xCoorZeroed = xCoorZeroed + 8


	#Display the appropriate scores under their innings. Only show 9 innings up to current inning
	awayScoresImage = Image.new("RGB", (72, 7)) #create image for the innings
	drawAwayScores = ImageDraw.Draw(awayScoresImage) 

	xCoorZeroed = 2
	fontYValue = -1
	#OVERALL_GAME_SCORE_HOME
	#OVERALL_GAME_SCORE_AWAY

	for inning in range(curr_inning-8, curr_inning) :

		if(len(str(inning)) > 1) : #center double digit innings
			draw.text((xCoorZeroed-2,fontYValue), str(OVERALL_GAME_SCORE_AWAY[inning]), fill=(255,255,255), font=inningFonts)
		else :
			draw.text((xCoorZeroed, fontYValue), str(OVERALL_GAME_SCORE_AWAY[inning]), fill=(255,255,255), font=inningFonts)

		xCoorZeroed = xCoorZeroed + 8


	homeScoresImage = Image.new("RGB", (72, 7)) #create image for the innings
	drawHomeScores = ImageDraw.Draw(homeScoresImage) 

	xCoorZeroed = 2
	fontYValue = -1
	#OVERALL_GAME_SCORE_HOME
	#OVERALL_GAME_SCORE_AWAY

	for inning in range(curr_inning-8, curr_inning) :

		if(len(str(inning)) > 1) : #center double digit innings
			draw.text((xCoorZeroed-2,fontYValue), str(OVERALL_GAME_SCORE_HOME[inning]), fill=(255,255,255), font=inningFonts)
		else :
			draw.text((xCoorZeroed, fontYValue), str(OVERALL_GAME_SCORE_HOME[inning]), fill=(255,255,255), font=inningFonts)

		xCoorZeroed = xCoorZeroed + 8


	#place the updates
	matrix.SetImage(newInningsImage, 14, 2)
	matrix.SetImage(awayScoresImage, 14, 10)
	matrix.SetImage(homeScoresImage, 14, 18)



def draw_new_inning_score(curr_inning, new_score, team) :

	zeroed_x = 14 #all x's start here, basically pretend its zero. 

	image = Image.new("RGB", (7, 5))  #The size of the image for the score
	draw = ImageDraw.Draw(image)  # Declare Draw instance before prims

	y_coor_away = 11 #away score is at (x, y_coor_away)
	y_coor_home = 19 #home score is at (x, y_coor_home)
	x_coor = zeroed_x


	ourInning = False
	tempInning = 1
	while(not ourInning) :
		if(tempInning == curr_inning) : 
			ourInning = True
		else : 
			x_coor = x_coor + 8 #next inning score coordinate

		tempInning = tempInning + 1

	ourInning = False

	inningFonts = ImageFont.truetype('pixelated.ttf', size = 8)
	
	text_coor_in_image = -2
	if(new_score == '-') : text_coor_in_image = -1 #if its '-' then raise it one pixel. To center it.


	if(len(new_score) > 1) : #if double digit
		draw.text((0, text_coor_in_image), new_score, fill = (255, 255, 255), font=inningFonts)
	else : # center the number since its only one digit
		draw.text((2, text_coor_in_image), new_score, fill = (255, 255, 255), font=inningFonts)
	
	if(team == 'HOME') : 
		matrix.SetImage(image,x_coor,y_coor_home)
	else :
		matrix.SetImage(image,x_coor,y_coor_away)

def draw_new_outs(numOfOuts) :
	imageBlank = Image.new("RGB", (1,1)) 
	imageLight = Image.new("RGB", (1,1))
	drawBlank = ImageDraw.Draw(imageBlank)
	drawLight = ImageDraw.Draw(imageLight)

	drawBlank.point((0,0), fill=(0,0,0))
	drawLight.point((0,0), fill=(255,255,0))

	if(numOfOuts>=1) : matrix.SetImage(imageLight, 116, 27)
	else : matrix.SetImage(imageBlank, 116, 27)

	if(numOfOuts>=2) : matrix.SetImage(imageLight, 120, 27)
	else : matrix.SetImage(imageBlank, 120, 27)

	if(numOfOuts>=3) : matrix.SetImage(imageLight, 124, 27)
	else : matrix.SetImage(imageBlank, 124, 27)

def draw_new_RHE(runs,hits,errors,team) :


	imageRuns = Image.new("RGB", (7,5))
	imageHits = Image.new("RGB", (7,5))
	imageErrors = Image.new("RGB", (7,5))

	drawRuns = ImageDraw.Draw(imageRuns)
	drawHits = ImageDraw.Draw(imageHits)
	drawErrors = ImageDraw.Draw(imageErrors)
	runshitserrors_font = ImageFont.truetype('pixelated.ttf', size = 8)

	y_coor_away = 11
	y_coor_home = 19

	if(len(runs) > 1) : drawRuns.text((0, -2), runs, fill = (255, 255, 255), font=runshitserrors_font)
	else : drawRuns.text((2, -2), runs, fill = (255, 255, 255), font=runshitserrors_font)

	if(len(hits) > 1) : drawHits.text((0, -2), hits, fill = (255, 255, 255), font=runshitserrors_font)
	else : drawHits.text((2, -2), hits, fill = (255, 255, 255), font=runshitserrors_font)

	if(len(errors) > 1) : drawErrors.text((0, -2), errors, fill = (255, 255, 255), font=runshitserrors_font)
	else : drawErrors.text((2, -2), errors, fill = (255, 255, 255), font=runshitserrors_font)

	xZeroed = 88

	if(team == 'HOME') : 
		matrix.SetImage(imageRuns, xZeroed, y_coor_home)
		matrix.SetImage(imageHits, xZeroed+8, y_coor_home)
		matrix.SetImage(imageErrors, xZeroed+16, y_coor_home)
	else :
		matrix.SetImage(imageRuns,xZeroed,y_coor_away)
		matrix.SetImage(imageHits,xZeroed+8,y_coor_away)
		matrix.SetImage(imageErrors,xZeroed+16,y_coor_away)

def draw_new_balls_strikes(balls, strikes) :

	imageStrikes = Image.new("RGB", (3,5))
	imageBalls = Image.new("RGB", (3,5))

	drawStrikes = ImageDraw.Draw(imageStrikes)
	drawBalls = ImageDraw.Draw(imageBalls)

	s_b_font = ImageFont.truetype('pixelated.ttf', size = 8)

	xZeroed = 115
	yZeroed = 19 #higher than calculated, since have to cover the init m

	drawStrikes.text((0,-2), strikes, fill=(255,255,0), font=s_b_font)
	drawBalls.text((0,-2), balls, fill=(255,255,0), font=s_b_font)

	matrix.SetImage(imageBalls, xZeroed, yZeroed)
	matrix.SetImage(imageStrikes, xZeroed+8, yZeroed)

def draw_inning_status(topBottom, inningNum) :

	imageInningStatus = Image.new("RGB", (11,5))
	drawInningStatus = ImageDraw.Draw(imageInningStatus)

	statusFont = ImageFont.truetype('pixelated.ttf', size = 8)

	yValueForGameStatus=0
	xValueForGameStatus=0

	if(topBottom == 'Top') : coordinates = [(xValueForGameStatus, yValueForGameStatus+2), (xValueForGameStatus+4, yValueForGameStatus+2), (xValueForGameStatus+2, yValueForGameStatus)]
	else : coordinates = [(xValueForGameStatus, yValueForGameStatus+2), (xValueForGameStatus+4, yValueForGameStatus+2), (xValueForGameStatus+2, yValueForGameStatus+4)]
	

	drawInningStatus.polygon(coordinates, fill=(255, 255, 0), outline=(255,255,0))
	#inning
	drawInningStatus.text((xValueForGameStatus+8, -2), inningNum, fill=(255,255,0), font=statusFont)

	matrix.SetImage(imageInningStatus, 115, 12)

def draw_base_runners(first,second,third) :

	imageNoRunner = Image.new("RGB", (1,1)) 
	imageRunnerOn = Image.new("RGB", (1,1))
	drawNoRunner = ImageDraw.Draw(imageNoRunner)
	drawRunnerOn = ImageDraw.Draw(imageRunnerOn)

	drawNoRunner.point((0,0), fill=(0,0,0))
	drawRunnerOn.point((0,0), fill=(255,255,0))

	if(third) : matrix.SetImage(imageRunnerOn, 116, 7)
	else : matrix.SetImage(imageNoRunner, 116, 7)

	if(second) : matrix.SetImage(imageRunnerOn, 120, 3)
	else : matrix.SetImage(imageNoRunner, 120, 3)

	if(first) : matrix.SetImage(imageRunnerOn, 124, 7)
	else : matrix.SetImage(imageNoRunner, 124, 7)



