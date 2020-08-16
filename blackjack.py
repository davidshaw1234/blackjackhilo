#implementation for playing a blackjack game
import random
from math import floor

#card object  
class Card:
    def __init__(self,suit,val):
        self.suit = suit
        self.val = val
    def getSuit(self):
        return self.suit
    def getVal(self):
        return self.val
    def getCard(self):
        return str(self.val) + ' of ' + self.suit


#returns a list containing values of a hand
def getHandVal(hand):
    l = []
    for c in hand:
        l.append(c.getVal())
    return l

#returns a string showing hand
def showHand(hand):
    handstring = "hand is"
    for card in hand:
        handstring = handstring + card.getCard() + ','
    return handstring

#returns a shuffled deck given number of decks
def buildADeck(number_of_decks):
    cards = []
    for x in range(number_of_decks):
        for x in ['spades','hearts','diamonds','clubs']:
            for r in range(1,14):
                cards.append(Card(x,r))
    random.shuffle(cards)
    return cards

#returns blackjack value of card, returns 11 for ACE
def getbjval(card):
    if card.getVal() in range(2,10):
        return card.getVal()
    elif card.getVal() in range(10,14):
        return 10
    else:
        return 11

#takes a list of cards(hand) and returns blackjack rank
def getbjrank(hand):
    numlist = []
    for x in hand:
        numlist.append(getbjval(x))
    aceOccur = numlist.count(11)
    if aceOccur > 0:
        total = sum(numlist)
        if aceOccur == 1 and total > 21:
            total -= 10
            return total
        elif aceOccur == 1 and total <=21:
            return total
        else:
            for x in range(aceOccur):
                total -= 10
                if total < 21:
                    return total
            return total
    else:
        total = sum(numlist)
        return total

#returns True if card is in, False if bust
def checkHand(hand):
    if getbjrank(hand) > 21:
        return False
    else:
        return True

#checks whether a value is in a hand
def isValueInHand(value,hand):
    for x in hand:
        if x.getVal() == value:
            return True
        else: 
            return False

#returns the count of a card given a card using hi-lo counting
def getCount(inputcard):
    if inputcard.getVal() in range(2,7):
        return 1
    if inputcard.getVal() in range(7,10):
        return 0
    if inputcard.getVal() in range(10,14) or inputcard.getVal() == 1:
        return -1

#returns the winner of the hand, 1 if dealer wins(first hand input), -1 if player wins(second hand input), 0 if tie
def whoWins(dealerhand,playerhand):
    dealerValue = getbjrank(dealerhand)
    playerValue = getbjrank(playerhand)
    if dealerValue > 21:
        if playerValue > 21:
            return 1
        else:
            return -1
    else:
        if playerValue > 21:
            return 1
        else:
            if dealerValue > playerValue:
                return 1
            elif dealerValue == playerValue:
                return 0
            else: 
                return -1

#returns True if blackjack, false otherwise
def blackjackhand(hand):
    if len(hand) == 2 and getbjrank(hand) == 21:
        return True
    else:
        return False


