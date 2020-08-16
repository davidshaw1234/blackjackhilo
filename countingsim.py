import blackjack as bj 
from getuserinput import userInput

print('welcome to blackjack hi-lo simulator!')

#get user input if you want to manually adjust 
#playerpref = userInput()


#simulation
NUM_OF_DECKS = 6

#at what true count will player participate in the game aka "wonging
#wonging is when you backcount the table until your desired count
#rule of thumb is your edge starts at -.5% when TC_OUT = 0, and increases by .5% for every 1 point increase in TC_OUT
TC_OUT = 3

#what total bankroll the player can start with
INITIAL = 30000


#preset settings if not using Userinput()
playerpref = {
        'numOfSimul':100, #how many times a player will visit a casino
        'numOfTables':25, #how many tables the player will "wong" in the casino
        'sessionBankroll':10000, #money brought to visit
        'otherPlayers':2, #how many players are playing at the table excluding player and dealer
        'betSpread':16, #bet spread
        'unit':15, # base bet
        'blackjackPayout':1.5, 
        'pen':.75, # deck penetration before reshuffle

        'insurance':True, #will the dealer offer insurance?
        'soft':True, #will dealer hit or stay on soft 17
        'doubleSplit': True, # are you allowed to double after split?
        'surrender':True # are you allowed to surrender(recieve half your initial bet back but fold the hand)
    }

numOfCareers = input('how many times would you like to play ' + str(playerpref['numOfSimul'])  +' sessions?')


#total result tracker, will obtain averages of each statistic after the simulation
avgResults = {
    'playerwins':0,
    'playerlosses':0,
    'playerties':0,
    'doubled':0,
    'splits':0,
    'insurance':0,
    'blackjacks':0,
    'surrenders':0,
    'balance':0
}

#tracks how many times you will reduce to 10 percent or less of your session bankroll in one casino visit
ruin = 0
#tracks how often you will lose most of your entire bankroll in your blackjack career, usually will only occur after >50 career simulations
career_ruin = 0

#tracks how many casino visits do you actually participate in
playergames = 0

#run career simulations
for r in range(int(numOfCareers)):
    print(r)

    #resets bankroll
    bankroll = INITIAL

    #runs the sessions in a career
    for simul in range(playerpref['numOfSimul']):
        print('simul:' + str(simul))

        #creating players,dealers and bots, checks if player can still pursue blackjack career
        dealerobj = bj.dealer([])
        if bankroll >= playerpref['sessionBankroll']:
            bankroll -= playerpref['sessionBankroll']
        else:
            career_ruin +=1
            break
        mainplayerobj = bj.player([],playerpref['sessionBankroll'],False,True)

        listOfPlayers = []
        listOfPlayers.append(mainplayerobj)

        for x in range(playerpref['otherPlayers']):
            listOfPlayers.append(bj.player([],1000000000000,True,False))
        
        #stat tracker for each game
        statDic = {
        'playerwins':0,
        'playerlosses':0,
        'playerties':0,
        'rc':0,
        'tc':0,
        'doubled':0,
        'splits':0,
        'insurance':0,
        'blackjacks':0,
        'surrenders':0
        }
        playThisTable = False
        
        for tables in range(playerpref['numOfTables']):
            mainplayerobj.updatePlaying(False)

            deckOfCards = bj.buildADeck(NUM_OF_DECKS)
            TOTAL_LENGTH = len(deckOfCards)

            statDic['rc'] = 0
            statDic['tc'] = 0

            #will only play a hand if there enough cards to deal
            while(len(deckOfCards) > round(TOTAL_LENGTH*(1-playerpref['pen']))):
                statDic = bj.playARound(dealerobj,listOfPlayers,statDic,deckOfCards,playerpref,mainplayerobj)
                if statDic['tc'] >= TC_OUT:
                    playThisTable = True
                    mainplayerobj.updatePlaying(True)
                if statDic['tc'] < TC_OUT:
                    mainplayerobj.updatePlaying(False)       
                if mainplayerobj.getBal() < 0.1 * playerpref['sessionBankroll']:
                    ruin += 1
                    break

        avgResults['playerwins'] += statDic['playerwins']
        avgResults['playerlosses'] += statDic['playerlosses']
        avgResults['playerties'] += statDic['playerties']
        avgResults['doubled'] += statDic['doubled']
        avgResults['splits'] += statDic['splits']
        avgResults['insurance'] += statDic['insurance']
        avgResults['blackjacks'] += statDic['blackjacks']
        avgResults['surrenders'] += statDic['surrenders']


        if playThisTable:
            playergames +=1
            avgResults['balance'] += mainplayerobj.getBal()
                
        bankroll += mainplayerobj.getBal()

#averages the results
for x in avgResults.keys():
    avgResults[x] = round(avgResults[x]/playergames)

#will only print the most recent career simulation performance
print('start at ' + str(INITIAL) + ' dollars, playing ' +str(playerpref['sessionBankroll']) + ' per session results in ' + str(bankroll) + ' dollars after ' + str(playerpref['numOfSimul']) + ' visits to the casino')

#how many casino visits did the player actually participate in total out of (careers * numOfSessions)
print('participated in ' +str(playergames) +' visits')

#prints the player settings
print(playerpref)

#prints total average results out of playergames variable
print(avgResults)

#prints ruin occurences
print('ruin: ' + str(ruin))
print('career ruin: ' + str(career_ruin))
