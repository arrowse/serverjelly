import discord
import random
from discord.ext import commands
from discord import app_commands
import os
import requests
import dotenv

mcServers = {
    "RiftCraft": "octobermc.duckdns.org:25565"
}
dotenv.load_dotenv()
serverApi = os.getenv('SERVER_API')
token = os.getenv('BOT_TOKEN')

def checkStatus(json = False):
    apiResponse = requests.get(f'{serverApi}')
    apiResponseJson = apiResponse.json()
    print(apiResponseJson)
    if json == False:
        if "error" in apiResponseJson:
            return "offline"
        else:
            return "online"
    else:
        return apiResponseJson


def run_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    client = commands.Bot(command_prefix='!', intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} has connected to Discord!')
        try:
            synced = await client.tree.sync()
            print(f"Synced {len(synced)} commands!")
        except Exception as e:
            print(f"Failed to sync commands: {e}")

    @client.event
    async def on_message(message):
        random_number = random.randint(1, 100)
        if message.author == client.user:
            return
        if random_number > 20:
            return

        if message.content.lower() == "how are you today server status jelly?":
            await message.channel.send(f"I ate 14 pretzels and a carrot toady I am PEAKING in life rn")
            return
        if 'yiik' in message.content.lower():
            await message.channel.send('YIIK?!???? I LOVE YIIK SO MUCH OH MY GOD slayy queeny go off')
            return
        if 'america' in message.content.lower() or 'usa' in message.content.lower():
            await message.channel.send('Now that is a country I have heard of! USA! USA! USA!')
            return
        if 'yaoi' in message.content.lower():
            await message.add_reaction('😒')
            return
        if 'reeflux' in message.content.lower() or 'hi' in message.content.lower():
            await message.add_reaction('🫃')
            return
        if 'cook' in message.content.lower():
            await message.add_reaction('👩‍🍳')
            return
        if 'yuri' in message.content.lower():
            await message.add_reaction('🏆')
            return
        if 'think' in message.content.lower():
            await message.channel.send('https://tenor.com/view/madness-splatoon-what-is-bro-yapping-about-yapping-jackpot-gif-10798239398195964455')
            return
        if 'jelly' in message.content.lower():
            await message.channel.send('https://tenor.com/view/i-am-losing-my-grip-on-reality-i-have-gone-clinically-insane-my-descent-to-madness-is-complete-ive-gone-completely-mental-i-am-beyond-the-point-of-no-return-gif-23191724')
            return
        if 'it girl' in message.content.lower():
            await message.channel.send(f"OMG I LOVE THAT SONG\nbitch, you know I'm sexy.. ugh, don't call just text me bitches cannot get on my speed.. They stare 'cause they know I'm the I-T G-I-R-L, you know I am that girl, shh, bitch don't kiss and tell, it girl from ATL. https://open.spotify.com/track/5a8z2vyIDKMh5qcRG6w9wu?si=7d1868619e1a4dd7")
            return
        if 'offline' in message.content.lower() or 'down' in message.content.lower():
            status = checkStatus()
            if status == "offline":
                await message.channel.send(f"omg guys the server is {status} I get to bother tab again!!!11 Yippee!! I'm so happy I get to do my job today yay yay yippee yay yay")
            else:
                await message.channel.send(f"The server is {status} also use /server-status PLEASE giver me something to do I am SO BORED so now I'm moderating this place without mod perms like a LOSER.")
            return
        if message.content.lower() == 'slay':
            await message.channel.send(f"💅💄")
            return

        await client.process_commands(message)

    @client.tree.command(name='server-status',
                         description="Check if the Minecraft server is running and notify Tab if it's not...")
    async def serverStatusCommand(interaction):
        await interaction.response.defer(ephemeral=True)
        status = checkStatus(json = True)

        if "error" in status:
            status = "offline"
        else:
            players = status["players"]["online"]
            latency = status["latency"]
            mcversion = status["version"]["broadcast"]
            status = "online"

        statusEmbed = discord.Embed(
            title=f"ORCraft",
            description=f"It's currently {status} and stuff (I think).",
            color=0x586b9e
)

        if status == "offline":
            tabUserId = 746209701804507136
            tabUser = await client.fetch_user(tabUserId)
            await tabUser.send("Hey, how's that network engineering degree going? Your server is offline lmao.")
            statusEmbed.add_field(name="Tab", value="Tab has been notified. Congratulations! 🎊")
        elif status == "online":
            statusEmbed.add_field(name="Latency", value=f"{latency}ms")
            statusEmbed.add_field(name="Players online", value=f"{players if players else 'No players online'}")
            statusEmbed.set_footer(text=f"Version: {mcversion} | IP: `octobermc.duckdns.org:25565`")

        await interaction.followup.send(embed=statusEmbed, ephemeral=True)

    client.run(token)

