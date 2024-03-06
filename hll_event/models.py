from datetime import datetime, timedelta
from typing import TypedDict
from typing import List

import pydantic


class GameState(pydantic.BaseModel):
    num_allied_players: int
    num_axis_players: int
    raw_time_remaining: str
    current_map: str


class Player(pydantic.BaseModel):
    name: str
    steam_id_64: str


class VipPlayer(pydantic.BaseModel):
    player: Player
    expiration_date: datetime | None


class PlayerEvent(pydantic.BaseModel):
    name: str
    steam_id_64: str
    session_date_first_register: str
    kills: List[dict]

class KillLog(pydantic.BaseModel):
    action: str
    player: str
    steam_id_64: str
    weapon: str


