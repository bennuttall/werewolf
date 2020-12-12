from ._anvil_designer import AddNewPlayerTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class AddNewPlayer(AddNewPlayerTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

  def delete_player(self, **event_args):
    self.parent.raise_event('x-delete-player', item=self.item)
    self.remove_from_parent()

  def validate_name(self, **event_args):
    if self.name.text == '':
      self.delete_player()
