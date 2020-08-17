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
        roasts.append( "{}, I suggest you go to Practice Mode to learn how to play. PLEASE! You suck balls my guy!".format(VictimName))
        roasts.append( "{}, go back to playing C S GO. Wait. Are you even good at C S GO?".format(VictimName))
        roasts.append( "{}, Can you like do something with your life other than League? You are legit trash".format(VictimName))
        roasts.append( "Oh my God. {} I cannot watch this game anymore. All of you are terrible.".format(VictimName))
        roasts.append( "{}, Just stop playing. Please.".format(VictimName))
        roasts.append( "Holy shit {}. Can you land anything? Next game, I don't want to see you in the lobby".format(VictimName))
        roasts.append( "God damn you are so fucking trash {}".format(VictimName))
        roasts.append( "Wow {}, You know it's a shame you play so much League but you are still trash.".format(VictimName))
        roasts.append( "{}, play any other game other than League, please.".format(VictimName))
        roasts.append( "Just don't play League again {}. Just please. I hate watching you play like shit.".format(VictimName))
        roasts.append( "You're a fucking piece of shit {}. You know that?".format(VictimName))
        roasts.append( "YOU. ARE. SHIT {}.".format(VictimName))
        roasts.append( "{} Just stop. PLEASEEEEEE.!".format(VictimName))
        roasts.append( "Get shit on {}".format(VictimName))
        roasts.append( "God damn. you suck {}".format(VictimName))
        roasts.append( "{} Stop playing. Just leave. The rest of your team does better without you feeding.".format(VictimName))
        roasts.append( "{}, You're the biggest Troglydite I have ever seen. Only someone with the IQ of an ape could have died there.".format(VictimName))
        return random.choice(roasts)
    
    def findPlayer(self, playerName):
        for player in self.game.players:
            if player.summoner_name == playerName:
                return player
        return None

    def getComp(self, KillerName):
        comps = []
        comps.append("Damn {}, you actually managed to kill someone".format(KillerName))
        comps.append("Those are some clean {} mechanics, {}".format(self.findPlayer(self.findSummoner(KillerName)).champion_name, KillerName))
        comps.append("I really thought you were gonna hard int this game. Oh well, its {}. You still have time to throw".format(KillerName))
        comps.append('{} is a dirty smurf'.format(KillerName))
        comps.append('Good job abusing someone with the IQ of a 3 year old, {}'.format(KillerName))
        comps.append('{} hit that guy with the patented {} {}'.format(KillerName, self.findPlayer(self.findSummoner(KillerName)).champion_name, self.findPlayer(self.findSummoner(KillerName)).position))
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
            response = 'You managed to survive long enough for you inhib to respawn, good job monkeys'
        
        else:
            response = 'The enemies inhib respawned, all that work for nothing. Good job, Troggs'
        
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
    