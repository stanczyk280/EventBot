import asyncio
import datetime
from dotenv import load_dotenv
from pathlib import Path
from data_management import load_player_data, save_player_data
import os
from helpers import filter_logs
from queries import get_kill_logs
from models import PlayerEvent
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)
api_key = os.getenv("API_KEY")
rcon_ip = os.getenv("RCON_IP")


class ApiClient:
    def __init__(self):
        if not api_key or not rcon_ip:
            raise ValueError("API_KEY or RCON_IP must be set.")

    async def initialize(self):
        self.player_events = await load_player_data()

    async def save_player_data(self):
        await save_player_data(self.player_events)

    async def process_logs(self):
        logs = await get_kill_logs(api_key, rcon_ip)

        logs = filter_logs(logs)

        for log in logs:
            steam_id_64 = log.steam_id_64

            if steam_id_64 not in self.player_events:
                logging.info("Player added")
                session_date_first_register = datetime.datetime.now().isoformat()
                self.player_events[steam_id_64] = PlayerEvent(
                    name=log.player,
                    steam_id_64=log.steam_id_64,
                    session_date_first_register=session_date_first_register,
                )

            player_event = self.player_events[steam_id_64]
            logging.info("kill added")
            player_event.add_kill(log.weapon)


async def main():
    client = ApiClient()
    await client.initialize()

    while True:
        await client.process_logs()
        await client.save_player_data()
        await asyncio.sleep(30)


if __name__ == "__main__":
    asyncio.run(main())