#returns player action using basic strategy, and indexes illustrious 18 and fab 4 deviations if surrender is allowed
#blackjacks should not be an input value
#returns 's' if player should stay
#returns 'd' if player should double down
#returns 'h' if player should hit
#returns 'sp' if player should split
#returns 'sr' if player should surrender
def playerAction(topCard,playerHand,playerpref,tc): 

    if len(playerHand) == 1:
        return 'h'

    #if blackjack or bust player will stay
    if getbjrank(playerHand) >= 21:
        return 's'

    dealerVal = getbjval(topCard)
    hardTotal = getbjrank(playerHand)

    #checks for surrender
    if playerpref['surrender'] and len(playerHand) == 2:
        hitOn17 = playerpref['soft']
        if getbjrank(playerHand) == 14 and dealerVal == 10 and tc >= 4:
            return 'sr'
        if getbjrank(playerHand) == 15 and dealerVal == 9 and tc >= 3:
            return 'sr'
        elif getbjrank(playerHand) == 15 and dealerVal == 10 and tc >= 0:
            return 'sr'
        elif getbjrank(playerHand) == 15 and dealerVal == 11:
            if tc >= -1 and hitOn17:
                return 'sr'
            elif tc >= 2 and not hitOn17:
                return 'sr'

    #checks starting hand strategy
    if len(playerHand) == 2:
        handVal = getHandVal(playerHand)
        doubleSplit = playerpref['doubleSplit']

        #check for pairsplit
        if handVal[0] == handVal[1]:
            if handVal[0] in (1,8):
                return 'sp'
            elif handVal[0] == 9:
                if dealerVal in (2,3,4,5,6,8,9):
                    return 'sp'
            elif handVal[0] == 7:
                if dealerVal in range(2,8):
                    return 'sp'
            elif handVal[0] == 6:
                if dealerVal in range(3,7):
                    return 'sp'
                elif doubleSplit == True and dealerVal == 2:
                    return 'sp'
            elif handVal[0] == 4 and doubleSplit == True:
                if dealerVal in range(5,7):
                    return 'sp'
            elif handVal[0] == 3:
                if dealerVal in range(4,8):
                    return 'sp'
                elif doubleSplit == True and dealerVal in range(2,4):
                    return 'sp'
            elif handVal[0] == 2:
                if dealerVal in range(4,8):
                    return 'sp'
                elif doubleSplit == True and dealerVal in range(2,4):
                    return 'sp'
        
        #check soft totals
        if 1 == handVal.count(1):
            softTotal = sum(handVal)
            if softTotal == 10:
                return 's'
            elif softTotal == 9:
                if dealerVal in (2,3,4,7,8,9,10,11):
                    return 's'
                elif (dealerVal == 6 or dealerVal == 5) and tc >= 1:
                    return 'd'
                else:
                    return 's'
            elif softTotal == 8:
                if dealerVal in range(2,7):
                    return 'd'
                elif dealerVal in (7,8):
                    return 's'
                else:
                    return 'h'
            elif softTotal == 7:
                if dealerVal in (2,7,8,9,10,11):
                    return 'h'
                else:
                    return 'd'
            elif softTotal == 6:
                if dealerVal in (2,3,7,8,9,10,11):
                    return 'h'
                else:
                    return 'd'
            elif softTotal == 5:
                if dealerVal in (2,3,7,8,9,10,11):
                    return 'h'
                else:
                    return 'd'
            elif softTotal == 4:
                if dealerVal in (2,3,4,7,8,9,10,11):
                    return 'h'
                else: 
                    return 'd'
            elif softTotal == 3:
                if dealerVal in (2,3,4,7,8,9,10,11):
                    return 'h'
                else: 
                    return 'd'
        

        #check hardtotals
        if hardTotal in range(17,22):
                return 's'
        if hardTotal in range(13,17):
            if dealerVal in range(2,7):
                if dealerVal == 3 and hardTotal == 13 and tc < -2:
                    return 'h'
                elif dealerVal == 2 and hardTotal == 13 and tc < -1:
                    return 'h'
                else:
                    return 's'
            elif  dealerVal == 10 and hardTotal == 16 and tc >=0:
                return 's'
            elif dealerVal == 9 and hardTotal == 16 and tc >5:
                return 's'
            elif dealerVal == 10 and hardTotal == 15 and tc >4:
                return 's'
            else:
                return 'h'
        if hardTotal == 12:
            if dealerVal in (2,3,7,8,9,10,11):
                if dealerVal == 2 and tc >= 3:
                    return 's'
                elif dealerVal == 2 and tc < 3:
                    return 'h'
                if dealerVal == 3 and tc >= 2:
                    return 's'
                elif dealerVal == 3 and tc < 2:
                    return 'h'
                if dealerVal == 4 and tc >= 0:
                    return 's'
                elif dealerVal == 4 and tc < 0:
                    return 'h'
                if dealerVal == 5 and tc >= -2:
                    return 's'
                elif dealerVal == 5 and tc < -2:
                    return 'h'
                if dealerVal == 6 and tc >= -1:
                    return 's'
                elif dealerVal == 6 and tc < -1:
                    return 'h'
                else:
                    return 'h'
            else:
                return 's'
        if hardTotal == 11:
            if dealerVal == 11 and tc >= 1:
                return 'd'
            elif dealerVal == 11 and tc < 1:
                return 'h'
            return 'd'
        if hardTotal == 10:
            if dealerVal in range(2,10):
                return 'd'
            elif dealerVal in (10,11) and tc >= 4:
                return 'd'
            else:
                return 'h'
        if hardTotal == 9:
            if dealerVal in range(3,7):
                return 'd'
            elif dealerVal == 7 and tc >= 4:
                return 'd'
            elif dealerVal == 2 and tc >= 1:
                return 'h'
            else:
                return 'h'
        if hardTotal <= 8:
            if hardTotal == 8 and dealerVal == 6 and tc >= 1:
                return 'd'
            elif hardTotal == 8 and dealerVal == 5 and tc >= 3:
                return 'd'
            else:
                return 'h'

    #if hand has more than 2 cards, uses hardTotal strategy
    else:
        if hardTotal in range(17,22):
                return 's'
        if hardTotal in range(13,17):
            if dealerVal in range(2,7):
                if dealerVal == 3 and hardTotal == 13 and tc < -2:
                    return 'h'
                elif dealerVal == 2 and hardTotal == 13 and tc < -1:
                    return 'h'
                else:
                    return 's'
            elif  dealerVal == 10 and hardTotal == 16 and tc >=0:
                return 's'
            elif dealerVal == 9 and hardTotal == 16 and tc >5:
                return 's'
            elif dealerVal == 10 and hardTotal == 15 and tc >4:
                return 's'
            else:
                return 'h'
        if hardTotal == 12:
            if dealerVal in (2,3,7,8,9,10,11):
                if dealerVal == 2 and tc >= 3:
                    return 's'
                elif dealerVal == 2 and tc < 3:
                    return 'h'
                if dealerVal == 3 and tc >= 2:
                    return 's'
                elif dealerVal == 3 and tc < 2:
                    return 'h'
                if dealerVal == 4 and tc >= 0:
                    return 's'
                elif dealerVal == 4 and tc < 0:
                    return 'h'
                if dealerVal == 5 and tc >= -2:
                    return 's'
                elif dealerVal == 5 and tc < -2:
                    return 'h'
                if dealerVal == 6 and tc >= -1:
                    return 's'
                elif dealerVal == 6 and tc < -1:
                    return 'h'
                else:
                    return 'h'
            else:
                return 's'
        if hardTotal == 11:
            if dealerVal == 11 and tc >= 1:
                return 'd'
            elif dealerVal == 11 and tc < 1:
                return 'h'
            return 'd'
        if hardTotal == 10:
            if dealerVal in range(2,10):
                return 'd'
            elif dealerVal in (10,11) and tc >= 4:
                return 'd'
            else:
                return 'h'
        if hardTotal == 9:
            if dealerVal in range(3,7):
                return 'd'
            elif dealerVal == 7 and tc >= 4:
                return 'd'
            elif dealerVal == 2 and tc >= 1:
                return 'h'
            else:
                return 'h'
        if hardTotal <= 8:
            return 'h'
   
