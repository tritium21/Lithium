import asyncio
import logging
import os

import diceparse
import discord


class DiscordEOTE(diceparse.EOTE):
    _discord_map = {
            "triumph": "<:triumph:300757237511618560>",
            "threat": "<:threat:300757237432057856>",
            "success": "<:success:300756067606855682>",
            "light": "<:lightside:300757237427732480>",
            "dark": "<:darkside:300757237327069195>",
            "failure": "<:failure:300757237175943172>",
            "advantage": "<:advantage:300755580199370752>",
            "dispair": "<:despair:300757238140764161>",
            "s": "<:setback:300760519852294144>",
            "p": "<:Proficiency:300758437363712032>",
            "a": "<:Ability:300758437514444801>",
            "c": "<:Challenge:300760519818608640>",
            "b": "<:boost:300760519722401793>",
            "d": "<:Difficulty:300760519596310530>",
            "f": "<:force:300760519831453696>",
    }
    def _str_block(self, items):
        items = sorted(items, key=self._str_order)
        items = ['{}'.format(self._discord_map[k] * v) for k, v in items]
        line =  ''.join(items)
        return line

    def __str__(self):
        def key(c):
            return list("pabdcs").index(c)

        instr = self._match.string.lower()
        instr = ''.join(self._discord_map[c] for c in sorted(instr, key=key))
        items = self.results.items()
        line = self._str_block(items)
        return '[{}: {}]'.format(instr, line)

roll = diceparse.Roller([diceparse.Standard, diceparse.UniFate, DiscordEOTE])

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
        lines = roll(rest, who=nick).split("\n")
        for line in lines:
            await client.send_message(message.channel, line)

def main():
    token = os.getenv('LITHIUM_TOKEN')
    if not token:
        token = input("Provide API Token: ").strip()
    client.run(token)

if __name__ == "__main__":
    main()
