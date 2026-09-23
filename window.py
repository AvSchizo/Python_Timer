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
		


	def progress(self, stopping=None, inList=None):
		if stopping == None:

			if inList == None:
				gonnaStop = False
			else:
				tener = True
				for block in inList:
					if block.type == "splitContainer":
						tener = False
				gonnaStop = tener
		
		else:
			gonnaStop = stopping
		
		if gonnaStop:
			self.pause()



	def update(self):
		if self.countingTime:
			self.countedTime += decimal(str(pygame.time.get_ticks()))-lastTime
		self.printedTime = self.font.render(self.setupPrintedTime(), True, self.fontColor)

	

	def draw(self, placement=0, inFrame=0):
		playPlace = [0, 0]
		forPlacement = [0, 0]

		# verticle
		if preferences["timeVertSpacing"] == "bottom":
			vertIncrement = self.printedTime.get_rect(bottom=self.playground.height)[1]
		elif preferences["timeVertSpacing"] == "middle":
			vertIncrement = self.printedTime.get_rect(center=(0, self.playground.height/2))[1]
		else:
			vertIncrement = 0
			if preferences["timeVertSpacing"] != "top":
				print("can't recognize \"timeVertSpacing\" in preferences.json")
		playPlace[1] = placement
		forPlacement[1] = placement + vertIncrement
		
		# horizontal
		if preferences["timeOnLeft"]:
			forPlacement[0] = 0
		else:
			forPlacement[0] = self.printedTime.get_rect(right=preferences["screen_defaultWidth"])[0]

		screen.blit(self.playground.actual, playPlace)
		screen.blit(self.printedTime, forPlacement)



	def setupPrintedTime(self, truncation=3):
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
					ab += preferences["incrementSeperator"]
					if preferences["spaceAfterIncrementSeperator"]:
						ab += " "

			return str(ab)

		toReturn = ""
		toReturn = ad(3, days, toReturn)
		toReturn = ad(2, hours, toReturn)
		toReturn = ad(1, minutes, toReturn)
		toReturn = ad(0, seconds, toReturn)
		toReturn += "." + str(flabber).split(".")[1][:truncation]

		return toReturn




# area text sits in
class playgroundClass():

	def __init__(self, inHeight, inColor):

		self.height = inHeight
		self.width = preferences["screen_defaultWidth"]

		self.actual = pygame.surface.Surface((self.width, self.height))
		self.actual.fill(inColor)




class bigTimerClass(timerClass):

	def __init__(self, inFontTotal=None, inFontFamily=None, inFontSize=None, inFontColor=None, playground_inHeight=None, playground_inColor=None):
		super().__init__()

		# font
		if inFontSize == None:
			forFontSize = preferences["bigTimer_fontSize"]
			forFontSize = int(forFontSize)

		else:
			forFontSize = inFontSize
		timerSetup(self=self, inFontTotal=inFontTotal, inFont=inFontFamily, inFontSize=forFontSize)

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
				playground_forHeight = preferences["bigTimer_playgroundHeight"]
			

			if preferences["bigTimer_extraPlaygroundSize_action"] == "*":
				playground_forHeight *= preferences["bigTimer_extraPlaygroundSize_value"]
			elif preferences["bigTimer_extraPlaygroundSize_action"] == "+":
				playground_forHeight += preferences["bigTimer_extraPlaygroundSize_value"]
			elif preferences["bigTimer_extraPlaygroundSize_action"] == "/":
				playground_forHeight /= preferences["bigTimer_extraPlaygroundSize_value"]
			elif preferences["bigTimer_extraPlaygroundSize_action"] == "-":
				playground_forHeight -= preferences["bigTimer_extraPlaygroundSize_value"]
			
			playground_forHeight = int(playground_forHeight)
		else:
			playground_forHeight = playground_inHeight

		if playground_inColor == None:
			playground_forColor = preferences["bigTimer_backgroundColor"]
		else:
			playground_forColor = playground_inColor

		self.playground = playgroundClass(playground_forHeight, playground_forColor)

		self.height = self.playground.height
	


	def setupPrintedTime(self):
		return super().setupPrintedTime(truncation=preferences["bigTimer_truncation"])




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



	def updateTime(self, time=None, inTruncation=None):
		if time == None:
			if self.time == None:
				wap = 0
			else:
				wap = self.time
		else:
			wap = time
		
		if inTruncation == None:
			truncation = preferences["split_truncation"]
		else:
			truncation = 2

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
			toReturn += "." + str(flabber).split(".")[1][:truncation]

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



	def draw(self, goDown=0, inFrame=None):
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
	"bigTimer_fontFamily": "sameasdefault",
	"bigTimer_extraPlaygroundSize_action": "*",
	"bigTimer_extraPlaygroundSize_value": (4/3),
	"bigTimer_fontSize": 40,
	"bigTimer_truncation": 2,
	#         ^                   ^
	# not implemented yet
	"split_backgroundColors": ["slateGrey"],
	"split_playgroundHeight": "sameasfont",
	"split_fontFamily": "sameasdefault",
	"split_truncation": 2,
	#       ^                  ^
	# not implemented yet
	"defaultFontFamily": "IBMPlexMono-Regular.ttf",
	"defaultFontColor": "black",
	"incrementSeperator": ":",
	"spaceAfterIncrementSeperator": False,
	"timeOnLeft": False,
	"timeVertSpacing": "bottom",
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

layout = [
	bigTimerClass(),
	splitContainerClass(),
]



screenHeight = 0
for block in layout:
	screenHeight += block.height
screen = pygame.display.set_mode((preferences["screen_defaultWidth"], screenHeight))
pygame.display.set_caption(preferences["timerCaption"])
screenColor = "black"
clock = pygame.time.Clock()











currentFrame = 0
while True:
	currentFrame += 1

	for event in pygame.event.get():
	
		if event.type == pygame.QUIT:

			running = False
			quit()


		if preferences["webMode"]:

			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				
				for block in layout:
					if block.type == "bigTimer":
						block.pause()



	# player inputs
	if not preferences["webMode"]:
		for key in preferences["commandHotkeys"].keys():
	
			if keyboard.is_pressed(preferences["commandHotkeys"]["pause"]) and not keysPressed["pause"]:
				for block in layout:
					if block.type == "bigTimer":
						block.pause()
				keysPressed["pause"] = True

		# restart
		if keyboard.is_pressed(preferences["commandHotkeys"]["restart"]) and not keysPressed["restart"]:
			for block in layout:
				if block.type == "bigTimer":
					block.restart()
			keysPressed["restart"] = True


		updatePressed(keysPressed)




	# updating area
	for block in layout:
		if block.type == "bigTimer":
			block.update()

	lastTime = decimal(str(pygame.time.get_ticks()))

	


			
	screen.fill(screenColor)

	indent = 0
	for block in layout:
		block.draw(indent, inFrame=currentFrame)
		indent += block.height


	pygame.display.update()
	clock.tick(100)
