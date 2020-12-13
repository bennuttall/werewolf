import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

from datetime import datetime
import random

@anvil.server.callable
def save_new_game(players, num_wolves, healer, seer, lovers):
  game = app_tables.games.add_row(dt=datetime.now(), healer=healer, seer=seer, lovers=lovers, phase='introductions')
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
  games = list(app_tables.games.search())
  if games:
    return games[-1]
    
@anvil.server.callable
def get_game_players(game):
  players = list(app_tables.players.search(game=game))
  random.shuffle(players)
  return players
    
@anvil.server.callable
def get_live_players(game):
  players = list(app_tables.players.search(game=game, alive=True))
  return players
    
@anvil.server.callable
def set_game_phase(game, phase):
  game.update(phase=phase)
 
@anvil.server.callable
def get_player(game, player_name):
  return app_tables.players.get(game=game, name=player_name)
 
@anvil.server.callable
def process_night_phase(game, killed_player_name, healed_player_name):
  killed_players = []
  if killed_player_name != healed_player_name:
    killed_player = app_tables.players.get(game=game, name=killed_player_name)
    killed_player.update(alive=False)
    killed_players.append(killed_player['name'])
    killed_lover = killed_player['lover']
    if killed_lover:
      killed_lover.update(alive=False)
      killed_players.append(killed_lover['name'])
      
  game.update(phase='day')
      
  return killed_players
  
  
  
  
  
  
  
  
  
  
  
  