#! python2.
class Card:
    suitList = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
    rankList = ['narf', 'Ace', '2', '3', '4', '5', '6', '7',
                '8', '9', '10', 'Jack', 'Queen', 'King']

    def __init__(self, suit=0, rank=2):
        self.suit = suit
        self.rank = rank

    def __cmp__(self, other):
        # check suits
        if self.suit > other.suit:
            return 1
        if self.suit < other.suit:
            return -1
        # if suits is the sam check ranks
        if self.rank > other.rank or (self.rank == 1 and other.rank != 1):
            return 1
        if self.rank < other.rank:
            return -1
        # ranks are the same....its a tie
        return 0

    def __str__(self):
        return (self.rankList[self.rank] + ' of ' +
                self.suitList[self.suit])


class Deck:
    def __init__(self):
        self.cards = []
        for suit in range(4):
            for rank in range(1, 14):
                self.cards.append(Card(suit, rank))

    def __str__(self):
        s = ''
        for i in range(len(self.cards)):
            s = s + ' ' * i + str(self.cards[i]) + '\n'
        return s

    def shuffle(self):
        from random import randrange
        nCards = len(self.cards)
        for i in range(nCards):
            j = randrange(i, nCards)
            nCard = self.cards[i]
            self.cards[i] = self.cards[j]
            self.cards[j] = nCard

    def removeCard(self, card):
        if card in self.cards:
            self.cards.remove(card)
            return True
        else:
            return False

    def popCard(self):
        return self.cards.pop()

    def isEmpty(self):
        return (len(self.cards) == 0)

    def deal(self, hands, ncards=999):
        nhands = len(hands)
        for i in range(ncards):
            if self.isEmpty():
                break  # break if out of cards
            Card = self.popCard()  # take the top card
            hand = hands[i % nhands]  # whose turn is next
            hand.addCard(Card)  # add card to the hand


class Hand(Deck):
    def __init__(self, name=''):
        self.cards = []
        self.name = name

    def addCard(self, card):
        self.cards.append(card)

    def __str__(self):
        s = 'Hand ' + str(self.name)
        if self.isEmpty():
            return s + ' is empty '
        else:
            return s + ' contains \n' + Deck.__str__(self)


class CardGame():
    """docstring for CradGame"""

    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()


class OldMaidHand(Hand):
    def removeMatches(self):
        count = 0
        originalCards = self.cards[:]
        for card in originalCards:
            match = Card(3 - card.suit, card.rank)
            if match in self.cards:
                self.cards.remove(card)
                self.cards.remove(match)
                print 'Hand %s: %s match %s' % (self.name, card, match)
                count = count + 1
        return count


class OldMaidGame(CardGame):

    def findNeighbor(self, i):
        numHands = len(self.hands)
        for next in range(1, numHands):
            neighbor = (i + next) % numHands
            if not self.hands[neighbor].isEmpty():
                return neighbor

    def playOneTurn(self, i):
        if self.hands[i].isEmpty():
            return 0
        neighbor = self.findNeighbor(i)
        pickedCard = self.hands[neighbor].popCard()
        self.hands[i].addCard(pickedCard)
        print 'Hand ', self.hands[i].name, ' picked ', pickedCard
        count = self.hands[i].removeMatches()
        self.hands[i].shuffle()
        return count

    def removeAllMatches(self):
        count = 0
        for hand in self.hands:
            count = count + hand.removeMatches()
        return count

    def printHands(self):
        for hand in self.hands:
            print hand

    def picklooser(self):
        for hand in self.hands:
            try:
                if hand.cards[0] == Card(3, 12):
                    return hand.name
            except IndexError:
                pass

    def play(self, names):
        '''remove Queen of clubs'''
        self.deck.removeCard(Card(0, 12))

        '''make a hand for each player'''
        self.hands = []
        for name in names:
            self.hands.append(OldMaidHand(name))

        '''deal the cards'''
        self.deck.deal(self.hands)
        print "---------- Cards have been dealt"
        self.printHands()

        '''remove initial matches'''
        matches = self.removeAllMatches()
        print "---------- Matches discarded, play begins"
        self.printHands()

        '''play until all 50 cards are matched'''
        turn = 0
        numhands = len(self.hands)
        while matches < 25:
            matches = matches + self.playOneTurn(turn)
            turn = (turn + 1) % numhands

        print "---------- Game is Over"
        self.printHands()
        print '\n----------------\n' + str(self.picklooser()) + ' loses'
