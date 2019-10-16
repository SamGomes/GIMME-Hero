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
	
	def saveplayerIncreases(self, playerId, stateIncreases):
		players[int(playerId)].pastModelIncreasesGrid.pushToGrid(stateIncreases)

	def resetPlayer(self, playerId):
		return 0


	def getSelectedPlayerIds(self):
		return [int(i) for i in range(100)]


	def getPlayerName(self, playerId):
		return players[int(playerId)].name

	def getPlayerCurrState(self,  playerId):
		return players[int(playerId)].currState

	def getPlayerCurrProfile(self,  playerId):
		return players[int(playerId)].currState.profile

	def getPlayerPastModelIncreases(self, playerId):
		return players[int(playerId)].pastModelIncreasesGrid.cells

	def getPlayerCurrCharacteristics(self, playerId):
		return players[int(playerId)].currState.characteristics
	
	def getPlayerPersonality(self, playerId):
		return players[int(playerId)].personality

	def setPlayerPersonality(self, playerId, personality):
		players[int(playerId)].personality = personality


	def setPlayerCharacteristics(self, playerId, characteristics):
		players[int(playerId)].currState.characteristics = characteristics

	def setPlayerCurrProfile(self, playerId, profile):
		players[int(playerId)].currState.profile = profile


