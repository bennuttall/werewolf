from ._anvil_designer import NightPhaseTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class NightPhase(NightPhaseTemplate):
  def __init__(self, game=None, **properties):
    self.init_components(**properties)
    self.game = game
    players = anvil.server.call('get_live_players', self.game)
    player_names = [player['name'] for player in players]
    villager_names = [player['name'] for player in players if player['role'] != 'werewolf']
    non_seer_names = [player['name'] for player in players if player['role'] != 'seer']
    self.player_killed.items = villager_names
    self.player_killed.placeholder = "Select..."
    self.player_healed.items = player_names
    self.player_healed.placeholder = "Select..."
    self.player_seen.items = player_names
    self.player_seen.placeholder = "Select..."

  def continue_to_day(self, **event_args):
    anvil.server.call('set_game_phase', game=self.game, phase='day')
    open_form('DayPhase')

  def enable_continue_btn(self, **event_args):
    selections = (self.player_killed, self.player_healed, self.player_seen)
    self.continue_btn.enabled = all(
      selection.selected_value is not None
      for selection in selections
    )


