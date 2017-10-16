import os
import subprocess
import asyncio
import aiohttp
from aiociscospark.bot import CommandBot, botcommand
from aiociscospark import ngrok


class UselessBot(CommandBot):
    @botcommand
    async def useless(self, _):
        """
        Pretty much useless
        Usage: useless
        """
        return "I am useless"


if __name__ == '__main__':
    try:
        p = subprocess.Popen(
            ['ngrok', 'start', '--none'], stdout=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
        access_token = os.environ["TOKEN"]
        async def main(loop):
            for i in range(5):
                try:
                    url = await ngrok.create_tunnel("bot", 8080, loop=loop)
                except aiohttp.client_exceptions.ClientConnectorError:
                    await asyncio.sleep(i)
                else:
                    break
            return url
        loop = asyncio.get_event_loop()
        url = loop.run_until_complete(main(loop))
        bot = UselessBot(access_token, url, loop)
        bot.run_server(8080)
    finally:
        p.terminate()
