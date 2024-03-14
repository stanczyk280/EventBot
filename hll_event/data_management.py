import json
from pathlib import Path
from models import PlayerEvent


PLAYER_DATA_FILE = "player_data.json"


async def load_player_data():
    player_events = {}
    if Path(PLAYER_DATA_FILE).is_file():
        with open(PLAYER_DATA_FILE, "r") as f:
            player_data = json.load(f)
            for player_id, player_info in player_data.items():
                player_events[player_id] = PlayerEvent(**player_info)
    return player_events


async def save_player_data(player_events):
    player_data = {
        steam_id: player_event.dict()
        for steam_id, player_event in player_events.items()
    }
    with open(PLAYER_DATA_FILE, "w") as f:
        json.dump(player_data, f, indent=4)
