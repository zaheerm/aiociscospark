import asyncio
from aiociscospark import bot
import os

import pytest


class BotForTests(bot.CommandBot):
    @bot.botcommand
    async def hmm(self, options):
        """
        test summary
        Usage: hmm
        """
        return "test result"


@pytest.mark.asyncio
async def test_command_bot_with_commands(event_loop):
    access_token = os.environ.get("TOKEN")
    bot = BotForTests(access_token, "https://127.0.0.1", event_loop)
    assert await bot.run_command("notacommand") == "I don't recognise that command"
    assert await bot.run_command("hmm") == "test result"
    result = await bot.run_command("help")
    assert "test summary" in result
    result = await bot.run_command("help hmm")
    assert bot.hmm.__doc__ in result
