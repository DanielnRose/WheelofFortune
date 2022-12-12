from config import dictionaryloc
from config import turntextloc
from config import wheeltextloc
from config import maxrounds
from config import vowelcost
from config import roundstatusloc
from config import finalprize
from config import finalRoundTextLoc

import random

players={0:{"roundtotal":0,"gametotal":0,"name":""},
         1:{"roundtotal":0,"gametotal":0,"name":""},
         2:{"roundtotal":0,"gametotal":0,"name":""},
        }

roundNum = 0
dictionary = []
turntext = ""
wheellist = []
roundWord = ""
blankWord = []
vowels = {"a", "e", "i", "o", "u"}
roundstatus = ""
finalroundtext = ""


def readDictionaryFile():
    global dictionary
    # Read dictionary file in from dictionary file location
    # Store each word in a list.
    with open(dictionaryloc) as f:
        lines = f.readlines()
    dictionary = [words.replace("\n","") for words in lines]
    
def readTurnTxtFile():
    global turntext   
    #read in turn intial turn status "message" from file
    with open(turntextloc) as f:
        lines = f.readlines()
    turntext = [words.replace("\n","") for words in lines]
        
def readFinalRoundTxtFile():
    global finalroundtext   
    #read in turn intial turn status "message" from file
    with open(finalRoundTextLoc) as f:
        lines = f.readlines()
    finalroundtext = [words.replace("\n","") for words in lines]

def readRoundStatusTxtFile():
    global roundstatus
    # read the round status  the Config roundstatusloc file location 
    with open(roundstatusloc) as f:
        lines = f.readlines()
    roundstatus = [words.replace("\n","") for words in lines]

def readWheelTxtFile():
    global wheellist
    # read the Wheel name from input using the Config wheelloc file location 
    with open(wheeltextloc) as f:
        lines = f.readlines()
    wheellist = [words.replace("\n","") for words in lines]

def getPlayerInfo():
    global players
    # read in player names from command prompt input
    for p in players:
        players[p]['name'] = input(f"Enter player {p+1}'s name: ")
        print()

def gameSetup():
    # Read in File dictionary
    # Read in Turn Text Files
    global turntext
    global dictionary
        
    readDictionaryFile()
    readTurnTxtFile()
    readWheelTxtFile()
    getPlayerInfo()
    readRoundStatusTxtFile()
    readFinalRoundTxtFile() 
    
def getWord():
    global dictionary
    global roundWord
    global blankWord

    #choose random word from dictionary
    #make a list of the word with underscores instead of letters.
    roundWord = dictionary[random.randrange(0,len(dictionary))]
    blankWord = "_" * len(roundWord)
    roundUnderscoreWord = "-" * len(roundWord)

    return roundWord,roundUnderscoreWord

def wofRoundSetup():
    global players
    global roundWord
    global blankWord
    # Set round total for each player = 0
    # Return the starting player number (random)
    # Use getWord function to retrieve the word and the underscore word (blankWord)
    for p in players:
        players[p]['roundtotal'] = 0

    roundWord, blankWord = getWord()
    initPlayer = random.randrange(1,4)
    return initPlayer


def spinWheel(playerNum):
    global wheellist
    global players
    global vowels

    # Get random value for wheellist
    # Check for bankrupcy, and take action.
    # Check for loose turn
    # Get amount from wheel if not loose turn or bankruptcy
    # Ask user for letter guess
    # Use guessletter function to see if guess is in word, and return count
    # Change player round total if they guess right.   
      
    wheelval = wheellist[random.randrange(0, len(wheellist))]
    if wheelval == "BANKRUPT":
        print("You Went BANKRUPT!!! \n")
        players[playerNum]['roundtotal'] = 0
        stillinTurn = False
    elif wheelval == "Loose a turn":
        print("You Loose a Turn :( \n")
        stillinTurn = False
    else:
        #add value
        print(f"You landed on ${wheelval}!")
        letter = input("Guess a letter: ")
        goodguess, count, letter = guessletter(letter)
        if goodguess == True:
            stillinTurn = True
            print(f"{letter} was in the word {count} times")
            players[playerNum]['roundtotal'] += int(wheelval)
        else:
            print(f'{letter} was not in the word')
            stillinTurn = False

    return stillinTurn


def guessletter(letter, v = 0): 
    global players
    global blankWord
    global roundWord
    # parameters:  take in a letter guess and player number
    # Change position of found letter in blankWord to the letter instead of underscore 
    # return goodGuess= true if it was a correct guess
    # return count of letters in word. 
    # ensure letter is a consonate.
    if v == 0:
        while letter in vowels and letter.isalpha():
            letter = input("Guess a consonate: ")
    newblankword = []
    l = 0
    count = 0
    goodGuess = False
    while l < len(roundWord):
        if roundWord[l] == letter:
            newblankword.append(roundWord[l])
            goodGuess = True
            count = count + 1
        elif blankWord[l] != "-" and blankWord[l] != "_":
            newblankword.append(roundWord[l])
        else:
            newblankword.append("_")
        l = l + 1

    blankWord = "".join(newblankword)

    return goodGuess, count, letter

