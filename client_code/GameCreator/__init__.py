from ._anvil_designer import GameCreatorTemplate
from anvil import *
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

  def add_player(self, **event_args):
    new_player = {'name': self.new_player_name.text}
    self.players.items += [new_player]
    self.new_player_name.text = ''
    recommended = calc_recommended_wolves(len(self.players.items))
    if recommended:
      self.recommended_wolves.text = f"recommended: {recommended}"
    self.num_wolves.items = [str(n) for n in range(1, len(self.players.items) // 3)]