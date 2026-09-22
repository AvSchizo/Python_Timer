import pygame
pygame.init()

import json

from decimal import Decimal
decimal = Decimal

from Verify_Game_Files import verifyGameFiles
from Save_Preferences import savePrefs




def autoVer():
	verifyGameFiles(default_preferences)






##########################################
##                                      ##
##             layout setup             ##
##                                      ##
##########################################

def timerSetup(self, inFontTotal=None, inFont=None, inFontSize=50):

	if inFont == None:
		fontFamily = "fonts/" + preferences["defaultFontFamily"]
	else:
		fontFamily = inFont

	# inFontTotal is whole pygame font object
	if inFontTotal == None:
		try:
			self.font = pygame.font.Font(fontFamily, inFontSize)
		except:
			self.font = pygame.font.Font(None, inFontSize)
			print("font not found, using default")
	else:
		self.font = inFontTotal




class timerClass():

	def pause(self):
		if self.countingTime:
			self.countingTime = False
		else:
			self.countingTime = True



	def restart(self):
		self.countingTime = False
		self.countedTime = decimal("0.000")



	def update(self):
		if self.countingTime:
			self.countedTime += decimal(str(pygame.time.get_ticks()))-lastTime
		self.printedTime = self.font.render(self.setupPrintedTime(), True, self.fontColor)

	

	def draw(self, placement=None):
		if placement == None:
			playPlace = (0, 0)
			if preferences["timeOnLeft"]:
				forPlacement = (0, 0)
			else:
				forPlacement = (self.printedTime.get_rect(right=preferences["screen_defaultWidth"])[0], 0)
		else:
			playPlace = (0, placement)
			if preferences["timeOnLeft"]:
				forPlacement = (0, placement)
			else:
				forPlacement = (self.printedTime.get_rect(right=preferences["screen_defaultWidth"])[0], placement)
		screen.blit(self.playground.actual, playPlace)
		screen.blit(self.printedTime, forPlacement)



	def setupPrintedTime(self):
		flabber = decimal(self.countedTime/decimal("1000"))

		secondsTotal = int(flabber)
		seconds = secondsTotal%60

		minutesTotal = int(secondsTotal/60)
		minutes = minutesTotal%60

		hoursTotal = int(minutesTotal/60)
		hours = hoursTotal%24

		daysTotal = int(hoursTotal/24)
		days = daysTotal%60


		startLevel = 0
		if minutesTotal > 0:
			startLevel = 1
		if hoursTotal > 0:
			startLevel = 2
		if daysTotal > 0:
			startLevel = 3

		def ad(l, i, ee):
			ab = ee
			if startLevel > l and i < 10:
				ab += "0"
			if startLevel >= l:
				ab += str(i)
				if l > 0:
					ab += ","

			return str(ab)

		toReturn = ""
		toReturn = ad(3, days, toReturn)
		toReturn = ad(2, hours, toReturn)
		toReturn = ad(1, minutes, toReturn)
		toReturn = ad(0, seconds, toReturn)
		toReturn += "." + str(flabber).split(".")[1]

		return toReturn




# area text sits in
class playgroundClass():

	def __init__(self, inHeight, inColor):

		self.height = inHeight
		self.width = preferences["screen_defaultWidth"]

		self.actual = pygame.surface.Surface((self.width, self.height))
		self.actual.fill(inColor)




class bigTimerClass(timerClass):

	def __init__(self, inFontTotal=None, inFontFamily=None, inFontSize=50, inFontColor=None, playground_inHeight=None, playground_inColor=None):
		super().__init__()

		# font
		timerSetup(self=self, inFontTotal=inFontTotal, inFont=inFontFamily, inFontSize=inFontSize)

		# type
		self.type = "bigTimer"

		# counting
		self.countingTime = False
		self.countedTime = decimal("0.000")

		# numbers
		if inFontColor == None:
			self.fontColor = preferences["defaultFontColor"]
		else:
			self.fontColor = inFontColor

		self.update()

		# playground
		if playground_inHeight == None:
			playground_forHeight = preferences["bigTimer_playgroundHeight"]
			if preferences["bigTimer_playgroundHeight"] == "sameasfont":
				playground_forHeight = self.printedTime.get_rect().height
		else:
			playground_forHeight = playground_inHeight

		if playground_inColor == None:
			playground_forColor = preferences["bigTimer_backgroundColor"]
		else:
			playground_forColor = playground_inColor

		self.playground = playgroundClass(playground_forHeight, playground_forColor)




