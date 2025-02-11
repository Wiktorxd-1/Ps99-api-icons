import discord
from discord import app_commands
from discord.ext import commands
import aiohttp

intents = discord.Intents.all()


bot = commands.Bot(command_prefix="!", intents=intents)

TOKEN = ('your token')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.tree.sync()

@bot.tree.command(name="pet", description="Get pet image")
@app_commands.describe(pet_name="Name of the pet to retrieve the icon")
async def pet_info(interaction: discord.Interaction, pet_name: str):
    image_url_base = "https://ps99.biggamesapi.io/image/"

    async with aiohttp.ClientSession() as session:
        async with session.get("https://ps99.biggamesapi.io/api/collection/pets") as response:
            data = await response.json()

    pet_data = [(pet["configName"], pet["configData"]["thumbnail"].replace("rbxassetid://", "")) for pet in data["data"]]
    
    selected_pet_thumbnail = next((thumbnail for label, thumbnail in pet_data if label.lower() == pet_name.lower()), None)

    if selected_pet_thumbnail:
        image_url = f"{image_url_base}{selected_pet_thumbnail}"

        embed = discord.Embed(
            title=pet_name,
            color=discord.Color.blue()
        )
        embed.set_image(url=image_url)
        embed.set_footer(text="Made by wiktorxd_1 :3")

        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("Pet not found. Please try again.")

@pet_info.autocomplete('pet_name')
async def pet_autocomplete(interaction: discord.Interaction, current: str):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://ps99.biggamesapi.io/api/collection/pets") as response:
            data = await response.json()

    pet_data = [pet["configName"] for pet in data["data"]]
    filtered_choices = [name for name in pet_data if current.lower() in name.lower()]

    return [app_commands.Choice(name=name, value=name) for name in filtered_choices[:25]]



@bot.tree.command(name="booths", description="Get booth image")
@app_commands.describe(booth_name="Name of the booth")
async def booth_info(interaction: discord.Interaction, booth_name: str):
    image_url_base = "https://ps99.biggamesapi.io/image/"

    async with aiohttp.ClientSession() as session:
        async with session.get("https://ps99.biggamesapi.io/api/collection/Booths") as response:
            data = await response.json()

    booth_data = [(booth["configName"], booth["configData"]["Icon"].replace("rbxassetid://", "")) for booth in data["data"]]
    
    selected_booth_icon = next((icon for label, icon in booth_data if label.lower() == booth_name.lower()), None)

    if selected_booth_icon:
        image_url = f"{image_url_base}{selected_booth_icon}"

        embed = discord.Embed(
            title=booth_name,
            color=discord.Color.blue()
        )
        embed.set_image(url=image_url)
        embed.set_footer(text="Made by wiktorxd_1 :3")
        
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("Booth not found. Please select a valid booth name.")

@booth_info.autocomplete('booth_name')
async def booth_autocomplete(interaction: discord.Interaction, current: str):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://ps99.biggamesapi.io/api/collection/booths") as response:
            data = await response.json()

    booth_data = [booth["configName"] for booth in data["data"]]
    filtered_choices = [name for name in booth_data if current.lower() in name.lower()]

    return [app_commands.Choice(name=name, value=name) for name in filtered_choices[:25]]


@bot.tree.command(name="eggs", description="Get egg icon and info")
@app_commands.describe(egg_name="Name of the egg")
async def egg_info(interaction: discord.Interaction, egg_name: str):
    image_url_base = "https://ps99.biggamesapi.io/image/"

    async with aiohttp.ClientSession() as session:
        async with session.get("https://ps99.biggamesapi.io/api/collection/eggs") as response:
            data = await response.json()

    egg_data = next(
        (egg for egg in data["data"] if egg["configName"].lower() == egg_name.lower()), None
    )

    if egg_data:
        egg_config = egg_data["configData"]
        pets = egg_config.get("pets", [])
        pet_chances = []

        for pet in pets:
            pet_name = pet[0]
            chance_percentage = pet[1]
            odds = int(round(1 / (chance_percentage / 100)))
            pet_chances.append(f"{pet_name}: 1 in {odds:,}")

        embed = discord.Embed(
            title=egg_data["configData"]["name"],
            description=f"Category: {egg_data.get('category', 'Unknown')}",
            color=discord.Color.blue()
        )
        embed.set_image(url=f"{image_url_base}{egg_config['icon'].replace('rbxassetid://', '')}")
        embed.add_field(name="Chances", value="\n".join(pet_chances), inline=False)
        embed.set_footer(text="Made by wiktorxd_1 :3")

        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("Egg not found. Please select a valid egg name.")

@egg_info.autocomplete("egg_name")
async def egg_autocomplete(interaction: discord.Interaction, current: str):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://ps99.biggamesapi.io/api/collection/eggs") as response:
            data = await response.json()

    egg_options = [egg["configName"] for egg in data["data"]]
    filtered_choices = [name for name in egg_options if current.lower() in name.lower()]

    return [app_commands.Choice(name=name, value=name) for name in filtered_choices[:25]]


@bot.tree.command(name="pet_petgo", description="Get info about a pet")
@app_commands.describe(pet="Name of the pet")
async def pet_info(interaction: discord.Interaction, pet: str):
    image_url_base = "https://ps99.biggamesapi.io/image/"

    async with aiohttp.ClientSession() as session:
        async with session.get("https://petsgo.biggamesapi.io/api/collection/pets") as response:
            data = await response.json()

    pet_data = {pet["configName"].lower(): pet["configData"]["thumbnail"].replace("rbxassetid://", "") for pet in data["data"]} 
    pet_rarity = {pet["configName"].lower(): pet["configData"]["difficulty"] for pet in data["data"]}
    
    selected_pet_thumbnail = pet_data.get(pet.lower())
    pet_rarity_value = pet_rarity.get(pet.lower())

    if selected_pet_thumbnail:
        image_url = f"{image_url_base}{selected_pet_thumbnail}"

        embed = discord.Embed(
            title=pet.capitalize(),
            color=discord.Color.blue()
        )
        embed.set_image(url=image_url)

        if pet_rarity_value is not None:
            formatted_rarity = format_rarity(pet_rarity_value)
            embed.add_field(name="Rarity", value=f"1 in {formatted_rarity}", inline=False)
        else:
            embed.add_field(name="Rarity", value="Not available", inline=False)

        embed.set_footer(text="Made by wiktorxd_1 :3")

        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("Pet not found. Please try again.")

@pet_info.autocomplete('pet')
async def pet_autocomplete(interaction: discord.Interaction, current: str):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://petsgo.biggamesapi.io/api/collection/pets") as response:
            data = await response.json()

    pet_data = [pet["configName"] for pet in data["data"]]
    filtered_choices = [name for name in pet_data if current.lower() in name.lower()]

    return [app_commands.Choice(name=name, value=name) for name in filtered_choices[:25]]

def format_rarity(value):
    if value >= 1_000_000_000_000:
        return f"{value/1_000_000_000_000}T"
    elif value >= 1_000_000_000:
        return f"{value/1_000_000_000}B"
    elif value >= 1_000_000:
        return f"{value/1_000_000}M"
    elif value >= 1_000:
        return f"{value/1_000}K"
    else:
        return str(value)
        

bot.run(TOKEN)
