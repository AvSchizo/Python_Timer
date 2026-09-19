import json

def savePrefs(prefs=None):
	if prefs == None:
		i = preferences
	else:
		i = prefs

	with open("preferences.json", "w") as f:
		json.dump(i, f, indent="\t")