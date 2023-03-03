from deck import Deck
from hand import DealerHand, PlayerHand
from card import Card

# don't change these imports
from numpy.random import randint, seed
seed(20)

class Blackjack:
    """
    Game of blackjack!

    # Removes the game summaries from the previous doctest run
    >>> from os import remove, listdir
    >>> for f in listdir("game_summaries"):
    ...    remove("game_summaries/" + f)

    #######################################
    ### Doctests for calculate_score() ####
    #######################################
    >>> card_1 = Card("A", "diamonds")
    >>> card_2 = Card("J", "spades")
    >>> hand_1 = PlayerHand()
    >>> Blackjack.calculate_score(hand_1)
    0
    >>> hand_1.add_card(card_1)
    >>> Blackjack.calculate_score(hand_1) # (Ace)
    11
    >>> hand_1.add_card(card_2)
    >>> Blackjack.calculate_score(hand_1) # (Ace, Jack)
    21

    >>> card_3 = Card("A", "spades")
    >>> hand_2 = PlayerHand()
    >>> hand_2.add_card(card_1, card_3)
    >>> Blackjack.calculate_score(hand_2) # (Ace, Ace)
    12
    >>> hand_2.add_card(card_2)
    >>> Blackjack.calculate_score(hand_2) # (Ace, Ace, Jack)
    12

    >>> hand_3 = PlayerHand()
    >>> card_4 = Card(2, "spades")
    >>> card_5 = Card(4, "spades")
    >>> hand_3.add_card(card_4, card_5)
    >>> Blackjack.calculate_score(hand_3)
    6

    #######################################
    ### Doctests for determine_winner() ####
    #######################################
    >>> blackjack = Blackjack(10)
    >>> blackjack.determine_winner(10, 12)
    -1
    >>> blackjack.determine_winner(21, 21)
    0
    >>> blackjack.determine_winner(22, 23)
    0
    >>> blackjack.determine_winner(12, 2)
    1
    >>> blackjack.determine_winner(22, 2)
    -1
    >>> blackjack.determine_winner(2, 22)
    1
    >>> print(blackjack.get_log())
    Player lost with a score of 10. Dealer won with a score of 12.
    Player and Dealer tie.
    Player and Dealer tie.
    Player won with a score of 12. Dealer lost with a score of 2.
    Player lost with a score of 22. Dealer won with a score of 2.
    Player won with a score of 2. Dealer lost with a score of 22.
    <BLANKLINE>
    >>> blackjack.reset_log()

    #######################################
    ### Doctests for play_round() #########
    #######################################
    >>> blackjack_2 = Blackjack(10)
    >>> blackjack_2.play_round(1, 15)
    >>> print(blackjack_2.get_log())
    Round 1 of Blackjack!
    wallet: 10
    bet: 5
    Player Cards: (10, clubs) (A, clubs)
    Dealer Cards: (Q, clubs) (?, ?)
    Dealer Cards Revealed: (7, diamonds) (Q, clubs)
    Player won with a score of 21. Dealer lost with a score of 17.
    <BLANKLINE>
    >>> blackjack_2.reset_log()

    >>> blackjack_2.play_round(3, 21)
    >>> print(blackjack_2.get_log())
    Round 2 of Blackjack!
    wallet: 15
    bet: 5
    Player Cards: (4, clubs) (7, clubs)
    Dealer Cards: (A, hearts) (?, ?)
    Player pulled a (J, hearts)
    Dealer Cards Revealed: (5, clubs) (A, hearts)
    Dealer pulled a (6, clubs)
    Dealer pulled a (2, clubs)
    Dealer pulled a (8, clubs)
    Player won with a score of 21. Dealer lost with a score of 22.
    Round 3 of Blackjack!
    wallet: 20
    bet: 10
    Player Cards: (6, hearts) (9, diamonds)
    Dealer Cards: (K, hearts) (?, ?)
    Player pulled a (Q, hearts)
    Dealer Cards Revealed: (J, diamonds) (K, hearts)
    Player lost with a score of 25. Dealer won with a score of 20.
    Round 4 of Blackjack!
    wallet: 10
    bet: 5
    Player Cards: (5, diamonds) (10, diamonds)
    Dealer Cards: (2, diamonds) (?, ?)
    Player pulled a (3, diamonds)
    Player pulled a (7, spades)
    Dealer Cards Revealed: (2, diamonds) (2, hearts)
    Dealer pulled a (K, spades)
    Dealer pulled a (3, spades)
    Player lost with a score of 25. Dealer won with a score of 17.
    <BLANKLINE>

    >>> with open("game_summaries/game_summary2.txt", encoding = 'utf-8') as f:
    ...     lines = f.readlines()
    ...     print("".join(lines[10:26]))
    Dealer Hand:
    ____
    |7  |
    | ♦ |
    |__7|
    ____
    |Q  |
    | ♣ |
    |__Q|
    Winner of ROUND 1: Player
    <BLANKLINE>
    ROUND 2:
    Player Hand:
    ____
    |4  |
    | ♣ |
    <BLANKLINE>

    >>> blackjack_3 = Blackjack(5)
    >>> blackjack_3.play_round(5, 21)
    >>> print(blackjack_3.get_log())
    Round 1 of Blackjack!
    wallet: 5
    bet: 5
    Player Cards: (2, clubs) (2, hearts)
    Dealer Cards: (2, diamonds) (?, ?)
    Player pulled a (3, clubs)
    Player pulled a (3, diamonds)
    Player pulled a (3, hearts)
    Player pulled a (3, spades)
    Player pulled a (4, clubs)
    Player pulled a (4, diamonds)
    Dealer Cards Revealed: (2, diamonds) (2, spades)
    Dealer pulled a (4, hearts)
    Dealer pulled a (4, spades)
    Dealer pulled a (5, clubs)
    Player lost with a score of 24. Dealer won with a score of 17.
    Wallet amount $0 is less than bet amount $5.

    >>> blackjack_4 = Blackjack(500)
    >>> blackjack_4.play_round(13, 21) # At least 52 cards will be dealt
    >>> blackjack_4.reset_log()
    >>> blackjack_4.play_round(1, 17)
    >>> print(blackjack_4.get_log())
    Not enough cards for a game.
    """
    # Class Attribute(s)

    def __init__(self, wallet):
        # Initialize instance attributes
        # auto-increment as needed
        self.wallet = wallet
        self.deck = Deck()
        self.log = ""
        self.game_number = 0
        self.rounds = 1
        self.min_bet = 5
        self.player_hand = PlayerHand()
        self.dealer_hand = DealerHand()

    def play_round(self, num_rounds, stand_threshold):
        """
        Plays `num_rounds` Blackjack rounds.

        Parameters:
            num_rounds (int): Number of rounds to play.
            stand_threshold (int): Score threshold for when the player
            will stand (ie player stands if they have a score >=
            this threshold)
        """
        # This could get pretty long!
        assert isinstance(num_rounds, int)
        assert isinstance(stand_threshold, int)

        self.min_bet = 5
        self.game_number = 2
        self.num_rounds = num_rounds
        self.stand_threshold = stand_threshold
        min_cards = 4
        results = 0
        for i in range(1, self.num_rounds + 1):
            if len(self.deck.get_cards()) < min_cards:
                self.log += 'Not enough cards for a game.'
                return None
            else:
                if self.wallet < self.min_bet:
                    self.log += 'Wallet amount ${0} is less than bet amount ${1}.'\
                    .format(self.wallet, self.min_bet)
                    return None
                else:
                    self.log += 'Round {0} of Blackjack!\n'.format(self.rounds)
                    self.log += 'wallet: {0}\n'.format(self.wallet)
                    self.log += 'bet: {0}\n'.format(self.min_bet)
                    self.deck.shuffle(mongean = randint(0, 6), \
                    modified_overhand = randint(0, 6))

                    self.deck.deal_hand(self.player_hand)
                    self.deck.deal_hand(self.dealer_hand)
                    self.deck.deal_hand(self.player_hand)
                    self.deck.deal_hand(self.dealer_hand)

                    self.log += 'Player Cards: {0}\n'\
                    .format(repr(self.player_hand)) +\
                    'Dealer Cards: {0}\n'.format(repr(self.dealer_hand))

                    if len(self.deck.get_cards()) > 0:
                        Blackjack.hit_or_stand(self, self.player_hand,\
                        stand_threshold)

                    self.dealer_hand.reveal_hand()
                    self.log += \
                    'Dealer Cards Revealed: {0}\n'.format(repr(self.dealer_hand))
                    if len(self.deck.get_cards()) > 0:
                        Blackjack.hit_or_stand(self,\
                        self.dealer_hand, stand_threshold)

                    results = Blackjack.determine_winner(self,\
                    Blackjack.calculate_score(self.player_hand),\
                    Blackjack.calculate_score(self.dealer_hand))
                    if results == 1:
                        Blackjack.add_to_file(self, self.player_hand,\
                        self.dealer_hand, 'Player')
                        self.rounds += 1
                    elif results == -1:
                        Blackjack.add_to_file(self, self.player_hand,\
                        self.dealer_hand, 'Dealer')
                        self.rounds += 1
                    else:
                        Blackjack.add_to_file(self, self.player_hand,\
                        self.dealer_hand, 'Tied')
                        self.rounds += 1
                    self.player_hand = PlayerHand()
                    self.dealer_hand = DealerHand()



    def calculate_score(hand):
        """
        Calculates the score of a given hand.

        Sums up the ranks of each card in a hand. Jacks, Queens, and Kings
        have a value of 10 and Aces have a value of 1 or 11. The value of each
        Ace card is dependent on which value would bring the score closer
        (but not over) 21.

        Should be solved using list comprehension and map/filter. No explicit
        for loops.

        Parameters:
            hand: The hand to calculate the score of.
        Returns:
            The best score as an integer value.
        """
        assert isinstance(hand, (PlayerHand, DealerHand))
        faces = 'KQJ'
        face_value = 10
        double_ace = 22
        ace_value2 = 11
        blackjack_value = 21
        if repr(hand) == '':
            return 0
        lst = [face_value if str(x.rank) in faces else x.rank for x in \
        hand.sort_hand()]

        hands1 = [1 if x == 'A' else x for x in lst]
        hands2 = [ace_value2 if x == 'A' else x for x in lst]

        if (blackjack_value - sum(hands1) >= 0)\
         & (blackjack_value - sum(hands2) >= 0):
            if abs(sum(hands1) - blackjack_value) < \
            abs(sum(hands2) - blackjack_value):
                return sum(hands1)
            elif sum(hands2) == double_ace:
                return ace_value2 + 1
            else:
                return sum(hands2)
        elif (blackjack_value - sum(hands1) < 0)\
         & (blackjack_value - sum(hands2) < 0):
            if abs(sum(hands1) - blackjack_value) < \
            abs(sum(hands2) - blackjack_value):
                return sum(hands1)
            elif sum(hands2) == double_ace:
                return ace_value2 + 1
            else:
                return sum(hands2)
        elif (blackjack_value - sum(hands1) < 0)\
         & (blackjack_value - sum(hands2) > 0):
            return sum(hands2)
        elif sum(hands2) == double_ace:
            return ace_value2 + 1
        else:
            return sum(hands1)

    def determine_winner(self, player_score, dealer_score):
        """
        Determine whether the Blackjack round ended with a tie, dealer winning,
        or player winning. Update the log to include the winner and
        their scores before returning.

        Returns:
            1 if the player won, 0 if it is a tie, and -1 if the dealer won
        """
        threshold = 21
        if (player_score == threshold) & (dealer_score != threshold):
            self.log += \
            'Player won with a score of {0}. Dealer lost with a score of {1}.'\
            .format(player_score, dealer_score) + '\n'
            self.wallet += self.min_bet
            self.min_bet += 5
            return 1
        if (player_score > threshold) & (dealer_score < threshold):
            self.log += \
            'Player lost with a score of {0}. Dealer won with a score of {1}.'\
            .format(player_score, dealer_score) + '\n'
            self.wallet -= self.min_bet
            if self.min_bet > 5:
                self.min_bet -= 5
            return -1
        elif (player_score < threshold) & (dealer_score > threshold):
            self.log += \
            'Player won with a score of {0}. Dealer lost with a score of {1}.'\
            .format(player_score, dealer_score) + '\n'
            self.wallet += self.min_bet
            self.min_bet += 5
            return 1
        elif (player_score == dealer_score) | ((player_score > threshold) &\
        (dealer_score > threshold)):
            self.log += 'Player and Dealer tie.\n'
            return 0
        else:
            if player_score - dealer_score < 0:
                self.log += \
                'Player lost with a score of {0}. Dealer won with a score of {1}.'\
                .format(player_score, dealer_score) + '\n'
                self.wallet -= self.min_bet
                if self.min_bet > 5:
                    self.min_bet -= 5
                return -1
            elif player_score - dealer_score > 0:
                self.log +=\
                'Player won with a score of {0}. Dealer lost with a score of {1}.'\
                .format(player_score, dealer_score) + '\n'
                self.wallet += self.min_bet
                self.min_bet += 5
                return 1
            else:
                self.log += 'Player and Dealer tie.\n'
                return 0

    def hit_or_stand(self, hand, stand_threshold):
        """
        Deals cards to hand until the hand score has reached or surpassed
        the `stand_threshold`. Updates the log everytime a card is pulled.

        Parameters:
            hand: The hand the deal the cards to depending on its score.
            stand_threshold: Score threshold for when the player
            will stand (ie player stands if they have a score >=
            this threshold).
        """
        dealer_threshold = 17
        if isinstance(hand, DealerHand):
            while Blackjack.calculate_score(self.dealer_hand)\
            < dealer_threshold:
                self.log += 'Dealer pulled a ' \
                + repr(self.deck.get_cards()[0]) + '\n'
                self.deck.deal_hand(hand)

        elif isinstance(hand, PlayerHand):
            while Blackjack.calculate_score(self.player_hand)\
             < stand_threshold:
                self.log += 'Player pulled a '\
                + repr(self.deck.get_cards()[0]) + '\n'
                self.deck.deal_hand(hand)


    def get_log(self):
        return self.log

    def reset_log(self):
        self.log = ""

    def add_to_file(self, player_hand, dealer_hand, result):
        """
        Writes the summary and outcome of a round of Blackjack to the
        corresponding .txt file. This file should be named game_summaryX.txt
        where X is the game number and it should be in `game_summaries`
        directory.
        """

        # Remember to use encoding = "utf-8"
#        if self.rounds == 0:
#            with open("./game_summaries/game_summary"\
#            + str(self.game_number)\
#            + ".txt", 'a', encoding = 'utf-8') as f:
#            f.write()

        with open("./game_summaries/game_summary"\
        + str(self.game_number)\
        + ".txt", 'a', encoding = 'utf-8') as f:
            f.write('ROUND {0}:\nPlayer Hand:\n{1}\n'\
            .format(self.rounds, player_hand))
            f.write('Dealer Hand:\n{0}\n'.format(dealer_hand))
            f.write('Winner of ROUND {0}: {1}\n\n'\
            .format(self.rounds, result))
