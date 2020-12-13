from ._anvil_designer import GameOverTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class GameOver(GameOverTemplate):
  def __init__(self, players_killed=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    players_killed_str = ', '.join(players_killed) if players_killed else 'None'
    self.players_killed.text = f"Players killed: {players_killed_str}"
    winners = anvil.server.call('get_winner')
    self.winners.text = f"{winners} win!"

  def go_to_start(self, **event_args):
    open_form('GameCreator')

