# MLB_LED_FEED
Welcome to this project. 

The program starts in the file main.py and displays the current score board of a baseball game real time. It will be able to display, on a 128x32 LED matrix (two 64x32 chained together), the scores per inning, how many current outs, current strikes, current balls, current inning (also top or bottom), baserunners, each teams runs, hits and errors.


The goal of this project was for me to get familiar with python as well as working with the Raspberry Pi and LED matrix board. It uses the API [mlbgame](https://github.com/panzarino/mlbgame/tree/master/mlbgame) to grab information of a game real time, and the library [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix) to be able to manipulate the LED matrix.

In order to run the program on boot for the Raspberry Pi. Paste this line to the etc/rc.local.save file 

sudo python /home/pi/Desktop/PiProjects/MakeLEDWork/rpi-rgb-led-matrix/bindings/python/MLB_Project/main.py & > /home/pi/Desktop/log.txt 2>&1

This is for my folder structure
