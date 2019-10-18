import json #to save complex objects without a more complex model

import sys
print(sys.path)
sys.path.append('/home/samgomes/Documents/doutoramento/reps/GIMME-rep/GIMME/GIMMECore/')
from GIMMECore import *

from djangoTest.core.models import User

def _json_object_hook(d): return object('X', d.keys())(*d.values())
def json2obj(data): return json.loads(data)


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
		player = User.objects.get(username = playerId)
		player.currState = newState
		player.save(update_fields=["active"])

	def resetPlayer(self, playerId):
		return 0


	def getSelectedPlayerIds(self):
		return [player.username for player in User.objects.all()]

	def getPlayerName(self, playerId):
		player = User.objects.get(username=playerId)
		return player.fullName

	def getPlayerCurrState(self,  playerId):
		player = User.objects.get(username=playerId)
		return json2obj(player.currState)

	def getPlayerCurrProfile(self,  playerId):
		player = User.objects.get(username=playerId)
		return json2obj(player.currState.profile)

	def getPlayerPastModelIncreases(self, playerId):
		player = User.objects.get(username=playerId)
		return json2obj(player.pastModelIncreasesGrid).cells

	def getPlayerCurrCharacteristics(self, playerId):
		player = User.objects.get(username=playerId)
		return json2obj(player.currState).characteristics
	
	def getPlayerPersonality(self, playerId):
		player = User.objects.get(username=playerId)
		return json2obj(player.personality)

	def setPlayerPersonality(self, playerId, personality):
		player = User.objects.get(username=playerId)
		player.personality = json.dumps(personality, default=lambda o: o.__dict__)
		player.save(update_fields=["active"])


	def setPlayerCharacteristics(self, playerId, characteristics):
		player = User.objects.get(username=playerId)
		currState = self.getPlayerCurrState(playerId)
		currState.characteristics = characteristics
		player.currState = json.dumps(currState, default=lambda o: o.__dict__)
		player.save(update_fields=["active"])

	def setPlayerCurrProfile(self, playerId, profile):
		player = User.objects.get(username=playerId)
		currState = self.getPlayerCurrState(playerId)
		currState.profile = profile
		player.currState = json.dumps(currState, default=lambda o: o.__dict__)
		player.save(update_fields=["active"])


