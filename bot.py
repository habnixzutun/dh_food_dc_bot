from dotenv import load_dotenv
import os
import discord
import calendar
from prettytable import PrettyTable

from site_scraper import *
from euklid import *

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)

    async def on_ready(self):
        await self.tree.sync()
        print(f'Eingeloggt als {self.user} und Befehle synchronisiert!')


intents = discord.Intents.default()
client = MyClient(intents=intents)


@client.tree.command(name="food", description="Gibt den Essensplan für heute zurück.")
async def food_command(interaction: discord.Interaction):
    weekday = datetime.date.today().weekday()
    timedelta = 0
    if weekday > 4:
        timedelta = 1
        weekday = 0
    food_plan = get_week_data(get_week_source(datetime.date.today() + datetime.timedelta(weeks=timedelta)))
    message = ""
    message += "***" + calendar.day_name[weekday] + "***\n"
    if timedelta > 0:
        food_plan_day = food_plan[weekday]
    else:
        food_plan_day = food_plan[1]
    for key, value in food_plan_day.items():
        if value:
            message += f"**{key}**\n"
        for element in value:
            message += f"* {element[0]} ({element[1]})\n"
        if value:
            message += "\n"

    await interaction.response.send_message(message)


@client.tree.command(name="food-next", description="Gibt den Essensplan für morgen zurück.")
async def food_next_command(interaction: discord.Interaction):
    weekday = datetime.date.today().weekday() + 1
    timedelta = 0
    if weekday > 4:
        timedelta = 1
        weekday = 0
    food_plan = get_week_data(get_week_source(datetime.date.today() + datetime.timedelta(weeks=timedelta)))
    message = ""
    message += "***" + calendar.day_name[weekday] + "***\n"
    if timedelta > 0:
        food_plan_day = food_plan[weekday]
    else:
        food_plan_day = food_plan[2]
    for key, value in food_plan_day.items():
        if value:
            message += f"**{key}**\n"
        for element in value:
            message += f"* {element[0]} ({element[1]})\n"
        if value:
            message += "\n"

    await interaction.response.send_message(message)


if __name__ == '__main__':
    load_dotenv()
    dc_token = os.getenv('DC_TOKEN')
    client.run(dc_token)
