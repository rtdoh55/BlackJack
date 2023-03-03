class Card:
    """
    Card class.

    # Doctests for str and repr
    >>> card_1 = Card("A", "spades")
    >>> print(card_1)
    ____
    |A  |
    | ♠ |
    |__A|
    >>> card_1
    (A, spades)
    >>> card_2 = Card("K", "spades")
    >>> print(card_2)
    ____
    |K  |
    | ♠ |
    |__K|
    >>> card_2
    (K, spades)
    >>> card_3 = Card("A", "diamonds")
    >>> print(card_3)
    ____
    |A  |
    | ♦ |
    |__A|
    >>> card_3
    (A, diamonds)

    # Doctests for comparisons
    >>> card_1 < card_2
    False
    >>> card_1 > card_2
    True
    >>> card_3 > card_1
    False

    # Doctests for set_visible()
    >>> card_3.set_visible(False)
    >>> print(card_3)
    ____
    |?  |
    | ? |
    |__?|
    >>> card_3
    (?, ?)
    >>> card_3.set_visible(True)
    >>> print(card_3)
    ____
    |A  |
    | ♦ |
    |__A|
    >>> card_3
    (A, diamonds)
    """

    # Class Attribute(s)

    def __init__(self, rank, suit, visible=True):
        """
        Creates a card instance and asserts that the rank and suit are valid.
        """
        if rank == 14:
            rank = 'A'
        elif rank == 11:
            rank = 'J'
        elif rank == 12:
            rank = 'Q'
        elif rank == 13:
            rank = 'K'
        if isinstance(rank, int):
            assert 2 <= rank <= 10
        if isinstance(rank, str):
            assert rank.lower() in 'akqj'

        self.rank = rank
        self.suit = suit
        self.visible = visible

    def __lt__(self, other_card):
        if isinstance(self.rank, str) & isinstance(other_card.rank, str):
            if self.rank < other_card.rank:
                return False
            elif self.rank > other_card.rank:
                return True
            else:
                if self.suit > other_card.suit:
                    return False
                else:
                    return True
        elif isinstance(self.rank, str) & isinstance(other_card.rank, int):
            return False
        elif isinstance(self.rank, int) & isinstance(other_card.rank, str):
            return True
        else:
            if self.rank < other_card.rank:
                return True
            elif self.rank > other_card.rank:
                return False
            else:
                if self.suit > other_card.suit:
                    return False
                else:
                    return True
    def __str__(self):
        """
        Returns ASCII art of a card with the rank and suit. If the card is
        hidden, question marks are put in place of the actual rank and suit.

        Examples:
        ____
        |A  |
        | ♠ |
        |__A|
        ____
        |?  |
        | ? |
        |__?|
        """
        suit = ""
        if self.suit == 'diamonds':
            suit = "♦"
        elif self.suit == 'spades':
            suit = "♠"
        elif self.suit == 'clubs':
            suit = "♣"
        else:
            suit = "♥"

        if self.visible:
            return '____\n|{0}  |\n| {1} |\n|__{0}|'\
            .format(self.rank, suit)
        else:
            return '____\n|{0}  |\n| {0} |\n|__{0}|'\
            .format('?')
    def __repr__(self):
        """
        Returns (<rank>, <suit>). If the card is hidden, question marks are
        put in place of the actual rank and suit.
        """
        if self.visible:
            return '({0}, {1})'.format(self.rank, self.suit)
        else:
            return '({0}, {0})'.format('?')


    def get_rank(self):
        return self.rank

    def get_suit(self):
        return self.suit

    def set_visible(self, visible):
        assert isinstance(visible, bool)
        self.visible = visible
