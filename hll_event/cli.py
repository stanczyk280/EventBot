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
        # await queries.message_player(
        #     api_key, rcon_ip, "76561198285431746", "elo, test bota"
        # )

        # vips = await queries.get_vips(api_key, rcon_ip)
        # for vip in vips:
        #     print(vip.player.name.encode("utf-8", "ignore").decode())

        # player = await queries.get_player(api_key, rcon_ip, "76561198111479386")
        # print(player.name)

        # data = await queries.get_live_game_stats(api_key, rcon_ip)

        # stats_value = data["stats"]
        # for stat in stats_value:
        #     try:
        #         print(str(stat).encode('utf-8', 'ignore').decode('utf-8'))
        #     except UnicodeEncodeError as e:
        #         continue
        kill_logs = await queries.get_kill_logs(api_key, rcon_ip)

        for log in kill_logs:
            print(log)
            print("================================")


async def main():
    client = ApiClient()
    await client.initialize()


if __name__ == "__main__":
    asyncio.run(main())
