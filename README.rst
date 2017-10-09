aiociscospark
==========

:info: Asyncio based sdk for Cisco Spark

.. image:: https://img.shields.io/travis/zaheerm/aioslacker.svg
    :target: https://travis-ci.org/zaheerm/aiociscospark

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
        async with people.People(TOKEN) as spark:
            me = await spark.me()
            print(me)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
