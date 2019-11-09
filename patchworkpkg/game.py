'''
Created on Nov 3, 2019

@author: Andy
'''

import sys
import patchworkGame
import player
import dialogMessages as dm
import shelve


class game:
    def __init__(self,name='NewGame',*args):
        self.completedRounds = 0
        self.name = name
        self.end = 53
        self.playerList = args
        self.thisboard = patchworkGame.board()
        self.logger = args[0]
        self.moveList = []
        self.player1 = player.player('Player1')
        self.player2 = player.player('Player2')
        self.play(self.player1, self.player2)

    #this will need to be modified  when the playing cadence or win criteria changes    
    def play(self, player1, player2):
        while not   self.checkEnd():
            self.takeTurn(self.player1, self.player2, self.thisboard)
            if self.checkEnd(): break
            self.takeTurn(self.player2, self.player1, self.thisboard)
        if self.projectPoints(player1)>self.projectPoints(player2):
            self.logger.info('Game Over!  Player {0} won {1} to {2}'.format(player1.name, self.projectPoints(player1),self.projectPoints(player2)))
        elif self.projectPoints(player2)>self.projectPoints(player1):
            self.logger.info('Game Over!  Player {0} won {1} to {2}'.format(player2.name, self.projectPoints(player2),self.projectPoints(player1)))
        elif self.projectPoints(player1)==self.projectPoints(player2):
            self.logger.info('Game Over!  Players tied! {0} to {1}'.format(self.projectedPoints(player1),self.projectedPoints(player2)))
        else:
            self.logger.info('Game Over!  Error!')
            
    def takeTurn(self, player1, player2, thisboard):

        self.thisboard = thisboard
        while player1.position <= player2.position:
            #self.printScore()
            self.logger.info(dm.sessionMessages['patchworkActions'].format(player1.name))
            self.logger.info(self.presentOptions(player1))
            indata = input()
            thisAction = self.createActionObject(indata, player1, player2)
            direction = self.takeAction(thisAction)
            player1 = thisAction['player1']
            player2 = thisAction['player2']
            if player1.position == player2.position and direction == -1 : break
        return player1

    def move(self, player, distance):    
        self.logger.info('Moving player {0} from position {1} to position {2}'.format(player.name,player.position,player.position+int(distance)))
        newpos = player.position+int(distance)
        if distance >= 0: 
            fromList = self.thisboard.singletokens
            toList = player.myTokens
            addRemove = 'Adding'
            direction = 1
            offset = 1
        else:
            fromList = self.thisboard.singletokens
            toList = player.myTokens
            addRemove = 'Removing'
            direction = -1
            offset = 0 
        for i in range(player.position+offset,newpos+offset, direction):
            if i in fromList:
                player.emptySquares += direction
                fromList.remove(i)
                toList.append(i)
                self.logger.info('{0} 2 points from a token to player {1}'.format(addRemove, player.name))
        for i in range(player.position+offset,newpos+offset, direction):
            if i in self.thisboard.buttons:
                player.points += direction*player.buttons
                player.buttonsleft -= direction
                self.logger.info('Adding {0} points from a button token to player {1}'.format(player.buttons,player.name))
        player.position = newpos

    def choosePass(self, thisAction, direction):
        passer = thisAction['player1']
        passed = thisAction['player2']
        if direction == 1: newposition = min(passed.position+direction, self.end) 
        else: newposition = thisAction['startpos']  
        self.logger.info('Player {0} is passing {1}'.format(passer.name,passed.name))
        self.logger.info('Player {0} is moving from position {1} to position {2}'.format(passer.name,passer.position,newposition))
        self.logger.info('Adding {0} points for passing movement.'.format(newposition-passer.position))
        passer.points += (newposition-passer.position)
        self.move(passer, (newposition-passer.position))
        self.completedRounds += (direction)
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
        self.logger.info(self.projectPoints(self.player1))
        self.logger.info('*********************')
        self.logger.info('Player: {0}'.format(self.player2.name))
        self.logger.info('Points: {0}'.format(self.player2.points))
        self.logger.info('Position: {0}'.format(self.player2.position))
        self.logger.info('Buttons on Tapestry: {0}'.format(self.player2.buttons))
        self.logger.info('Empty Squares: {0}'.format(self.player2.emptySquares))
        self.logger.info(self.projectPoints(self.player2))
        self.logger.info('**********************')


    def chooseTile(self, thisAction, direction = 1):
        self.logger.info('\nBuying tile {0}\n'.format(thisAction['tile']))
        for key in thisAction['tile'].keys():
            g = thisAction['tile'][key]
        if direction ==1: 
            movedistance = min(int(g[1]), self.end-thisAction['player1'].position)
            thisAction['player1'].buy(g)
            self.move(thisAction['player1'],movedistance)
            g[4] = True
        else: 
            movedistance = -1*int(g[1])
            self.move(thisAction['player1'],movedistance)
            thisAction['player1'].sell(g)
            g[4] = False
 
        self.thisboard.contents[key] = g
        self.logger.info('Marking token {0} as used.'.format(key))
        self.logger.info('Moving token from {0} to {1}'.format(self.thisboard.tokenPos,key))
        self.thisboard.tokenPos = key
        self.logger.info('\n')

    def checkEnd(self):
        if self.end <= self.player1.position and self.end <= self.player2.position:
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

    
    def takeAction(self, thisAction, direction=1):
        indata = thisAction['action']
        player1 = thisAction['player1']
        player2 = thisAction['player2']
        if indata == 'Q':
            sys.exit()
        elif indata == 'B':
            self.thisboard.printBoard()
            self.logger.debug(self.moveList)
            self.printScore()
        elif indata == 'S':
            self.saveGameState()
        elif indata == 'L':
            self.loadGameState(thisAction)
        elif indata == 'P':
            if 'startpos' not in thisAction.keys(): thisAction['startpos'] = player1.position
            self.choosePass(thisAction,direction)
            self.logMove(thisAction, direction)
        elif indata == 'U':
            self.logger.info('Unrolling move:')
            self.unrollAction()
            direction = -1
        elif indata == 'T':
            thisAction['player1'].points+=direction*7
            self.logMove(thisAction, direction)
        elif indata in map(str,range(0,3)):
            try:
                #backup = player.player(player1.name, player1.position, player1.points, player1.buttons, player1.emptySquares)
                
                self.augmentAction(thisAction, 'tile', thisAction.get('tile',self.thisboard.nextOptions[int(indata)]))
                self.chooseTile(thisAction, direction)
                self.completedRounds += direction
                self.logMove(thisAction,direction)
            except Exception as e:
                self.logger.info(e)
                self.logger.info('Reverting')
                #player1 = backup
                self.logger.info('Try Again')
        else:
            self.logger.info('Invalid entry.  Try again')
        
        return direction

    def createActionObject(self, *args):
        thisActionObject={'action': args[0]}
        thisActionObject['player1'] = args[1]
        thisActionObject['player2'] = args[2]
        if len(args) > 3: thisActionObject['tile'] = args[3]
        return thisActionObject
    
    def augmentAction(self,*args):
        args[0][args[1]] = args[2]
    
    def unrollAction(self):
        unrolledAction = self.moveList.pop()
        self.logger.info(unrolledAction)
        self.takeAction(unrolledAction,-1)
        self.logger.info('Action {0} unrolled!'.format(unrolledAction))
               
    def logMove(self, actionObject, direction=1):
        if direction == 1: self.moveList.append(actionObject)
        
    def saveGameState(self, name='test'):
        self.logger.info('\nEnter name of saved game:\n')
        name = input()
        self.gameState = {
                            'board': self.thisboard,
                            'moveList': self.moveList,
                            'player1': self.player1,
                            'player2': self.player2
                         }
        gameStore = shelve.open('patchworkGame') 
        gameStore[name] = self.gameState 
        gameStore.close()

    def loadGameState(self, thisAction, name='test'):
        self.logger.info('\nEnter name of saved game to load\n')
        gameStore = shelve.open('patchworkGame')
        for i in gameStore.keys(): print(i)
        name = input()
        self.gameState = gameStore.get(name)
        self.thisboard = self.gameState['board']

        self.player1 =  self.gameState['player1']
        self.player2 = self.gameState['player2']
        self.moveList = self.gameState['moveList']
        self.completedRounds = len(self.moveList)
        thisAction['player1'] = self.gameState['player1']
        thisAction['player2'] = self.gameState['player2']


    def projectPoints(self, player1):
        return('Projected points: {0}'.format(player1.points+(self.end-player1.position)+(player1.buttonsleft*player1.buttons)-(2*player1.emptySquares)))
     
