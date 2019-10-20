import json #to save complex objects without a more complex model

import sys
print(sys.path)
sys.path.append('/home/samgomes/Documents/doutoramento/reps/GIMME-rep/GIMME/GIMMECore/')
from GIMMECore import *

from djangoTest.core.models import User


class CustomTaskModelBridge(TaskModelBridge):
	
	def getSelectedTaskIds(self):
		return []

	def getTaskInteractionsProfile(self, taskId):
		return InteractionsProfile()

	def getTaskMinRequiredAbility(self, taskId):
		return 0

	def getTaskDifficultyWeight(self, taskId):
		return 0

	def getTaskProfileWeight(self, taskId):
		return 0


class CustomPlayerModelBridge(PlayerModelBridge):
	
	def savePlayerState(self, playerId, newState):
		player = User.objects.get(username = playerId)
		player.currState = newState
		player.save(update_fields=["active"])

	def resetPlayer(self, playerId):
		return 0


	def getSelectedPlayerIds(self):
		return Views.currSelectedPlayers

	def getPlayerName(self, playerId):
		player = User.objects.get(username=playerId)
		return player.fullName

	
	def getPlayerCurrProfile(self,  playerId):
		player = User.objects.get(username=playerId)
		profile = json.loads(player.currState)["profile"]
		return InteractionsProfile(K_cl= profile["K_cl"], K_cp= profile["K_cp"], K_i= profile["K_i"])

	def getPlayerPastModelIncreases(self, playerId):
		player = User.objects.get(username=playerId)
		return json.loads(player.pastModelIncreasesGrid)["cells"]

	def getPlayerCurrCharacteristics(self, playerId):
		player = User.objects.get(username=playerId)
		characteristics = json.loads(player.currState)["characteristics"]
		return PlayerCharacteristics(ability= characteristics["ability"], engagement= characteristics["engagement"])
	
	def getPlayerPersonality(self, playerId):
		player = User.objects.get(username=playerId)
		personality = json.loads(player.personality)
		return InteractionsProfile(K_cl=personality["K_cl"], K_cp=personality["K_cp"], K_i=personality["K_i"])
	
	def getPlayerCurrState(self,  playerId):
		player = User.objects.get(username=playerId)
		return PlayerState(profile = self.getPlayerCurrProfile(playerId), characteristics = self.getPlayerCurrCharacteristics(playerId), dist = json.loads(player.currState)["dist"])


	def setPlayerPersonality(self, playerId, personality):
		player = User.objects.get(username=playerId)
		player.personality = json.dumps(personality, default=lambda o: o.__dict__)
		player.save()


	def setPlayerCharacteristics(self, playerId, characteristics):
		player = User.objects.get(username=playerId)
		newState = self.getPlayerCurrState(playerId)
		newState.characteristics = characteristics
		player.currState = json.dumps(newState, default=lambda o: o.__dict__)
		player.save()

	def setPlayerCurrProfile(self, playerId, profile):
		player = User.objects.get(username=playerId)
		newState = self.getPlayerCurrState(playerId)
		newState.profile = profile
		player.currState = json.dumps(newState, default=lambda o: o.__dict__)
		player.save()


