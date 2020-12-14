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
    
@anvil.server.callable
def get_latest_game():
  games = list(app_tables.games.search())
  if games:
    return games[-1]
    
@anvil.server.callable
def get_game_players():
  game = get_latest_game()
  players = list(app_tables.players.search(game=game))
  random.shuffle(players)
  return players
    
@anvil.server.callable
def get_live_players():
  game = get_latest_game()
  players = list(app_tables.players.search(game=game, alive=True))
  return players
    
@anvil.server.callable
def set_game_phase(phase):
  game = get_latest_game()
  game.update(phase=phase)
 
@anvil.server.callable
def get_player(player_name):
  game = get_latest_game()
  return app_tables.players.get(game=game, name=player_name)
 
@anvil.server.callable
def process_night_phase(killed_player_name, healed_player_name):
  game = get_latest_game()
  killed_players = []
  if killed_player_name != healed_player_name:
    killed_player = app_tables.players.get(game=game, name=killed_player_name)
    killed_player.update(alive=False)
    killed_players.append(killed_player)
    killed_lover = killed_player['lover']
    if killed_lover:
      killed_lover.update(alive=False)
      killed_players.append(killed_lover)
      
  game.update(phase='day')
      
  return killed_players
 
@anvil.server.callable
def process_day_phase(lynched_player_name):
  game = get_latest_game()
  killed_players = []
  killed_player = app_tables.players.get(game=game, name=lynched_player_name)
  killed_player.update(alive=False)
  killed_players.append(killed_player)
  killed_lover = killed_player['lover']
  if killed_lover:
    killed_lover.update(alive=False)
    killed_players.append(killed_lover)
      
  game.update(phase='night')
      
  return killed_players
  
@anvil.server.callable
def get_winner():
  game = get_latest_game()
  live_players = app_tables.players.search(game=game, alive=True)
  wolves = [player for player in live_players if player['role'] == 'werewolf']
  villagers = [player for player in live_players if player['role'] != 'werewolf']
  if len(live_players) == 2 and all(player['lover'] is not None for player in live_players):
    set_game_phase('over')
    return 'lovers'
  elif len(wolves) == len(villagers):
    set_game_phase('over')
    return 'werewolves'
  elif len(wolves) == 0:
    set_game_phase('over')
    return 'villagers'
  return False
  
@anvil.server.callable
def remove_player_from_game(player):
  player.update(alive=False)
  
  
  
  