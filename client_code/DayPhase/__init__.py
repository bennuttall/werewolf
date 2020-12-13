from ._anvil_designer import DayPhaseTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class DayPhase(DayPhaseTemplate):
  def __init__(self, game=None, players_killed=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.game = game
    players_killed_str = ', '.join(players_killed) if players_killed else 'None'
    self.players_killed.text = f"Players killed: {players_killed_str}"