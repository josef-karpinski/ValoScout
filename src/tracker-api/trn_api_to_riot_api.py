from copy import deepcopy
import scrape_trngg as trn

MATCH_DTO = {
    "matchInfo": {},
    "players": [],
    "coaches": [],
    "teams": [],
    "roundResults": []
}

MATCH_INFO_DTO = {
    "matchId": "",
    "mapId": "",
    "gameLengthMillis": 0,
    "gameStartMillis": 0,
    "provisioningFlowId": "",
    "isCompleted": False,
    "customGameName": "",
    "queueId": "",
    "gameMode": "",
    "isRanked": False,
    "seasonId": ""
}

PLAYER_DTO = {
    "riotId": "",
    "gameName": "",
    "tagLine": "",
    "teamId": "",
    "partyId": "",
    "characterId": "",
    "stats": {},
    "competitiveTier": 0,
    "playerCard": "",
    "playerTitle": ""
}

PLAYER_STATS_DTO = {
    "score": 0,
    "roundsPlayed": 0,
    "kills": 0,
    "deaths": 0,
    "assists": 0,
    "playtimeMillis": 0,
    "abilityCasts": {}
}

ABILITY_CASTS_DTO = {
    "grenadeCasts": 0,
    "ability1Casts": 0,
    "ability2Casts": 0,
    "ultimateCasts": 0
}

COACH_DTO = {
    "riotId": "",
    "teamId": ""
}

TEAM_DTO = {
    "teamId": "",
    "won": False,
    "roundsPlayed": 0,
    "roundsWon": 0,
    "numPoints": 0
}

ROUND_RESULT_DTO = {
    "roundNum": 0,
    "roundResult": "",
    "roundCeremony": "",
    "winningTeam": "",
    "bombPlanter": "",
    "bombDefuser": "",
    "plantRoundTime": 0,
    "plantPlayerLocations": [],
    "plantLocation": {},
    "plantSite": "",
    "defuseRoundTime": 0,
    "defusePlayerLocations": [],
    "defuseLocation": {},
    "playerStats": [],
    "roundResultCode": ""
}

PLAYER_LOCATIONS_DTO = {
    "riotId": "",
    "viewRadians": 0.0,
    "location": {}
}

LOCATION_DTO = {
    "x": 0,
    "y": 0
}

PLAYER_ROUND_STATS_DTO = {
    "riotId": "",
    "kills": [],
    "damage": [],
    "score": 0,
    "economy": {},
    "ability": {}
}

KILL_DTO = {
    "timeSinceGameStartMillis": 0,
    "timeSinceRoundStartMillis": 0,
    "killer": "",
    "victim": "",
    "victimLocation": {},
    "assistants": [],
    "playerLocations": [],
    "finishingDamage": {}
}

FINISHING_DAMAGE_DTO = {
    "damageType": "",
    "damageItem": "",
    "isSecondaryFireMode": False
}

DAMAGE_DTO = {
    "receiver": "",
    "damage": 0,
    "legshots": 0,
    "bodyshots": 0,
    "headshots": 0
}

ECONOMY_DTO = {
    "loadoutValue": 0,
    "weapon": "",
    "armor": "",
    "remaining": 0,
    "spent": 0
}

ABILITY_DTO = {
    "grenadeEffects": "",
    "ability1Effects": "",
    "ability2Effects": "",
    "ultimateEffects": ""
}


