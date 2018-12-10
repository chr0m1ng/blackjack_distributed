from deck import Deck
from player import Player
import re
from prettytable import PrettyTable


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

    def obterVencedor(self):

        maior = Player('127.0.0.1', '5001', 'X')
        maior.points = -1

        for player in self.playersList:
            if player.points <= 21 and player.points > maior.points:
                maior = player
        return maior

    def showGameStatus(self):
        t = PrettyTable(['NAME', 'POINTS', 'FINISHED'])
        for player in self.playersList:
            t.add_row([player.name, player.points, player.isFinished()])
        print(t)

        if self.allFinished():
            winner = self.obterVencedor()
            if winner != None:
                print('Winner Winner Chicken Dinner!\nCongratulations %s' %
                      winner.name)
            else:
                print('NO WINNERS MY FRIENDS!')

    def getCard(self, playerID):
        player = self.findPlayer(playerID)
        if player != None:
            if player.isFinished() == False:
                if self.deck.empty() == False:
                    card = self.deck.pop()
                    player.newCard(card)
                    self.showPlayer(player, card)
                    if player.isFinished():
                        self.showGameStatus()
            else:
                self.showGameStatus()