def buyVowel(playerNum):
    global players
    global vowels
    global blankWord
    global roundWord

    # Take in a player number
    # Ensure player has 250 for buying a vowelcost
    # Use guessLetter function to see if the letter is in the file
    # Ensure letter is a vowel
    # If letter is in the file let goodGuess = True
    goodGuess = False
    if players[playerNum]['roundtotal'] >= 250:
        players[playerNum]['roundtotal'] -= 250
        letter = input("Guess a Vowel: ")
        while letter.isalpha() and letter not in vowels:
            letter = input("Buy a Vowel: ")
        l = 0
        count = 0
        goodGuess = False
        newblankword = []
        while l < len(roundWord):
            if roundWord[l] == letter:
                newblankword.append(roundWord[l])
                goodGuess = True
                count = count + 1
            elif blankWord[l] != "-" and blankWord[l] != "_":
                newblankword.append(roundWord[l])
            else:
                newblankword.append("_")
            l = l + 1
        blankWord = "".join(newblankword)
    else:
        print("You do not have enough money")
        return True
    return goodGuess      
        
def guessWord(playerNum, v = 0):
    global players
    global blankWord
    global roundWord
    
    # Take in player number
    # Ask for input of the word and check if it is the same as wordguess
    # Fill in blankList with all letters, instead of underscores if correct 
    # return False ( to indicate the turn will finish)  
    
    word = input("Enter a word: ")
    if word == roundWord:
        blankWord = word
        if v == 0:
            print("You have won the round")
            players[playerNum]['gametotal'] += players[playerNum]['roundtotal']
        return False
    print("Incorrect word")
    return False
    
    
def wofTurn(playerNum):  
    global roundWord
    global blankWord
    global turntext
    global players

    # take in a player number. 
    # use the string.format method to output your status for the round
    # and Ask to (s)pin the wheel, (b)uy vowel, or G(uess) the word using
    # Keep doing all turn activity for a player until they guess wrong
    # Do all turn related activity including update roundtotal 
    
    stillinTurn = True
    while stillinTurn:
        newtextturn = turntext
        print(f"|{blankWord}|")
        newtextturn[0] = f"{players[playerNum]['name']}'s turn \nYou have {players[playerNum]['roundtotal']}"
        print()
        print("\n".join(newtextturn))
        print()
        choice = input("Select an action: ")
        print()
        # use the string.format method to output your status for the round
        # Get user input S for spin, B for buy a vowel, G for guess the word
        

        if(choice.strip().upper() == "S"):
            stillinTurn = spinWheel(playerNum)
        elif(choice.strip().upper() == "B"):
            stillinTurn = buyVowel(playerNum)
        elif(choice.upper() == "G"):
            stillinTurn = guessWord(playerNum)
        else:
            print("Not a correct option")        
    return(stillinTurn)
    # Check to see if the word is solved, and return false if it is,
    # Or otherwise break the while loop of the turn.     


def wofRound(roundnumber):
    global players
    global roundWord
    global blankWord
    global roundstatus
    initPlayer = wofRoundSetup()
    firstplayer = random.randrange(1,4)
    print()
    print("The first player is player " + players[firstplayer-1]['name'])
    # Keep doing things in a round until the round is done ( word is solved)
        # While still in the round keep rotating through players
        # Use the wofTurn fuction to dive into each players turn until their turn is done.
    turns = True
    turnstrue = True
    turncounter = 0
    while turnstrue:
        wofTurn((turncounter + firstplayer - 1) % 3)
        turncounter = turncounter + 1
        if blankWord == roundWord:
            turnstrue = False
    print("----------------------------------------------")
    print(f"After round {roundnumber + 1}")
    
    for p in players:
        print(f"{players[p]['name']} has ${players[p]['gametotal']}")
    # Print roundstatus with string.format, tell people the state of the round as you are leaving a round.

def wofFinalRound():
    global roundWord
    global blankWord
    global finalroundtext
    global players
    winplayer = 0
    amount = 0

    # Find highest gametotal player.  They are playing.
    # Print out instructions for that player and who the player is.
    # Use the getWord function to reset the roundWord and the blankWord ( word with the underscores)
    # Use the guessletter function to check for {'R','S','T','L','N','E'}
    # Print out the current blankWord with whats in it after applying {'R','S','T','L','N','E'}
    # Gather 3 consonats and 1 vowel and use the guessletter function to see if they are in the word
    # Print out the current blankWord again
    # Remember guessletter should fill in the letters with the positions in blankWord
    # Get user to guess word
    # If they do, add finalprize and gametotal and print out that the player won 

    highmoney = 0
    highnumber = 0
    x = 0
    while x < 3:
        if players[x]["gametotal"] >= highmoney:
            highmoney = players[x]["gametotal"]
            highnumber = x
        x += 1
    
    print(f"Player {players[highnumber]['name']} is up for the final round \n")
    roundWord,blankWord = getWord()
    guessletter("r")
    guessletter("s")
    guessletter("t")
    guessletter("l")
    guessletter("n")
    guessletter("e", 1)

    print(f"Final round's word: {blankWord}")
    letter = input("Guess 3 consanants and one vowel seperated by spaces: ")
    guesses = letter.split(" ")
    guessletter(guesses[0])
    guessletter(guesses[1])
    guessletter(guesses[2])
    guessletter(guesses[3], 1)
    print()
    print(f"Final round's word: {blankWord}")
    print()
    guessWord(highnumber, 1)
    if ("_" or "-") in blankWord:
        print(f"That was incorrect \nThe word was {roundWord}")
    else:
        players[highnumber]["gametotal"] += finalprize
        print(f"Congragulations, You won {finalprize} \nYour Final total is {players[highnumber]['gametotal']}")
        


def main():
    global players
    gameSetup()  
    for i in range(0,maxrounds):
        if i in [0,1]:
            wofRound(i)
        else:
            wofFinalRound()

if __name__ == "__main__":
    main()
    
    
