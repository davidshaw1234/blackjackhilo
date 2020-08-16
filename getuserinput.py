#gets user input and returns a dictionary containing their answers
#can also manually set inputs in countingsim.py

def userInput():

    #user inputs
    numOfSimul = input('Simulation/session count(int): ')#int
    numOfTables = input('How many tables would you like to wong per session(int): ')#int
    sessionBankroll = input('How much money would you like to play with in a session?(500 - 1000000): ')#int
    otherPlayers = input('How many other players?(1 - 5): ')#int
    betSpread = input('What is your bet spread? 1 to (choose 1-8): ')#int
    unit = input('what is one unit of your bet?:')#int

    blackjackPayout = input('How much would you like blackjacks to payout? (1.2,1.5, or 2): ')#float
    pen = input('Penetration ratio(0.0-1.0): ')#float

    insure = input('Insurance?(Y/N): ')#string
    soft17 = input('Will the dealer hit on soft seventeens?(Y/N): ')#string
    doubleAfterSplit = input('Are you allowed to double down after splitting?(Y/N): ')#string
    surrender = input('Are you allowed to surrender?: ')#string

    #convert string inputs to True or False
    insurance = True
    if str(insure) == 'Y' or  str(insure) == 'y':
        insurance = True
    else:
        insurance = False

    soft = True
    if str(soft17) == 'Y' or str(soft17) == 'y':
        soft = True
    else:
        soft = False 

    doubleSplit = True
    if str(doubleAfterSplit) == 'Y' or str(doubleAfterSplit) == 'y':
        doubleSplit = True
    else:
        doubleSplit = False
    
    surrender1 = True
    if str(surrender) == 'Y' or str(surrender) == 'y':
        surrender1 = True
    else:
        surrender1 = False

    return {
        'numOfSimul':int(numOfSimul),
        'numOfTables':int(numOfTables),
        'sessionBankroll':int(sessionBankroll),
        'otherPlayers':int(otherPlayers),
        'betSpread':int(betSpread),
        'unit':int(unit),
        'blackjackPayout':float(blackjackPayout),
        'pen':float(pen),

        'insurance':insurance,
        'soft':soft,
        'doubleSplit': doubleSplit,
        'surrender':surrender1
    }
   


