class Shuffle:
    """
    Different kinds of shuffling techniques.

    >>> cards = [i for i in range(52)]
    >>> cards[25]
    25
    >>> mod_oh = Shuffle.modified_overhand(cards, 1)
    >>> mod_oh[0]
    25
    >>> mod_oh[25]
    24

    >>> mongean_shuffle = Shuffle.mongean(mod_oh)
    >>> mongean_shuffle[0]
    51
    >>> mongean_shuffle[26]
    25
    """

    def modified_overhand(cards, num):
        """
        Takes `num` cards from the middle of the deck and puts them at the
        top.
        Then decrement `num` by 1 and continue the process till `num` = 0.
        When num is odd, the "extra" card is taken from the bottom of the
        top half of the deck.
        """

        # Use Recursion.
        # Note that the top of the deck is the card at index 0.
        assert isinstance(cards, list)
        assert isinstance(num, int)
        even = 2
        if num == 0:
            return cards
        else:
            if ((len(cards) % even) == 0) & ((num % even) == 0):
                cards = cards[:(len(cards) // even)][-(num // even):] + \
                cards[(len(cards) // even):][:(num // even)] + \
                cards[:((len(cards) // even) - (num // even))] + \
                cards[((len(cards) // even) + (num // even)):]
                return Shuffle.modified_overhand(cards, num - 1)
            elif ((len(cards) % even) == 0) & ((num % even) == 1):
                cards = cards[:(len(cards) // even)][-(num // even + 1):] + \
                cards[(len(cards) // even):][:(num // even)] + \
                cards[:((len(cards) // even) - (num // even + 1))] + \
                cards[((len(cards) // even) + (num // even)):]
                return Shuffle.modified_overhand(cards, num - 1)
            else:
                cards = cards[:(len(cards) // even)][-(num // even + 1):] + \
                cards[(len(cards) // even):][:(num // even)] + \
                cards[:((len(cards) // even) - (num // even + 1))] + \
                cards[((len(cards) // even) + (num // even)):]
                return Shuffle.modified_overhand(cards, num - 1)


    def mongean(cards):
        """
        Implements the mongean shuffle.
        Check wikipedia for technique description. Doing it 12 times restores the deck.
        """


        # Remember that the "top" of the deck is the first item in the list.
        # Use Recursion. Can use helper functions.
        increment = 2
        return Shuffle.shuff(cards[1:]) + [cards[0]] \
        + Shuffle.shuff(cards[increment:])

    def shuff(cards):
        even = 2
        if len(cards) == 0:
            return []
        else:
            if len(cards) % even == 0:
                return [cards[0]] + Shuffle.shuff(cards[even:])
            else:
                return Shuffle.shuff(cards[even:]) + [cards[0]]
