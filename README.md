# blackjackhilo
blackjackhilo
This is a project to simulate blackjack hi-lo counting strategy. Hi-lo counting is a basic counting strategy for blackjack that allows the player to gain an edge in blackjack when playing in casinos.

To run this simulation, download the repo and run the countingsim.py file. It will prompt you to for how many blackjack careers to simulate. After running the simulation it will present the average results including wins, losses, ties, blackjacks, double downs, splits, insurance if used, surrenders if used, as well as expected value of counting.

In the countingsim.py file, there is also a way to change it so that instead of some preset settings, the user can adjust blackjack counting specifications such as starting bankroll, session bankroll, true count(TC_OUT) to start playing, and many others. The countingsim.py file has documentation to describe all the variables and dictionary keys and what they do.

To change settings, open the countingsim.py file and click on the playerpref dictionary and adjust to your own liking. To change it everytime you run the simulation, comment out the playerpref dictionary and instead uncomment line 6:#playerpref = userInput(), this will allow you to change the settings everytime you run.

test run(without uncommenting line 6, if user types 1):
```
welcome to blackjack hi-lo simulator!
how many times would you like to play 100 sessions? 1
```
will print simul: 0......100 and then give a return result of:
```
start at 30000 dollars, playing 10000 per session results in 37470.0 dollars after 100 visits to the casino
participated in 100 visits
{'numOfSimul': 100, 'numOfTables': 25, 'sessionBankroll': 10000, 'otherPlayers': 2, 'betSpread': 16, 'unit': 15, 'blackjackPayout': 1.5, 'pen': 0.75, 'insurance': True, 'soft': True, 'doubleSplit': True, 'surrender': True}
{'playerwins': 17, 'playerlosses': 19, 'playerties': 3, 'doubled': 4, 'splits': 1, 'insurance': 3, 'blackjacks': 3, 'surrenders': 2, 'balance': 10075}
ruin: 0
career ruin: 0
```
