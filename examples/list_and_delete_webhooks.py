import asyncio
from aiociscospark import webhooks


async def main(loop):
    access_token = open("access_token.txt").read().strip()
    webhooks_api = Webhooks(access_token, loop=loop)
    all_webhooks = await webhooks_api.list()
    print(all_webhooks)
    if all_webhooks:
        for item in all_webhooks:
            result = await item.delete()
            if not result:
                print("Failed to delete webhook {}".format(item))


loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
