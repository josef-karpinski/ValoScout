import trn_api_to_riot_api as trn2riot
import json
from datetime import datetime, timedelta, timezone
import cloudscraper
import random
import time


def get_matches_raw(riot_id, min_sleep_time = 5, max_sleep_time = 10, page_limit = float('inf')):
    """
    Uses cloudscraper to scrape all custom match data for a given riot id.
    
    :param riot_id: A tuple containing Riot ID information.
                    riot_id[0] is the riot name
                    riot_id[1] is the riot tagline
    :type riot_id: tuple(str, str)

    :return: A dictionary containing all match data for riot_id
             The "matches" key hold a list of all match entries.
    :rtype: dict
    """
    # Instantiate cloudscraper object
    scraper = cloudscraper.create_scraper()

    # Tracker url prefix and suffix
    # riot_id[0] + "%23" + riot_id[1] goes in between
    # Page number goes at end
    URL_PREFIX = "https://api.tracker.gg/api/v2/valorant/standard/matches/riot/"
    URL_SUFFIX = "?type=custom&season=&agent=all&map=all&next="
    URL_MIDFIX = str(riot_id[0]) + "%23" + str(riot_id[1])
    
    # Iterate through the page numbers for the match lists
    page_num = 0
    
    # List to store and return all match data found
    result = []

    # Iterate until we find a page with no match entries (or we hit the set page_limit)
    while page_num < page_limit:
        try:
            # Sleep for random amount of time
            time.sleep(random.uniform(min_sleep_time, max_sleep_time))
            # Create the url
            url = URL_PREFIX + URL_MIDFIX + URL_SUFFIX + str(page_num)
            # Scrape content and convert to JSON
            content = scraper.get(url).text
            json_content = json.loads(content)
            # If there is match content, append to result, otherwise break
            if len(json_content["data"]["matches"]) == 0:
                break
            for match in json_content["data"]["matches"]:
                result.append(match)
            print("Searched url: " + str(url))
        except Exception as e:
            print(e)
            break

        page_num += 1
    
    return result

def get_valid_match_ids(riot_ids, min_num_players=1, time_frame_days=-1):
    """
    Goes through each riot_id and creates a list of all possible matches.
    A match_id is valid if at least min_num_players occurences of the match appear
    AND it is within time_frame_days days ago. (-1 for all time)

    :param riot_ids: A list of tuples containing Riot ID information.
    :type riot_ids: List[tuple(str,str)]

    :param min_num_players: An integer representing the minimum number of players needed for a match to be valid
                            Default value is 1 signifying only 1 of the specified Riot IDs needs to be in the match
    :type min_num_players: int

    :param time_frame_days: An integer representing the time frame for valid matches
                            Example: if time_frame_days = 90, valid matches must be within last 90 days
                            Defualt value is -1 which means to grab all-time stats (no time frame)
    :type time_frame_days: int

    :return: A list of "valid" match_ids
    :rtype: List[str]
    """
    # Using get_matches_raw(), get a list of all matches between the riot_ids
    all_matches = []
    for riot_id in riot_ids:
        matches = get_matches_raw(riot_id)
        all_matches.extend(matches)

    # Filter for match_ids that match time frame and gamemode
    match_ids_valid_date = []
    if time_frame_days == -1:
        for match in all_matches:
            if match["metadata"]["modeKey"] == "bomb":
                match_ids_valid_date.append(match["attributes"]["id"])
    else:
        cur_time = datetime.now(timezone.utc)
        past_time = cur_time - timedelta(days=time_frame_days)
        for match in all_matches:
            match_time = datetime.fromisoformat(match["metadata"]["timestamp"])
            if match_time > past_time and match["metadata"]["modeKey"] == "bomb":
                match_ids_valid_date.append(match["attributes"]["id"])
            
    # Count frequency of each match_id
    freq = {}
    for match_id in match_ids_valid_date:
        if match_id in freq:
            freq[match_id] += 1
        else:
            freq[match_id] = 1

    # For each match_id, if its frequency is >= min_num_players, it is valid
    result = []
    for match_id in freq.keys():
        if freq[match_id] >= min_num_players:
            result.append(match_id)
    return result

def get_match_data(match_ids, min_sleep_time = 5, max_sleep_time = 10):
    URL_PREFIX = "https://api.tracker.gg/api/v2/valorant/standard/matches/"
    
    matches = {}

    # Initialize scraper
    scraper = cloudscraper.create_scraper()

    # Generate urls from match_ids
    trn_urls = []
    for match_id in match_ids:
        trn_url = URL_PREFIX + match_id
        trn_urls.append(trn_url)

    # Iterate through urls and scrape/convert/save data
    for url in trn_urls:
        try:
            # Sleep for random amount of time
            time.sleep(random.uniform(min_sleep_time, max_sleep_time))

            # Scrape content and convert to Riot api
            content = scraper.get(url).text
            content_json = json.loads(content)
            content_riot = trn2riot.convert(content_json)

            # Append the riot api content to result
            matches[content_riot["matchInfo"]["matchId"]] = content_riot
            print("Searched url: " + str(url))
        except:
            break

    return matches