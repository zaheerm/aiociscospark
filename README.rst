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
