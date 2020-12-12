from ._anvil_designer import GameCreatorTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

def calc_recommended_wolves(num_players):
  if num_players > 18:
    return 5
  if num_players > 15:
    return 4
  if num_players > 12:
    return 3
  if num_players > 9:
    return 2
  if num_players > 6:
    return 1


class GameCreator(GameCreatorTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.players.items = []
    self.players.set_event_handler('x-delete-player', self.delete_player)

  def add_player(self, **event_args):
    if self.new_player_name.text in set(i['name'] for i in self.players.items):
      alert("Player name must be unique")
      return
    new_player = {'name': self.new_player_name.text}
    self.players.items += [new_player]
    self.new_player_name.text = ''
    self.update_num_players()
    recommended = calc_recommended_wolves(len(self.players.items))
    if recommended is None:
      self.recommended_wolves.text = ""
      self.num_wolves.enabled = False
      self.num_wolves.items = []
      self.start_btn.enabled = False
    else:
      self.recommended_wolves.text = f"recommended: {recommended}"
      self.num_wolves.enabled = True
      self.num_wolves.items = [str(n) for n in range(1, (len(self.players.items) // 3) + 1)]

  def enable_start_btn(self, **event_args):
    self.start_btn.enabled = True
    
  def delete_player(self, item, **event_args):
    self.players.items.remove(item)
    self.update_num_players()
    
  def update_num_players(self):
    n = len(self.players.items)
    self.players_title.text = f"Players ({n})"

  def save_new_game(self, **event_args):
    anvil.server.call('save_new_game',
                       players=self.players.items,
                       wolves=self.num_wolves.text,
                       healer=self.healer.checked,
                       seer=self.healer.checked,
                       lovers=self.healer.checked)

