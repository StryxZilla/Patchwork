'''
Created on Nov 3, 2019

@author: Andy
'''
import boardFile as bf

class board:
    def __init__(self, configFile = {}):
        self.contents = {}
        self.tokenPos = 0
        self.nextOptions = {}
        self.boardpieces = 33
        self.singletokens = [26,32,38,44,50]
        self.buttons = (5,11,17,23,29,35,41,47,53)
        self.setBoard(True, bf.boardFromFile)
        

    def printBoard(self):
        print(self.contents)

    def setBoard(self, loadFromFile=True, initBoard={}):
        if loadFromFile:
            print('Setting board from file.\n')
            self.contents = initBoard
            self.updateBoard()
        elif not loadFromFile:
            for i in range(0,self.boardpieces):
                print('Enter piece at location {0} of {1}'.format(i,self.boardpieces))
                thisinput = input().split(',')
                thisinput.append(False)
                while len(thisinput) != 5:
                    print('Wrong input length.  Try again')
                    thisinput = input().split(',')
                    thisinput.append(False)
                self.addPiece(i,thisinput)
        print('Board set\n')
        self.getNextAvailable()

    def getNextAvailable(self):
        self.nextOptions = {}
        nextOptions = self.nextOptions
        for i in range(self.tokenPos,self.tokenPos+self.boardpieces): 

            if (not self.contents[i%(self.boardpieces)][4]) and len(nextOptions)<3 :
                nextOptions[len(nextOptions)]={i%(self.boardpieces):self.contents[i%(self.boardpieces)]}
  
                   
    def addPiece(self,location, piece):
        print('\nAttempting to add piece {0} to location {1}'.format(piece,location))
        if location in self.contents:
            print('Piece already at exists at this location!  Aborting!\n')
        else:
            self.contents[location] = piece
            print('Success'+'\n')

    def removePiece(self,location, piece):
        print('Attempting to remove piece {0} to location {1}'.format(piece,location))
        if location not in self.contents:
            print('Piece does not exist at this location!  Aborting!')
        else:
            del self.contents[location]
            
    def updateBoard(self):
        newDict = {
                    'AA':1,
                    'Z':2,
                    'K':3,
                    'O':4,
                    'Y':5,
                    'S':6,
                    'GG':7,
                    'Q':8,
                    'V':9,
                    'FF':10,
                    'CC':11,
                    'F':12,
                    'I':13,
                    'M':14,
                    'C':15,
                    'R':16,
                    'L':17,
                    'E':18,
                    'U':19,
                    'D':20,
                    'X':21,
                    'A':22,
                    'W':23,
                    'H':24,
                    'N':25,
                    'DD':26,
                    'P':27,
                    'J':28,
                    'BB':29,
                    'EE':30,
                    'G':31,
                    'T':32,
                    'B':33
                    }
        
        for key, value in newDict.items():
            self.contents[(value-1)] = self.contents[key]
            del self.contents[key]