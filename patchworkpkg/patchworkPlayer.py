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