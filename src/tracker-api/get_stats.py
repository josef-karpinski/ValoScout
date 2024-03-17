def get_all_stats(match_data, match_ids, riot_ids, map_names):
    """
    Returns a dictionary of all stats with the given match_ids
    """
    teams = get_teams(match_data, match_ids, riot_ids)

    stats = {}

    stats["all"] = {}
    stats["all"]["match_ids"] = list(match_ids)
    stats["all"]["match_results"] = get_match_results(match_data, stats["all"]["match_ids"], teams)
    stats["all"]["round_results"] = get_round_results(match_data, stats["all"]["match_ids"], teams)
    stats["all"]["agent_comps"] = get_agent_comps(match_data, stats["all"]["match_ids"], teams)

    for map in map_names:
        stats[map] = {}
        stats[map]["match_ids"] = get_match_ids_by_map(match_data, map)
        stats[map]["match_results"] = get_match_results(match_data, stats[map]["match_ids"], teams)
        stats[map]["round_results"] = get_round_results(match_data, stats[map]["match_ids"], teams)
        stats[map]["agent_comps"] = get_agent_comps(match_data, stats[map]["match_ids"], teams)
    
    return stats


def get_match_ids_by_map(match_data, map_name):
    """
    Returns a list of match_ids contained in match_data with the correct map_name
    """
    match_ids = []
    for match_id in match_data.keys():
        if match_data[match_id]["matchInfo"]["mapId"] == map_name:
            match_ids.append(match_id)
    return match_ids

def get_teams(match_data, match_ids, riot_ids):
    """
    Returns a dict which maps match_ids to the team for that match
    """
    teams = {}
    for match_id in match_ids:
        if match_id in match_data:
            match = match_data[match_id]
            count = {"Red":0, "Blue":0}
            for player in match["players"]:
                if player["riotId"] in riot_ids:
                    player_team = player["teamId"]
                    count[player_team] += 1
            team = ""
            if count["Red"] >= count["Blue"]:
                team = "Red"
            else:
                team = "Blue"
            teams[match_id] = team
    return teams

def get_match_results(match_data, match_ids, teams):
    """
    Returns a dict containing total/wins/losses stats of given match_ids in match_data
    We count ties as losses for simplicity
    """
    results = {"total":{"value":0,"match_ids":[]},
               "won":{"value":0,"match_ids":[]},
               "lost":{"value":0,"match_ids":[]}}
    
    for match_id in match_ids:
        if match_id in match_data:
            match = match_data[match_id]
            for team in match["teams"]:
                if team["teamId"] == teams[match_id]:
                    if team["won"]:
                        results["won"]["value"] += 1
                        results["won"]["match_ids"].append(match_id)
                    else:
                        results["lost"]["value"] += 1
                        results["lost"]["match_ids"].append(match_id)
                    results["total"]["value"] += 1
                    results["total"]["match_ids"].append(match_id)
    return results



def get_round_results(match_data, match_ids, teams):
    """
    Returns a dict containing wins/losses stats of rounds of given match_ids in match_data
    """
    round_results = {
        "all":{
            "total":{"value":0},
            "won":{"value":0},
            "lost":{"value":0}
        },
        "attack":{
            "total":{"value":0},
            "won":{"value":0},
            "lost":{"value":0}
        },
        "defense":{
            "total":{"value":0},
            "won":{"value":0},
            "lost":{"value":0}
        }
    }
    for match_id in match_ids:
        if match_id in match_data:
            match = match_data[match_id]
            for team in match["teams"]:
                if team["teamId"] == teams[match_id]:
                    round_results["all"]["total"]["value"] += team["roundsPlayed"]
                    round_results["all"]["won"]["value"] += team["roundsWon"]
                    round_results["all"]["lost"]["value"] += (team["roundsPlayed"] - team["roundsWon"])
            if teams[match_id] == "Blue":
                starting_side = "defense"
            else:
                starting_side = "attack"
            for round in match["roundResults"]:
                side = ""
                if round["roundNum"] <= 12:
                    side = starting_side
                elif round["roundNum"] <= 24:
                    if starting_side == "attack":
                        side = "defense"
                    else:
                        side = "attack"
                else:
                    if round["roundNum"] % 2 == 1:
                        side = starting_side
                    else:
                        if starting_side == "attack":
                            side = "defense"
                        else:
                            side = "attack"

                round_results[side]["total"]["value"] += 1
                if round["winningTeam"] == teams[match_id]:
                    round_results[side]["won"]["value"] += 1
                else:
                    round_results[side]["lost"]["value"] += 1
    return round_results

def get_agent_comps(match_data, match_ids, teams):
    """
    Returns a dict containing agent compositions for each match_id
    """
    comps = {}
    for match_id in match_ids:
        if match_id in match_data:
            team = teams[match_id]
            agents = []
            for player in match_data[match_id]["players"]:
                if player["teamId"] == team:
                    agents.append(player["characterId"])
            agents.sort()
            agents_str = '-'.join(agents)
            if agents_str not in comps:
                comps[agents_str] = {}
                comps[agents_str]["match_ids"] = []
            comps[agents_str]["match_ids"].append(match_id)

    for comp in comps.keys():
        match_results = get_match_results(match_data, comps[comp]["match_ids"], teams)
        comps[comp]["results"] = match_results

    return comps

def get_player_stats(match_data, match_ids, riot_ids):
    """
    Returns a dict containing general player stats
    """
    player_stats = {}
    for riot_id in riot_ids:
        player_stats[riot_id] = {
            "kills": 0,
            "assists": 0,
            "deaths": 0,
            "plants": 0,
            "first_kills": 0,
            "first_deaths": 0,
            "headshots": 0,
            "bodyshots": 0,
            "legshots": 0,
            "total_damage": 0,
            "total_combat_score": 0,
            "num_kast_rounds": 0,
            "match_stats": {},
            "round_stats": {}
        }
        #Needs to be implemented !!!
        for match_id in match_ids:
            break

    return player_stats


def get_attack_plant_stats(match_data, match_ids, teams):
    """
    Returns plant stats when on attack
    """
    pass

def get_defense_plant_stats(match_data, match_ids, teams):
    """
    Returns plant stats when on defense
    """
    pass

if __name__ == "__main__":
    fd = open("stan-kpin-john-bawz-poseidon_matches.txt", "r")
    content = fd.read()
    fd.close()

    import json
    match_data = json.loads(content)
    match_ids = match_data.keys()
    riot_ids = ["Stan#88888","kPin#2875","BigOleTimothy#7749","Poseidon#14534","bawz#zzzzz"]
    teams = get_teams(match_data, match_ids, riot_ids)

    comps = get_agent_comps(match_data, match_ids, teams)
    comps_json = json.dumps(comps)
    print(comps_json)
    print()

    results = get_match_results(match_data, match_ids, teams)
    results_json = json.dumps(results)
    print(results_json)
    print()

    
    test_id = list(match_ids)[0]
    round_results = get_round_results(match_data, [test_id], teams)
    round_results_json = json.dumps(round_results)
    print(test_id)
    print(round_results_json)
    print()

    match_ids_ascent = get_match_ids_by_map(match_data, "Ascent")
    m_json = json.dumps(match_ids_ascent)
    print(m_json)
    print()

    maps = ["Ascent", "Bind", "Breeze", "Fracture", "Pearl", "Icebox", "Sunset", "Haven", "Split", "Lotus"]
    stats = get_all_stats(match_data, match_ids, riot_ids, maps)
    stats_json = json.dumps(stats)
    print(stats_json)
