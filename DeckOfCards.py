# A deck of cards for use in poker, blackjack, etc.

SUPPORTED_GAMES = ("poker", "blackjack")
SUITS = ("Hearts", "Diamonds", "Clubs", "Spades")
FACE_CARDS = ['J', 'Q', 'K', 'A']
CARD_VALUES = [str(d) for d in xrange(2, 11)] + FACE_CARDS


class Card(object):
    "A baseclass for a generic Card"
    def __init__(self, value_char, suit):
        self.value_char = value_char.upper()  # 1, K, A, etc.
        self.suit = suit

    def get_int_value(self, game_context=None):
        """Return the numeric value for the card based on its string value.
           Passing in an optional context (i.e. blackjack) is supported for
           doing this like 'Ace'=(1 or 11)"""

        try:
            int_value = int(self.value_char)
        except ValueError:
            # Callers must ensure the non-numeric card characters are valid
            int_value = self._get_game_value_dict(game_context).get(self.value_char)
        return int_value

    def _get_game_value_dict(self, game_context):
        """Depending on the game, return a dict of values for each non-numeric
             card."""

        # Confirm they are requesting a game that we currently support
        if game_context is None:
            # Just assign to the first game in the list if no game passed
            game_context = SUPPORTED_GAMES[0]
        try:
            assert game_context in SUPPORTED_GAMES
        except AssertionError:
            print "Sorry, %s is not yet supported!\n" % game_context
            raise

        games = {'blackjack': {'J': 10,
                               'Q': 10,
                               'K': 10,
                               'A': (1, 11)},
                 'poker': {'J': 11,
                           'Q': 12,
                           'K': 13,
                           'A': (1, 14)}}
        return games.get(game_context.lower(), None)


class DeckOfCards(object):
    """DeckOfCards using all 52 combinations from Card class.
       `cards` is a data structure with Value/Suit keys and int values"""

    def __init__(self, game):
        # Set up a deck with all cards and populate the values based on game
        from itertools import product
        self.game = game
        keys = product([v for v in CARD_VALUES], [s for s in SUITS])
        self.cards = dict.fromkeys(keys)
        for card in self.cards:
            self.cards[card] = Card(card[0], card[1]).get_int_value(self.game)

    def __repr__(self):
        return "Deck Of Cards for %s" % self.game


class Singleton(type):
    """ from http://stackoverflow.com/a/6798042
        class MyClass(object):
            __metaclass__ = Singleton"""
    _instances = {}

    def __call__(cls, *args, **kwargs):
      if cls not in cls._instances:
        cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
      return cls._instances[cls]


class SingleDeckOfCards(DeckOfCards):
    __metaclass__ = Singleton


class LiteDeckOfCards:
    "This Deck depends on callers to handle exceptions, retrieve values, etc"
    def __init__(self):
        from itertools import product
        suits = 'dhsc'
        vals = '23456789TJQKA'
        self.cards = [''.join(card) for card in product([v for v in vals],
                                                        [s for s in suits])]

    def __repr__(self):
        return "Deck Of Cards for %s" % self.game
