from discord import app_commands
from dotenv import load_dotenv
import os
import discord
import calendar
from prettytable import PrettyTable
from requests import get

from math_christmas_tree import christmas_tree
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
        food_plan_day = food_plan[weekday + 1]
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
        food_plan_day = food_plan[weekday + 1]
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
    message = "```\n"

    result = euklid(a, b)
    table = PrettyTable(["i", "a", "b", "q", "r"])
    for i, value in result.items():
        if i == "result":
            continue
        table.add_row([i, *value.values()])
    message += table.get_string()
    message += f"\nggt{a, b} = {result['result']}"

    message += "\n```"

    await interaction.response.send_message(message)


@client.tree.command(name="extended-euklid", description="Extended Euklid")
@app_commands.describe(
    a="zahl1",
    b="zahl2",
)
async def extended_euklid_command(interaction: discord.Interaction, a: int, b: int):
    message = "```\n"

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

    message += "\n```"

    await interaction.response.send_message(message)


@client.tree.command(name="hex", description="Nimmt eine Hexadezimalzahl an und rechnet sie in alles mögliche um")
@app_commands.describe(
    zahl="zahl",
)
async def hex_command(interaction: discord.Interaction, zahl: str):
    orig_base16 = zahl
    message = ""

    try:
        base10 = str(int(orig_base16, 16))
        base2 = bin(int(orig_base16, 16))
        base8 = oct(int(orig_base16, 16))
        base16 = hex(int(orig_base16, 16))
    except ValueError:
        await interaction.response.send_message(f"'*{orig_base16}*' is not a hex number")
        return

    message += f"**Deine Zahl**: {orig_base16}\n"
    message += f"**Bin:** {base2}\n"
    message += f"**Oct:** {base8}\n"
    message += f"**Dec:** {base10}\n"
    message += f"**Hex:** {base16}\n"

    await interaction.response.send_message(message)


@client.tree.command(name="bin", description="Nimmt eine Binärzahl an und rechnet sie in alles mögliche um")
@app_commands.describe(
    zahl="zahl",
)
async def bin_command(interaction: discord.Interaction, zahl: str):
    orig_base2 = zahl
    message = ""

    try:
        base10 = str(int(orig_base2, 2))
        base2 = bin(int(orig_base2, 2))
        base8 = oct(int(orig_base2, 2))
        base16 = hex(int(orig_base2, 2))
    except ValueError:
        await interaction.response.send_message(f"'*{orig_base2}*' is not a bin number")
        return

    message += f"**Deine Zahl**: {orig_base2}\n"
    message += f"**Bin:** {base2}\n"
    message += f"**Oct:** {base8}\n"
    message += f"**Dec:** {base10}\n"
    message += f"**Hex:** {base16}\n"

    await interaction.response.send_message(message)


@client.tree.command(name="dec", description="Nimmt eine Dezimalzahl an und rechnet sie in alles mögliche um")
@app_commands.describe(
    zahl="zahl",
)
async def dec_command(interaction: discord.Interaction, zahl: str):
    orig_base10 = zahl
    message = ""

    try:
        base10 = str(int(orig_base10, 10))
        base2 = bin(int(orig_base10, 10))
        base8 = oct(int(orig_base10, 10))
        base16 = hex(int(orig_base10, 10))
    except ValueError:
        await interaction.response.send_message(f"'*{orig_base10}*' is not a dec number")
        return

    message += f"**Deine Zahl**: {orig_base10}\n"
    message += f"**Bin:** {base2}\n"
    message += f"**Oct:** {base8}\n"
    message += f"**Dec:** {base10}\n"
    message += f"**Hex:** {base16}\n"

    await interaction.response.send_message(message)


@client.tree.command(name="weihnachtsbaum", description="Gibt einen Weihnachtsbaum aus")
async def christmastree_command(interaction: discord.Interaction):
    await interaction.response.send_message("```\n" + christmas_tree() + "\n```")


@client.tree.command(name="leaderboard", description="Gibt das hexToBinTrainer Leaderboard zurück")
async def leaderboard_command(interaction: discord.Interaction):
    response = get(os.getenv("LEADERBOARD_ENDPOINT"))
    if response.status_code != 200:
        await interaction.response.send_message("Something went wrong :(")
        return
    raw = response.json()

    table = PrettyTable(["Platz", "Name", "Richtig", "Falsch", "Punkte"])
    for index, value in raw.items():
        if index == 1:
            value["index"] = "🏆"
        elif index == 1:
            value["index"] = "🥈"
        elif index == 1:
            value["index"] = "🥉"
        table.add_row([value["index"], value["name"], value["correct"], value["wrong"], value["points"]])

    message = "```\n" + table.get_string() + "\n```"

    await interaction.response.send_message(message)


if __name__ == '__main__':
    load_dotenv()
    dc_token = os.getenv('DC_TOKEN')
    client.run(dc_token)
