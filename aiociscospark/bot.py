import os
import shlex
import subprocess
import asyncio
import json
import docopt
import aiohttp
from aiohttp import web
from aiociscospark import webhooks
from aiociscospark import people
from aiociscospark import messages
from aiociscospark import common
from aiociscospark import ngrok


def _split_into_arguments(message):
    return shlex.split(message)


def botcommand(func):
    doc = func.__doc__
    summary = doc.strip()
    summary = summary[0:summary.find('\n')]
    func.__summary = summary
    return func


class CommandBot:
    def __init__(self, access_token, base_url, loop):
        self.me = None
        self.people = people.People(access_token, loop=loop)
        self.messages = messages.Messages(access_token, loop=loop)
        self.base_url = base_url
        self.loop = loop
        self.access_token = access_token

    async def whoami(self):
        if not self.me:
            self.me = await self.people.me()
        return self.me

    async def run_command(self, message):
        args = _split_into_arguments(message)
        command = args[0]
        try:
            func = getattr(self, command)
            if callable(func) and getattr(func, '__summary'):
                pass
            else:
                return "I don't recognise that command"
            try:
                options = docopt.docopt(func.__doc__, args[1:])
            except docopt.DocoptExit:
                info = "Command given not matching usage."
                usage = await self.help(docopt.docopt(self.help.__doc__, [command]))
                return "{}\n\n{}".format(info, usage)
            except Exception as exc:
                return "That didn't work as expected"
            else:
                try:
                    result = await func(options)
                    return result
                except Exception as exc:
                    return "That didn't work as expected"
        except AttributeError:
            return "I don't recognise that command"

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
            response = await self.run_command(message.text)
            print(response)
            if message.room_type == "direct":
                sent_message = await self.messages.send_to_person(
                    person_id=person_id, message_markdown=response)
            else:
                person = await self.people.get(person_id)
                sent_message = await self.messages.send_to_room(
                    room_id=message.room_id,
                    message_markdown="<@personId:{}|{}> {}".format(
                        person_id, person.display_name, response)
                )
            print(sent_message)
        return web.Response(text=str(data))

    @botcommand
    async def help(self, options):
        """
        gives help on commands
        Usage:
        help [<command>]
        """
        command = options["<command>"]
        all_commands = [method_name for method_name in dir(self)
                        if callable(getattr(self, method_name)) and
                        hasattr(getattr(self, method_name), '__summary')]
        if command:
            if command in all_commands:
                return "{}: {}".format(command, getattr(self, command).__doc__)
            else:
                return "There is no command named {}".format(command)
        else:
            result = ''
            for method_name in all_commands:
                func = getattr(self, method_name)
                result = "{}- {}: {}\n".format(result, method_name, getattr(func, '__summary'))
            return result

    def run_server(self, port=8080):
        async def initiate_webhook():
            webhooks_obj = webhooks.Webhooks(self.access_token, loop=self.loop)
            the_webhook = await webhooks_obj.create(
                "incoming", self.base_url, "messages", "created")
            return the_webhook
        the_webhook = self.loop.run_until_complete(initiate_webhook())
        app = web.Application()
        app.router.add_post('/', self.message_created)
        app.router.add_post('/{name}', self.message_created)
        web.run_app(app, loop=self.loop)
        self.loop.run_until_complete(the_webhook.delete())
