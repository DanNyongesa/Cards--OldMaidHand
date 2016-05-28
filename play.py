#! python2
import cards


def getValues():
    players = raw_input('Enter player names seperated by a comma: \n names: ')
    str(players)
    players = players.split(',')
    return players


def playGame(nPlayers):
    count = 1
    while len(nPlayers) > 1:
        print '****************** Round %d ***********' % count
        game = cards.OldMaidGame()
        game.play(nPlayers)
        nPlayers.remove(game.picklooser())
        count = count + 1
    print '\n**********************************\n%s Wins' % (nPlayers[0])


def main():
    s = getValues()
    playGame(s)

if __name__ == '__main__':
    main()
