from ._anvil_designer import PlayersTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Players(PlayersTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    if self.item['lover'] is not None:
      self.lover.icon = 'fa:heart'

  def delete_player(self, **event_args):
    c = confirm(title="Are you sure you want to remove this player from the game?")
    if c:
      anvil.server.call('remove_player_from_game', player=self.item)
      alert("Please refresh the page to continue")