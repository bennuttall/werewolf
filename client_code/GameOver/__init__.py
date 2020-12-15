from ._anvil_designer import GameOverTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..helpers import get_players_killed_str

class GameOver(GameOverTemplate):
  def __init__(self, players_killed=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.players_killed.text = get_players_killed_str(players_killed)
    winners = anvil.server.call('get_winner')
    self.winners.text = f"{winners} win!"

  def go_to_start(self, **event_args):
    open_form('GameCreator')

