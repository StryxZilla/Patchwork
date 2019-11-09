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
        self.maxSquares = emptySquares
        self.emptySquares = self.maxSquares
        self.buttonsleft = 9
        self.myTokens = []

    def buy(self, info):
        if self.points < int(info[0]):
            raise Exception('Cannot spend more buttons than you have')
            return    
        print('Buying piece that costs {0} buttons and {1} time. Adding {2} buttons to your tapestry.'.format(info[0],info[1],info[2]))
        print('Changing points from {0} to {1} '.format(self.points, (self.points-int(info[0]))))
        self.points = self.points-int(info[0])
        print('Changing tapestry buttons from to '.format(self.buttons,self.buttons+int(info[2]))) 
        self.buttons = self.buttons+int(info[2])
        print('Changing empty squares from to '.format(self.emptySquares,max(self.emptySquares-int(info[3]),0)))
        self.emptySquares = max(self.emptySquares-int(info[3]),0)
        
    def sell(self, info): 
        print('Selling piece that costs {0} buttons and {1} time. Removing {2} buttons from your tapestry.'.format(info[0],info[1],info[2]))
        print('Changing points from {0} to {1} '.format(self.points, (self.points+int(info[0]))))
        self.points = self.points+int(info[0])
        print('Changing tapestry buttons from {1} to {0}'.format(self.buttons,self.buttons-int(info[2]))) 
        self.buttons = self.buttons-int(info[2])
        print('Changing empty squares from {1} to {0}'.format(self.emptySquares,max(self.emptySquares+int(info[3]),0)))
        self.emptySquares = min(self.emptySquares+int(info[3]),self.maxSquares)
