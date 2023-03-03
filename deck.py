from card import Card
from hand import PlayerHand, DealerHand
from shuffle import Shuffle

class Deck:
    """
    Card deck of 52 cards.

    >>> deck = Deck()
    >>> deck.get_cards()[:5]
    [(2, clubs), (2, diamonds), (2, hearts), (2, spades), (3, clubs)]

    >>> deck.shuffle(modified_overhand=2, mongean=3)
    >>> deck.get_cards()[:5]
    [(A, clubs), (Q, clubs), (10, clubs), (7, diamonds), (5, diamonds)]

    >>> hand = PlayerHand()
    >>> deck.deal_hand(hand)
    >>> deck.get_cards()[0]
    (Q, clubs)
    """

    # Class Attribute(s)

    def __init__(self):
        """
        Creates a Deck instance containing cards sorted in ascending order.
        """
        upper_bound = 15
        suits = ['clubs', 'diamonds', 'hearts', 'spades']
        self.deck = [Card(i, suit) \
        for i in range(2, upper_bound) for suit in suits]

    def shuffle(self, **shuffle_and_count):
        """Shuffles the deck using a variety of different shuffles.

        Parameters:
            shuffle_and_count: keyword arguments containing the
            shuffle type and the number of times the shuffled
            should be called.
        """
        for key, value in shuffle_and_count.items():
            assert isinstance(value, int)
            assert isinstance(key, str)
            assert (key == 'modified_overhand') | (key == 'mongean')

        for key, value in shuffle_and_count.items():
            if key == 'modified_overhand':
                self.deck =\
                Shuffle.modified_overhand(self.deck, value)

        for key, value in shuffle_and_count.items():
            if key == 'mongean':
                for i in range(value):
                    self.deck = Shuffle.mongean(self.deck)


    def deal_hand(self, hand):
        """
        Takes the first card from the deck and adds it to `hand`.
        """
        assert isinstance(hand, PlayerHand)
        self.hand = hand
        self.hand.add_card(self.deck[0])
        self.deck = self.deck[1:]


    def get_cards(self):
        return self.deck
