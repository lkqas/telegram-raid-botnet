# https://github.com/json1c
# Copyright (C) 2021  json1c

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.

import asyncio
import random
import os
from rich.prompt import Prompt, Confirm
from rich.console import Console

from telethon import functions

from functions.function import Function

console = Console()


class PollVoteFunc(Function):
    """Vote in poll"""

    async def vote(self, session, channel, post_id, option_number):
        if not self.storage.initialize:
            await session.connect()

        await session(
            functions.messages.SendVoteRequest(
                peer=channel,
                msg_id=post_id,
                options=[str(option_number)]
            )
        )

    async def execute(self):
        self.ask_accounts_count()

        post_link = console.input("[bold red]enter link to msg/post> ")
        option_number = int(console.input("[bold red]enter answer number (e.g 1, 2)> ")) - 1

        channel = post_link.split("/")[-2]
        post_id = int(post_link.split("/")[-1])

        with console.status("Voting"):
            await asyncio.wait([
                self.vote(session, channel, post_id, option_number)
                for session in self.sessions
            ])

        