def convert(tracker_data):
    """
    Method for converting data from Tracker Network VALORANT into the Riot API Format (well-documented and easier use)

    :param tracker_data: The data returned from "https://api.tracker.gg/api/v2/valorant/standard/matches/" + match_id
    :type tracker_data: dict

    :return: Returns a dict in the form of the MATCH_DTO object, see riot_api.md for more details
    :rtype: dict
    """
    # Initialize match as MatchDto
    match = deepcopy(MATCH_DTO)

    # Initialize match["matchInfo"] as MatchInfoDto
    match["matchInfo"] = deepcopy(MATCH_INFO_DTO)
    match["matchInfo"]["matchId"] = tracker_data["data"]["attributes"]["id"]
    match["matchInfo"]["mapId"] = tracker_data["data"]["metadata"]["mapName"]
    match["matchInfo"]["gameLengthMillis"] = tracker_data["data"]["metadata"]["duration"]
    match["matchInfo"]["gameStart"] = tracker_data["data"]["metadata"]["dateStarted"]
    # match["matchInfo"]["provisioningFlowId"]
    match["matchInfo"]["isCompleted"] = True
    # match["matchInfo"]["customGameName"]
    # match["matchInfo"]["queueId"]
    match["matchInfo"]["gameMode"] = tracker_data["data"]["metadata"]["modeName"]
    match["matchInfo"]["isRanked"] = tracker_data["data"]["metadata"]["isRanked"]
    match["matchInfo"]["seasonId"] = tracker_data["data"]["metadata"]["seasonId"]

    # Iterate through type = "team-summary", initialize match["teams"] as TeamDto for each team
    for segment in tracker_data["data"]["segments"]:
        if segment["type"] == "team-summary":
            match["teams"].append(deepcopy(TEAM_DTO))
            match["teams"][-1]["teamId"] = segment["attributes"]["teamId"]
            match["teams"][-1]["won"] = segment["metadata"]["hasWon"]
            match["teams"][-1]["roundsWon"] = segment["stats"]["roundsWon"]["value"]
            match["teams"][-1]["roundsPlayed"] = match["teams"][-1]["roundsWon"] + segment["stats"]["roundsLost"]["value"]
            # match["teams"][-1]["numPoints"]
            # Could add a TEAM_DTO similar to PLAYER_DTO, with kills, assists, deaths, damage

    # Iterate through type = "player-summary", initialize match["players"] as PlayerDto for each player
    for segment in tracker_data["data"]["segments"]:
        if segment["type"] == "player-summary":
            match["players"].append(deepcopy(PLAYER_DTO))
            match["players"][-1]["riotId"] = segment["attributes"]["platformUserIdentifier"]
            # match["players"][-1]["gameName"]
            # match["players"][-1]["tagLine"]
            match["players"][-1]["teamId"] = segment["metadata"]["teamId"]
            # match["players"][-1]["partyId"]
            match["players"][-1]["characterId"] = segment["metadata"]["agentName"]

            match["players"][-1]["stats"] = deepcopy(PLAYER_STATS_DTO)
            # match["players"][-1]["stats"]["score"]
            # match["players"][-1]["stats"]["roundsPlayed"]
            match["players"][-1]["stats"]["kills"] = segment["stats"]["kills"]["value"]
            match["players"][-1]["stats"]["deaths"] = segment["stats"]["deaths"]["value"]
            match["players"][-1]["stats"]["assists"] = segment["stats"]["assists"]["value"]
            # match["players"][-1]["stats"]["playtimeMillis"]

            match["players"][-1]["stats"]["abilityCasts"] = deepcopy(ABILITY_CASTS_DTO)
            match["players"][-1]["stats"]["abilityCasts"]["grenadeCasts"] = segment["stats"]["grenadeCasts"]["value"]
            match["players"][-1]["stats"]["abilityCasts"]["ability1Casts"] = segment["stats"]["ability1Casts"]["value"]
            match["players"][-1]["stats"]["abilityCasts"]["ability2Casts"] = segment["stats"]["ability2Casts"]["value"]
            match["players"][-1]["stats"]["abilityCasts"]["ultimateCasts"] = segment["stats"]["ultimateCasts"]["value"]

            match["players"][-1]["competitiveTier"] = segment["stats"]["rank"]["value"]
            # match["players"][-1]["playerCard"] = 
            # match["players"][-1]["playerTitle"]
            # Could add an ADVANCED_STATS_DTO with singles, doubles, kast, clutches, fks, fds, etc.

    # Iterate through type = "round-summary", append to match["roundResults"] as RoundResultDto for each round
    for segment in tracker_data["data"]["segments"]:
        if segment["type"] == "round-summary":
            match["roundResults"].append(deepcopy(ROUND_RESULT_DTO))
            match["roundResults"][-1]["roundNum"] = segment["attributes"]["round"]
            match["roundResults"][-1]["roundResult"] = segment["stats"]["roundResult"]["value"]
            # match["roundResults"][-1]["roundCeremony"]
            match["roundResults"][-1]["winningTeam"] = segment["stats"]["winningTeam"]["value"]
            if segment["metadata"]["plant"] is not None:
                match["roundResults"][-1]["bombPlanter"] = segment["metadata"]["plant"]["platformUserIdentifier"]
                match["roundResults"][-1]["plantRoundTime"] = segment["metadata"]["plant"]["roundTime"]
                for playerLocation in segment["metadata"]["plant"]["playerLocations"]:
                    match["roundResults"][-1]["plantPlayerLocations"].append(deepcopy(PLAYER_LOCATIONS_DTO))
                    match["roundResults"][-1]["plantPlayerLocations"][-1]["riotId"] = playerLocation["platformUserIdentifier"]
                    match["roundResults"][-1]["plantPlayerLocations"][-1]["viewRadians"] = playerLocation["viewRadians"]
                    match["roundResults"][-1]["plantPlayerLocations"][-1]["location"] = deepcopy(LOCATION_DTO)
                    match["roundResults"][-1]["plantPlayerLocations"][-1]["location"]["x"] = playerLocation["location"]["x"]
                    match["roundResults"][-1]["plantPlayerLocations"][-1]["location"]["y"] = playerLocation["location"]["y"]
                match["roundResults"][-1]["plantLocation"] = deepcopy(LOCATION_DTO)
                match["roundResults"][-1]["plantLocation"]["x"] = segment["metadata"]["plant"]["location"]["x"]
                match["roundResults"][-1]["plantLocation"]["y"] = segment["metadata"]["plant"]["location"]["y"]
                match["roundResults"][-1]["plantSite"] = segment["metadata"]["plant"]["site"]
            else:
                match["roundResults"][-1]["bombPlanter"] = None
                match["roundResults"][-1]["plantRoundTime"] = None
                match["roundResults"][-1]["plantPlayerLocations"] = None
                match["roundResults"][-1]["plantLocation"] = None
                match["roundResults"][-1]["plantSite"] = None
            
            if segment["metadata"]["defuse"] is not None:
                match["roundResults"][-1]["bombDefuser"] = segment["metadata"]["defuse"]["platformUserIdentifier"]
                match["roundResults"][-1]["defuseRoundTime"] = segment["metadata"]["defuse"]["roundTime"]
                for playerLocation in segment["metadata"]["defuse"]["playerLocations"]:
                    match["roundResults"][-1]["defusePlayerLocations"].append(deepcopy(PLAYER_LOCATIONS_DTO))
                    match["roundResults"][-1]["defusePlayerLocations"][-1]["riotId"] = playerLocation["platformUserIdentifier"]
                    match["roundResults"][-1]["defusePlayerLocations"][-1]["viewRadians"] = playerLocation["viewRadians"]
                    match["roundResults"][-1]["defusePlayerLocations"][-1]["location"] = deepcopy(LOCATION_DTO)
                    match["roundResults"][-1]["defusePlayerLocations"][-1]["location"]["x"] = playerLocation["location"]["x"]
                    match["roundResults"][-1]["defusePlayerLocations"][-1]["location"]["y"] = playerLocation["location"]["y"]
                match["roundResults"][-1]["defuseLocation"] = deepcopy(LOCATION_DTO)
                match["roundResults"][-1]["defuseLocation"]["x"] = segment["metadata"]["defuse"]["location"]["x"]
                match["roundResults"][-1]["defuseLocation"]["y"] = segment["metadata"]["defuse"]["location"]["y"]

            else:
                match["roundResults"][-1]["bombDefuser"] = None
                match["roundResults"][-1]["defuseRoundTime"] = None
                match["roundResults"][-1]["defusePlayerLocations"] = None
                match["roundResults"][-1]["defuseLocation"] = None

            match["roundResults"][-1]["playerStats"] = []
            # match["roundResults"][-1] ["roundResultCode"]

    # Iterate through type = "player-round", initialize and append to match["roundResults"][idx]["playerStats"] as PlayerRoundStatsDto
    # Also initialize match["roundResults"][idx]["playerStats"][i]["economy"]
    for segment in tracker_data["data"]["segments"]:
        if segment["type"] == "player-round":
            round = segment["attributes"]["round"]
            idx = -1
            for i in range(len(match["roundResults"])):
                if match["roundResults"][i]["roundNum"] == round:
                    idx = i
                    break
            match["roundResults"][idx]["playerStats"].append(deepcopy(PLAYER_ROUND_STATS_DTO))
            match["roundResults"][idx]["playerStats"][-1]["riotId"] = segment["attributes"]["platformUserIdentifier"]
            match["roundResults"][idx]["playerStats"][-1]["kills"] = []
            match["roundResults"][idx]["playerStats"][-1]["damage"] = []
            # match["roundResults"][idx]["playerStats"][-1]["score"]
            match["roundResults"][idx]["playerStats"][-1]["economy"] = deepcopy(ECONOMY_DTO)
            match["roundResults"][idx]["playerStats"][-1]["economy"]["loadoutValue"] = segment["stats"]["loadoutValue"]["value"]
            # match["roundResults"][idx]["playerStats"][-1]["economy"]["weapon"]
            # match["roundResults"][idx]["playerStats"][-1]["economy"]["armor"]
            match["roundResults"][idx]["playerStats"][-1]["economy"]["remaining"] = segment["stats"]["remainingCredits"]["value"]
            match["roundResults"][idx]["playerStats"][-1]["economy"]["spent"] = segment["stats"]["spentCredits"]["value"]
            # ["ability"] = deepcopy(ABILITY_DTO) (useless)

    # Iterate through type = "player-round-damage", append to match["roundResults"][idx1]["playerStats"][idx2]["damage"] as DamageDto
    for segment in tracker_data["data"]["segments"]:
        if segment["type"] == "player-round-damage":
            round = segment["attributes"]["round"]
            riotId = segment["attributes"]["platformUserIdentifier"]
            idx1 = -1
            for i in range(len(match["roundResults"])):
                if match["roundResults"][i]["roundNum"] == round:
                    idx1 = i
                    break
            idx2 = -1
            for i in range(len(match["roundResults"][idx]["playerStats"])):
                if match["roundResults"][idx1]["playerStats"][i]:
                    if match["roundResults"][idx1]["playerStats"][i]["riotId"] == riotId:
                        idx2 = i
                        break
            match["roundResults"][idx1]["playerStats"][idx2]["damage"].append(deepcopy(DAMAGE_DTO))
            match["roundResults"][idx1]["playerStats"][idx2]["damage"][-1]["receiver"] = segment["attributes"]["opponentPlatformUserIdentifier"]
            match["roundResults"][idx1]["playerStats"][idx2]["damage"][-1]["damage"] = segment["stats"]["damage"]["value"]
            match["roundResults"][idx1]["playerStats"][idx2]["damage"][-1]["legshots"] = segment["stats"]["legshots"]["value"]
            match["roundResults"][idx1]["playerStats"][idx2]["damage"][-1]["bodyshots"] = segment["stats"]["bodyshots"]["value"]
            match["roundResults"][idx1]["playerStats"][idx2]["damage"][-1]["headshots"] = segment["stats"]["headshots"]["value"]

    # Iterate through type = "player-round-kills", append to match["roundResults"][idx1]["playerStats"][idx2]["kills"] as KillDto
    for segment in tracker_data["data"]["segments"]:
        if segment["type"] == "player-round-kills":
            round = segment["attributes"]["round"]
            riotId = segment["attributes"]["platformUserIdentifier"]
            idx1 = -1
            for i in range(len(match["roundResults"])):
                if match["roundResults"][i]["roundNum"] == round:
                    idx1 = i
                    break
            idx2 = -1
            for i in range(len(match["roundResults"][idx]["playerStats"])):
                if match["roundResults"][idx1]["playerStats"][i]:
                    if match["roundResults"][idx1]["playerStats"][i]["riotId"] == riotId:
                        idx2 = i
                        break
            match["roundResults"][idx1]["playerStats"][idx2]["kills"].append(deepcopy(KILL_DTO))
            
            match["roundResults"][idx1]["playerStats"][idx2]["kills"][-1]["timeSinceGameStartMillis"] = segment["metadata"]["gameTime"]
            match["roundResults"][idx1]["playerStats"][idx2]["kills"][-1]["timeSinceRoundStartMillis"] = segment["metadata"]["roundTime"]
            match["roundResults"][idx1]["playerStats"][idx2]["kills"][-1]["killer"] = segment["attributes"]["platformUserIdentifier"]
            match["roundResults"][idx1]["playerStats"][idx2]["kills"][-1]["victim"] = segment["attributes"]["opponentPlatformUserIdentifier"]
            match["roundResults"][idx1]["playerStats"][idx2]["kills"][-1]["victimLocation"] = deepcopy(LOCATION_DTO)
            match["roundResults"][idx1]["playerStats"][idx2]["kills"][-1]["victimLocation"]["x"] = segment["metadata"]["opponentLocation"]["x"]
            match["roundResults"][idx1]["playerStats"][idx2]["kills"][-1]["victimLocation"]["y"] = segment["metadata"]["opponentLocation"]["y"]
            match["roundResults"][idx1]["playerStats"][idx2]["kills"][-1]["assistants"] = []
            for assistant in segment["metadata"]["assistants"]:
                match["roundResults"][idx1]["playerStats"][idx2]["kills"][-1]["assistants"].append(assistant["platformUserHandle"])
            for playerLocation in segment["metadata"]["playerLocations"]:
                match["roundResults"][idx1]["playerStats"][idx2]["kills"][-1]["playerLocations"].append(deepcopy(PLAYER_LOCATIONS_DTO))
                match["roundResults"][idx1]["playerStats"][idx2]["kills"][-1]["playerLocations"][-1]["riotId"] = playerLocation["platformUserIdentifier"]
                match["roundResults"][idx1]["playerStats"][idx2]["kills"][-1]["playerLocations"][-1]["viewRadians"] = playerLocation["viewRadians"]
                match["roundResults"][idx1]["playerStats"][idx2]["kills"][-1]["playerLocations"][-1]["location"] = deepcopy(LOCATION_DTO)
                match["roundResults"][idx1]["playerStats"][idx2]["kills"][-1]["playerLocations"][-1]["location"]["x"] = playerLocation["location"]["x"]
                match["roundResults"][idx1]["playerStats"][idx2]["kills"][-1]["playerLocations"][-1]["location"]["y"] = playerLocation["location"]["y"]
            
            match["roundResults"][idx1]["playerStats"][idx2]["kills"][-1]["finishingDamage"] = deepcopy(FINISHING_DAMAGE_DTO)
            match["roundResults"][idx1]["playerStats"][idx2]["kills"][-1]["finishingDamage"]["damageType"] = segment["metadata"]["finishingDamage"]["damageType"]
            match["roundResults"][idx1]["playerStats"][idx2]["kills"][-1]["finishingDamage"]["damageItem"] = segment["metadata"]["finishingDamage"]["damageItem"]
            match["roundResults"][idx1]["playerStats"][idx2]["kills"][-1]["finishingDamage"]["isSecondaryFireMode"] = segment["metadata"]["finishingDamage"]["isSecondaryFireMode"]
    #Return MATCH_DTO
    return match