#how bots will play
def botAction(topCard,playerHand):
    botHand = getbjrank(playerHand)
    if botHand > 21:
        return 's'
    else:
        if botHand >= 17:
            return 's'
        elif botHand > 10+getbjval(topCard):
            return 's'
        else:
            return 'h'


#player objects, for bots and regular player
class player():
    def __init__(self,hand,amt_of_money,playing,truePlayer):
        self.money = amt_of_money
        self.handnumber = 1
        self.hands = {self.handnumber:hand}
        self.play = playing
        self.truePlayer = truePlayer
    

    def getHands(self):
        return self.hands

    def isTruePlayer(self):
        return self.truePlayer

    def isPlaying(self):
        return self.play
    
    def updatePlaying(self,isPlay):
        self.play = isPlay

    def updateBal(self,amount):
        self.money = self.money + amount
    
    def getHandNumber(self):
        return self.handnumber

    def getHand(self,key):
        return self.hands[key]
    
    def getBal(self):
        return self.money

    def split(self,key):
        self.hands.update({key+1:[self.hands[key].pop()]})
        #update number of hands
        self.handnumber = self.handnumber + 1

    def hit(self,key,card):
        self.hands[key].append(card)
    
    def clearHand(self):
        self.handnumber = 1
        self.hands = {self.handnumber:[]}

    def updateHand(self,hand):
        self.hands.update({self.handnumber:hand})


