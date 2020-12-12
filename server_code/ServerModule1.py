import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

from datetime import datetime

@anvil.server.callable
def save_new_game(players, num_wolves, ):
  game = app_tables.games.add_row(dt=datetime.now())
  for player in players:
    app_tables.players.add_row(game=game, name=player, alive=True, role=role)