import asyncio
from aiociscospark import people


async def main(loop):
    access_token = open("access_token.txt").read().strip()
    people = people.People(access_token, loop=loop)
    me = await people.me()
    if me:
        print(me)
    else:
        print("Failed to get my Spark Person")


loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