#dealer object
class dealer():
    def __init__(self,hand):
        self.hand = hand 

    def hit(self,card):
        self.hand.append(card)

    #returns True if dealer needs to hit, false otherwise
    def needToHit(self):
        if getbjrank(self.hand) <= 16:
            return True
        else:
            return False

    def clearHand(self):
        self.hand = []

    def updateHand(self,hand):
        self.hand = hand

    def getHand(self):
        return self.hand


#betstrat1 depends on spread and unit, betstrat2 and 3 follow bankroll management rules/kelly criterion approximation
def betStrat1(tc,spread):

    if spread >= 15:
        if tc <= 2:
            return 1
        elif tc == 3:
            return 2
        elif tc == 4:
            return 8
        elif tc >= 5:
            return spread

    if spread >= 10:
        if tc <= 2:
            return 1
        elif tc == 3:
            return 4
        elif tc == 4:
            return 6
        elif tc >= 5:
            return spread
    
    if tc <= 0:
        return 1
    elif tc == 1:
        if spread > 1:
            return 2
        else:
            return 1
    elif tc == 2:
        if spread > 2:
            return 3
        elif spread > 1:
            return 2
        else:
            return 1
    elif tc == 3:
        if spread >3:
            return 4
        elif spread > 2:
            return 3
        elif spread > 1:
            return 2
        else:
            return 1
    elif tc >= 4:
        if spread > 4:
            return spread
        elif spread > 3:
            return 4
        elif spread > 2:
            return 3
        elif spre > 1:
            return 2
        else:
            return 1
def betStrat2(tc,playerBal,betSize):
    if tc <= 1:
        return playerBal * .5 *betSize
    elif tc == 2:
        return playerBal  *betSize
    elif tc == 3:
        return playerBal * 2 * betSize
    else:
        return playerBal * 5 * betSize
def betStrat3(playerBal,betSize):
    return playerBal * betSize

