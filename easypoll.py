
import discord
import os
import random
import re

from dataclasses import dataclass
from dotenv import load_dotenv
from typing import List, Dict, Optional
 
REGEX = re.compile(r'"(.*?)"')
class PollException(Exception):
    pass



@dataclass
class Poll:
    question: str
    choices: List[str]
    
    @classmethod
    def from_str(cls, poll_str: str) -> "Poll":
        quotes_count = poll_str.count('"')
        if quotes_count == 0 or quotes_count % 2 != 0:
            raise PollException("Poll must have an even number of double quotes")

        fields = re.findall(REGEX, poll_str)
        return cls(fields[0], fields[1:] if len(fields) > 0 else [])

    def get_message(self):
        """Get the poll question with emoji"""
        return "📊 " + self.question

    def get_embed(self) -> Optional[discord.Embed]:
        if not self.choices:
            return None
        #sakhtan e choice ha
        description = "\n".join(
            self.get_regional_indicator_symbol(idx) + " " + choice
            for idx, choice in enumerate(self.choices)
        )
        embed = discord.Embed(
            description=description, color=discord.Color.dark_red()
        )
        return embed

    def reactions(self) -> List[str]:
        """Add as many reaction as the Poll choices needs"""
        print(self.choices ,"dddd")
        if self.choices:
            return [
                self.get_regional_indicator_symbol(i) for i in range(len(self.choices))
            ]
        else:
            return ["👍", "👎"]

    @staticmethod
    def get_regional_indicator_symbol(idx: int) -> str:
        """idx=0 -> A, idx=1 -> B, ... idx=25 -> Z"""
        if 0 <= idx < 26:
            return chr(ord("\U0001F1E6") + idx)
        return ""


class EasyPoll(discord.Client):
    def __init__(self,intents=discord.Intents.default()):
        intents.message_content = True
        super().__init__(intents=intents)
        self.polls: Dict[int, Poll] = {}
        for i in self.polls:
            print(i)

    @staticmethod
    def help() -> discord.Embed:
        description = """/poll "Question"
        Or
        /poll "Question" "Choice A" "Choice B" "Choice C"
        """
        embed = discord.Embed(
            title="Usage:", description=description, color=discord.Color.dark_red()
        ).setImage("https://images-ext-2.discordapp.net/external/cC-YBJkH2GXnX7MHMASUM9Gle1S1im3rDJj2K54A28w/%3Fcid%3D73b8f7b19a5ccc575679c0a7fc4a673b753e4ce993f35223%26rid%3Dgiphy.mp4/https/media2.giphy.com/media/Q8bEDnj9hZd6vivXSZ/giphy.mp4").setThumbnail("https://images-ext-2.discordapp.net/external/cC-YBJkH2GXnX7MHMASUM9Gle1S1im3rDJj2K54A28w/%3Fcid%3D73b8f7b19a5ccc575679c0a7fc4a673b753e4ce993f35223%26rid%3Dgiphy.mp4/https/media2.giphy.com/media/Q8bEDnj9hZd6vivXSZ/giphy.mp4")
        embed.set_footer(text="HEPIA powered")
        return embed

    async def on_ready(self) -> None:
        print(f"{self.user} has connected to Discord!")
        activity = discord.Game("/poll")
        await self.change_presence(activity=activity)

    async def send_reactions(self, message: discord.message) -> None:
        """Add the reactions to the just sent poll embed message"""
        for i in range(len(self.polls)):
            print(i)
        poll = self.polls.get(message.nonce)
        print(poll)
        if poll:
            for reaction in poll.reactions():
                print(reaction)
                print(poll.reactions)
                await message.add_reaction(reaction)
            self.polls.pop(message.nonce)

    async def send_poll(self, message: discord.message) -> None:
        """Send the embed poll to the channel"""
        poll = Poll.from_str(message.content)
        nonce = random.randint(0, 1e9)
    
        self.polls[nonce] = poll

        await message.delete()
        await message.channel.send(poll.get_message(), embed=poll.get_embed() , nonce=nonce)
        await message.
        await react_message.add_reaction(reaction)
        embed.set_footer(text='Poll ID: {}'.format(react_message.id))
        await react_message.edit_message(embed=embed)

    async def on_message(self, message: discord.message) -> None:
        """Every time a message is send on the server, it arrives here"""
        if message.content.startswith("/poll"):
            try:
                await self.send_poll(message)
            except PollException:
                await message.channel.send(embed=self.help())
        await self.send_reactions(message)
        return


if __name__ == "__main__":
    
    load_dotenv()
    # token = os.getenv("DISCORD_TOKEN")
    # client = EasyPoll()
    # client.run(token)

    client = EasyPoll()
    client.send_reactions
    client.run("MTAzMjU5MzEyMzI0MDU3OTA4Mg.G4-wx1.4ArGj9GacU9UQUk096_c4TMtOjm-py5thCjbFs")



# import discord

# intents = discord.Intents.default()
# intents.message_content = True

# client = discord.Client(intents=intents)

# @client.event
# async def on_ready():
#     print(f'We have logged in as {client.user}')

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     if message.content.startswith('$hello'):
#         await message.channel.send('Hello!')

# client.run("MTAzMjU5MzEyMzI0MDU3OTA4Mg.GSujz1.funzlGUU0YhJkZoirj1hiJGgEgFCK8C5UWVs4M")


# # 