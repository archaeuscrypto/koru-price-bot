import discord
import requests
import asyncio
import logging
import os

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
BIRDEYE_API_KEY = os.getenv("BIRDEYE_API_KEY")
GUILD_ID = '1392171241586298880'
TOKEN_ADDRESS = 'D1mM9THeoBEa2xBbRHpinBPc9x6rDeKUYzMvcUDzpump'
UPDATE_INTERVAL = 10  # seconds


intents = discord.Intents.default()
intents.guilds = True
intents.members = True

client = discord.Client(intents=intents)

async def update_price_nickname():
    await client.wait_until_ready()
    while not client.is_closed():
        try:
            url = f"https://public-api.birdeye.so/public/price?address={TOKEN_ADDRESS}"
            headers = {"x-api-key": BIRDEYE_API_KEY}
            response = requests.get(url, headers=headers)
            data = response.json()
            price = data['data']['value']
            formatted_price = f"${price:.6f}"
            logging.info(f"Fetched price: {formatted_price}")
            guild = discord.utils.get(client.guilds, id=GUILD_ID)
            if guild is None:
                logging.error("Guild not found. Check GUILD_ID.")
                await asyncio.sleep(UPDATE_INTERVAL)
                continue
            member = guild.get_member(client.user.id)
            if member is None:
                logging.error("Bot member not found in guild.")
                await asyncio.sleep(UPDATE_INTERVAL)
                continue
            await member.edit(nick=formatted_price)
            logging.info("Nickname updated.")
        except Exception as e:
            logging.error(f"Error updating nickname: {e}")
        await asyncio.sleep(UPDATE_INTERVAL)

@client.event
async def on_ready():
    logging.info(f"Logged in as {client.user}")
    client.loop.create_task(update_price_nickname())

def main():
    logging.basicConfig(level=logging.INFO)
    client.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main()
