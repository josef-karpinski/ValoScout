#APIFunctions.py
import requests

def get_puu_ids(api_key, riot_ids):
    puu_ids = []
    for riot_id in riot_ids:
        url = "https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/"
        api_url = url + riot_id[0] + "/" + riot_id[1] + "?api_key=" + api_key
        resp = requests.get(api_url)
        puu_ids.append(resp.json()["puuid"])
    return puu_ids
    

def get_valid_matches_by_id(api_key, puu_ids, min_num_players, time_frame_days):
    #create dictionary with the key being the matchId and the value being the amount of puu_ids included
    all_matches = dict()
    for puu_id in puu_ids:
        url = "https://americas.api.riotgames.com/val/match/v1/matchlists/by-puuid/"
        api_url = url + puu_id + "?api_key=" + api_key
        resp = requests.get(api_url)
        if time_frame_days == -1:
            for match in resp.json()["history"]:
                if match["queueId"] != "customs":
                    continue
                if match["matchId"] in all_matches:
                    all_matches[match["matchId"]] += 1
                else:
                    all_matches[match["matchId"]] = 1
        else:
            #time_frame_days needs to be implemented with resp.json()["history"]["gameStartTimeMillis"]
            pass
    valid_matches_by_id = []
    for matchId in all_matches:
        if all_matches[matchId] >= min_num_players:
            valid_matches_by_id.append(matchId)

    return valid_matches_by_id

def get_match_list(api_key, matches_by_id, map_pool):
    match_list = {}
    for map_ in map_pool:
        match_list[map_] = []
    for matchId in matches_by_id:
        url = "https://americas.api.riotgames.com/val/match/v1/matches/"
        api_url = url + matchId + "?api_key=" + api_key
        resp = requests.get(api_url)
        if resp.json()["matchInfo"]["customGameName"] == "normal":
            if resp.json()["matchInfo"]["mapId"] in match_list:
                match_list[resp.json()["matchInfo"]["mapId"].lower()].append(resp.json())
    return match_list

def get_data(match_list, puu_ids):
    data_by_map = {}
    for map_ in match_list:
        data_by_map[map_] = {}
        data_by_map[map_]['teamStats'] = get_team_data(match_list[map_], puu_ids)
        data_by_map[map_]['playerStats'] = get_player_stats(match_list[map_], puu_ids)
        data_by_map[map_]['comps'] = get_team_comps(match_list[map_], puu_ids)
    return data_by_map

def get_team_data(matches, puu_ids):
    output = {}
    output['games'] = {'played':len(matches),'won':0,'lost':0}
    output['rounds'] = {'total':{'played':0,'won':0,'lost':0},
                        'attack':{'played':0,'won':0,'lost':0},
                        'defense':{'played':0,'won':0,'lost':0} }
    for match in matches:
        team = ''
        teams = {'red':0,'blue':0} #count what teams the players are on
        for player in match['players']:
            if player['puuid'] in puu_ids:
                teams[player['teamId'].lower()] += 1
        if teams['red'] > teams['blue']:
            team = 'red'
        else:
            team = 'blue'
        for t in match['teams']:
            if t['teamId'].lower() == team:
                if t['won']:
                    output['games']['won'] += 1
                else:
                    output['games']['lost'] += 1
                output['rounds']['total']['played'] += t['roundsPlayed']
                output['rounds']['total']['won'] += t['roundsWon']
                output['rounds']['total']['lost'] += t['roundsPlayed'] - t['roundsWon']
                #attack and defense rounds data to be implemented here
    return output

def get_player_stats(matches, puu_ids):
    output = {}
    for puuid in puu_ids:
        output[puuid] = {'kills': 0, 'deaths': 0, 'assists':0}
        #much more can be added, round win rate, agents, acs
    for match in matches:
        for player in match['players']:
            if player['puuid'] in output:
                output[player['puuid']]['kills'] += player['stats']['kills']
                output[player['puuid']]['deaths'] += player['stats']['deaths']
                output[player['puuid']]['assists'] += player['stats']['assists']
    return output 

def get_team_comps(matches, puu_ids):
    comps = {}
    for match in matches:
        team = ''
        teams = {'red':0,'blue':0} #count what teams the players are on
        for player in match['players']:
            if player['puuid'] in puu_ids:
                teams[player['teamId'].lower()] += 1
        if teams['red'] > teams['blue']:
            team = 'red'
        else:
            team = 'blue'
        comp = set()
        for player in match['players']:
            if player['puuid'] in puu_ids and player['teamId'].lower() == team:
                comp.add(player['charcterId'])
        comp_fs = frozenset(comp)
        if comp_fs in comps:
            comps[comp_fs] += 1
        else:
            comps[comp_fs] = 0
    output = {}
    for comp in comps:
        comp_str = str(comp)[11:-2] #JSON only allows key names to be strings. str(comp) = 'frozenset({...})'
        output[comp_str] = comps[comp]
    return output
        
                
