import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

def get_players_killed_str(players_killed):
  if players_killed:
    strs = [
      f"{player['name']} ({player['profession']})"
      for player in players_killed
    ]
    players_killed_str = ', '.join(strs)
  else:
    players_killed_str = "None"
  return f"Players killed: {players_killed_str}"
