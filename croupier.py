from deck import Deck
from player import Player
import re


class Croupier:
    def __init__(self, config_file):
        ip_file = open(config_file, 'r')
        ips_names = [line.rstrip('\n') for line in ip_file]
        self.playersList = [
            Player(re.search(r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})', x).group(0), re.search(r'(?<=\b )(\w+)', x).group(0)) for x in ips_names]
        self.deck = Deck()

    def showPlayer(self, player):
        print ('Points: %s\nStatus: %s' % (player.points, player.isFinished()))

    def allFinished(self):
        return all(x.finished for x in self.playersList)

    def findPlayer(self, playerID):
        return next((x for x in self.playersList if x.ip == playerID), None)

    def finish(self, playerID):
        player = self.findPlayer(playerID)
        if player != None:
            player.setFinished(True)

    def showGameStatus(self):
        winner = next((x for x in self.playersList if x.points == 21), None)
        if winner != None:
            print ('Winner Winner Chicken Dinner!\nCongratulations %s', winner.name)
        else:
            print (
                'Common guys, the game is ON\n====SCOREBOARD====\nNAME\tPOINTS\tSTILL PLAYING')
            [print('%s\t%s\t%s' % (x.name, x.points, x.isFinished())) for x in self.playersList]

    def getCard(self, playerID):
        player = self.findPlayer(playerID)
        if player != None:
            if player.isFinished() == False:
                if self.deck.empty() == False:
                    player.newCard(self.deck.pop())
                    self.showPlayer(player)
            if self.allFinished():
                self.showGameStatus()
