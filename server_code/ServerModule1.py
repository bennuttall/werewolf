import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

from datetime import datetime
import random

@anvil.server.callable
def save_new_game(players, num_wolves, healer, seer, lovers):
  game = app_tables.games.add_row(dt=datetime.now(), healer=healer, seer=seer, lovers=lovers)
  for player in players:
    player['role'] = 'villager'
  players.shuffle()
  for wolf in players[:num_wolves]:
    wolf['role'] = 'werewolf'
  if healer:
    the_healer = [player for player in players if player['role'] == 'villager'][0]
    the_healer['role'] = 'healer'
  if seer:
    the_seer = [player for player in players if player['role'] == 'villager'][0]
    the_seer['role'] = 'seer'
  if lovers:
    the_lovers = [player for player in players if player['role'] == 'villager'][:1]
    for lover in the_lovers:
      lover['role'] = 'lover'
    
  for player in players:
    app_tables.players.add_row(game=game, name=player['name'], alive=True, role=player['role'])
  