#simulates one round of blackjack
#WILL ONLY PLAY WHEN THE TRUE COUNT IS 0 and WHEN PLAYER HAS ENOUGH MONEY
#returns a dictionary with updated trackingDic
def playARound(thedealer,listOfPlayers,trackingDic,deck,playerpref,mainplayerobj):


    playerwins = trackingDic['playerwins']
    playerlosses = trackingDic['playerlosses']
    playerties = trackingDic['playerties']
    rc = trackingDic['rc']
    tc = trackingDic['tc']
    doubled = trackingDic['doubled']
    splits = trackingDic['splits']
    insuranceC = trackingDic['insurance']
    bjCount = trackingDic['blackjacks']
    surr = trackingDic['surrenders']

    returnDic = {
                'playerwins':playerwins,
                'playerlosses':playerlosses,
                'playerties':playerties,
                'rc':rc,
                'tc':tc,
                'doubled':doubled,
                'splits':splits,
                'insurance':insuranceC,
                'blackjacks':bjCount,
                'surrenders':surr
    }

    #betting strategy, can only choose 1
        #strat 1
    spread = playerpref['betSpread']
    betRatio = betStrat1(tc,spread)
    playerbet = betRatio * playerpref['unit']
        #strat 2
    #playerbet = betStrat2(tc,mainplayerobj.getBal(),0.005)
        #strat 3
    #playerbet = betStrat3(mainplayerobj.getBal(),.01)


    #list of hand keys where player double downed to track payout
    doubledownlist = []
    #list of hand keys where player surrendered to track payout
    surrenderlist = []

    #let player place bet
    for p in listOfPlayers:
        if p.isPlaying():
            if p.isTruePlayer():
                    p.updateBal(-1 * playerbet)

    #clears hands of players and dealer
    thedealer.clearHand()
    for p in listOfPlayers:
        p.clearHand()

    #deals cards from the deck to players and dealer
    for p in listOfPlayers:
        if p.isPlaying() == True:
            c = deck.pop()
            p.hit(1,c)
            rc += getCount(c)
    dealerc1 = deck.pop()
    thedealer.hit(dealerc1)
    rc += getCount(dealerc1)

    for p in listOfPlayers:
        if p.isPlaying() == True:
            c = deck.pop()
            p.hit(1,c)
            rc += getCount(c)

    dealerc2 = deck.pop()
    thedealer.hit(dealerc2)
    rc += getCount(dealerc2)


    #check to see if player got 21 in the flop
    for p in listOfPlayers:
        if p.isTruePlayer() == True:
            if p.isPlaying() == True:
                if getbjrank(p.getHand(1)) == 21 and getbjrank(thedealer.getHand()) != 21:
                    p.updateBal((1+playerpref['blackjackPayout'])*playerbet)
                    returnDic['blackjacks'] += 1
                    returnDic['playerwins'] += 1
                    p.updatePlaying(False)
                elif getbjrank(p.getHand(1)) == 21 and getbjrank(thedealer.getHand()) == 21:
                    p.updateBal(playerbet)
                    returnDic['blackjacks'] += 1
                    returnDic['playerties'] += 1
                    p.updatePlaying(False)
                

    #if dealer shows an Ace, check for insurance
    if thedealer.getHand()[1].getVal() == 1:
        if playerpref['insurance'] == True:
            for p in listOfPlayers:
                if p.isTruePlayer() == True and p.isPlaying() == True:
                    if (floor(rc/(floor(len(deck)/52))+1) >= 3): 
                        returnDic['insurance'] += 1
                        if getbjrank(thedealer.getHand()) == 21:
                            p.updateBal(playerbet)
                            returnDic['playerlosses'] +=1
                            returnDic['rc'] = rc
                            returnDic['tc'] = floor(rc/(floor(len(deck)/52))+1)
                            return returnDic
                        else:
                            p.updateBal(-1 * playerbet)

                        
    #checks if dealer has 21 given they show a face card
    if getbjrank(thedealer.getHand()) == 21:
        for p in listOfPlayers:
            if p.isPlaying() and p.isTruePlayer():
                returnDic['playerlosses'] += 1
        returnDic['rc'] = rc
        returnDic['tc'] = floor(rc/((len(deck)/52)+1))
        return returnDic


    #how the players will play the hand
    for p in listOfPlayers:
        if p.isPlaying() == True:
             #player action
            if p.isTruePlayer() == True:
                checkingAllHands = True
                while(checkingAllHands):
                    listOfHands = list(p.getHands().items())
                    howManyHands = len(listOfHands)
                    for hands in listOfHands:
                        inPlay = True
                        while(inPlay):
                            truecount = floor(rc/(floor(len(deck)/52)+1))
                            if playerAction(thedealer.getHand()[1],hands[1],playerpref,truecount) == 's':
                                inPlay = False
                            elif playerAction(thedealer.getHand()[1],hands[1],playerpref,truecount) == 'h':
                                hitcard = deck.pop()
                                rc += getCount(hitcard)
                                p.hit(hands[0],hitcard)
                            elif ((playerAction(thedealer.getHand()[1],hands[1],playerpref,truecount) == 'd') and (p.getBal() >= playerbet)):
                                returnDic['doubled'] += 1
                                hitcard = deck.pop()
                                rc += getCount(hitcard)
                                p.hit(hands[0],hitcard)
                                doubledownlist.append(hands[0])
                                p.updateBal(-1 * playerbet)
                                inPlay = False
                            elif ((playerAction(thedealer.getHand()[1],hands[1],playerpref,truecount) == 'sp') and (p.getBal() >= playerbet)):
                                returnDic['splits'] += 1
                                p.split(hands[0])
                                p.updateBal(-1*playerbet)
                                hitcard = deck.pop()
                                rc += getCount(hitcard)
                                p.hit(hands[0],hitcard)
                            elif playerAction(thedealer.getHand()[1],hands[1],playerpref,truecount) == 'sr':
                                surrenderlist.append(hands[0])
                                returnDic['surrenders'] += 1
                                p.updateBal(.5 * playerbet)
                                inPlay = False
                            elif ((p.getBal() < playerbet) and (botAction(thedealer.getHand()[1],hands[1]) == 's')):
                                inPlay = False
                            elif ((p.getBal() < playerbet) and (botAction(thedealer.getHand()[1],hands[1]) == 'h')):
                                hitcard = deck.pop()
                                rc += getCount(hitcard)
                                p.hit(hands[0],hitcard)
                    if howManyHands == len(p.getHands()):
                        checkingAllHands = False            
            #bot action
            else:
                inPlay = True
                while(inPlay):
                    if botAction(thedealer.getHand()[1],p.getHand(1)) == 's':
                        inPlay = False
                    else:
                        hitcard = deck.pop()
                        rc += getCount(hitcard)
                        p.hit(1,hitcard)


    #how the dealer will play the hand

        #if dealer hits on soft 17 he will hit
    if 1 in getHandVal(thedealer.getHand()) and sum(getHandVal(thedealer.getHand())) == 7:
        if playerpref['soft'] == True:
            c = deck.pop()
            thedealer.hit(c)
            rc += getCount(c)
    while(thedealer.needToHit()):
        c = deck.pop()
        thedealer.hit(c)
        rc += getCount(c)

    #calculate how much payout
    payoutratio = 0
    for p in listOfPlayers:
        if p.isPlaying() == True:
            if p.isTruePlayer() == True:
                for hands in p.getHands().items():
                    #do blackjack payout
                    if hands[0] in surrenderlist:
                        returnDic['playerlosses'] += 1
                        continue
                    if blackjackhand(hands[1]) == True and whoWins(thedealer.getHand(),hands[1]) == -1:
                        payoutratio += (1+ playerpref['blackjackPayout'])
                        returnDic['playerwins'] += 1
                        returnDic['blackjacks'] += 1
                        continue
                    if whoWins(thedealer.getHand(),hands[1]) == 1:
                        returnDic['playerlosses'] +=1
                        continue
                    elif whoWins(thedealer.getHand(),hands[1]) == 0:
                        if hands[0] in doubledownlist:
                            returnDic['playerties'] +=1
                            payoutratio += 2
                        else:
                            returnDic['playerties'] += 1
                            payoutratio += 1
                    elif whoWins(thedealer.getHand(),hands[1]) == -1:
                        if hands[0] in doubledownlist:
                            returnDic['playerwins'] +=1
                            payoutratio += 4
                        else:
                            returnDic['playerwins'] +=1
                            payoutratio += 2
                p.updateBal(payoutratio*playerbet)

    returnDic['rc'] = rc
    returnDic['tc'] = floor(rc/(floor(len(deck)/52)+1))

    return returnDic

