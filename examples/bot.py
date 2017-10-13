from aiohttp import web
import asyncio
import json
import ngrok
from aiociscospark import webhooks
from aiociscospark import people
from aiociscospark import messages


class Bot:
    def __init__(self, access_token, loop):
        self.me = None
        self.people = people.People(access_token, loop=loop)
        self.messages = messages.Messages(access_token, loop=loop)

    async def whoami(self):
        if not self.me:
            self.me = await self.people.me()
        return self.me

    async def message_created(self, request):
        data = await request.json()
        room_id = data["data"]["roomId"]
        message_id = data["data"]["id"]
        person_id = data["data"]["personId"]
        me = await self.whoami()
        if me.person_id == person_id:
            print("I sent that message so not replying!")
        else:
            message = await self.messages.get(data["data"]["id"])
            print("{} sent: {}".format(message.person_email, message.text))
            sent_message = await self.messages.send_to_person(
                person_id=person_id, message_text="Thanks I got that")
            print(sent_message)
        return web.Response(text=str(data))


def start_server(access_token, loop):
    app = web.Application()
    bot = Bot(access_token, loop)
    app.router.add_post('/', bot.message_created)
    app.router.add_post('/{name}', bot.message_created)
    web.run_app(app, loop=loop)


if __name__ == '__main__':
    access_token = open("access_token.txt").read().strip()
    async def main(loop):
        webhooks_obj = webhooks.Webhooks(access_token, loop=loop)
        port = 8080
        url = await ngrok.create_tunnel("sysdig_bot", 8080, loop=loop)
        the_webhook = await webhooks_obj.create("incoming", url, "messages", "created")
        return the_webhook

    loop = asyncio.get_event_loop()
    the_webhook = loop.run_until_complete(main(loop))

    start_server(access_token, loop)
    loop.run_until_complete(asyncio.gather(the_webhook.delete(), ngrok.delete_tunnel("sysdig_bot")))
