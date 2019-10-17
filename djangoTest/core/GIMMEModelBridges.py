import json #to save complex objects without a more complex model

import sys
print(sys.path)
sys.path.append('/home/samgomes/Documents/doutoramento/reps/GIMME-rep/GIMME/GIMMECore/')
from GIMMECore import *

from djangoTest.core.models import User



class CustomTaskModelBridge(TaskModelBridge):
	
	def getSelectedTaskIds(self):
		pass

	def getTaskInteractionsProfile(self, taskId):
		pass

	def getTaskMinRequiredAbility(self, taskId):
		pass

	def getTaskDifficultyWeight(self, taskId):
		pass

	def getTaskProfileWeight(self, taskId):
		pass


class CustomPlayerModelBridge(PlayerModelBridge):
	
	def savePlayerState(self, playerId, newState):
		player = User(playerId=playerId).objects[0]
		player.currState = newState
		player.save(update_fields=["active"])

	def resetPlayer(self, playerId):
		return 0


	def getSelectedPlayerIds(self):
		return [player.playerId for player in User.objects.all()]


	def getPlayerName(self, playerId):
		player = User(playerId=playerId).objects[0]
		return player.fullName

	def getPlayerCurrState(self,  playerId):
		player = User(playerId=playerId).objects[0]
		return player.currState

	def getPlayerCurrProfile(self,  playerId):
		player = User(playerId=playerId).objects[0]
		return player.currState.profile

	def getPlayerPastModelIncreases(self, playerId):
		player = User(playerId=playerId).objects[0]
		return player.pastModelIncreasesGrid.cells

	def getPlayerCurrCharacteristics(self, playerId):
		player = User(playerId=playerId).objects[0]
		return player.currState.characteristics
	
	def getPlayerPersonality(self, playerId):
		player = User(playerId=playerId).objects[0]
		return player.personality

	def setPlayerPersonality(self, playerId, personality):
		player = User(playerId=playerId).objects[0]
		player.personality = personality


	def setPlayerCharacteristics(self, playerId, characteristics):
		player = User(playerId=playerId).objects[0]
		player.currState.characteristics = characteristics

	def setPlayerCurrProfile(self, playerId, profile):
		player = User(playerId=playerId).objects[0]
		player.currState.profile = profile


