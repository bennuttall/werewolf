import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import *

game = anvil.server.call('get_latest_game')

phases = {
  'introductions': 'Introductions',
  'night': 'NightPhase',
  'day': 'DayPhase',
}

if game:
  form = phases[game['phase']]
else:
  form = 'GameCreator'
  
open_form(form)