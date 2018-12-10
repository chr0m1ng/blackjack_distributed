from croupier import Croupier
import socket
import pickle
import sys
import re

ME = sys.argv[1]
config_file = open('./configfile.txt', 'r')
config_lines = config_file.readlines()
config_file.close()
STARTER = config_lines[0].find(ME) != -1
CROUPIER = None
NEXTPLAYER = None
ME_IP = re.search(
    r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})', ME).group(0)
ME_PORT = int((re.search(r'(\:[0-9]{1,5})', ME).group(0))[1:])

for i, line in enumerate(config_lines):
    if line.find(ME) != -1:
        try:
            nextip = re.search(
                r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})', config_lines[i + 1]).group(0)
            nextport = re.search(
                r'(\:[0-9]{1,5})', config_lines[i + 1]).group(0)
            NEXTPLAYER = (nextip, int(nextport[1:]))
        except IndexError:
            nextip = re.search(
                r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})', config_lines[0]).group(0)
            nextport = re.search(
                r'(\:[0-9]{1,5})', config_lines[0]).group(0)
            NEXTPLAYER = (nextip, int(nextport[1:]))


def showMenu():
    print('(0) - New Game')
    print('(1) - Card')
    print('(2) - No more cards')
    print('(3) - Next')
    op = input()
    if op == '0':
        print('Are you sure you want to start a new game?\n(0) - Yes\n(any) - No')
        confimation = input()
        if confimation == '0':
            return int(op)
        else:
            return showMenu()
    else:
        try:
            return int(op)
        except:
            showMenu()


def recvCroupier():
    PREVIOUS_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    PREVIOUS_SOCKET.bind((ME_IP, ME_PORT))
    PREVIOUS_SOCKET.listen(1)
    conn, addr = PREVIOUS_SOCKET.accept()
    data = b''
    while True:
        packet = conn.recv(4096)
        if not packet:
            break
        data += packet
    return pickle.loads(data)


def sendCroupier(croupier):
    croupier_obj = pickle.dumps(croupier)
    NEXT_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    NEXT_SOCKET.connect(NEXTPLAYER)
    NEXT_SOCKET.send(croupier_obj)
    NEXT_SOCKET.close()
    CROUPIER = None


def playing(croupier):
    op = showMenu()
    if op == 0:
        croupier.showGameStatus()
        croupier.restart()
    elif op == 1:
        croupier.getCard(ME)
    elif op == 2:
        croupier.finish(ME)
        croupier.showGameStatus()
    elif op == 3:
        sendCroupier(croupier)
        return
    playing(croupier)


if STARTER:
    CROUPIER = Croupier('./configfile.txt')

while True:
    if CROUPIER != None:
        playing(CROUPIER)
    CROUPIER = recvCroupier()
