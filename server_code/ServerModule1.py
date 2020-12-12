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
    player['lover'] = None
  random.shuffle(players)
  for wolf in players[:num_wolves]:
    wolf['role'] = 'werewolf'
  if healer:
    the_healer = [player for player in players if player['role'] == 'villager'][0]
    the_healer['role'] = 'healer'
  if seer:
    the_seer = [player for player in players if player['role'] == 'villager'][0]
    the_seer['role'] = 'seer'
    
  for player in players:
    app_tables.players.add_row(game=game, name=player['name'], alive=True, role=player['role'])
    
  if lovers:
    random.shuffle(players)
    the_lovers = players[:2]
    the_lovers[1]['lover'], the_lovers[0]['lover'] = the_lovers
    for lover in the_lovers:
      this_lover_row = app_tables.players.get(game=game, name=lover['name'])
      other_lover_row = app_tables.players.get(game=game, name=lover['lover']['name'])
      this_lover_row.update(lover=other_lover_row)
  
  return game
    
@anvil.server.callable
def get_latest_game():
  return list(app_tables.games.search())[-1]
    
@anvil.server.callable
def get_game_players(game):
  players = list(app_tables.players.search(game=game))
  random.shuffle(players)
  return players
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  