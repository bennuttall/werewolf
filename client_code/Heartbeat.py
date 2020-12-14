from ._anvil_designer import HeartbeatTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Heartbeat(HeartbeatTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

  def ping_server(self, **event_args):
    anvil.server.call('ping')