# split stuff
class splitClass():

	def __init__(self, splitNumber="", inFontTotal=None, inFontFamily=None, inFontSize=25, inFontColor=None, playground_inHeight=None, playground_inColor=None):

		self.type = "split"

		self.name = "split" + str(splitNumber)

		# font
		timerSetup(self=self, inFontTotal=inFontTotal, inFont=inFontFamily, inFontSize=inFontSize)
		if inFontColor == None:
			self.fontColor = preferences["defaultFontColor"]
		else:
			self.fontColor = inFontColor

		self.time = None

		self.updateTime()

		if playground_inHeight == None:
			playground_forHeight = preferences["split_playgroundHeight"]
			if preferences["split_playgroundHeight"] == "sameasfont":
				playground_forHeight = max(self.printedName.get_rect().height, self.printedTime.get_rect().height)
		else:
			playground_forHeight = playground_inHeight

		if playground_inColor == None:
			playground_forColor = preferences["split_backgroundColors"][(splitNumber-1)%len(preferences["split_backgroundColors"])]
		else:
			playground_forColor = playground_inColor

		self.playground = playgroundClass(playground_forHeight, playground_forColor)

		self.height = self.playground.height



	def updateTime(self, time=None):
		if time == None:
			if self.time == None:
				wap = 0
			else:
				wap = self.time
		else:
			wap = time

		flabber = decimal(wap/decimal("1000"))

		secondsTotal = int(flabber)
		seconds = secondsTotal%60

		minutesTotal = int(secondsTotal/60)
		minutes = minutesTotal%60

		hoursTotal = int(minutesTotal/60)
		hours = hoursTotal%24

		daysTotal = int(hoursTotal/24)
		days = daysTotal%60


		startLevel = 0
		if minutesTotal > 0:
			startLevel = 1
		if hoursTotal > 0:
			startLevel = 2
		if daysTotal > 0:
			startLevel = 3

		def ad(l, i, ee):
			ab = ee
			if startLevel > l and i < 10:
				ab += "0"
			if startLevel >= l:
				ab += str(i)
				if l > 0:
					ab += ","

			return str(ab)

		toReturn = ""
		toReturn = ad(3, days, toReturn)
		toReturn = ad(2, hours, toReturn)
		toReturn = ad(1, minutes, toReturn)
		toReturn = ad(0, seconds, toReturn)
		if wap == 0:
			toReturn = ''
		else:
			toReturn += "." + str(flabber).split(".")[1][:2]

		self.printedTime = self.font.render(toReturn, True, self.fontColor)
		self.printedName = self.font.render(self.name, True, self.fontColor)



	def draw(self, placement=None):
		if placement == None:
			playPlace = (0, 0)
			forPlacement = (self.printedTime.get_rect(right=preferences["screen_defaultWidth"])[0], 0)
		else:
			playPlace = (0, placement)
			forPlacement = (self.printedTime.get_rect(right=preferences["screen_defaultWidth"])[0], placement)
		screen.blit(self.playground.actual, playPlace)
		screen.blit(self.printedName, playPlace)
		screen.blit(self.printedTime, forPlacement)




class splitContainerClass():

	def __init__(self, amountOfSplits=1):

		self.type = "splitContainer"

		self.splits = []
		for i in range(max(1, amountOfSplits)):
			self.splits.append(splitClass(i+1))

		self.splitPointer = 0

		self.findHeight()



	def findHeight(self):
		self.height = 0
		for p in self.splits:
			self.height += p.playground.actual.get_height()



	def draw(self, goDown=0):
		down = 0
		for s in self.splits:
			s.draw(goDown+down)
			down += s.height
		














#### UPON STARTUP ####

# preferences
default_preferences = {
	"commandHotkeys": {
		"progress": "ctrl+shift+alt+end",
		"pause": "shift+down",
		"returnSplit": "ctrl+shift+alt+delete+page up",
		"skipSplit": "ctrl+shift+alt+delete+page down",
		"restart": "ctrl+shift+alt+delete+end",
	},
	"webMode": False,
	"timerCaption": "TEST TIMER",
	"screen_defaultWidth": 400,
	"bigTimer_backgroundColor": "lavender",
	"bigTimer_playgroundHeight": "sameasfont",
	"split_backgroundColors": ["slateGrey"],
	"split_playgroundHeight": "sameasfont",
	"defaultFontFamily": "IBMPlexMono-Regular.ttf",
	"defaultFontColor": "black",
	"timeOnLeft": False,
}
autoVer()

# for testing: remove later
savePrefs(prefs=default_preferences)

with open("preferences.json", "r") as f:
	preferences = json.load(f)




if preferences["webMode"]:
	pass

else:
	# import is here because you can't tell whether it's webMode if you import it at the top
	import keyboard

	def updatePressed(dict):
		for key in preferences["commandHotkeys"].keys():
			if not keyboard.is_pressed(preferences["commandHotkeys"][key]):
				keysPressed[key] = False

	keysPressed = {}
	for key in preferences["commandHotkeys"].keys():
		keysPressed[key] = False







lastTime = decimal(str(pygame.time.get_ticks()))

bigTimer1 = bigTimerClass()
splitContainer1 = splitContainerClass()



screenHeight = 0
screenHeight += bigTimer1.playground.actual.get_height()
screenHeight += splitContainer1.height
screen = pygame.display.set_mode((preferences["screen_defaultWidth"], screenHeight))
pygame.display.set_caption(preferences["timerCaption"])
screenColor = "black"
clock = pygame.time.Clock()











while True:

	for event in pygame.event.get():
	
		if event.type == pygame.QUIT:

			running = False
			quit()


		if preferences["webMode"]:

			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				bigTimer1.pause()



	# player inputs
	if not preferences["webMode"]:
		for key in preferences["commandHotkeys"].keys():
	
			if keyboard.is_pressed(preferences["commandHotkeys"]["pause"]) and not keysPressed["pause"]:
				bigTimer1.pause()
				keysPressed["pause"] = True

		# restart
		if keyboard.is_pressed(preferences["commandHotkeys"]["restart"]) and not keysPressed["restart"]:
			bigTimer1.restart()
			keysPressed["restart"] = True


		updatePressed(keysPressed)




	# updating area
	bigTimer1.update()

	lastTime = decimal(str(pygame.time.get_ticks()))

	


			
	screen.fill(screenColor)

	bigTimer1.draw()
	splitContainer1.draw(bigTimer1.playground.height)


	pygame.display.update()
	clock.tick(1000)
