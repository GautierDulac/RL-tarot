# STILL WIP


from rlcard.games.tarot.dealer import TarotDealer as Dealer
from rlcard.games.tarot.dog import TarotDog as Dog
from rlcard.games.tarot.bid_round import BidRound
from rlcard.games.tarot.player import TarotPlayer as Player
from rlcard.games.tarot.round import TarotRound as Round


class TarotGame(object):

    def __init__(self):
        self.num_players = 4
        self.num_cards_per_player = 18
        self.num_cards_dog = 6
        self.payoffs = [0 for _ in range(self.num_players)]
        # Initialize a dealer that can deal cards
        self.dealer = Dealer()
        # Initialize four players to play the game
        self.players = [Player(i) for i in range(self.num_players)]
        # Initialize the dog
        self.dog = Dog()
        # Initialize a Bid instance
        self.bid_round = None
        # Initialize a Round instance
        self.round = None

    def init_game(self):
        """ Initialize players and state

        Returns:
            (tuple): Tuple containing:

                (dict): The first state in one game
                (int): Current player's id
        """

        # Deal 18 cards to each player to prepare for the game
        for player in self.players:
            self.dealer.deal_cards(player, self.num_cards_per_player)

        # Deal 6 cards to the dog
        self.dealer.deal_cards(self.dog, self.num_cards_dog)

        # Initialize bid Round
        self.bid_round = BidRound(self.num_players)

        # Initialize a Round
        self.round = Round(self.dealer, self.num_players)

        player_id = self.round.current_player_id
        state = self.get_state(player_id)
        return state, player_id

    def step(self, played_card):
        """ Get the next state

        Args:
            played_card (TarotCard): A specific card

        Returns:
            (tuple): Tuple containing:

                (dict): next player's state
                (int): next plater's id
        """

        self.round.proceed_round(self.players, played_card)
        player_id = (self.round.current_player_id + 1) % self.num_players
        state = self.get_state(player_id)
        self.round.current_player_id = player_id
        return state, player_id

    def get_state(self, player_id):
        """ Return player's state

        Args:
            player_id (int): player id

        Returns:
            (dict): The state of the player
        """
        state = self.round.get_state(self.players, player_id)
        return state

    def get_payoffs(self):
        # TODO : Compute real payoffs (depending on bid and total value in the end of the game)
        """ Return the payoffs of the game

        Returns:
            (list): Each entry corresponds to the payoff of one player
        """
        winner = self.round.winner
        if winner is not None and len(winner) == 1:
            self.payoffs[winner[0]] = 1
            self.payoffs[1 - winner[0]] = -1
        return self.payoffs

    def get_legal_actions(self):
        """ Return the legal actions for current player

        Returns:
            (list): A list of legal actions
        """

        return self.round.get_legal_actions(self.players, self.round.current_player_id)

    def get_player_num(self):
        """ Return the number of players in Tarot

        Returns:
            (int): The number of players in the game
        """
        return self.num_players

    @staticmethod
    def get_action_num():
        # TODO : understand why ?
        """ Return the number of applicable actions

        Returns:
            (int): The number of actions. There are 78 actions
        """
        # TODO : change number of actions
        return 78

    def get_player_id(self):
        """ Return the current player's id

        Returns:
            (int): current player's id
        """
        return self.round.current_player_id

    def is_over(self):
        """ Check if the game is over

        Returns:
            (boolean): True if the game is over
        """
        return self.round.is_over
