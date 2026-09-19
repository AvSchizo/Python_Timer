import json
from Save_Preferences import savePrefs

def verifyGameFiles(defPref):

	# preferences.json
	try:
		with open("preferences.json", "r") as f:
			pass
	except:
		savePrefs(defPref)