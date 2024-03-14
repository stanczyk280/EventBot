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


class WeaponKillCount(pydantic.BaseModel):
    name: str
    kills: int = 0


class PlayerEvent(pydantic.BaseModel):
    name: str
    steam_id_64: str
    session_date_first_register: str
    kills: List[WeaponKillCount] = []

    def add_kill(self, weapon_name: str):
        for weapon_kill in self.kills:
            if weapon_kill.name == weapon_name:
                weapon_kill.kills += 1
                break
        else:
            self.kills.append(WeaponKillCount(name=weapon_name, kills=1))


class KillLog(pydantic.BaseModel):
    action: str
    player: str
    steam_id_64: str
    weapon: str
    timestamp_ms: int
