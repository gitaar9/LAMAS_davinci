import random

from player import SimpleRandomPlayer, HumanControlledPlayer
from tile import Tile


class Game:
    def __init__(self, amount_of_players=3, amount_of_starting_tiles=4, player_class=SimpleRandomPlayer, add_human_player=False):
        self.unplayed_tiles = Tile.complete_set()
        self.tiles_open_on_table = []
        random.shuffle(self.unplayed_tiles)

        self.players = []
        for name in range(amount_of_players):
            p = player_class(self.unplayed_tiles[:amount_of_starting_tiles], name)
            self.unplayed_tiles = self.unplayed_tiles[amount_of_starting_tiles:]
            self.players.append(p)

        if add_human_player:
            self.players.append(HumanControlledPlayer(self.unplayed_tiles[:amount_of_starting_tiles], len(self.players)))
            self.unplayed_tiles = self.unplayed_tiles[amount_of_starting_tiles:]

        self.current_player_idx = 0

    def game_str(self):
        return 'GAME STATE:\n' + \
               '\n'.join(p.game_str() for p in self.players) + \
               f'\nTable: {" ".join(t.game_str() for t in self.tiles_open_on_table)}' + \
               '\n'

    def play_round(self, view=None):
        self.players[self.current_player_idx].play_round(self, view=view)
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)

    def take_tile_from_table(self):
        return self.unplayed_tiles.pop() if self.unplayed_tiles else None

    def put_open_on_table(self, tile):
        tile.become_visible()
        self.tiles_open_on_table.append(tile)
