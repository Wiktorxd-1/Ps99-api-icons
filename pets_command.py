import discord
from discord import app_commands
from discord.ext import commands
import aiohttp

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

TOKEN = ('Your tkn yk')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.tree.sync()

@bot.tree.command(name="pet", description="Get pet image URL by selecting a pet")
@app_commands.describe(pet_name="Name of the pet to retrieve the icon")
async def pet_info(interaction: discord.Interaction, pet_name: str):
    image_url_base = "https://ps99.biggamesapi.io/image/"

    async with aiohttp.ClientSession() as session:
        async with session.get("https://ps99.biggamesapi.io/api/collection/pets") as response:
            data = await response.json()

    pet_options = [(pet["configName"], pet["configData"]["thumbnail"].replace("rbxassetid://", "")) for pet in data["data"]]
    
    selected_pet_id = next((pet_id for label, pet_id in pet_options if label.lower() == pet_name.lower()), None)

    if selected_pet_id:
        image_url = f"{image_url_base}{selected_pet_id}"
        await interaction.response.send_message(image_url)
    else:
        await interaction.response.send_message("Pet not found. Please select a valid pet name.")

@pet_info.autocomplete('pet_name')
async def pet_autocomplete(interaction: discord.Interaction, current: str):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://ps99.biggamesapi.io/api/collection/pets") as response:
            data = await response.json()

    pet_options = [pet["configName"] for pet in data["data"]]
    filtered_choices = [name for name in pet_options if current.lower() in name.lower()]

    return [app_commands.Choice(name=name, value=name) for name in filtered_choices[:25]]


bot.run(TOKEN)
