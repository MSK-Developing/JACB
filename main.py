import asyncio
from datetime import datetime
import os.path
import os
import random
import discord
from discord import app_commands
import string

from config import Config

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

async def transform_color_from_config(color):
    # rosso, giallo, verde, blu
    if type(color) is str:
        if color.lower() == "rosso":
            return 0xff0000
        if color.lower() == "giallo":
            return 0xfbff00
        if color.lower() == "verde":
            return 0x00ff33
        if color.lower() == "blu":
            return 0x0033ff
        else:
            return discord.Color.random()
    if type(color) is int:
        return color
    else:
        return discord.Color.random()

async def log_copuon_creation(command_maker: str, code:str):
    interaction = discord.Interaction
    channel = client.get_channel(Config.LOG_CHANNEL_ID)

    log_embed=discord.Embed(color=await transform_color_from_config(Config.colore_embed_successo))
    log_embed.add_field(name=":bell:  ・ [ Cuopon Logs • MSK ] ・  :bell:", value=f":small_blue_diamond: Avviso: Coupon Creato\n:small_blue_diamond: Autore: {command_maker}\n:small_blue_diamond: Codice: `{code}`\n:small_blue_diamond: Data e Ora: `{datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}`", inline=False)
    await channel.send(embed=log_embed)

async def create_coupon(discount: str):
    chars = string.ascii_uppercase + str(string.digits)
    code = f"{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}-{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}-{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}-{random.choice(chars)}{random.choice(chars)}{random.choice(chars)}{discount if discount > 9 else f'0{discount}'}"
    return code

async def get_discount(code):
    code_leght = len(code)
    new = code[code_leght - 2:]
    return new

async def get_all_codes():
    with open('data\coupons.txt', 'r') as cfile:
        #content = cfile.read()
        #return content
        codes = []
        for line in cfile:
            codes.append(line.rstrip())
        return '\n'.join(codes)

async def check_cuopon_code(code: str):
    with open('data\coupons.txt', 'r') as cfile:
        content = cfile.read()

        if code in content:
            return True
        else:
            return False

async def mark_as_used(code: str):
    with open("data\coupons.txt", "r") as cfile:
        lines = cfile.readlines()

    with open("data\coupons.txt", "w") as cfile:
        for line in lines:
            if line.strip("\n") != code:
                cfile.write(line)

async def append_coupun(coupun):
    with open('data\coupons.txt', 'a') as cfile:
        cfile.write(coupun + "\n")
        cfile.close()

async def create_coupons_folder():
    if os.path.exists('data/coupons.txt'):
        print("Exsist")
    else:
        os.mkdir('data')
        with open('data/coupons.txt', 'w') as f:
            f.write('\n')
            f.close()

async def get_dev_token():
    with open('token', 'r') as token_file:
        token = token_file.read()
        return token

async def start_rich_presence(type:str, text:str):
    try:
        if type == "Watching":
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=text))
        if type == "Playing":
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=text))
        if type == "Listening":
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=text))
        else:
            #print('Invalid RichPresence type, must be: "Playing", "Listening", "Watching"')
            pass
    except Exception as e:
        print(f'Impossibile avviare la RPresence: {e}')

@client.event
async def on_ready():
    print(f"Coupon Bot Loaded!\nLogged as {client.user.name}#{client.user.discriminator}\nGuild: {Config.GUILD_ID}")
    print("Syncking commands")
    await tree.sync(guild=discord.Object(id=Config.GUILD_ID))
    await create_coupons_folder()
    await start_rich_presence(Config.Presence.type, Config.Presence.text)
    

@tree.command(name="gen_coupon", description=Config.lang['GEN_COUPON_COMMAND_DESCRIPTION'], guild=discord.Object(id=Config.GUILD_ID))
async def gen_coupon(interaction: discord.Interaction, discount: int):
    code = await create_coupon(discount)
    await append_coupun(code)
    
    await log_copuon_creation(interaction.user.mention, code)

    embed=discord.Embed(color=0x04ff00)
    embed.add_field(name=Config.lang['GEN_COUPON_EMBED_TITLE'], value=f"Code: {code}", inline=True)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@tree.command(name="delete_coupon", description=Config.lang['DELETE_COUPON_COMMAND_DESCRIPTION'], guild=discord.Object(id=Config.GUILD_ID))
async def deleate_coupon(interaction: discord.Interaction, code: str):
    await mark_as_used(code)
    embed=discord.Embed(color=0x04ff00)
    embed.add_field(name=Config.lang['DELETE_COUPON_EMBED_TITLE'], value=f"Code: {code}", inline=True)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@tree.command(name="use_coupon", description=Config.lang['USE_COUPON_COMMAND_DESCTRIPTION'], guild=discord.Object(id=Config.GUILD_ID))
async def deleate_coupon(interaction: discord.Interaction, code: str):
    state = await check_cuopon_code(code)

    if state:
        await mark_as_used(code)
    
        embed=discord.Embed(color=await transform_color_from_config(Config.colore_embed_successo))
        embed.add_field(name=Config.lang['USE_COUPON_COMMAND_SUCCESS_EMBED_TITLE'], value=f"Code Used: {code}\nDiscount Applied: {await get_discount(code)}%", inline=True)
        await interaction.response.send_message(embed=embed)
    else:
        embed=discord.Embed(color=await transform_color_from_config(Config.colore_embed_fallimento))
        embed.add_field(name=Config.lang['USE_COUPON_COMMAND_FAILED_EMBED_TITLE'], value="Sorry :(", inline=True)
        await interaction.response.send_message(embed=embed)

@tree.command(name="check_coupon", description=Config.lang['CHECK_COUPON_COMMAND_DESCRIPTION'], guild=discord.Object(id=Config.GUILD_ID))
async def check_coupon(interaction: discord.Interaction, code: str):
    state = await check_cuopon_code(code)
    if state:
        embed=discord.Embed(color=await transform_color_from_config(Config.colore_embed_successo))
        embed.add_field(name=Config.lang['CHECK_COUPON_COMMAND_SUCCESS_EMBED_TITLE'], value=Config.lang['CHECK_COUPON_COMMAND_SUCCESS_EMBED_DESCRIPTION'], inline=True)
        await interaction.response.send_message(embed=embed)
    else:
        embed=discord.Embed(color=await transform_color_from_config(Config.colore_embed_fallimento))
        embed.add_field(name=Config.lang['CHECK_COUPON_COMMAND_FAILED_EMBED_TITLE'], value=Config.lang['CHECK_COUPON_COMMAND_FAILED_EMBED_DESCRIPTION'], inline=True)
        await interaction.response.send_message(embed=embed, ephemeral=True)

@tree.command(name="list_coupon", description=Config.lang['LIST_COUPON_COMMAND_DESCRIPTION'], guild=discord.Object(id=Config.GUILD_ID))
async def list_coupon(interaction: discord.Interaction):
    embed=discord.Embed(color=await transform_color_from_config(Config.colore_embed_successo))
    embed.add_field(name=Config.lang['LIST_COUPON_EMBED_TITLE'], value=f"```{await get_all_codes()}```", inline=True)
    await interaction.response.send_message(embed=embed, ephemeral=True)

client.run(Config.BOT_TOKEN)