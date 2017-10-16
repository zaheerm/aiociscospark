aiociscospark
==========

:info: Asyncio based sdk for Cisco Spark

.. image:: https://img.shields.io/travis/zaheerm/aiociscospark.svg
    :target: https://travis-ci.org/zaheerm/aiociscospark
.. image:: https://img.shields.io/coveralls/zaheerm/aiociscospark.svg
    :target: https://coveralls.io/github/zaheerm/aiociscospark

Installation
------------

.. code-block:: shell

    pip install aiociscospark

Usage
-----

.. code-block:: python

    import asyncio

    from aiociscospark import people

    TOKEN = 'xxxxx'

    async def main():
        spark = people.People(TOKEN)
        me = await spark.me()
        print(me)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()

Creating a bot
--------------

.. code-block:: python

    import os
    import asyncio
    from aiociscospark.bot import CommandBot, botcommand


    class UselessBot(CommandBot):
        @botcommand
        async def useless(self, _):
            """
            Pretty much useless
            Usage: useless
            """
            return "I am useless"


    if __name__ == '__main__':
          access_token = os.environ["TOKEN"]
          url = os.environ["BASE_URL"]
          loop = asyncio.get_event_loop()
          bot = UselessBot(access_token, url, loop)
          bot.run_server(8080)
