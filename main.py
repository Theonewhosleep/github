#  modules that the script uses
import os
import random
import discord
import cloudscraper, requests
from discord.ext import commands
import time
import math
import random
from discord_webhook import DiscordWebhook, DiscordEmbed




# Setup/Configs
TOKEN="paste your discord bot token here"
bombs=1    #  This is for maths it will show the % when one bomb is used you can make the % with this higher or lower

#  Discord bot definition
intents = discord.Intents.all()
client = commands.Bot(command_prefix='.', help_command=None, intents=intents)
client.remove_command("help")




# Stuff used for predicter
scraper = cloudscraper.create_scraper()




#  Event when the bot is online
@client.event
async def on_ready():
  print('Bot is online')


  

#  Tower predictor
@client.command(name="towers")
async def rege(ctx, e):
    a = len(e)
    if a == 36:
      await ctx.send(f'Getting round id {e}')
      await anu(ctx, e)
    else:
      time.sleep(2)
      await ctx.send('invalid round id')
async def anu(ctx, e):
  an = []
  an.clear()
  for i in range(8):
    seq = [":red_circle:", ":red_circle:", ":red_circle:"]
    a = random.randrange(0, len(seq))
    seq[a] = ":green_circle:" 
    an.append(" ".join(seq))
  embed=discord.Embed(title="xolos prediction", description=f"predicting: {e}")
  embed.add_field(name="towers", value="\n".join(an), inline=False)
  await ctx.send(ctx.author.mention, embed=embed)



  
#  Mines predictor
@client.command(name="mines")
async def reg(ctx, e):
    a = len(e)
    if a == 36:    #  Checks if the message is 36 characters long
      await ctx.send(f'Getting round id {e}')
      await mines(ctx, e)    #  Starts the mine predictor
    else:
      time.sleep(2)
      await ctx.send('invalid round id')



# Mines predictor code
async def mines(ctx, e):
    def check(msg):
      return msg.author == ctx.author and msg.channel == ctx.channel
    tiles = list(range(1,26))
    time.sleep(2)
    await ctx.send(f'{ctx.author.mention} How many tiles do you want open? ')
    msg = await client.wait_for("message", check=check)
    msgo = int(msg.content)
    totalsquaresleft = 25
    formel = ((totalsquaresleft - bombs) / (totalsquaresleft))
    totalsquareslefts = 24
    formel2 = ((totalsquareslefts - bombs) / (totalsquareslefts))
    for i in range(msgo):
     if msgo == 1:
      break
     formel2 *= formel
     totalsquaresleft -= 1
     totalsquareslefts -= 1
     while True:
            tile_to_unlock = random.choice(tiles)
            if tile_to_unlock != "unlocked!":
                tiles[tile_to_unlock] = "unlocked!"
                break
    counter = 0
    output = ""
    for tile in tiles:
        if counter == 5:
            output += "\n"
            counter = 0
        if tile == "unlocked!":
            output += " :green_circle: "
        else:
            output += " :red_circle: "
        counter += 1
    end = formel2 * 100
    multiplier = calculate_multiplier(msgo, bombs)
    embed=discord.Embed(title="xolos prediction", description=f" predicting: {e}")
    embed.add_field(name="mines", value=output, inline=False)
    embed.add_field(name="chances", value=f"Your win chance is {int(end)}%", inline=False)
    embed.add_field(name="winnings", value="Multiplier: {0:.2f}".format(multiplier), inline=False)
    await ctx.send(ctx.author.mention, embed=embed)

#  Maths for mines
def nCr(n,r):
  f = math.factorial
  return f(n) // f(r) // f(n-r)

def calculate_multiplier(bombs, msgo):
  house_edge = 0.01
  return (0.96 - house_edge) * nCr(25, msgo) / nCr(25 - bombs, msgo)




#  Crash could get banned from the api
@client.command(name='crash')
async def crash(ctx):
    games = scraper.get("https://rest-bf.blox.land/games/crash").json()
    if ctx.author.id != client.user.id:
        ok = await ctx.send(embed=discord.Embed(title="checking api",description="please wait until the bot checks the api",color=0x5ca3ff))
        def lol():
          r=scraper.get("https://rest-bf.blox.land/games/crash").json()["history"]
          yield [r[0]["crashPoint"], [float(crashpoint["crashPoint"]) for crashpoint in r[-2:]]]
        for game in lol():
            games = game[1]
            lastgame = game[0]
            avg = sum(games)/len(games)
            chance = 1
            for game in games:
                chance = chance = 95/game
                prediction = (1/(1-(chance))+avg)/2
                if float(prediction) > 2:
                    color = 0x81fe8f
                else:
                    color = 0xfe8181
                desc = f"""
        **Crashpoint:**
        *{prediction:.2f}x*
        **Chance:**
        ```{chance:.2f}%```
        """
                em=discord.Embed(description=desc,color=color)
                await ok.edit(embed=em)



#  Runs the token
try:
  client.run(TOKEN)
except:
    os.system('Token invalid or raate limit')
