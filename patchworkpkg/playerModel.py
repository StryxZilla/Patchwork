'''
Created on Nov 3, 2019

@author: Andy
'''

class player:
    def __init__(self,name, logger, position=0,points=5,buttons=0,totalSquares=81):
        self.name = name
        self.logger = logger
        self.points = points
        self.buttons = buttons
        self.pieceList = []
        self.position = position
        self.totalSquares = totalSquares
        self.emptySquares = totalSquares
        self.buttonsleft = 9
        self.myTokens = []

    def addPoints(self, pointsToAdd):
        self.points += pointsToAdd
        
    def addButtons(self, buttonsToAdd):
        self.buttons += buttonsToAdd
        
    def addPiece(self, newPiece):
        if newPiece in self.pieceList:
            self.logger.info('Player already owns piece.  Add failed.')
            return False
        else: 
            self.pieceList.append(newPiece)
            return True
              
    def removePiece(self, oldPiece):
        if oldPiece not in self.pieceList:
            self.logger.info('Player does not own piece.  Remove failed.')
            return False
        else: 
            self.pieceList.remove(oldPiece)
            return True
    
    def changePosition(self, newPosition):
        self.position = newPosition
        
    def calculateEmptySquares(self):
        counter = 0
        for i in self.pieceList: 
            for j in i.values(): counter+=j.getSquares()
        self.emptySquares = self.totalSquares - counter
        return self.totalSquares - counter
                
            