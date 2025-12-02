from discord import app_commands
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


@client.tree.command(name="euklid", description="Euklid")
@app_commands.describe(
    a="zahl1",
    b="zahl2",
)
async def euklid_command(interaction: discord.Interaction, a: int, b: int):
    message = "```"

    result = euklid(a, b)
    table = PrettyTable(["i", "a", "b", "q", "r"])
    for i, value in result.items():
        if i == "result":
            continue
        table.add_row([i, *value.values()])
    message += table.get_string()
    message += f"\nggt{a, b} = {result['result']}"

    message += "```"

    await interaction.response.send_message(message)


@client.tree.command(name="extended-euklid", description="Extended Euklid")
@app_commands.describe(
    a="zahl1",
    b="zahl2",
)
async def extended_euklid_command(interaction: discord.Interaction, a: int, b: int):
    message = "```"

    result_extended = extended_euklid(a, b)
    table = PrettyTable(["i", "a", "b", "q", "r", "x", "y"])
    for i, value in result_extended.items():
        if isinstance(i, int):
            x_val = value.get('x', '')
            y_val = value.get('y', '')
            table.add_row([i, value['a'], value['b'], value['q'], value['r'], x_val, y_val])

    message += table.get_string()

    ggt, x, y = result_extended['result']
    if a < b:
        a, b = b, a
    message += f"\nggt({a}, {b}) = {ggt}"
    message += f"\n{ggt} = {a} * {x} + {b} * {y}"

    message += "```"

    await interaction.response.send_message(message)

if __name__ == '__main__':
    load_dotenv()
    dc_token = os.getenv('DC_TOKEN')
    client.run(dc_token)
