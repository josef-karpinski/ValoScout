import requests
import APIFunctions as api
import json

#input Riot Games Production API Key
api_key = ""

#input at least 5 player's riot id's for the algorithm to run
#Riot ID's consist of a gameName (first tuple entry), and a tagLine (second tuple entry)
riot_ids = [("kPin","2875"),
            ("stan","88888"),
            ("Poseidon","2411"),
            ("DRAINGANGjboogie","drain"),
            ("joe","zzzzz")
            ]

#input the minimum number of players in the list needed to count a match (3 recommeneded)
min_num_players = 4

#input how many days back you want the search to go, in days (input -1 for all time stats)
time_frame_days = -1

#input the map pool you want to search for
map_pool = ["ascent", "bind", "fracture", "haven", "lotus", "pearl", "split"]

def run(api_key, riot_ids, min_num_players, time_frame_days, map_pool):
    puu_ids = api.get_puu_ids(api_key, riot_ids)
    valid_matches_by_id = api.get_valid_matches_by_id(api_key, puu_ids, min_num_players, time_frame_days)
    match_list = api.get_match_list(api_key, valid_matches_by_id, map_pool)
    output = api.get_data(match_list, puu_ids)
    print(json.dumps(output, indent = 4))

if __name__ == '__main__':
   run(api_key, riot_ids, min_num_players, time_frame_days, map_pool)

