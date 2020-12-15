import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users

anvil.users.login_with_form()

game = anvil.server.call('get_latest_game')

phases = {
  'introductions': 'Introductions',
  'night': 'NightPhase',
  'day': 'DayPhase',
  'over': 'GameOver',
}

if game:
  winner = anvil.server.call('get_winner')
  if winner:
    form = 'GameOver'
    anvil.server.call('set_game_phase', 'over')
  else:
    form = phases[game['phase']]
else:
  form = 'GameCreator'
  
open_form(form)