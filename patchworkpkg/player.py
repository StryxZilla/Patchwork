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
        
        print('Buying piece that costs {0} buttons and {1} time. Adding {2} buttons to your tapestry.'.format(info[0],info[1],info[2]))
        print('Changing points from {0} to {1} '.format(self.points, (self.points-int(info[0]))))
        self.points = self.points-int(info[0])
        print('Changing tapestry buttons from to '.format(self.buttons,self.buttons+int(info[2]))) 
        self.buttons = self.buttons+int(info[2])
        print('Changing empty squares from to '.format(self.emptySquares,max(self.emptySquares-int(info[3]),0)))
        self.emptySquares = max(self.emptySquares-int(info[3]),0)

    def projectPoints(self, thisgame):
        buttonsleft = self.buttonsleft
        print('Projected points: '.format(self.points+(thisgame.end-self.position)+(buttonsleft*self.buttons)-(2*self.emptySquares)))
