import socket


class Player:

    def __init__(self, ip, port, name):
        self.id = ip + port
        self.ip = ip
        self.port = int(port[1:])
        self.name = name
        self.finished = False
        self.points = 0

    def setFinished(self, value):
        self.finished = value

    def isFinished(self):
        return self.finished

    def newCard(self, card):
        self.points += card.value
        if self.points > 21:
            self.finished = True

    def __str__(self):
        return '%s - %s - finished: %s' % (self.name, self.id, self.isFinished())
