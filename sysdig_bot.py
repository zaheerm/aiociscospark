from aiohttp import web
import requests
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


def main(public_url):
    print(public_url)
    app = web.Application()
    app.router.add_post('/', handle)
    app.router.add_post('/{name}', handle)
    web.run_app(app)


if __name__ == '__main__':
    access_token = open("access_token.txt").read().strip()
    port = 8080
    url = ngrok.create_tunnel("sysdig_bot", 8080)
    webhook_id = webhook.create("incoming", url, "messages", "created", access_token)
    main(url)
    webhook.delete(webhook_id, access_token)
    ngrok.delete_tunnel("sysdig_bot")
