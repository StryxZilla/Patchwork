'''
Created on Nov 3, 2019

@author: Andy
'''
import logging
import gameController
import sys


def main():
    


    logging.basicConfig(level=logging.DEBUG, format='%(message)s')
    logger = logging.getLogger()
    fh = logging.FileHandler('test3.log','a')
    fh.setLevel(logging.INFO)
    logger.addHandler(fh)
    
#     sh = logging.StreamHandler(sys.stdout)
#     sh.setLevel(logging.DEBUG)
#     logger.addHandler(sh)

    logger.info('Starting gameConsole')
    myGame = gameController.game('newgame',logger)
    logger.info('Application closing')
 
    for handler in logger.handlers:
        handler.close()
        logger.removeFilter(handler)   
                

if __name__ == '__main__':
    main()