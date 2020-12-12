from ._anvil_designer import DayPhaseTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class DayPhase(DayPhaseTemplate):
  def __init__(self, game=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.game = anvil.server.call('get_latest_game') if game is None else game
    
