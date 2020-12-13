from ._anvil_designer import NightPhaseTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class NightPhase(NightPhaseTemplate):
  def __init__(self, players_killed=None, **properties):
    self.init_components(**properties)
    players_killed_str = ', '.join(players_killed) if players_killed else 'None'
    self.players_killed.text = f"Players killed: {players_killed_str}"
    players = anvil.server.call('get_live_players')
    player_names = [player['name'] for player in players]
    villager_names = [player['name'] for player in players if player['role'] != 'werewolf']
    non_seer_names = [player['name'] for player in players if player['role'] != 'seer']
    self.player_killed.items = villager_names
    self.player_healed.items = player_names
    self.player_seen.items = player_names

  def enable_continue_btn(self, **event_args):
    selections = (self.player_killed, self.player_healed, self.player_seen)
    self.continue_btn.enabled = all(
      selection.selected_value is not None
      for selection in selections
    )

  def reveal_player_to_seer(self, **event_args):
    if self.player_seen.selected_value is None:
      self.reveal_card.visible = False
      self.enable_continue_btn()
    else:
      player = anvil.server.call(
        'get_player', player_name=self.player_seen.selected_value
      )
      self.seer_reveal.text = f"{player['name']} is a {player['role']}"
      self.reveal_card.visible = True
      self.enable_continue_btn()

  def continue_to_day(self, **event_args):
    players_killed = anvil.server.call(
      'process_night_phase',
      killed_player_name=self.player_killed.selected_value,
      healed_player_name=self.player_healed.selected_value,
    )
    winner = anvil.server.call('get_winner')
    if winner:
      form = 'GameOver'    
    else:
      form = 'DayPhase'
    open_form(form, players_killed=players_killed)



