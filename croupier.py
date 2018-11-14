from deck import Deck
from player import Player
import re


class Croupier:
    def __init__(self, config_file):
        ip_file = open(config_file, 'r')
        ips_names = [line.rstrip('\n') for line in ip_file]
        ip_file.close()
        self.playersList = [
            Player(re.search(r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})', x).group(0), re.search(r'(\:[0-9]{1,5})', x).group(0), re.search(r'(?<=\b )(\w+)', x).group(0)) for x in ips_names]
        self.deck = Deck()

    def restart(self):
        self.deck = Deck()
        for player in self.playersList:
            player.points = 0
            player.setFinished(False)
        print('Game restarted')

    def showPlayer(self, player, card):
        print('Withdrawn: %s\nPoints: %s\nFinished: %s' %
              (card, player.points, player.isFinished()))

    def allFinished(self):
        return all(x.finished for x in self.playersList)

    def findPlayer(self, playerID):
        return next((x for x in self.playersList if x.id == playerID), None)

    def finish(self, playerID):
        player = self.findPlayer(playerID)
        if player != None:
            player.setFinished(True)

    def showGameStatus(self):
        winner = next((x for x in self.playersList if x.points == 21), None)
        if winner != None:
            print('Winner Winner Chicken Dinner!\nCongratulations %s' %
                  winner.name)
        else:
            score = 'Common guys, the game is ON\n====SCOREBOARD====\nNAME\t\tPOINTS\t\tSTILL PLAYING\n'
            for player in self.playersList:
                score += ('%s\t\t%s\t\t%s\n' %
                          (player.name, player.points, player.isFinished()))
            print(score)

    def getCard(self, playerID):
        player = self.findPlayer(playerID)
        if player != None:
            if player.isFinished() == False:
                if self.deck.empty() == False:
                    card = self.deck.pop()
                    player.newCard(card)
                    self.showPlayer(player, card)
            else:
                self.showGameStatus()
