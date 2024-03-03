import httpx
import models


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


async def get_post_response(api_key: str, rcon_ip: str, query: str, body: str):
    url = f"{rcon_ip}/api/{query}"
    headers = {"Authorization": f"Bearer {api_key}"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=body)
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


async def get_game_state(api_key: str, rcon_ip: str) -> models.GameState:
    response = await get_response(api_key, rcon_ip, "get_gamestate")

    if response and response.status_code == 200:
        data = response.json()
        result = data.get("result", {})
        return models.GameState(
            num_allied_players=result.get("num_allied_players", 0),
            num_axis_players=result.get("num_axis_players", 0),
            raw_time_remaining=result.get("raw_time_remaining", ""),
            current_map=result.get("current_map", ""),
        )
    else:
        print("Error fetching game state")
        return None


#
async def get_player(api_key: str, rcon_ip: str, steam_id_64: str) -> models.Player:
    response = await get_response(api_key, rcon_ip, f"player?steam_id_64={steam_id_64}")
    data = response.json()
    result = data.get("result", {})

    # Extract relevant information
    name = result.get("names", [{}])[0].get("name", "")
    steam_id_64 = result.get("steam_id_64", "")
    current_playtime_seconds = result.get("current_playtime_seconds", 0)
    return models.Player(
        name=name,
        steam_id_64=steam_id_64,
        current_playtime_seconds=current_playtime_seconds,
    )


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
