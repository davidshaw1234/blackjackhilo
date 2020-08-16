import tkinter as tk
import blackjack  as bj

#incomplete
#requires GUI implementation

class Application(tk.Tk):

    def __init__(self,*args,**kwargs):
        #parameters that can be changed in settings
        self.numDecks = 1
        self.insure = False 
        self.startMoney = 500

        tk.Tk.__init__(self,*args,**kwargs)
        container = tk.Frame(self)
        container.pack(side = 'top',fill ='both',expand = True)
        container.grid_rowconfigure(0,weight = 1)
        container.grid_columnconfigure(0,weight = 1)

        self.frames = {}
        for F in (StartPage, SettingPage, GamePage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)


    def show_frame(self,cont):
        frame = self.frames[cont]
        frame.tkraise()
    #functions for settings
    def updatedeck(self,input):
        self.numDecks = input

    def updateInsure(self):
        if self.insure == False:
            self.insure = True
        else:
            self.insure = False
    def updateStartMoney(self,amount):
        self.startMoney = amount

    def getNumDeck(self):
        return self.numDecks

    def getInsure(self):
        return self.insure
    
    def getMoney(self):
        return self.startMoney

class StartPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text = 'start page', font = ('verdana',12))
        label.pack(pady= 10,padx = 10)
        #widgets
        gameButton = tk.Button(self,text = 'Start Game', command = lambda: controller.show_frame(GamePage))
        gameButton.pack()
        settingButton = tk.Button(self,text = 'Settings',command = lambda: controller.show_frame(SettingPage))
        settingButton.pack()

class SettingPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text = 'settings', font = ('verdana',12))
        label.grid(row = 0,column =1)

        #widgets
        #update number of decks
        updateDeckLabel = tk.Label(self,text = 'enter # of decks', font = ('verdana',12))
        updateDeckLabel.grid(row = 1)
        updateDeckEntry = tk.Entry(self)
        updateDeckEntry.grid(row = 1, column = 1)
        updateDeckButton = tk.Button(self,text = 'update!',command = lambda: controller.updatedeck(updateDeckEntry))
        updateDeckButton.grid(row = 1,column = 2)

        #update insurance
        c = tk.Checkbutton(self, text = 'insurance',command = lambda: controller.updateInsure)
        c.grid(row = 2, columnspan = 2)


        #update money
        updateMoneyLabel = tk.Label(self,text = 'enter amount of money(default is 500)', font = ('verdana',12))
        updateMoneyLabel.grid(row = 3)
        updateMoneyEntry = tk.Entry(self)
        updateMoneyEntry.grid(row = 3, column = 1)
        updateMoneyButton = tk.Button(self,text = 'update!',command = lambda: controller.updateStartMoney(updateMoneyEntry))
        updateMoneyButton.grid(row = 3,column = 2)


        #back button
        backButton = tk.Button(self,text = 'back',command = lambda: controller.show_frame(StartPage))
        backButton.grid(row = 4,columnspan = 2)

class GamePage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text = 'game', font = ('verdana',12))
        label.grid(row = 0,column = 1,columnspan = 2)


        self.bet = 0


        #initializing blackjack game
        deckOfCards = bj.buildADeck(controller.getNumDeck())
        dealerStartingHand = []
        playerStartingHand = []
        
        self.thedealer = bj.dealer(dealerStartingHand,controller.getInsure())
        self.theplayer = bj.player(playerStartingHand,controller.getMoney())

        #game interface
        self.game = True
        self.betscreen = True
        self.gameplayscreen = False
        while(self.game):

            while(betscreen):
                betLabel = tk.Label(self,text = 'enter bet for this round', font = ('verdana',12))
                betLabel.grid(row = 1)
                betEntry = tk.Entry(self)
                betEntry.grid(row = 1, column = 1)
                updateDeckButton = tk.Button(self,text = 'place !',command = self.updateBet(betEntry))
                updateDeckButton.grid(row = 1,column = 2)
                currentbalancelabel = tk.Label(self,text ='current balance:'+str(theplayer.checkBalance()),font = ('verdana',12))
                currentbalancelabel.grid(row = 2)

            while(gameplayscreen):
                
                    #clear old hands and deal new ones
                    self.thedealer.clearHand()
                    self.theplayer.clearHand()
                    for x in range(1,3):
                        playerStartingHand.append(bj.dealCard(deckOfCards))
                        dealerStartingHand.append(bj.dealCard(deckOfCards))
                    self.thedealer.updateHand(dealerStartingHand)
                    self.theplayer.updateHand(playerStartingHand)

                    dealerLabel = tk.Label(self,text = 'dealer shows: ' + self.thedealer.getHand()[1].getCard())
                    dealerLabel.grid(row = 1)

                    playerLabel = tk.Label(self,text = 'player shows: '+ bj.showHand(self.theplayer.getHand(1)))
                    playerLabel.grid(row = 2)

                    hitButton = tk.Button(self,text = 'hit!',command = self.theplayer.hit(1,bj.dealCard(deckOfCards)))
                    hitButton.grid(row=3)

                #will show different widgets based on length of hand





        #widgets
        backButton = tk.Button(self,text = 'back',command = lambda: controller.show_frame(StartPage))
        backButton.grid(row = 10,column =1,columnspan =2)

    def updateBet(self,amount):
        self.bet = amount
        self.theplayer.updateBal(-amount)
        self.updateScreen()

    #switches between betscreen and gameplay screen
    def updateScreen(self):
        if self.betscreen == True:
            self.betscreen = False
            self.gameplayscreen = True
        else:
            self.betscreen = True
            self.gameplayscreen = False



app = Application()
app.mainloop()
