'''
Created on Nov 3, 2019

@author: Andy
'''
import player as pl
import sys
import dialogMessages as dm
import game 

class gameSession:
    def __init__(self,*args):
        self.logger = args[0]
        self.createActionList()
        self.playerList = []
        self.sm = dm.sessionMessages
        self.gameList = dm.availableGames
        self.run()
      
    def run(self):
        exitMarker = False
        while not exitMarker:
            self.logger.debug(self.sm['displayActions'])
            self.processAction(input())
    
    def processAction(self, *args):
        self.actionList.get(args[0],self.invalidSelection)(args[0])
    
    def invalidSelection(self, *args):
        self.logger.info(self.sm['invalidSelection'] % args[0])
    
    def addPlayer(self, *args):
        self.logger.info(self.sm['getPlayerName'])
        ap = input()
        self.playerList.append(pl.player(ap))
        self.logger.info('Added player %s.' % self.playerList[-1].name)
        
    def removePlayer(self, *args):
        self.logger.info(self.sm['removePlayer'])
        rp = input()
        for i in self.playerList :
            if i.name == rp:
                self.playerList.remove(i) 
                self.logger.info('Removed player %s.' % i.name)
    
    def showPlayers(self, *args):
        self.logger.debug(self.sm['showPlayers'] % len(self.playerList))
        for i in self.playerList: self.logger.info(i.name)
    
    def playGame(self, *args):
        #try:
            game.game(args[0],self.logger,self.playerList)
        #except Exception as e:
           # self.logger.info(e)
            self.logger.info('Failed when starting or playing game')
        
    
    def showGames(self, *args):
        for value in self.gameList.values(): self.logger.info(value)
        self.logger.debug(self.sm['selectGame'])
        self.playGame(self.gameList.get(input()))
        
    
    def quitConsole(self, *args):
        self.logger.info(self.sm['exitMessage'])
        sys.exit()
    
    def createActionList(self):
        self.actionList = {
            'A': self.addPlayer,
            'R': self.removePlayer,
            'S': self.showPlayers,
            'Q': self.quitConsole,
            'P': self.showGames}
        
    
        
        