from ._anvil_designer import IntroductionsTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Introductions(IntroductionsTemplate):
  def __init__(self, game=None, **properties):
    self.game = anvil.server.call('get_latest_game') if game is None else game
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.players.items = anvil.server.call('get_game_players', self.game)

  def go_to_game(self, **event_args):
    open_form('GameFlow', self.game)