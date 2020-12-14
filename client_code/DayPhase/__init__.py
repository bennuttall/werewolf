from ._anvil_designer import DayPhaseTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..helpers import get_players_killed_str

class DayPhase(DayPhaseTemplate):
  def __init__(self, players_killed=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.players_killed.text = get_players_killed_str(players_killed)
    players = anvil.server.call('get_live_players')
    player_names = [player['name'] for player in players]
    self.player_lynched.items = player_names

  def enable_continue_btn(self, **event_args):
    self.continue_btn.enabled = self.player_lynched.selected_value is not None

  def continue_to_night(self, **event_args):
    players_killed = anvil.server.call(
      'process_day_phase',
      lynched_player_name=self.player_lynched.selected_value,
    )
    winner = anvil.server.call('get_winner')
    if winner:
      form = 'GameOver'    
    else:
      form = 'NightPhase'
    open_form(form, players_killed=players_killed)



