'''
Created on Nov 3, 2019

@author: Andy
'''

import sys
import patchworkPlayer
import player
import dialogMessages as dm

class game:
    
    class moveObject:
        def __init(self):
            pass
    
    def __init__(self,name='NewGame',*args):
        self.completedRounds = 0
        self.name = name
        self.end = 53
        self.playerList = args
        self.thisboard = patchworkPlayer.board()
        self.logger = args[0]
        self.moveList = {}
        self.player1 = args[1][0]
        self.player2 = args[1][1]
        self.play(self.player1, self.player2)
        
    def play(self, player1, player2):
        while not   self.checkEnd():
            self.player1 = self.takeTurn(player1, player2, self.thisboard)
            self.player2 = self.takeTurn(player2, player1, self.thisboard)
        if self.player1.projectPoints()>self.player2.projectPoints():
            self.logger.info('Game Over!  Player {0} won {1} to {2}'.format(player1.name, self.player1.projectedPoints(),self.player2.projectedPoints()))
        elif self.player2.projectPoints()>self.player1.projectPoints():
            self.logger.info('Game Over!  Player {0} won {1} to {2}'.format(player2.name, self.player2.projectedPoints(),self.player1.projectedPoints()))
        elif self.player2.projectPoints()==self.player2.projectPoints():
            self.logger.info('Game Over!  Players tied! {0} to {1}'.format(self.player1.projectedPoints(),self.player2.projectedPoints()))
        else:
            self.logger.info('Game Over!  Error!')
            
    def takeTurn(self, player1, player2, thisboard):
        self.thisboard = thisboard
        while player1.position <= player2.position:
            self.logger.info(self.printScore())
            print('test')
            self.logger.info(dm.sessionMessages['patchworkActions'].format(player1.name))
            self.logger.info(self.presentOptions(player1))
            indata = input()
            player1 = self.takeAction(indata,player1)
        return player1

    def move(self, player, distance):    
        self.logger.info('Moving player {0} from position {1} to position {2}'.format(player.name,player.position,player.position+int(distance)))
        newpos = player.position+int(distance)
        for i in range(player.position+1,newpos+1):
            if i in self.thisboard.singletokens:
                player.emptySquares += 1
                self.thisboard.singletokens.remove(i)
                self.logger.info('Adding 2 points from a token to player {0}'.format(player.name))
        for i in range(player.position+1,newpos+1):
            if i in self.thisboard.buttons:
                player.points += player.buttons
                player.buttonsleft -= 1
                self.logger.info('Adding {0} points from a button token to player {1}'.format(player.buttons,player.name))
        player.position = newpos

    def choosePass(self, passer, passed):
        newposition = min(passed.position+1,self.end)
        self.logger.info('Player {0} is passing {1}'.format(passer.name,passed.name))
        self.logger.info('Player {0} is moving from position {1} to position {2}'.format(passer.name,passer.position,newposition))
        self.logger.info('Adding {0} points for passing movement.'.format(newposition-passer.position))
        passer.points += (newposition-passer.position)
        self.move(passer, (newposition-passer.position))
        self.logger.info('New points: {0}'.format(passer.points))
        self.logger.info('New position: {0}'.format(passer.position))

    def printScore(self): 
        self.logger.info('**********************')
        self.logger.info('Completed Rounds: {0}'.format(self.completedRounds))
        self.logger.info('Token Location: {0}'.format(self.thisboard.tokenPos))
        self.logger.info('*********************\nPlayer: {0}'.format(self.player1.name))
        self.logger.info('Points: {0}'.format(self.player1.points))
        self.logger.info('Position: {0}'.format(self.player1.position))
        self.logger.info('Buttons on Tapestry: {0}'.format(self.player1.buttons))
        self.logger.info('Empty Squares: {0}'.format(self.player1.emptySquares))
        self.logger.info('*********************')
        self.logger.info('Player: {0}'.format(self.player2.name))
        self.logger.info('Points: {0}'.format(self.player2.points))
        self.logger.info('Position: {0}'.format(self.player2.position))
        self.logger.info('Buttons on Tapestry: {0}'.format(self.player2.buttons))
        self.logger.info('Empty Squares: {0}'.format(self.player2.emptySquares))
        self.logger.info('**********************')


    #this method does not keep track of the tile options
    def chooseTile(self, chooser):
        self.logger.info('Enter tile (buttoncost, timecost, buttons, coveredsquares?')
        g=input().split(',')
        chooser.buy(g)
        movedistance = min(int(g[1]), self.end-chooser.position)
        self.move(chooser,movedistance)

    def chooseTile2(self, tile, chooser):
        self.logger.info('Buying tile {0}\n'.format(tile))
        key = list(tile)[0]
        g=tile[list(tile)[0]][0:4]
        chooser.buy(g)
        movedistance = min(int(g[1]), self.end-chooser.position)
        self.move(chooser,movedistance)
        g.append(True)
        self.thisboard.contents[key] = g
        self.logger.info('Marking token {0} as used.'.format(key))
        self.logger.info('Moving token from {0} to {1}'.format(self.thisboard.tokenPos,key))
        self.thisboard.tokenPos = key
        self.logger.info('\n')

    def chooseOption(self, optionIndex, chooser):
        self.logger.info('Buying tile with local option index {0}'.format(optionIndex))
        for value in self.thisboard.nextOptions[optionIndex].values():
            holder = value[0:4]
            holder.append(chooser.buttonsleft*int(value[2]))
            self.chooseTile2(self.thisboard.nextOptions[optionIndex],chooser)

    def checkEnd(self):
        if self.end < self.player1.position or self.end < self.player2.position:
            return True
        else:
            return False

    def presentOptions(self, player):
        self.thisboard.getNextAvailable()
        returnString = ''
        for key, value in self.thisboard.nextOptions.items():
            for innervalue in value.values():
                if int(innervalue[0])>int(player.points): returnString+='**'
                returnString += 'Index {0} has value ({1}) and dimensions ({2})\n'.format(key,(player.buttonsleft*int(innervalue[2]))+(2*int(innervalue[3]))-(int(innervalue[0])+int(innervalue[1])),','.join(innervalue[0:4]))
        return (returnString)

    
    def takeAction(self, *args):
            print('test')
            indata = args[0]
            player1 = args[1]
            if indata == 'Q':
                sys.exit()
            elif indata == 'S':
                self.logger.info(self.printScore())
            elif indata == 'P':
                self.logger.infoBoard()
            elif indata == 'A':
                thisMove = self.createMoveObject(player1, indata)
                self.logMove(thisMove)
                self.choosePass(player)
                self.completedRounds += 1
            elif indata == 'T':
                player.points+=7
            elif indata in map(str,range(0,3)):
                try:
                    backup = player.player(player1.name, player1.position, player1.points, player1.buttons, player1.emptySquares)
                    self.chooseOption(int(indata),player1)
                    self.completedRounds += 1
                except Exception as e:
                    self.logger.info(e)
                    self.logger.info('Reverting')
                    player1 = backup
                    self.logger.info('Try Again')
            else:
                self.logger.info('Invalid entry.  Try again')
        
            return player1  
     
    def createMoveObject(self, *args):
        self.logger.debug('test')
        thisMoveObject = {self.completedRounds: args}
        return thisMoveObject
                
    def logMove(self, moveObject):
        pass
       
    def buildActions(self):
        self.actionList = {
            'Q':[sys.exit],
            'S':[self.logger.info(self.printScore())],
            'P':[self.logger.infoBoard()]
            }
        print(self.actionList)
        