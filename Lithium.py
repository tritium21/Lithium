import asyncio
import logging
import os
import re

import diceparse
import discord


class Destiny:
    def __init__(self, light=None, dark=None):
        self.reset()
        self.set(light, dark)

    def parse(self, instr):
        instr = instr.strip().lower()
        match = re.match(r"(?=.*?([0-9]+)l)?(?=.*?([0-9]+)d)?[0-9dl]+", instr)
        if instr in {"l", "light"}:
            self.flip(True)
        elif instr in {"d", "dark"}:
            self.flip(False)
        elif instr == "reset":
            self.reset()
        elif match:
            self.set(*match.groups())
        return str(self) or None

    def set(self, light=None, dark=None):
        self.light = int(light) if light is not None else self.light
        self.dark = int(dark) if dark is not None else self.dark
        return self

    def reset(self):
        self.set(0, 0)
        return self

    def flip(self, light=True):
        if light and self.light >= 1:
            self.light -= 1
            self.dark += 1
        elif not light and self.dark >= 1:
            self.light += 1
            self.dark -= 1
        return self

    def __repr__(self):
        return "{}(light={}, dark={})".format(
            self.__class__.__name__,
            self.light,
            self.dark
        )

    def __str__(self):
        ds = "<:darkside:300757237327069195>"
        ls = "<:lightside:300757237427732480>"
        return (ls * self.light) + (ds * self.dark)


class DiscordEOTE(diceparse.EOTE):
    _discord_map = {
            "triumph": "<:triumph:300757237511618560>",
            "threat": "<:threat:300757237432057856>",
            "success": "<:success:300756067606855682>",
            "light": "<:lightside:300757237427732480>",
            "dark": "<:darkside:300757237327069195>)",
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
            return "fpabcds".index(c)

        instr = self._match.string.lower()
        instr = ''.join(self._discord_map[c] for c in sorted(instr, key=key))
        items = self.results.items()
        line = self._str_block(items)
        return '[{}: {}]'.format(instr, line)

roll = diceparse.Roller([diceparse.Standard, diceparse.UniFate, DiscordEOTE])

logging.basicConfig(level=logging.INFO)
destiny = Destiny()
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
    elif message.content.startswith("!destiny"):
        _, _, rest = message.content.partition(" ")
        line = destiny.parse(rest)
        if line:
            await client.send_message(message.channel, "Destiny: " + line)
        else:
            await client.send_message(message.channel, "No Destiny set.")

def main():
    token = os.getenv('LITHIUM_TOKEN')
    if not token:
        token = input("Provide API Token: ").strip()
    client.run(token)

if __name__ == "__main__":
    main()
