from discord import app_commands
from dotenv import load_dotenv
import os
import discord
import calendar
from prettytable import PrettyTable
from requests import get
import yt_dlp

from math_christmas_tree import christmas_tree
from site_scraper import *
from euklid import *

load_dotenv()
try:
    OPUS_PATH = os.getenv("OPUS_PATH")

    print(f"Versuche Opus von folgendem Pfad zu laden: {OPUS_PATH}")
    discord.opus.load_opus(OPUS_PATH)
    print(">>> Opus-Bibliothek erfolgreich geladen!")
except Exception as e:
    print(f">>> FEHLER beim manuellen Laden von Opus: {repr(e)}")
    exit(-1)

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)

    async def on_ready(self):
        await self.tree.sync()
        print(f'Eingeloggt als {self.user} und Befehle synchronisiert!')


intents = discord.Intents.default()
client = MyClient(intents=intents)
YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}



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


@client.tree.command(name="join", description="Der Bot betritt deinen aktuellen Sprachkanal.")
async def join(interaction: discord.Interaction):
    if not interaction.user.voice:
        await interaction.response.send_message("Du befindest dich in keinem Sprachkanal, dem ich beitreten könnte.",
                                                ephemeral=True)
        return

    voice_channel = interaction.user.voice.channel
    await voice_channel.connect()
    await interaction.response.send_message(f"Erfolgreich dem Kanal `{voice_channel.name}` beigetreten!",
                                            ephemeral=True)


@client.tree.command(name="leave", description="Der Bot verlässt den Sprachkanal.")
async def leave(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    if voice_client and voice_client.is_connected():
        await voice_client.disconnect()
        await interaction.response.send_message("Sprachkanal verlassen.", ephemeral=True)
    else:
        await interaction.response.send_message("Ich bin derzeit in keinem Sprachkanal.", ephemeral=True)


@client.tree.command(name="play", description="Spielt einen Song von YouTube ab.")
@app_commands.describe(query="Gib den YouTube-Link oder einen Suchbegriff ein.")
async def play(interaction: discord.Interaction, query: str):
    voice_client = interaction.guild.voice_client

    if not voice_client:
        await interaction.response.send_message("Ich bin in keinem Sprachkanal. Bitte benutze zuerst `/join`.",
                                                ephemeral=True)
        return

    if voice_client.is_playing():
        await interaction.response.send_message("Es wird bereits ein Song abgespielt.", ephemeral=True)
        return

    # === HIER IST DIE WICHTIGE ÄNDERUNG ===
    # Teile Discord sofort mit, dass du Zeit brauchst.
    await interaction.response.defer()

    try:
        # Führe die langsame Operation (YouTube-Suche) aus
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]

        url = info['url']
        source = discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS)
        voice_client.play(source)

        # Sende die finale Antwort mit .followup
        await interaction.followup.send(f"▶️ Spiele jetzt: **{info['title']}**")


    except Exception as e:
        print(f"Ein detaillierter Fehler ist aufgetreten: {repr(e)}")
        print(f"Fehlertyp: {type(e)}")
        await interaction.followup.send("Ein Fehler ist beim Verarbeiten des Songs aufgetreten. Bitte sieh im Terminal nach Details.")

if __name__ == '__main__':
    dc_token = os.getenv('DC_TOKEN')
    client.run(dc_token)
