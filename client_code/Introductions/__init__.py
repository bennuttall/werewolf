from ._anvil_designer import IntroductionsTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Introductions(IntroductionsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.players.items = anvil.server.call('get_game_players')

  def continue_to_night(self, **event_args):
    anvil.server.call('set_game_phase', phase='night')
    open_form('NightPhase')

  def restart_game(self, **event_args):
    c = confirm("Restart game?")
    if c:
      open_form('GameCreator')
    
