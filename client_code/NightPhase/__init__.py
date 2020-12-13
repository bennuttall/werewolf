from ._anvil_designer import NightPhaseTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class NightPhase(NightPhaseTemplate):
  def __init__(self, game=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.game = game
    players = anvil.server.call('get_live_players', self.game)
#     self.player_killed.items = players

  def continue_to_day(self, **event_args):
    open_form('DayPhase')

