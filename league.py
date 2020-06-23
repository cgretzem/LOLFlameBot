import requests, json, random
from time import sleep
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

with open('./Friends.json') as f:
    friendList = json.load(f)

friends = friendList['Friends']



def getRoast(VictimName):
    roasts = []
    roasts.append( "{}, I suggest you go to Practice Mode to learn how to play. PLEASE! You suck balls my guy!")
    roasts.append( "{}, go back to playing C S GO. Wait. Are you even good at C S GO?")
    roasts.append( "{}, Can you like do something with your life other than League? You are legit trash")
    roasts.append( "Oh my God. {} I cannot watch this game anymore. All of you are terrible.")
    roasts.append( "{}, Just stop playing. Please.")
    roasts.append( "Holy shit {}. Can you land anything? Next game, I don't want to see you in the lobby")
    roasts.append( "God damn you are so fucking trash {}")
    roasts.append( "Wow {}, You know it's a shame you play so much League but you are still trash.")
    roasts.append( "{}, play any other game other than League, please.")
    roasts.append( "Just don't play League again {}. Just please. I hate watching you play like shit.")
    roasts.append( "You're a fucking piece of shit {}. You know that?")
    roasts.append( "YOU. ARE. SHIT {}.")
    roasts.append( "{} Just stop. PLEASEEEEEE.!")
    roasts.append( "Get shit on {}")
    roasts.append( "God damn. you suck {}")
    roasts.append( "{} Stop playing. Just leave. The rest of your team does better without you feeding.")
    roasts.append( "{}, You're the biggest Troglydite I have ever seen. Only someone with the IQ of an ape could have died there.")
    return random.choice(roasts).format(VictimName)
    
def getGameEvents():  #returns a library of events
    #URL is localhost on port 2999
    url = "https://127.0.0.1:2999/liveclientdata/eventdata"
    try:
        #Verify = False in order to enable use
        response = requests.get(url, verify = False)
        return response.json()
    except Exception:
        pass
        
    
    




eventIDList = []
eventList = []

def updateEventList():
 
    output = getGameEvents()
    for event in output['Events']:
        if not event['EventID'] in eventIDList:
            eventIDList.append(event['EventID'])
            eventList.append(event)
            

def getLastEvent():
    if not eventList:
        return None
    else:
        return eventList[-1]

def checkFriends(friendName):
    output = False
    for friend in friends:
        if friend['IGN'] == friendName:
            output = True
            break
        else:
            output = False
    return output

def findFriend(friendName):
    output = None
    for friend in friends:
        if friend['IGN'] == friendName:
            output = friend['IRL']
    return output

def championKill():
    if checkFriends(getLastEvent()['VictimName']):
        response = getRoast(findFriend(getLastEvent()['VictimName']))
    else:
        response = "{} killed {}".format(getLastEvent()['KillerName'], getLastEvent()['VictimName'])
       
    return response

def towerKill():
    response = "{} destroyed a tower".format(getLastEvent()['KillerName'])
    return response

def firstBlood():
    response = "Wow! {} got first blood!".format(getLastEvent()['Recipient'])
    return response


def inhibKilled():
    inhibs = {
        'ORDER' : ['Barracks_T1_R1','Barracks_T1_C1','Barracks_T1_L1'],
        'CHAOS' : ['Barracks_T2_R1','Barracks_T2_C1','Barracks_T2_L1']
    }
    
    if getLastEvent()['InhibKilled'] in inhibs[checkPlayerTeam()]:
        response = 'God Damn it you guys lost an inhib. How retarded are you?'
    #print (getLastEvent()['InhibKilled'])
    else:
        response = 'You finally killed an inhib'
    return response

def firstTower():
    response = "{} destroyed the first tower".format(getLastEvent()['KillerName'])
    return response

def gameOver():
    response = "Game is done!"
    return response

def gameStart():
    response = 'The game has started'
    return response

def minions():
    response = 'Minions have spawned'
    return response

def dragonKill():
    response = '{} has slain the {} dragon'.format(getLastEvent()['KillerName'], getLastEvent()['DragonType'])
    return response

def baronKill():
    response = "{} has slain Baron Nashor".format(getLastEvent()['KillerName'])
    return response

def heraldKill():
    if checkFriends(getLastEvent()['KillerName']):
        response = "{} used all of his brainpower this game to kill a big crab. Good job".format(getLastEvent()['KillerName'])
    else:
        response = None
    return response

def multiKill():
    response = None
    return response

def checkPlayerTeam():
    try:
        #Verify = False in order to enable use
        response = requests.get('https://127.0.0.1:2999/liveclientdata/playerlist', verify = False)
        champs = response.json()
        for champ in champs:
            if champ['summonerName'] == getPlayerName():
                return champ['team']
    except Exception as e:
        print('Something happened, {}'.format(e))
        pass

def getPlayerName():
    try:
        url = 'https://127.0.0.1:2999/liveclientdata/activeplayername'
        name = requests.get(url, verify = False)
        return name.json()
    except Exception as e:
        print('Error getting player name, {}'.format(e))
        return None

def inhibRespawned():
    inhibs = {
        'ORDER' : ['Barracks_T1_R1','Barracks_T1_C1','Barracks_T1_L1'],
        'CHAOS' : ['Barracks_T2_R1','Barracks_T2_C1','Barracks_T2_L1']
    }

    if getLastEvent()['InhibRespawningSoon'] in inhibs[checkPlayerTeam()]:
        response = 'Your inhibitor is almost back up, do you think you can go 30 seconds without inting for once so it can respawn?'
    
    else:
        response = 'The enemies inhib is coming back up soon because you all were too stupid to end the game'
    
    return response

def inhibRespawn():
    inhibs = {
        'ORDER' : ['Barracks_T1_R1','Barracks_T1_C1','Barracks_T1_L1'],
        'CHAOS' : ['Barracks_T2_R1','Barracks_T2_C1','Barracks_T2_L1']
    }

    
    if getLastEvent()['InhibRespawned'] in inhibs[checkPlayerTeam()]:
        response = 'You managed to survive long enough for you inhib to respawn, good job monkeys'
    
    else:
        response = 'The enemies inhib respawned, all that work for nothing. Good job, Troggs'
    
    return response

def ace():
    #   to be implemented: checks if enemy ace or your ace
    response = "Ace"
    return response

def cases(case):
   
    switcher = {
        'ChampionKill' : championKill,
        'FirstBlood' : firstBlood,
        'FirstBrick' : firstTower,
        'TurretKilled' : towerKill,
        'InhibKilled' : inhibKilled,
        'GameEnd' : gameOver,
        'GameStart' : gameStart,
        'MinionsSpawning' : minions,
        'DragonKill' : dragonKill,
        'BaronKill' : baronKill,
        'HeraldKill' : heraldKill,
        'Multikill' : multiKill,
        'InhibRespawningSoon' : inhibRespawned,
        'InhibRespawned' : inhibRespawn,
        'Ace' : ace
    }
    
    return switcher[case]()

def main():
    run = True
    while run:
        
        size = len(eventList)
        try:
            updateEventList()
        except:
            run = False
            return 'Could not connect to game'
            
        if len(eventList) != size:
            lastEvent = getLastEvent()
            if not lastEvent == None:
                event_name = lastEvent['EventName']
                if event_name == 'GameEnd':
                    run = False
                    return 'League Game over! Type #GamerTime to restart the bot.'
                if not cases(event_name) == None:
                    return cases(event_name)
                
    sleep(2)
    eventIDList.clear()
    eventList.clear()


def test():
    pass
if __name__ == "__main__":
    test()        
    
