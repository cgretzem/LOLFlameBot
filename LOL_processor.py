import requests, json, random
import leaguepkg
from leaguepkg import active
from leaguepkg.active import ActiveGame
import asyncio

class Game():
    def __init__(self, active_game:ActiveGame):
        self.game = active_game
        with open('./Friends.json') as f:
            friendList = json.load(f)
        self.friends = friendList['Friends']
        self.current = self.game.getLastEvent()
    def getRoast(self, VictimName):
        roasts = []
        # ADD CUSTOM ROASTS HERE!
        return random.choice(roasts)
    
    def findPlayer(self, playerName):
        for player in self.game.players:
            if player.summoner_name == playerName:
                return player
        return None

    def getComp(self, KillerName):
        comps = []
        # ADD CUSTOM COMPLIMENTS HERE
        return random.choice(comps)

    def checkFriends(self, friendName):
        output = False
        for friend in self.friends:
            if friend['IGN'] == friendName:
                output = True
                break
            else:
                output = False
        return output

    def findFriend(self, friendName):
        output = None
        for friend in self.friends:
            if friend['IGN'] == friendName:
                output = friend['IRL']
        return output

    def findSummoner(self, friendName):
        output = None
        for friend in self.friends:
            if friend['IRL'] == friendName:
                output = friend['IGN']
        return output

    def championKill(self):
        if self.checkFriends(self.current['VictimName']):
            response = self.getRoast(self.findFriend(self.current['VictimName']))
        elif self.checkFriends(self.current['KillerName']):
            response = self.getComp(self.findFriend(self.current['KillerName']))
        else:
            response = None
        return response

    def towerKill(self):
        response = "{} destroyed a tower".format(self.current['KillerName'])
        return response

    def firstBlood(self):
        response = "Wow! {} got first blood!".format(self.current['Recipient'])
        return response


    def inhibKilled(self):
        inhibs = {
            'ORDER' : ['Barracks_T1_R1','Barracks_T1_C1','Barracks_T1_L1'],
            'CHAOS' : ['Barracks_T2_R1','Barracks_T2_C1','Barracks_T2_L1']
        }
        
        if self.current['InhibKilled'] in inhibs[self.game.active_player.team]:
            response = 'God Damn it you guys lost an inhib. How retarded are you?'
        #print (self.current['InhibKilled'])
        else:
            response = 'You finally killed an inhib'
        return response

    def firstTower(self):
        response = "{} destroyed the first tower".format(self.current['KillerName'])
        return response

    def gameOver(self):
        response = "Game is done!"
        return response

    def gameStart(self):
        response = 'The game has started'
        return response

    def minions(self):
        response = 'Minions have spawned'
        return response

    def dragonKill(self):
        response = '{} has slain the {} dragon'.format(self.current['KillerName'], self.current['DragonType'])
        return response

    def baronKill(self):
        response = "{} has slain Baron Nashor".format(self.current['KillerName'])
        return response

    def heraldKill(self):
        if self.checkFriends(self.current['KillerName']):
            response = "{} used all of his brainpower this game to kill a big crab. Good job".format(self.current['KillerName'])
        else:
            response = None
        return response

    def multiKill(self):
        response = None
        return response

    
    def inhibRespawned(self):
        inhibs = {
            'ORDER' : ['Barracks_T1_R1','Barracks_T1_C1','Barracks_T1_L1'],
            'CHAOS' : ['Barracks_T2_R1','Barracks_T2_C1','Barracks_T2_L1']
        }

        if self.current['InhibRespawningSoon'] in inhibs[self.game.active_player.team]:
            response = 'Your inhibitor is almost back up, do you think you can go 30 seconds without inting for once so it can respawn?'
        
        else:
            response = 'The enemies inhib is coming back up soon because you all were too stupid to end the game'
        
        return response

    def inhibRespawn(self):
        inhibs = {
            'ORDER' : ['Barracks_T1_R1','Barracks_T1_C1','Barracks_T1_L1'],
            'CHAOS' : ['Barracks_T2_R1','Barracks_T2_C1','Barracks_T2_L1']
        }

        
        if self.current['InhibRespawned'] in inhibs[self.game.active_player.team]:
            response = 'You managed to survive long enough for you inhib to respawn'
        
        else:
            response = 'The enemies inhib respawned, all that work for nothing.'
        
        return response

    def ace(self):
        #   to be implemented: checks if enemy ace or your ace
        response = "Ace"
        return response

    
    def cases(self, case):
    
        switcher = {
            'ChampionKill' : self.championKill,
            'FirstBlood' : self.firstBlood,
            'FirstBrick' : self.firstTower,
            'TurretKilled' : self.towerKill,
            'InhibKilled' : self.inhibKilled,
            'GameEnd' : self.gameOver,
            'GameStart' : self.gameStart,
            'MinionsSpawning' : self.minions,
            'DragonKill' : self.dragonKill,
            'BaronKill' : self.baronKill,
            'HeraldKill' : self.heraldKill,
            'Multikill' : self.multiKill,
            'InhibRespawningSoon' : self.inhibRespawned,
            'InhibRespawned' : self.inhibRespawn,
            'Ace' : self.ace
        }
        
        return switcher[case]()

async def send():
    
    delay = 1.5
    while not active.check_status():
        await asyncio.sleep(delay)
    active_game = Game(ActiveGame())
    newEvents = []
    output = []
    while not newEvents:
        await asyncio.sleep(delay)
        newEvents = active_game.game.updateEventList()
    for event in newEvents:
        active_game.current = event
        output.append(active_game.cases(event['EventName']))
    return output

if __name__ == '__main__':
    active_game = Game(ActiveGame())
    
