from aiohttp import web
import asyncio
import json
import ngrok
import webhook


async def handle(request):
    data = await request.json()
    print("Got data {}".format(data))
    room_id = data["data"]["roomId"]
    message_id = data["data"]["id"]
    person_id = data["data"]["personId"]

    return web.Response(text=str(data))


def start_server(loop):
    app = web.Application()
    app.router.add_post('/', handle)
    app.router.add_post('/{name}', handle)
    web.run_app(app, loop=loop)


if __name__ == '__main__':
    async def main(loop):
        access_token = open("access_token.txt").read().strip()
        webhooks = webhook.Webhooks(access_token, loop=loop)
        port = 8080
        url = await ngrok.create_tunnel("sysdig_bot", 8080, loop=loop)
        the_webhook = await webhooks.create("incoming", url, "messages", "created")
        return the_webhook

    loop = asyncio.get_event_loop()
    the_webhook = loop.run_until_complete(main(loop))

    start_server(loop)
    loop.run_until_complete(asyncio.gather(the_webhook.delete(), ngrok.delete_tunnel("sysdig_bot")))
