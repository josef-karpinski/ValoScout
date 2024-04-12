import get_stats as stats
import scrape_match_data as scrape

import json


# INPUTS
riot_ids = [
    ("UNH mank","soap"),
    ("aneXcks","6537"),
    ("UNH Sauced","7401"),
    ("UNH 0pt1mal","0517"),
    ("UNH Frikchik","worm")
]
riot_ids_compact = [
    "UNH mank#soap",
    "aneXcks#6537",
    "UNH Sauced#7401",
    "UNH 0pt1mal#0517",
    "UNH Frikchik#worm"
]
maps = ["Ascent", "Bind", "Breeze", "Icebox", "Lotus", "Split", "Sunset"]
time_frame_days = -1
min_num_players = 4

if __name__ == "__main__":
    match_ids = scrape.get_valid_match_ids(riot_ids=riot_ids, min_num_players=min_num_players, time_frame_days=time_frame_days)
    match_data = scrape.get_match_data(match_ids=match_ids)
    match_stats = stats.get_all_stats(match_data=match_data, match_ids=match_ids, riot_ids=riot_ids_compact, map_names=maps)
    stats_json = json.dumps(match_stats)
    print(stats_json)
