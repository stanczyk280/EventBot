from dotenv import load_dotenv
from pathlib import Path
import os
import asyncio
import queries
import utils

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)
api_key = os.getenv("API_KEY")
rcon_ip = os.getenv("RCON_IP")


class ApiClient:
    def __init__(self):
        if not api_key or not rcon_ip:
            raise ValueError("API_KEY or RCON_IP must be set.")

    async def initialize(self):
        # status = await queries.get_status(api_key, rcon_ip)
        # print(status.text)

        # gameState = await queries.get_game_state(api_key, rcon_ip)
        # print(gameState)

        await queries.message_player(
            api_key, rcon_ip, "76561198285431746", "elo, test bota"
        )

        # player = await queries.get_player(api_key, rcon_ip, "76561198111479386")
        # print(player.name)


async def main():
    client = ApiClient()
    await client.initialize()


if __name__ == "__main__":
    asyncio.run(main())
