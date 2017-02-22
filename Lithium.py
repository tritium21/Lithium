import asyncio
import logging
import os

import diceparse
import discord

logging.basicConfig(level=logging.INFO)

client = discord.Client()

@client.event
async def on_ready():
    logging.info(
        "Logged in as %s, %s",
        client.user.name,
        client.user.id
    )

@client.event
async def on_message(message):
    if message.content.startswith("!r"):
        _, _, rest = message.content.partition(" ")
        nick = message.author.display_name
        lines = diceparse.roll(rest, who=nick).split("\n")
        for line in lines:
            await client.send_message(message.channel, line)

def main():
    token = os.getenv('LITHIUM_TOKEN')
    if not token:
        token = input("Provide API Token").strip()
    client.run(token)

if __name__ == "__main__":
    main()