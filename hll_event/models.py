from datetime import datetime, timedelta
from typing import TypedDict

import pydantic


class GameState(pydantic.BaseModel):
    num_allied_players: int
    num_axis_players: int
    raw_time_remaining: str
    current_map: str

class Player(pydantic.BaseModel):
    name: str
    steam_id_64: str
    current_playtime_seconds: int