from ._anvil_designer import SummaryTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Summary(SummaryTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    players = anvil.server.call('get_live_players')
    wolves = [player for player in players if player['role'] == 'werewolf']
    villagers = [player for player in players if player['role'] != 'werewolf']
    self.score.text = f"Wolves {len(wolves)} - {len(villagers)} Villagers"
    self.wolves_list.items = wolves
    self.villagers_list.items = villagers