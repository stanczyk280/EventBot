from datetime import datetime
from typing import List
import httpx
from models import Player, VipPlayer, GameState, KillLog


async def get_response(api_key: str, rcon_ip: str, query: str):
    url = f"{rcon_ip}/api/{query}"
    headers = {"Authorization": f"Bearer {api_key}"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response
        except httpx.HTTPError as e:
            print(f"HTTP error while fetching response: {e}")
            return None


async def get_status(api_key: str, rcon_ip: str):
    response = await get_response(api_key, rcon_ip, "get_status")
    if response and response.status_code == 200:
        return response
    else:
        print("Error fetching game status")
        return None


async def get_player(api_key: str, rcon_ip: str, steam_id_64: str) -> Player:
    response = await get_response(api_key, rcon_ip, f"player?steam_id_64={steam_id_64}")
    data = response.json()
    result = data.get("result", {})
    name = result.get("names", [{}])[0].get("name", "")
    steam_id_64 = result.get("steam_id_64", "")
    return Player(
        name=name,
        steam_id_64=steam_id_64,
    )


async def get_live_game_stats(api_key: str, rcon_ip: str):
    response = await get_response(api_key, rcon_ip, f"get_live_game_stats")
    data = response.json()
    result = data.get("result", {})
    return result


async def message_player(
    api_key: str,
    rcon_ip: str,
    steam_id_64: str,
    message: str,
):
    url = f"{rcon_ip}/api/do_message_player"
    headers = {"Authorization": f"Bearer {api_key}"}
    player = await get_player(api_key, rcon_ip, steam_id_64)
    body = {"steam_id_64": steam_id_64, "player": player.name, "message": message}
    async with httpx.AsyncClient() as client:
        response = await client.post(url=url, json=body, headers=headers)
        return response


async def get_vips(api_key: str, rcon_ip: str) -> List[VipPlayer]:
    response = await get_response(api_key, rcon_ip, "get_vip_ids")
    data = response.json()
    vip_data = data.get("result", [])

    vips = []
    for vip in vip_data:
        steam_id_64 = vip.get("steam_id_64", "")
        name = vip.get("name", "").encode("utf-8", "ignore").decode("unicode_escape")
        vip_expiration_str = vip.get("vip_expiration", "")
        vip_expiration = (
            datetime.fromisoformat(vip_expiration_str) if vip_expiration_str else None
        )

        player = Player(name=name, steam_id_64=steam_id_64)
        vip_player = VipPlayer(player=player, expiration_date=vip_expiration)
        vips.append(vip_player)

    return vips


async def get_kill_logs(api_key: str, rcon_ip: str) -> List[KillLog]:
    url = f"{rcon_ip}/api/get_recent_logs"
    headers = {"Authorization": f"Bearer {api_key}"}

    payload = {
        "end": 250,
        "filter_action": ["KILL"],  # Filter only KILL actions
        "filter_player": [],
        "inclusive_filter": True,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url=url, headers=headers, json=payload)
        data = response.json()
        result = data["result"]
        logs_data = result["logs"]
        logs = []
        current_timestamp_ms = (
            datetime.now().timestamp() * 1000
        )

        for log in logs_data:
            timestamp_ms = current_timestamp_ms
            if "timestamp_ms" in log:
                timestamp_ms = log["timestamp_ms"]
                
            kill_log = KillLog(
                action=log["action"],
                player=log["player"],
                steam_id_64=log["steam_id_64_1"],
                weapon=log["weapon"],
                timestamp_ms=timestamp_ms,
            )

            logs.append(kill_log)

    return logs


def check_player_event_status():
    return None
