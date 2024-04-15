from flask import Flask, request, jsonify
import get_stats as stats
import scrape_match_data as scrape

app = Flask(__name__)

@app.route('/api/customs-scout', methods=['GET'])
def team_scout():
    """
    Returns custom match data for specified team and parameters.

    Parameters:
    - riot-ids (list of str): A list of riot IDs with format GameName%23tagline
    - maps (list of str): A list of map names, must be a valid map name
    - time-frame-days (int): Represents how far back to go in match history, in days
    - min-num-players (int): Represents how many of given riot-ids need to be in match for it to be "valid"
    """
    ### Get parameters
    riot_ids_compact = request.args.getlist('riot-ids')
    maps = request.args.getlist('maps')
    time_frame_days = request.args.get('time-frame-days')
    min_num_players = request.args.get('min-num-players')

    ### Verify parameters
    valid_maps = ["Ascent", "Bind", "Breeze", "Fracture", "Haven", "Icebox", "Lotus", "Pearl", "Split", "Sunset"]
    
    # Verify and convert riot_ids
    riot_ids_split = []
    for id in riot_ids_compact:
        if "#" not in id:
            return f"Invalid parameter: {id} does not have a valid format", 400
        id_split = id.split("#")
        riot_ids_split.append((id_split[0],id_split[1]))
    
    # Verify maps
    if "all" in maps:
        maps = list(valid_maps)
    else:
        for map in maps:
            if map not in valid_maps:
                return f"Invalid parameter: {map} is not a valid map name, valid_maps={valid_maps}", 400
    
    # Verify time_frame_days
    if time_frame_days is not None:
        try:
            time_frame_days = int(time_frame_days)
        except:
            return f"Invalid parameter: 'time-frame-days' needs to be a positive integer value, or -1", 400
        if time_frame_days < 0:
            time_frame_days = -1
    else:
        time_frame_days = -1

    # Verify min_num_players
    if min_num_players is not None:
        try:
            min_num_players = int(min_num_players)
        except:
            return f"Invalid parameter: 'min-num-players' needs to be a positive integer value in range [0,5], inclusive", 400
        if min_num_players < 0 or min_num_players > 5:
            return f"Invalid parameter: 'min-num-players' needs to be a positive integer value in range [0,5], inclusive", 400
    else:
        min_num_players = min(len(riot_ids_compact), 5)
    
    if min_num_players < 0 or min_num_players > 5:
        return f"Invalid parameter: 'min-num-players' needs to be a positive integer value in range [0,5], inclusive", 400
    if min_num_players > len(riot_ids_compact):
        return f"Invalid parameter: 'min-num-players' is greater than the number of riot-ids specified", 400
    print(riot_ids_compact)
    print(riot_ids_split)
    print(maps)
    print(time_frame_days)
    print(min_num_players)
    # Main API Functionality
    match_ids = scrape.get_valid_match_ids(riot_ids=riot_ids_split, min_num_players=min_num_players, time_frame_days=time_frame_days)
    print(match_ids)
    match_data = scrape.get_match_data(match_ids=match_ids)
    match_stats = stats.get_all_stats(match_data=match_data, match_ids=match_ids, riot_ids=riot_ids_compact, map_names=maps)

    return jsonify(match_stats)

# example url: http://127.0.0.1:5000/api/customs-scout?riot-ids=kPin%232875&riot-ids=stan%2388888&riot-ids=kueji%23NA1&riot-ids=UCONN%20Mike%23woof&riot-ids=BigOleTomothy%237749&maps=all&min-num-players=5&time-frame-days=-1
if __name__ == "__main__":
    app.run()
