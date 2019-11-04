'''
Created on Nov 3, 2019

@author: Andy
'''
class player:
    def __init__(self,name, position=0,points=5,buttons=0,emptySquares=81):
        self.name = name
        self.position = position
        self.points = points
        self.buttons = buttons
        self.emptySquares = emptySquares
        self.buttonsleft = 9


    def buy(self, info):
        if self.points < int(info[0]):
            raise Exception('Cannot spend more buttons than you have')
        
        print('Buying piece that costs '+str(info[0])+' buttons and '+str(info[1])+' time. Adding '+str(info[2])+' buttons to your tapestry.')
        print('Changing points from '+str(self.points)+' to '+str(self.points-int(info[0])))
        self.points = self.points-int(info[0])
        print('Changing tapestry buttons from '+str(self.buttons)+' to '+str(self.buttons+int(info[2]))) 
        self.buttons = self.buttons+int(info[2])
        print('Changing empty squares from '+str(self.emptySquares)+' to '+str(max(self.emptySquares-int(info[3]),0)))
        self.emptySquares = max(self.emptySquares-int(info[3]),0)

    def projectPoints(self, thisgame):
        buttonsleft = self.buttonsleft
        print('Projected points: '+str(self.points+(thisgame.end-self.position)+(buttonsleft*self.buttons)-(2*self.emptySquares)))
